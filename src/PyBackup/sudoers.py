# =============================================================================
# Grant drafts. This login does not write /etc.
# requirement-sudoer-json-file — four command objects, compact JSON.
# requirement-three-layer-privilege-model — generate, submit, print, remove.
# requirement-domain-folder-backup — verb catalog.
# =============================================================================
from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime

from .archive import Settings
from .storage import DomainError, config_dir, login_name

FORBIDDEN_SNIPS = (
    "/usr/bin/mkdir",
    "/bin/mkdir",
    "/usr/bin/cp",
    "/bin/cp",
    "/usr/bin/tar",
    "/bin/tar",
    "/bin/rm ",
    "/usr/bin/rm ",
    "/usr/bin/install",
    "/usr/bin/chmod",
    "/bin/chmod",
)


def _user() -> str:
    return login_name()


def grant_commands(path: str) -> list[dict]:
    """The only elevated argv this product emits. Four objects. No OS tools."""
    specs = (
        ["backup", "*"],
        ["restore", "*"],
        ["--json", "backup", "*"],
        ["--json", "restore", "*"],
    )
    return [
        {"runas": "root", "tags": ["NOPASSWD"], "path": path, "args": list(args)}
        for args in specs
    ]


def grant_object(settings: Settings, action: str, user: str, purpose: str = "") -> dict:
    if action not in ("add", "update"):
        raise DomainError(
            "action must be add or update (got {0})".format(action),
            "py-backup generate-sudoer-request --add",
        )
    if not purpose:
        purpose = "Allow {0} to run {1} backup and restore as root.".format(user, settings.console)
    return {
        "schema_version": 1,
        "purpose": purpose,
        "username": user,
        "service": settings.app_name,
        "action": action,
        "commands": grant_commands(settings.grant_path()),
    }


def grant_compact(body: dict) -> str:
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False)


def refuse_forbidden(text: str, path: str) -> None:
    for snip in FORBIDDEN_SNIPS:
        if snip in text:
            raise DomainError(
                "refusing sudoer grant with OS-tool commands (need {0} backup|restore only)".format(
                    path,
                ),
                "py-backup generate-sudoer-request",
            )


def verify_verbs(text: str, path: str) -> None:
    if '"backup"' not in text:
        raise DomainError(
            "Sudoer file is incomplete: it does not allow backup. Path: {0}".format(path),
            "py-backup generate-sudoer-request",
        )
    if '"restore"' not in text:
        raise DomainError(
            "Sudoer file is incomplete: it does not allow restore. Path: {0}".format(path),
            "py-backup generate-sudoer-request",
        )
    if '"*"' not in text:
        raise DomainError(
            "Sudoer file is incomplete: backup and restore need a sudoers operand wildcard (*). Path: {0}".format(path),
            "py-backup generate-sudoer-request",
        )
    if '"--json"' not in text:
        raise DomainError(
            "Sudoer file is incomplete: backup and restore need the --json twins. Path: {0}".format(path),
            "py-backup generate-sudoer-request",
        )


def trust_tier(settings: Settings) -> str:
    """production when the global console script is executable. Else test_local or unmanaged."""
    global_path = settings.grant_path()
    home = os.environ.get("HOME", "")
    local_path = os.path.join(home, ".local", "bin", settings.console) if home else ""
    if os.path.isfile(global_path) and os.access(global_path, os.X_OK):
        return "production"
    if local_path and os.path.isfile(local_path) and os.access(local_path, os.X_OK):
        return "test_local"
    return "unmanaged"


def require_emit_trust(settings: Settings, verb: str, allow_test: bool) -> str:
    tier = trust_tier(settings)
    if tier != "production" and not allow_test and os.environ.get("ALLOW_TEST_LOCAL_SUDOERS") != "1":
        raise DomainError(
            "{0} trust tier is {1} (not production).".format(verb, tier),
            "py-backup {0} --allow-test-local".format(verb),
        )
    return tier


def host_fragment(user: str) -> str:
    """This user's host sudoers file, including the folder-backup legacy name."""
    names = (
        "PyBackup-{0}".format(user),
        "py-backup-{0}".format(user),
        "folder-backup-{0}".format(user),
    )
    for name in names:
        path = os.path.join("/etc/sudoers.d", name)
        if os.path.isfile(path):
            return path
    return ""


def default_action(explicit: str) -> tuple[str, str, str]:
    """Return action, source, and host path. Host file present means update."""
    user = _user()
    fragment = host_fragment(user)
    if explicit in ("add", "update"):
        return explicit, "explicit", fragment
    if fragment:
        return "update", "detected", fragment
    return "add", "detected", ""


