# =============================================================================
# Folder archive backup and restore.
# requirement-folder-archive-backup — create, name, deposit, verify, restore.
# requirement-python-idempotency — next archive number does not overwrite.
# requirement-python-sudo-command — writable first, then sudo -n. Inner OS-tool sudo stays Gap.
# requirement-folder-archive-backup-retention-daily — cap 5.
# requirement-folder-archive-backup-retention-total — cap 30.
# requirement-domain-folder-backup — verbs backup and restore.
# =============================================================================
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tarfile
from datetime import datetime

from .storage import DomainError, login_name, normal_user_only, positive_int, resolve_storage

_NAME_RE = re.compile(r"^(?P<name>.+)-(?P<day>\d{8})-(?P<n>\d+)\.tar\.gz$")
_HARD_ROOTS = {
    "/", "/bin", "/boot", "/dev", "/etc", "/lib", "/lib64",
    "/proc", "/root", "/run", "/sbin", "/sys", "/usr", "/var",
}
_SYSTEM_PREFIXES = (
    "/bin/", "/boot/", "/dev/", "/etc/", "/lib/", "/lib64/",
    "/proc/", "/root/", "/run/", "/sbin/", "/sys/", "/usr/",
)


class Settings:
    """Paths and caps for one backup or restore. Environment overrides win."""

    def __init__(self, version: str = "") -> None:
        self.app_name = "PyBackup"
        self.console = "py-backup"
        self.version = version
        self.backup_root = os.environ.get("BACKUP_ROOT", "/var/backup")
        self.notation = os.environ.get("BACKUP_NOTATION", "PyBackup")
        self.max_daily = positive_int(os.environ.get("MAX_DAILY_BACKUPS"), 5)
        self.max_total = positive_int(os.environ.get("MAX_TOTAL_BACKUPS"), 30)
        self.projects_root = os.environ.get("PROJECTS_ROOT", "")
        self.ram_root = os.environ.get("RAM_ROOT", "/dev/shm")
        self.global_bin = os.environ.get("GLOBAL_BIN", "/usr/local/bin")
        self.json = False

    def deposit_dir(self) -> str:
        return os.path.join(self.backup_root, self.notation)

    def grant_path(self) -> str:
        return os.path.join(self.global_bin, self.console)


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def sanitize_folder_name(path: str) -> str:
    """One path segment. Empty, dot, and dot-dot fail closed."""
    base = os.path.basename(os.path.abspath(path))
    if base in ("", ".", ".."):
        return ""
    safe = []
    for ch in base:
        if ch.isalnum() or ch in "._-":
            safe.append(ch)
        else:
            safe.append("_")
    return "".join(safe)


def count_tree(root: str) -> tuple[int, int]:
    """Directory entries, and regular files. Symlinks are entries, not files.

    Matches find plus find -type f. Does not follow links.
    requirement-folder-archive-backup and incident INC-20261008-001.
    """
    entries = 0
    files = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        entries += 1
        kept = []
        for name in dirnames:
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                entries += 1
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            entries += 1
            path = os.path.join(dirpath, name)
            if os.path.isfile(path) and not os.path.islink(path):
                files += 1
    return entries, files


def _tar_members(archive: str) -> list[str]:
    if not os.path.exists(archive):
        raise DomainError(
            "Verification failed: archive missing: {0}".format(archive),
            "py-backup print-sudoers",
        )
    if os.access(archive, os.R_OK) or os.geteuid() == 0:
        proc = _run(["tar", "-tzf", archive])
        if proc.returncode != 0:
            raise DomainError(
                "Verification failed: cannot list archive {0}".format(archive),
                "py-backup print-sudoers",
            )
        text = proc.stdout.decode("utf-8", "replace")
        return [line for line in text.splitlines() if line]
    if normal_user_only():
        raise DomainError(
            "Cannot list {0}. This login does not wrap sudo.".format(archive),
            "py-backup help",
        )
    for tar_bin in ("/usr/bin/tar", "/bin/tar"):
        if not os.path.isfile(tar_bin):
            continue
        proc = _run(["sudo", "-n", tar_bin, "-tzf", archive])
        if proc.returncode == 0:
            text = proc.stdout.decode("utf-8", "replace")
            return [line for line in text.splitlines() if line]
    raise DomainError(
        "Verification failed: cannot list archive {0}".format(archive),
        "py-backup print-sudoers",
    )


