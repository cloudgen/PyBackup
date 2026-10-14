# folder-backup - Local folder archive backup and restore with narrow sudo deposit

![Version](https://img.shields.io/badge/Version-1.26.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/folder-backup?style=flat-square)](https://github.com/cloudgen/folder-backup)

**folder-backup** packs a folder you name into a dated gzip archive under `/var/backup/folder-backup/`, checks the file count and size, and can put that folder back onto the hard-disk projects tree.

| You (your own login) | Admin / already root | Not this |
|----------------------|----------------------|----------|
| Install to `~/.local/bin`, write a grant you can read, submit it, then run backup/restore after an admin has installed the grant | Install into `/usr/local/bin` and install the sudoers fragment | A normal login does not write `/etc`. A terminal with no command does not download. |

| Includes | Excludes |
|----------|----------|
| Pipe install, numbered boards, backup/restore, grant draft, local `install`, self-update | A terminal with no command that downloads |
| Admin-installed narrow grant for `/var/backup` | A normal login writing `/etc` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install from the internet | No root. Places the program in `~/.local/bin` (mode `0700`). | `curl -fsSL https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup \| sh` |
| Open the boards | On a real terminal, a bare run shows client-side, sudoers, self-management, language, and Exit. Server-side is not available. | `folder-backup` |
| Write a grant you can read | JSON under your config folder. An admin still installs it. | `folder-backup generate-sudoer-request` |
| Pack a folder after the grant exists | Copies the archive into `/var/backup/folder-backup/`. | `folder-backup backup /path/to/project` |

## Features

- **Install for yourself**: copy this program into `~/.local/bin` (`install`); remove it (`uninstall`); ask where it lives (`where-is-me`)
- **Pipe install**: `curl … \| sh` places this program (`self-install`). A checkout file copies; a pipe downloads. Your login gets mode `0700`. Root gets `/usr/local/bin` at mode `0755`. `version-check` and `self-update` use the same GitHub raw URL. `self-uninstall` removes that placed binary. A terminal with no command does not do this.
- **Scratch stays with this login and this run**: temporary files live in a private folder named for you and this process. `about` prints the folder in use, the preferred folder, and the fallbacks. A folder that cannot be used is skipped quietly. Notes that must survive a reboot stay in `~/.local/folder-backup`
- **Numbered boards**: on a real terminal, a bare `folder-backup` (or `menu` / `main`) shows client-side, sudoers, self-management, language, and Exit. Server-side is not available, and number 2 stays reserved. **1** then **11** packs a folder. **5** opens grant and drafts (submit and remove). **6** opens install, version, and update. **7** chooses the display language. A finished command returns to the front. **0** steps back.
- **Backup a folder**: pack it to a dated gzip under `/var/backup/folder-backup/`, check counts, then keep at most **5** same-day and **30** total copies per project name
- **Restore**: put an archive back onto the hard-disk projects tree (or a path you name)
- **Restore dest guard**: allow `/etc/<your-login>`; refuse `/etc/passwd` and other system paths
- **Grant you can read**: write JSON (`generate-sudoer-request`); hand it to the approval queue (`submit-sudoer-request`) without writing `/etc`
- **Admin grant install**: print a sudoers draft and an admin script; an admin copies it to `/etc/sudoers.d/`
- **Fail closed**: missing source, unauthorized deposit, verify mismatch, non-empty restore without `--force`
- **Scratch stays with this login and this run**: temporary files live in a private folder named for you and this process. `about` prints the folder in use, the preferred folder, and the fallbacks. A folder that cannot be used is skipped quietly. Notes that must survive a reboot stay in `~/.local/folder-backup`

## Quick Installation

### Online (this is the install)

**Your own login (no root):**

```sh
curl -fsSL https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup | sh
```

That one line places `~/.local/bin/folder-backup` (mode `0700`). It does not print help. A second run says the program is already installed.

**Already a root login.** Same one-liner as root. The file lands in `/usr/local/bin/folder-backup` (mode `0755`):

```sh
curl -fsSL https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup | sh
```

Then:

```sh
folder-backup version
```

**From a checkout** (copy this file, mode `0755`, no download):

```sh
sh src/folder-backup install
```

`sh src/folder-backup` with no command, off a terminal, is the other place: it copies this file the way `self-install` does (mode `0700` for your login). On a terminal that same bare run opens the boards and does not copy.

**Local copy detail (your own login, no root needed):**

```sh
# From this repository checkout
sh src/folder-backup install
# or force refresh after updates
sh src/folder-backup install --force

# Ensure ~/.local/bin is on PATH, then:
folder-backup version
```

**Global (preferred before durable sudoers / production elevation):**

```sh
sudo sh src/folder-backup install
# or: folder-backup install --global   # needs write access to /usr/local/bin
# Managed binary mode is always 0755 so every user can run the installed program.
# If an older install left 0711 (rwx--x--x), re-run: sudo sh src/folder-backup install
```

**Sudoers (required for non-root deposit / restore of root-owned archives):**

```sh
# Prefer: refresh project-sudoers-file + write admin script under /dev/shm
# Production (global install present):
folder-backup print-sudoers-install-script
# Test mode only (local/unmanaged):
folder-backup print-sudoers-install-script --allow-test-local

# Admin (account with sudo rights) — handoff script (path printed by CLI):
sudo sh /dev/shm/folder-backup-<user>-sudoers-admin.sh install   # visudo + install 0440
sudo sh /dev/shm/folder-backup-<user>-sudoers-admin.sh replace   # remove old then install
sudo sh /dev/shm/folder-backup-<user>-sudoers-admin.sh uninstall # leave test elevation
sudo sh /dev/shm/folder-backup-<user>-sudoers-admin.sh status

# Manual equivalent still valid (paths are per-user — multi-user safe):
# sudo visudo -c -f ~/.config/folder-backup/sudoers.fragment-<user>
# sudo install -m 0440 ~/.config/folder-backup/sudoers.fragment-<user> /etc/sudoers.d/folder-backup-<user>
```

**Security note:** Local `~/.local/bin` install is **not** production-secure for host elevation — the user can change the binary and stage trees. Prefer global install for any host that keeps `/etc/sudoers.d/folder-backup-<user>`. Multi-user hosts get **one fragment file per user** (no shared overwrite). See [`SECURITY.md`](./SECURITY.md).

**Named channel verbs.** `self-install` places this program the same way the one-liner above does (your login: `~/.local/bin/folder-backup`, mode `0700`; root: `/usr/local/bin/folder-backup`, mode `0755`). `version-check`, `self-update`, and `self-uninstall` use that channel. Local `install` is a different verb: it copies the file you are running (mode `0755`) and does not download.

```sh
folder-backup self-install
folder-backup version-check
```

**Source repository:** [cloudgen/folder-backup](https://github.com/cloudgen/folder-backup)  
Config identity: `REPO_USER=cloudgen`, `REPO_NAME=folder-backup`. The default channel is `https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup`. Override `SCRIPT_URL` or `REPO_*` before those verbs if you use a fork. An empty `SCRIPT_URL` does not turn the channel off (`:=` fills it). Set a non-empty unreachable URL when you need the verbs to fail closed offline.

**Automatic SHA-256 check** (download path of `self-install` and `self-update` when `CHECKSUM` is unset). The program fetches the companion next to the script:

`https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup.sha256`

The file in this repository is `src/folder-backup.sha256` (one line, 64 hex digits). A `sha256sum` line is also accepted; the first field is the digest.

| Outcome | What happens |
|---------|----------------|
| **Match** | HTTP 200 and the digest equals the downloaded file. Install continues. Human output shows the companion link, the expected value, the actual value, and `Automatic checksum result: PASS`. |
| **Mismatch** | The companion arrived and the digest does not match (or is empty). Install stops. The new file is not placed. |
| **Missing** | The companion is not HTTP 200. Human output warns and the install continues without that check. |

`CHECKSUM` set to a 64-hex digest is a strict pin for that one run: a match installs, a mismatch stops. It is not listed in `help` or `about`. A pin taken from the same URL is the same trust as the automatic companion: the bytes match each other. It is not a separate signature. Local `install` does not download and does not use this check.

After install, on a terminal:

```text
$ folder-backup
[INFO] **folder-backup**(*1.26.0*) — numbered list
[INFO] server-side is not available: this program does not run a host service. Number 2 stays reserved.
1. **client-side**: *this login's folders: pack and restore*
5. **sudoers**: *Grant and drafts*
6. **self-management**: *this CLI install, version, update, uninstall*
7. **language**: *display language for this menu*
9. Exit
Choose a number, or type the command name:
```

![Front board](images/menu-front.png)

```text
[INFO] **folder-backup**(*1.26.0*) — client-side
11. **backup**: *Pack a named folder into a dated gzip archive under /var/backup/folder-backup*
12. **restore**: *Put an archive back onto the hard-disk projects tree*
0. Back
Choose a number, or type the command name:
```

![Client-side](images/menu-client.png)

```text
[INFO] **folder-backup**(*1.26.0*) — sudoers (grant and drafts)
[INFO] test commands are not available: type generate-sudoer-request, print-sudoers, or print-sudoers-install-script. Numbers 51, 53, and 54 stay reserved.
52. **submit-sudoer-request**: *Hand the JSON grant to the approval queue*
55. **remove-project-sudoers**: *Remove the local grant draft only*
0. Back
Choose a number, or type the command name:
```

![Sudoers](images/menu-sudoers.png)

```text
[INFO] **folder-backup**(*1.26.0*) — self-management
61. **install**: *Copy this program into your bin or /usr/local/bin*
62. **version**: *Show version and detailed diagnostics (about)*
63. **about**: *Show diagnostics including sudoers trust tier*
64. **version-check**: *Compare this version with the channel*
65. **self-update**: *Replace the placed binary from the channel*
66. **self-uninstall**: *Remove the channel-placed binary*
67. **self-install**: *Copy this file, or download it when the shell is a pipe*
0. Back
Choose a number, or type the command name:
```

![Self-management](images/menu-self.png)

```text
[INFO] **folder-backup**(*1.26.0*) — language
71. **English**: *use English for this menu*
72. **繁體中文**: *use Traditional Chinese for this menu*
73. **Español**: *use Spanish for this menu*
74. **Français**: *use French for this menu*
75. **Deutsch**: *use German for this menu*
76. **简体中文**: *use Simplified Chinese for this menu*
77. **日本語**: *use Japanese for this menu*
78. **한국어**: *use Korean for this menu*
0. Back
Choose a number, or type the command name:
```

![Language](images/menu-language.png)

Human `help` and human `about` follow the display language. JSON `about` and `folder-backup version` stay English. `generate-sudoer-request`, `print-sudoers`, and `print-sudoers-install-script` stay typed commands. `folder-backup sudoers` is not a command. `folder-backup language` is not a command. In a script or pipe, `folder-backup` with no arguments places this program. Naming `menu` or `self-management` in a script stops: menu needs a terminal.

## Usage

```sh
folder-backup                               # TTY numbered boards; a pipe places this program
folder-backup help
folder-backup menu                          # same boards on a TTY; a script stops: menu needs a terminal
folder-backup about
folder-backup --json about

folder-backup backup /path/to/project
folder-backup restore project-name              # → hard-disk PROJECTS_ROOT/project-name
folder-backup restore project-name --disk       # explicit hard-disk
folder-backup restore project-name --ram        # → /dev/shm/project-name
folder-backup restore NAME-YYYYMMDD-N.tar.gz /explicit/dest
folder-backup restore project-name --force      # allow non-empty dest

folder-backup print-sudoers
folder-backup generate-sudoer-request   # local verified JSON (review this file)
folder-backup submit-sudoer-request     # JSON request into /var/sudoer-cli/sudoer-request (if present)
folder-backup submit-sudoer-request ~/.config/folder-backup/sudoer-request-$(id -un).json
folder-backup uninstall --force
```

**Environment (selected):**

| Variable | Role |
|----------|------|
| `REPO_USER` | Git host owner (default `cloudgen`) |
| `REPO_NAME` | Git repository name (default `folder-backup`) |
| `SCRIPT_URL` | Channel for `self-install` / `version-check` / `self-update` (default `https://raw.githubusercontent.com/cloudgen/folder-backup/main/src/folder-backup`). Empty does not turn it off. |
| `BACKUP_ROOT` | Durable root (default `/var/backup`) |
| `BACKUP_NOTATION` | Subdir (default `folder-backup`) |
| `PROJECTS_ROOT` | Hard-disk projects tree for restore default |
| `RAM_ROOT` | RAM projects root (default `/dev/shm`) |
| `RESTORE_HOST_DEFAULT` | `hard-disk` (default) or `ram-drive` |
| `ALLOW_TEST_LOCAL_SUDOERS` | `1` = allow test-mode `print-sudoers` / `generate-sudoer-request` / `submit-sudoer-request` without `--allow-test-local` |
| `SUDOER_CLI` | Override path to `sudoer-cli` |
| `SUDOER_ADM_USER` | Approver login to detect (default `sudoer-adm`) |
| `FOLDER_BACKUP_LANG` | This run only: `en`, `zh-Hant`, `es`, `fr`, `de`, `zh-Hans`, `ja`, or `ko`. Does not write the language file. A menu pick writes `~/.local/folder-backup/language`. Human `help` and human `about` follow it. JSON `about` and `version` stay English. |

## Examples

```sh
# Backup the RAM genesis tree
folder-backup backup /dev/shm/genesis-template

# Restore latest genesis-template-* archive to hard-disk projects tree
folder-backup restore genesis-template

# Restore into a temporary path
folder-backup restore genesis-template-20260803-3.tar.gz /tmp/genesis-restore
```

## Platform Compatibility

| Platform | Cache | What this program does |
|----------|--------|------------------------|
| Debian 12 (bookworm), Debian 13 (trixie) | Linux chain | Backup and restore. Narrow deposit into `/var/backup/folder-backup` when an admin has installed the grant. No package install |
| Ubuntu 22.04 (jammy), 24.04 (noble), 26.04 (resolute) | Linux chain | Same backup and deposit behavior as Debian. No package install |
| Other Linux (including Debian 11, Ubuntu 20.04, CentOS, Rocky, Alma, Amazon Linux, Oracle Linux) | Linux chain | Same backup and deposit behavior. Cache kind `linux` is not by itself this label |
| Alpine | Linux chain | Same backup and deposit behavior. No `apk` |
| Fedora and Red Hat Enterprise Linux | Linux chain | Same backup and deposit behavior. No `dnf` |
| Termux | Linux chain (this build does not read `TERMUX_VERSION`) | Your own login only. No sudoers fragment, no in-tool sudo, no `pkg` |
| Windows Git Bash | Git Bash chain | Your own login only. No sudoers fragment, no in-tool sudo, no `pkg`. Windows Command Prompt is the same privilege class and is not Git Bash |
| macOS | Mac chain | Cache fallbacks under your home. Not the primary host for `/var/backup/folder-backup`. No `brew` |
| `tar`, `find`, `date` | — | Required |
| `sudo` + narrow sudoers | — | Required for non-root deposit of root-owned archives on a Linux host |

## Related Projects

- [folder-backup](https://github.com/cloudgen/folder-backup) — this product
- [CIAO Defensive Programming](https://github.com/cloudgen/ciao)
- [CIAO-Lite](https://github.com/cloudgen/ciao-lite)
- [selfmanaged](https://github.com/cloudgen/selfmanaged) — bootstrap parent. This product keeps that channel and adds backup, restore, and the numbered boards.

## Contributing

Keep changes surgical. Honor **CIAO-Lite Protection Zones** in `src/folder-backup`. Product behavior must stay consistent with live `docs/requirements/requirement-*.md`. Run `sh tests/run.sh` before proposing commits.

## License

MIT License — see [`LICENSE.md`](./LICENSE.md).

## Last Update

2026-10-14 — version **1.26.0** (front row **5** is sudoers, **6** is self-management, **7** is languages; the terminal boards in Quick Installation are the live capture; eight OS family requirements follow sibling tn5250-cli).

2026-10-10 — version **1.25.0** (the front board and the sudoers board say what is not available, in the same sentence shape).
2026-10-08 — version **1.24.0** (archive file count is regular files; symlinks stay in the archive).
2026-09-30 — version **1.23.0** (human `help` and human `about` follow the display language; JSON `about` and `version` stay English).
2026-09-30 — version **1.22.0** (front row **6** chooses the display language; eight languages; the choice is kept for this login).
2026-09-30 — version **1.21.0** (sudoers moves from client **17** to front **7**; submit is **72** and remove is **75**; Back returns to the front).
2026-09-30 — version **1.20.0** (naming `menu` or `self-management` off a terminal stops; an empty line on the front leaves; row **82** shows diagnostics; a pipe with no command still places this program).
2026-09-30 — version **1.19.0** (a pipe, or `--quiet` / `--json` with no command, places this program; a terminal with no command stays the numbered boards; local `install` stays the mode `0755` copy).
2026-09-30 — version **1.18.0** (numbered boards: client-side, hidden server-side, self-management, Exit; sudoers board shows submit and remove; a finished command returns to the front).
2026-09-30 — version **1.17.0** (rebuilt from selfmanaged; channel verbs explicit; empty argv stays the work list; `install` stays the local copy; automatic SHA-256 companion on download).
2026-09-27 — version **1.16.5** (scratch folder is per login and per process; `about` prints used, preferred, 1st fallback, and 2nd fallback; a skipped folder is silent).
2026-09-23 — version **1.16.4** (private cache leaf mode 0700; live cache line in about; multi-draft remove reads the choice in this shell).
2026-09-06 — version **1.16.3** (help lists grant-emit testers apart; README people-and-folders voice; requirement human-facing + coverage).
2026-09-03 — version **1.16.2** (suite no longer queues live sudoer inbound; TP-CLI-13 / L-INBOUND-02).
2026-09-03 — version **1.16.1** (dedicated sudoers-submenu requirement; five grant/draft setup verbs stay live CLI commands; TP-CLI-13/16/18).
2026-09-03 — version **1.15.0** (numbered list look: **folder-backup**(*version*) header; italic gray descriptions; TP-CLI-18).
2026-08-30 — version **1.14.0** (storage = cache folder + persistence `${HOME}/.local/folder-backup/`; TP-CLI-06/12).
2026-08-30 — version **1.13.0** (about Cache folder preferred `/dev/shm/cache/cache-folder-backup`; TP-CLI-06/12).
2026-08-28 — version **1.12.0** (TTY empty argv opens the numbered work list; off-TTY still help; TP-CLI-07/13).
2026-08-23 — version **1.11.0** (`menu` / `main` numbered work list; TP-CLI-13..16).
2026-08-23 — version **1.10.0** (`print-sudoers` / JSON emit `backup *` / `restore *`; TP-26; INC-20260823-001).
2026-08-18 — housekeeping: Description rewritten in people-and-folders voice (no Type-1 lead); install heading says “your own login.” Version still **1.9.0** (no product-source change).
2026-08-17 — version **1.9.0** (`generate-sudoer-request`; independent generate dest; operator-readable errors; TP-24/25).
2026-08-17 — version **1.8.2** (submit **update** when `/etc/sudoers.d/folder-backup-<user>` exists; TP-23).
2026-08-17 — version **1.8.1** (submit inbound fidelity; pretty JSON re-encode; TP-22e/22f; review JR-1..8).
2026-08-15 — version **1.8.0** (JSON sudoer file = `folder-backup` backup/restore only; TP-22/22b/22c).