def _refuse_dest(path: str, verb: str) -> None:
    if path == "/etc" or path.startswith("/etc/"):
        raise DomainError(
            "{0} refuses to write under /etc.".format(verb),
            "py-backup {0} ~/.config/PyBackup/sudoer-request.json".format(verb),
        )
    if path == "/var/sudoer-cli" or path.startswith("/var/sudoer-cli/"):
        raise DomainError(
            "{0} does not write inbound.".format(verb),
            "py-backup generate-sudoer-request",
        )
    if os.path.islink(path):
        raise DomainError("refusing symlink dest: {0}".format(path), "py-backup help")
    if os.path.isdir(path):
        raise DomainError("dest is a directory: {0}".format(path), "py-backup help")


def default_json_path(user: str) -> str:
    folder = config_dir()
    if not folder:
        raise DomainError("HOME is not set.", "py-backup help")
    return os.path.join(folder, "sudoer-request-{0}.json".format(user))


def default_fragment_path(user: str) -> str:
    folder = config_dir()
    if not folder:
        raise DomainError("HOME is not set.", "py-backup help")
    return os.path.join(folder, "sudoers.fragment-{0}".format(user))


def generate(settings: Settings, dest: str = "", action: str = "", allow_test: bool = False, purpose: str = "") -> str:
    """Write a compact JSON grant this login can read. No /etc. No inbound mkdir."""
    user = _user()
    chosen, source, fragment = default_action(action)
    require_emit_trust(settings, "generate-sudoer-request", allow_test)
    path = dest or default_json_path(user)
    _refuse_dest(path, "generate-sudoer-request")
    folder = os.path.dirname(path)
    os.makedirs(folder, mode=0o700, exist_ok=True)
    body = grant_object(settings, chosen, user, purpose)
    text = grant_compact(body) + "\n"
    refuse_forbidden(text, settings.grant_path())
    verify_verbs(text, path)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    if not os.access(path, os.R_OK):
        raise DomainError(
            "generated sudoer file is not readable: {0}".format(path),
            "py-backup generate-sudoer-request",
        )
    lines = [
        "Wrote verified sudoer file to {0}".format(path),
        "Grant allows: {0} backup and restore (action={1} {2})".format(settings.console, chosen, source),
        "Convert check: skipped unless sudoer-cli is on PATH. File still lists backup and restore.",
        "Review the file, then submit it:",
        "   py-backup submit-sudoer-request {0}".format(path),
    ]
    if fragment:
        lines.append("host_fragment={0}".format(fragment))
    if settings.json:
        lines.append(json.dumps({
            "verb": "generate-sudoer-request",
            "status": "written",
            "path": path,
            "readable": True,
            "verified": True,
            "action": chosen,
            "action_source": source,
            "host_fragment_present": bool(fragment),
            "user": user,
        }, separators=(",", ":")))
    return "\n".join(lines)


def fragment_text(settings: Settings, user: str, tier: str) -> str:
    path = settings.grant_path()
    installed = "/etc/sudoers.d/PyBackup-{0}".format(user)
    purpose = "Allow {0} to run {1} backup and restore as root.".format(user, settings.console)
    if tier == "production":
        banner = (
            "# Trust tier: production (global managed binary: {0})\n"
            "# Install as {1} (per-user suffix)."
        ).format(path, installed)
    else:
        banner = (
            "# WARNING: TEST MODE ONLY — NOT PRODUCTION-SECURE\n"
            "# Local/unmanaged install can be rewritten by this login.\n"
            "# Uninstall this fragment soon:\n"
            "#   sudo rm {0}"
        ).format(installed)
    lines = [
        "# Purpose: {0}".format(purpose),
        "# {0} — backup/restore only (review before install)".format(settings.console),
        "# Target user: {0}".format(user),
        "# Install: sudo install -m 0440 <this-file> {0}".format(installed),
        "# Validate: sudo visudo -c -f {0}".format(installed),
        "# Trust tier: {0}".format(tier),
        banner,
        "# Grant is the project command only.",
        "{0} ALL=(root) NOPASSWD: {1} backup *".format(user, path),
        "{0} ALL=(root) NOPASSWD: {1} restore *".format(user, path),
        "{0} ALL=(root) NOPASSWD: {1} --json backup *".format(user, path),
        "{0} ALL=(root) NOPASSWD: {1} --json restore *".format(user, path),
        "",
    ]
    return "\n".join(lines)


def print_sudoers(settings: Settings, dest: str = "", allow_test: bool = False) -> str:
    """Write the text dual. Does not copy it to /etc."""
    user = _user()
    tier = require_emit_trust(settings, "print-sudoers", allow_test)
    path = dest or default_fragment_path(user)
    _refuse_dest(path, "print-sudoers")
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    text = fragment_text(settings, user, tier)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return "Wrote project-sudoers-file to {0}\nThis command did not write /etc.".format(path)