def _tar_regular_files(archive: str) -> int | None:
    """Regular-file members from tar -tvzf. None when the archive is not readable.

    Type '-' and hard-link type 'h' count. Symlinks do not. No sudo.
    """
    if not os.access(archive, os.R_OK) and os.geteuid() != 0:
        return None
    proc = _run(["tar", "-tvzf", archive])
    if proc.returncode != 0:
        return None
    count = 0
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        if line[:1] in ("-", "h"):
            count += 1
    return count


def file_size(path: str) -> int:
    try:
        return os.stat(path).st_size
    except OSError:
        return 0


def _match(basename: str, src_name: str) -> tuple[str, int] | None:
    if not basename.startswith(src_name + "-"):
        return None
    found = _NAME_RE.match(basename)
    if found is None or found.group("name") != src_name:
        return None
    return found.group("day"), int(found.group("n"))


def next_archive_name(src_name: str, dest_dir: str, day: str | None = None) -> str:
    """SOURCE-YYYYMMDD-N.tar.gz. N starts at 1 and does not overwrite."""
    if day is None:
        day = datetime.now().strftime("%Y%m%d")
    n = 1
    while n <= 9999:
        name = "{0}-{1}-{2}.tar.gz".format(src_name, day, n)
        if not os.path.exists(os.path.join(dest_dir, name)):
            return name
        n += 1
    raise DomainError(
        "Could not allocate archive name under {0}".format(dest_dir),
        "py-backup help",
    )


def _deposit(stage: str, dest: str, settings: Settings) -> None:
    dest_dir = os.path.dirname(dest)
    if not os.path.isfile(stage):
        raise DomainError("Staged archive missing: {0}".format(stage), "py-backup help")
    if os.geteuid() == 0 or (os.path.isdir(dest_dir) and os.access(dest_dir, os.W_OK)):
        os.makedirs(dest_dir, mode=0o755, exist_ok=True)
        shutil.copy2(stage, dest)
        os.chmod(dest, 0o640)
        return
    try:
        os.makedirs(dest_dir, mode=0o755, exist_ok=True)
    except OSError:
        pass
    if os.path.isdir(dest_dir) and os.access(dest_dir, os.W_OK):
        shutil.copy2(stage, dest)
        try:
            os.chmod(dest, 0o640)
        except OSError:
            pass
        return
    if normal_user_only():
        raise DomainError(
            "Deposit into {0} needs a grant. This login does not wrap sudo.".format(dest_dir),
            "py-backup help",
        )
    if shutil.which("sudo") is None:
        raise DomainError(
            "sudo not found. Deposit requires an elevated copy into {0}.".format(dest_dir),
            "py-backup print-sudoers",
        )
    _run(["sudo", "-n", "mkdir", "-p", dest_dir])
    if not os.path.isdir(dest_dir):
        raise DomainError(
            "Cannot create {0}. Ask an admin to install the grant.".format(dest_dir),
            "py-backup print-sudoers",
        )
    install = shutil.which("install")
    if install and _run(["sudo", "-n", install, "-m", "0640", stage, dest]).returncode == 0:
        return
    if _run(["sudo", "-n", "cp", stage, dest]).returncode == 0:
        _run(["sudo", "-n", "chmod", "0640", dest])
        return
    raise DomainError(
        "Deposit failed. sudo is not authorized to copy into {0}.".format(dest_dir),
        "py-backup print-sudoers",
    )


def _remove_deposit(path: str, settings: Settings) -> bool:
    dep = settings.deposit_dir()
    if not path.startswith(dep + os.sep) or not path.endswith(".tar.gz"):
        return False
    if not os.path.exists(path):
        return True
    if os.geteuid() == 0 or os.access(path, os.W_OK) or os.access(dep, os.W_OK):
        try:
            os.remove(path)
            return True
        except OSError:
            pass
    if normal_user_only() or shutil.which("sudo") is None:
        return False
    for rm_bin in ("/bin/rm", "/usr/bin/rm"):
        if _run(["sudo", "-n", rm_bin, "-f", path]).returncode == 0 and not os.path.exists(path):
            return True
    return False


def _list_product(dest_dir: str, src_name: str) -> list[tuple[str, int, str]]:
    found = []
    if not os.path.isdir(dest_dir):
        return found
    for name in os.listdir(dest_dir):
        matched = _match(name, src_name)
        if matched is None:
            continue
        path = os.path.join(dest_dir, name)
        if os.path.isfile(path):
            found.append((matched[0], matched[1], path))
    return found


