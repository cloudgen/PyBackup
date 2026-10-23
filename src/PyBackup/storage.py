# =============================================================================
# Scratch storage and operator errors for PyBackup.
# requirement-python-cli-storage — scratch leaf and persistence.
# requirement-folder-archive-backup — stage under the per-run cache.
# requirement-python-error-handling — one error shape.
# =============================================================================
from __future__ import annotations

import os
import tempfile


class DomainError(Exception):
    """A fail-closed stop with the next step the operator can take."""

    def __init__(self, message: str, nxt: str) -> None:
        super().__init__(message)
        self.message = message
        self.nxt = nxt


def positive_int(raw: str | None, default: int) -> int:
    """A positive integer, or the default when the text is empty or not one."""
    if raw is None or raw == "":
        return default
    if not raw.isdigit():
        return default
    value = int(raw)
    if value <= 0:
        return default
    return value


def login_name() -> str:
    """The invoking login. Never a secret."""
    try:
        import pwd
        return pwd.getpwuid(os.geteuid()).pw_name
    except Exception:
        return os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"


def normal_user_only() -> bool:
    """Termux, Git Bash, and Windows cmd. This class does not wrap sudo.

    requirement-domain-folder-backup — command line for normal user only.
    WSL is not this class.
    """
    prefix = os.environ.get("PREFIX", "")
    if "com.termux" in prefix or os.environ.get("TERMUX_VERSION"):
        return True
    msystem = os.environ.get("MSYSTEM", "")
    if msystem.startswith("MINGW") or msystem.startswith("MSYS"):
        return True
    if os.environ.get("OS") == "Windows_NT":
        comspec = os.environ.get("COMSPEC", "").lower()
        ostype = os.environ.get("OSTYPE", "").lower()
        if "cmd.exe" in comspec and "cygwin" not in ostype and not os.environ.get("WSL_DISTRO_NAME"):
            if not msystem:
                return True
    return False


def resolve_storage() -> str:
    """A private folder for this login and this process.

    Preferred order: TMPDIR, /dev/shm, then /tmp. A folder that cannot be
    used is skipped. The leaf mode is 0700.
    """
    user = login_name()
    leaf = "cache-PyBackup-{0}-{1}".format(user, os.getpid())
    candidates = []
    tmpdir = os.environ.get("TMPDIR", "")
    if tmpdir:
        candidates.append(tmpdir)
    if os.path.isdir("/dev/shm"):
        candidates.append("/dev/shm")
    candidates.append(tempfile.gettempdir() or "/tmp")
    seen = []
    for root in candidates:
        if root in seen:
            continue
        seen.append(root)
        path = os.path.join(root, leaf)
        try:
            os.makedirs(path, mode=0o700, exist_ok=True)
            os.chmod(path, 0o700)
        except OSError:
            continue
        if os.path.isdir(path) and os.access(path, os.W_OK):
            return path
    raise DomainError(
        "No writable scratch folder for this run.",
        "py-backup help",
    )


def persistence_dir() -> str:
    """Notes that survive a reboot. ~/.local/PyBackup."""
    home = os.environ.get("HOME", "")
    if not home:
        return ""
    return os.path.join(home, ".local", "PyBackup")


def config_dir() -> str:
    """Grant drafts this login can read. ~/.config/PyBackup."""
    home = os.environ.get("HOME", "")
    if not home:
        return ""
    return os.path.join(home, ".config", "PyBackup")