def admin_script(settings: Settings, fragment: str, user: str) -> str:
    installed = "/etc/sudoers.d/PyBackup-{0}".format(user)
    return """#!/bin/sh
# Admin handoff for PyBackup. A normal login does not run this against /etc.
set -eu
FRAGMENT={fragment}
INSTALLED={installed}
cmd=${{1:-status}}
case "$cmd" in
  install)
    visudo -c -f "$FRAGMENT"
    install -m 0440 "$FRAGMENT" "$INSTALLED"
    ;;
  uninstall)
    rm -f "$INSTALLED"
    ;;
  replace)
    rm -f "$INSTALLED"
    visudo -c -f "$FRAGMENT"
    install -m 0440 "$FRAGMENT" "$INSTALLED"
    ;;
  status)
    if [ -f "$INSTALLED" ]; then
      echo "present $INSTALLED"
    else
      echo "absent $INSTALLED"
    fi
    ;;
  *)
    echo "usage: sh $0 install|uninstall|replace|status" >&2
    exit 1
    ;;
esac
""".format(fragment=sh_quote(fragment), installed=sh_quote(installed))


def sh_quote(text: str) -> str:
    return "'" + text.replace("'", "'\"'\"'") + "'"


def print_install_script(settings: Settings, dest: str = "", allow_test: bool = False) -> str:
    """Write the admin script under /dev/shm or the temp dir. Does not install it."""
    user = _user()
    require_emit_trust(settings, "print-sudoers-install-script", allow_test)
    fragment = default_fragment_path(user)
    if not os.path.isfile(fragment):
        print_sudoers(settings, fragment, allow_test=allow_test)
    if dest:
        path = dest
        _refuse_dest(path, "print-sudoers-install-script")
        os.makedirs(os.path.dirname(path) or ".", mode=0o700, exist_ok=True)
    else:
        folder = "/dev/shm" if os.path.isdir("/dev/shm") and os.access("/dev/shm", os.W_OK) else config_dir()
        path = os.path.join(folder, "py-backup-{0}-sudoers-admin.sh".format(user))
    text = admin_script(settings, fragment, user)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o700)
    return (
        "Wrote admin script to {0}\n"
        "Admin (sudo): sudo sh {0} install\n"
        "This command did not write /etc."
    ).format(path)


def list_drafts(user: str) -> list[str]:
    folder = config_dir()
    if not folder or not os.path.isdir(folder):
        return []
    found = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isfile(path) or os.path.islink(path):
            continue
        if name.startswith("sudoers.fragment-") or name.startswith("sudoer-request-"):
            found.append(path)
    return found


def remove_draft(path: str, force: bool, confirm: bool) -> str:
    """Delete a local draft. Never a path under /etc."""
    if not path:
        drafts = list_drafts(_user())
        if not drafts:
            raise DomainError(
                "No project-sudoers draft to remove.",
                "py-backup generate-sudoer-request",
            )
        if len(drafts) > 1 and not force:
            listing = "\n".join(drafts)
            raise DomainError(
                "Several drafts. Name one path.\n{0}".format(listing),
                "py-backup remove-project-sudoers <path> --force",
            )
        path = drafts[0]
    if path == "/etc" or path.startswith("/etc/"):
        raise DomainError(
            "remove-project-sudoers does not delete /etc ({0}).".format(path),
            "py-backup remove-project-sudoers",
        )
    if os.path.islink(path):
        raise DomainError("refusing symlink: {0}".format(path), "py-backup help")
    if not os.path.isfile(path):
        raise DomainError("draft not found: {0}".format(path), "py-backup remove-project-sudoers")
    if not force and not confirm:
        raise DomainError(
            "Refusing to remove {0} without confirmation.".format(path),
            "py-backup remove-project-sudoers {0} --force".format(path),
        )
    os.remove(path)
    return "Removed project-sudoers draft {0}\nThis command did not write /etc.".format(path)


def detect_sudoer_cli(settings: Settings) -> str:
    forced = os.environ.get("SUDOER_CLI", "")
    if forced:
        return forced if os.path.isfile(forced) and os.access(forced, os.X_OK) else ""
    for folder in (settings.global_bin, os.path.join(os.environ.get("HOME", ""), ".local", "bin")):
        path = os.path.join(folder, "sudoer-cli")
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    found = shutil.which("sudoer-cli")
    return found or ""