def apply_retention(src_name: str, dest_dir: str, day: str, settings: Settings) -> dict:
    """Drop oldest same-day copies past the daily cap, then oldest overall past the total cap."""
    daily_removed = 0
    total_removed = 0
    rows = _list_product(dest_dir, src_name)
    same = sorted((n, path) for d, n, path in rows if d == day)
    while len(same) > settings.max_daily:
        _n, path = same.pop(0)
        if not _remove_deposit(path, settings):
            raise DomainError(
                "Retention daily prune failed. Cannot remove {0}.".format(path),
                "py-backup print-sudoers",
            )
        daily_removed += 1
    rows = _list_product(dest_dir, src_name)
    ordered = sorted(rows)
    while len(ordered) > settings.max_total:
        _day, _n, path = ordered.pop(0)
        if not _remove_deposit(path, settings):
            raise DomainError(
                "Retention total prune failed. Cannot remove {0}.".format(path),
                "py-backup print-sudoers",
            )
        total_removed += 1
    remaining_daily = len([1 for d, _n, _p in _list_product(dest_dir, src_name) if d == day])
    remaining_total = len(_list_product(dest_dir, src_name))
    return {
        "daily_removed": daily_removed,
        "daily_remaining": remaining_daily,
        "total_removed": total_removed,
        "total_remaining": remaining_total,
    }


def backup(source: str, settings: Settings) -> str:
    """Pack a directory, deposit it, verify counts, then apply retention."""
    if normal_user_only():
        raise DomainError(
            "backup is not available on this command-line class. It does not wrap sudo.",
            "py-backup help",
        )
    if not source:
        raise DomainError(
            "Usage: py-backup backup <source-folder>",
            "py-backup backup <source-folder>",
        )
    if not os.path.isdir(source):
        raise DomainError(
            "Source is not a directory: {0}".format(source),
            "py-backup backup <source-folder>",
        )
    if not os.access(source, os.R_OK):
        raise DomainError(
            "Source directory is not readable: {0}".format(source),
            "py-backup backup <source-folder>",
        )
    source_abs = os.path.abspath(source)
    src_name = sanitize_folder_name(source_abs)
    if not src_name:
        raise DomainError("Invalid source folder name", "py-backup backup <source-folder>")
    if shutil.which("tar") is None:
        raise DomainError("tar is required for backup", "py-backup help")
    dest_dir = settings.deposit_dir()
    archive_name = next_archive_name(src_name, dest_dir)
    stage_root = resolve_storage()
    stage = os.path.join(stage_root, archive_name)
    parent = os.path.dirname(source_abs)
    leaf = os.path.basename(source_abs)
    entries, files = count_tree(source_abs)
    lines = [
        "Source inventory: entries={0} files={1}".format(entries, files),
        "Creating archive {0} from {1}".format(archive_name, source_abs),
    ]
    try:
        proc = _run(["tar", "-C", parent, "-czf", stage, leaf])
        if proc.returncode != 0:
            raise DomainError(
                "tar failed for {0}".format(source_abs),
                "py-backup help",
            )
        os.chmod(stage, 0o600)
        members = _tar_members(stage)
        got_files = _tar_regular_files(stage)
        if got_files is None:
            raise DomainError(
                "Verification failed: cannot count files in staged archive",
                "py-backup help",
            )
        if len(members) != entries or got_files != files:
            raise DomainError(
                "Verification failed: staged inventory does not match source "
                "(members={0} files={1} source_entries={2} source_files={3})".format(
                    len(members), got_files, entries, files,
                ),
                "py-backup help",
            )
        stage_size = file_size(stage)
        if stage_size <= 0:
            raise DomainError(
                "Verification failed: staged archive empty",
                "py-backup help",
            )
        dest = os.path.join(dest_dir, archive_name)
        lines.append("Depositing to {0}".format(dest))
        _deposit(stage, dest, settings)
        if not os.path.exists(dest):
            raise DomainError(
                "Verification failed: deposited archive missing: {0}".format(dest),
                "py-backup print-sudoers",
            )
        dest_size = file_size(dest)
        if dest_size <= 0 or dest_size != stage_size:
            raise DomainError(
                "Verification failed: deposited size {0} != staged size {1}".format(
                    dest_size, stage_size,
                ),
                "py-backup print-sudoers",
            )
        verify_mode = "stage_counts+dest_size"
        dest_members = len(members)
        dest_files = got_files
        try:
            rel = _tar_members(dest)
        except DomainError:
            rel = []
        rel_files = _tar_regular_files(dest)
        if rel and rel_files is not None:
            if len(rel) != dest_members or rel_files != dest_files:
                raise DomainError(
                    "Verification failed: deposited inventory does not match the stage",
                    "py-backup print-sudoers",
                )
            verify_mode = "dest_tar_list+size"
            dest_members = len(rel)
            dest_files = rel_files
        elif rel:
            if len(rel) != dest_members:
                raise DomainError(
                    "Verification failed: deposited members do not match the stage",
                    "py-backup print-sudoers",
                )
            dest_members = len(rel)
        day = archive_name.split("-")[-2]
        retention = apply_retention(src_name, dest_dir, day, settings)
        lines.append("Backup complete: {0}".format(dest))
        lines.append(
            "Verified: source_files={0} archive_files={1} members={2} size={3} mode={4}".format(
                files, dest_files, dest_members, dest_size, verify_mode,
            )
        )
        if retention["daily_removed"] or retention["total_removed"]:
            lines.append(
                "Retention: daily_removed={0} daily_remaining={1}/{2} "
                "total_removed={3} total_remaining={4}/{5}".format(
                    retention["daily_removed"],
                    retention["daily_remaining"],
                    settings.max_daily,
                    retention["total_removed"],
                    retention["total_remaining"],
                    settings.max_total,
                )
            )
        if settings.json:
            lines.append(json.dumps({
                "verb": "backup",
                "status": "ok",
                "app": settings.app_name,
                "source": source_abs,
                "archive_name": archive_name,
                "destination": dest,
                "backup_notation": settings.notation,
                "source_entries": entries,
                "source_files": files,
                "archive_members": dest_members,
                "archive_files": dest_files,
                "archive_size": dest_size,
                "verified": True,
                "verify_mode": verify_mode,
                "retention_daily_cap": settings.max_daily,
                "retention_daily_removed": retention["daily_removed"],
                "retention_total_cap": settings.max_total,
                "retention_total_removed": retention["total_removed"],
                "version": settings.version,
            }, separators=(",", ":")))
        return "\n".join(lines)
    finally:
        if os.path.isfile(stage):
            try:
                os.remove(stage)
            except OSError:
                pass


def refuse_restore_dest(dest: str, settings: Settings) -> None:
    """Hard-deny system roots and /etc/passwd. Allow this login's /etc name and home."""
    if not dest:
        raise DomainError("Restore destination empty", "py-backup restore <archive> [dest]")
    dest = os.path.abspath(dest)
    if dest in _HARD_ROOTS:
        raise DomainError(
            "Refusing restore to dangerous system path: {0}".format(dest),
            "py-backup restore <archive> <dest-under-your-home>",
        )
    if dest == "/etc/passwd":
        raise DomainError(
            "Refusing restore to protected system path: /etc/passwd",
            "py-backup restore <archive> <dest-under-your-home>",
        )
    dep = settings.deposit_dir()
    if dest == settings.backup_root or dest == dep or dest.startswith(dep + os.sep):
        raise DomainError(
            "Refusing restore into deposit tree: {0}".format(dest),
            "py-backup restore <archive> <dest-under-your-home>",
        )
    user = login_name()
    if user and user != "passwd":
        etc_user = "/etc/" + user
        if dest == etc_user or dest.startswith(etc_user + os.sep):
            return
    home = os.environ.get("HOME", "")
    if home and home not in ("/", "/etc/passwd"):
        home = os.path.abspath(home)
        if dest == home or dest.startswith(home + os.sep):
            return
    for prefix in _SYSTEM_PREFIXES:
        if dest.startswith(prefix):
            raise DomainError(
                "Refusing restore under system path (not on restore dest whitelist): {0}".format(dest),
                "py-backup restore <archive> <dest-under-your-home>",
            )


def parse_project_name(archive: str) -> str:
    base = os.path.basename(archive)
    if base.endswith(".tar.gz"):
        base = base[: -len(".tar.gz")]
    found = re.match(r"^(?P<name>.+)-\d{8}-\d+$", base)
    if found:
        return found.group("name")
    return base