def detect_sudoer_adm() -> str:
    name = os.environ.get("SUDOER_ADM_USER", "sudoer-adm")
    proc = subprocess.run(["id", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if proc.returncode == 0:
        return name
    return ""


def detect_inbound() -> tuple[str, bool]:
    """The public queue if it already exists. This function does not create it."""
    override = os.environ.get("SUDOER_QUEUE_INBOUND", "")
    candidates = []
    if override:
        candidates.append(override)
    app = os.environ.get("SUDOER_APPROVAL_APP", "sudoer-cli")
    base = os.environ.get("SUDOER_INBOUND_BASENAME", "sudoer-request")
    public = os.environ.get("SUDOER_PUBLIC_ROOT", "/var/{0}".format(app))
    candidates.append(os.path.join(public, base))
    for path in candidates:
        if path and os.path.isdir(path):
            return path, os.access(path, os.W_OK)
    return "", False


def submit(
    settings: Settings,
    src: str = "",
    action: str = "",
    allow_test: bool = False,
    purpose: str = "",
) -> str:
    """Hand a JSON grant to sudoer-cli. Does not mkdir the inbound and does not write /etc."""
    user = _user()
    chosen, source, fragment = default_action(action)
    if not purpose:
        purpose = "Allow {0} to run {1} backup and restore as root.".format(user, settings.console)
    if src:
        if not os.path.isfile(src) or os.path.islink(src):
            raise DomainError(
                "sudoers file not found: {0}".format(src),
                "py-backup generate-sudoer-request",
            )
        with open(src, "r", encoding="utf-8") as handle:
            text = handle.read()
        refuse_forbidden(text, src)
        verify_verbs(text, src)
        payload = src
        cleanup = False
    else:
        require_emit_trust(settings, "submit-sudoer-request", allow_test)
        folder = config_dir()
        os.makedirs(folder, mode=0o700, exist_ok=True)
        payload = os.path.join(folder, ".submit-{0}.json".format(os.getpid()))
        body = grant_object(settings, chosen, user, purpose)
        text = grant_compact(body) + "\n"
        verify_verbs(text, payload)
        with open(payload, "w", encoding="utf-8") as handle:
            handle.write(text)
        cleanup = True
    try:
        cli = detect_sudoer_cli(settings)
        if not cli:
            raise DomainError(
                "sudoer-cli not found. Submit does not write /etc.",
                "py-backup help",
            )
        adm = detect_sudoer_adm()
        if not adm:
            raise DomainError(
                "sudoer-adm not found. Ask an admin to run: sudo sudoer-cli setup",
                "py-backup help",
            )
        inbound, writable = detect_inbound()
        if not inbound:
            raise DomainError(
                "sudoer inbound queue not found (preferred /var/sudoer-cli/sudoer-request). "
                "This command does not create it.",
                "py-backup help",
            )
        if not writable:
            raise DomainError(
                "sudoer inbound not writable: {0}".format(inbound),
                "py-backup help",
            )
        verb = "update-sudoer-request" if chosen == "update" else "add-sudoer-request"
        argv = [cli]
        if settings.json:
            argv.append("--json")
        queue_root = os.path.dirname(inbound)
        if os.environ.get("SUDOER_QUEUE_INBOUND"):
            argv.extend(["--queue-root", queue_root])
        argv.extend([
            verb,
            "--file", payload,
            "--purpose", purpose,
            "--service", settings.app_name,
        ])
        proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        out = proc.stdout.decode("utf-8", "replace")
        err = proc.stderr.decode("utf-8", "replace").strip()
        if proc.returncode != 0:
            raise DomainError(
                "sudoer-cli {0} failed: {1}".format(verb, err or "exit {0}".format(proc.returncode)),
                "py-backup generate-sudoer-request",
            )
        request_id = ""
        for token in out.replace(",", " ").split():
            if "request_id" in token and "=" in token:
                request_id = token.split("=", 1)[1].strip('"')
        if '"request_id"' in out:
            try:
                parsed = json.loads(out)
                request_id = str(parsed.get("request_id", request_id))
            except json.JSONDecodeError:
                pass
        if request_id:
            queued = os.path.join(inbound, request_id)
            if os.path.isfile(queued) and os.access(queued, os.R_OK):
                with open(queued, "r", encoding="utf-8") as handle:
                    body = handle.read()
                verify_verbs(body, queued)
        lines = [
            "Submitted {0} request via {1}".format(chosen, cli),
            "action_source={0}".format(source),
            "host_fragment={0}".format(fragment or "absent"),
            "inbound={0}  (approver: {1})".format(inbound, adm),
            "This CLI did not write /etc. Approver must approve the request.",
        ]
        if request_id:
            lines.insert(1, "request_id={0}".format(request_id))
        if settings.json:
            lines.append(json.dumps({
                "verb": "submit-sudoer-request",
                "status": "submitted",
                "request_id": request_id,
                "action": chosen,
                "action_source": source,
                "host_fragment_present": bool(fragment),
                "service": settings.app_name,
                "user": user,
                "sudoer_cli": cli,
                "sudoer_adm": adm,
                "inbound": inbound,
            }, separators=(",", ":")))
        return "\n".join(lines)
    finally:
        if cleanup and os.path.isfile(payload):
            try:
                os.remove(payload)
            except OSError:
                pass