def resolve_archive(spec: str, settings: Settings) -> str:
    """An existing file, a deposit basename, or the latest prefix match."""
    if not spec:
        return ""
    if os.path.isfile(spec):
        return os.path.abspath(spec)
    dep = settings.deposit_dir()
    exact = os.path.join(dep, spec)
    if os.path.isfile(exact):
        return exact
    if not spec.endswith(".tar.gz"):
        with_suffix = os.path.join(dep, spec + ".tar.gz")
        if os.path.isfile(with_suffix):
            return with_suffix
    if not os.path.isdir(dep):
        return ""
    matches = []
    prefix = spec + "-"
    for name in os.listdir(dep):
        if name.startswith(prefix) and name.endswith(".tar.gz"):
            path = os.path.join(dep, name)
            if os.path.isfile(path):
                matches.append(path)
    if not matches:
        return ""
    matches.sort()
    return matches[-1]


def resolve_projects_root(settings: Settings) -> str:
    if settings.projects_root and os.path.isdir(settings.projects_root):
        return settings.projects_root
    cwd = os.path.abspath(os.getcwd())
    marker = os.sep + "prjs"
    if marker in cwd:
        root = cwd.split(marker)[0] + marker
        if os.path.isdir(root):
            return root
    home = os.environ.get("HOME", "")
    for cand in (
        os.path.join(home, "prjs") if home else "",
        "/var/www/html/prjs",
    ):
        if cand and os.path.isdir(cand):
            return cand
    return ""


def _default_dest(project: str, host: str, settings: Settings) -> tuple[str, str]:
    if host in ("ram", "ram-drive", "shm"):
        return "ram-drive", os.path.join(settings.ram_root, project)
    root = resolve_projects_root(settings)
    if not root:
        raise DomainError(
            "Cannot resolve PROJECTS_ROOT for hard-disk restore. Set PROJECTS_ROOT or pass a destination.",
            "py-backup restore <archive> <dest>",
        )
    return "hard-disk", os.path.join(root, project)


def list_archives(settings: Settings) -> str:
    dep = settings.deposit_dir()
    if not os.path.isdir(dep):
        return "Deposit directory missing: {0}".format(dep)
    names = sorted(
        name for name in os.listdir(dep)
        if name.endswith(".tar.gz") and os.path.isfile(os.path.join(dep, name))
    )
    lines = ["Archives under {0}:".format(dep)]
    lines.extend("  " + name for name in names)
    return "\n".join(lines)


def restore(spec: str, dest_in: str, settings: Settings, force: bool = False, host: str = "") -> str:
    """Put an archive back. The default destination is the hard-disk projects tree."""
    if normal_user_only():
        raise DomainError(
            "restore is not available on this command-line class. It does not wrap sudo.",
            "py-backup help",
        )
    if not spec:
        listing = list_archives(settings)
        raise DomainError(
            listing + "\nUsage: py-backup restore <archive|project-prefix> [dest-dir]",
            "py-backup restore <archive|project-prefix> [dest]",
        )
    if shutil.which("tar") is None:
        raise DomainError("tar is required for restore", "py-backup help")
    archive = resolve_archive(spec, settings)
    if not archive or not os.path.exists(archive):
        raise DomainError(
            "Archive not found for '{0}' under {1}.".format(spec, settings.deposit_dir()),
            "py-backup restore",
        )
    project = parse_project_name(archive)
    if dest_in:
        if not os.path.isabs(dest_in):
            dest = os.path.abspath(dest_in)
        else:
            dest = dest_in
        host_name = "explicit"
    else:
        chosen = host or os.environ.get("RESTORE_HOST") or os.environ.get("RESTORE_HOST_DEFAULT") or "hard-disk"
        host_name, dest = _default_dest(project, chosen, settings)
    refuse_restore_dest(dest, settings)
    if os.path.exists(dest):
        try:
            with os.scandir(dest) as scan:
                nonempty = any(scan)
        except OSError:
            nonempty = True
        if nonempty and not force:
            raise DomainError(
                "Destination not empty: {0}".format(dest),
                "py-backup restore {0} {1} --force".format(spec, dest),
            )
    parent = os.path.dirname(dest)
    os.makedirs(parent, mode=0o755, exist_ok=True)
    work = archive
    staged = ""
    if not os.access(archive, os.R_OK):
        if normal_user_only():
            raise DomainError(
                "Cannot read the archive. This login does not wrap sudo.",
                "py-backup help",
            )
        stage_root = resolve_storage()
        staged = os.path.join(stage_root, os.path.basename(archive))
        copied = False
        for cp_bin in ("/usr/bin/cp", "/bin/cp"):
            if _run(["sudo", "-n", cp_bin, archive, stage_root + os.sep]).returncode == 0:
                copied = True
                break
        if not copied or not os.access(staged, os.R_OK):
            raise DomainError(
                "Cannot stage the archive for restore.",
                "py-backup print-sudoers",
            )
        work = staged
    try:
        members = _tar_members(work)
        file_count = _tar_regular_files(work)
        proc = _run(["tar", "-C", parent, "-xzf", work])
        if proc.returncode != 0:
            raise DomainError("tar extract failed for {0}".format(work), "py-backup help")
        restored = os.path.join(parent, project)
        if not os.path.isdir(restored):
            if os.path.isdir(dest):
                restored = dest
            else:
                raise DomainError(
                    "Restore extract did not create expected directory: {0}".format(restored),
                    "py-backup help",
                )
        got_entries, got_files = count_tree(restored)
        if len(members) != got_entries:
            raise DomainError(
                "Restore verification failed: tree entries {0} != archive members {1}".format(
                    got_entries, len(members),
                ),
                "py-backup help",
            )
        if file_count is not None and got_files != file_count:
            raise DomainError(
                "Restore verification failed: tree files {0} != archive files {1}".format(
                    got_files, file_count,
                ),
                "py-backup help",
            )
        lines = [
            "Archive: {0}".format(archive),
            "Restore host SSOT: {0} → {1}".format(host_name, restored),
            "Restore complete: {0}".format(restored),
            "Verified: files={0} entries={1} host={2}".format(got_files, got_entries, host_name),
        ]
        if settings.json:
            lines.append(json.dumps({
                "verb": "restore",
                "status": "ok",
                "app": settings.app_name,
                "archive": archive,
                "destination": restored,
                "restore_host": host_name,
                "project": project,
                "source_entries": got_entries,
                "source_files": got_files,
                "archive_members": len(members),
                "verified": True,
                "version": settings.version,
            }, separators=(",", ":")))
        return "\n".join(lines)
    finally:
        if staged and os.path.isfile(staged):
            try:
                os.remove(staged)
            except OSError:
                pass


def about_fields(settings: Settings) -> list[str]:
    """Domain diagnostics for the about page. Best-effort and honest."""
    from .sudoers import detect_inbound, detect_sudoer_adm, detect_sudoer_cli, host_fragment

    dep = settings.deposit_dir()
    user = login_name()
    fragment = host_fragment(user)
    cli = detect_sudoer_cli(settings)
    adm = detect_sudoer_adm()
    inbound, writable = detect_inbound()
    if os.geteuid() == 0:
        deposit = "root"
    elif os.path.isdir(dep) and os.access(dep, os.W_OK):
        deposit = "writable"
    elif shutil.which("sudo"):
        deposit = "sudo_required"
    else:
        deposit = "not_probeable"
    return [
        "Backup root: {0}".format(settings.backup_root),
        "Backup notation: {0}".format(settings.notation),
        "Deposit directory: {0}".format(dep),
        "Sudo deposit status: {0}".format(deposit),
        "sudoer-cli: {0}".format(cli or "not_found"),
        "sudoer-adm: {0}".format(adm or "absent"),
        "sudoer inbound: {0}".format(inbound or "not_found"),
        "sudoer inbound writable: {0}".format("true" if writable else "false"),
        "host_sudoers_present: {0}".format("true" if fragment else "false"),
        "host_sudoers_path: {0}".format(fragment or "absent"),
    ]


def cache_fields() -> list[str]:
    """Which scratch folder this run can use. A miss is quiet."""
    preferred = os.environ.get("TMPDIR") or "/dev/shm"
    try:
        used = resolve_storage()
    except DomainError:
        used = "unavailable"
    return [
        "Cache folder used: {0}".format(used),
        "Cache folder preferred: {0}".format(preferred),
        "Cache folder 1st: /dev/shm",
        "Cache folder 2nd: /tmp",
        "Persistence storage: {0}".format(persistence_label()),
    ]


def persistence_label() -> str:
    from .storage import persistence_dir
    path = persistence_dir()
    return path or "unavailable"
