**file**: docs/requirements/requirement-other-linux.md
**Status**: Active (Version 1.0.0)
**Area**: shell
**Key**: `requirement-other-linux`
**ID**: RQ-OTHER-LINUX
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement owns the other-Linux family label for folder-backup: a Linux host that is not Debian 12 or 13, not Ubuntu 22.04, 24.04, or 26.04, not Alpine, not Fedora, not Red Hat Enterprise Linux, and not Termux.

Family labels cite detection pairs from sibling project tn5250-cli. Those pairs name the host. They do not import that project's compiler install, CMake build, or payload copy. folder-backup backs up and restores folder archives. It does not build a curses client.

The ship unit's live host split is `util_cache_host_kind` in `src/folder-backup`. It returns `linux`, `gitbash`, or `mac`. Force with `FOLDER_BACKUP_CACHE_HOST` or `SELFMANAGED_CACHE_HOST`. Git Bash for that function is a non-empty `MSYSTEM`, or `uname -s` matching `MINGW*` or `MSYS*`. Mac is `uname -s` `Darwin`. Every other `uname` returns `linux`, including Termux, Debian, Ubuntu, Alpine, Fedora, Red Hat Enterprise Linux, other Linux, and a BSD `uname`. The function does not read `/etc/os-release` and does not read `TERMUX_VERSION`. It does not refuse a host. Cache paths stay on `docs/requirements/requirement-shell-cli-storage.md`. This file must not invent a second chain. This product does not compile a C payload, does not install compiler packages, and does not report `payload_platform`.

### 1.1 Human-facing

**In one sentence:** This requirement owns the other-Linux family label for folder-backup: a Linux host that is not Debian 12 or 13, not Ubuntu 22.04, 24.04, or 26.04, not Alpine, not Fedora, not Red Hat Enterprise Linux, and not Termux.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person running `folder-backup` on this family | `folder-backup about` |
| The other role | An admin on a Linux host who installs the narrow deposit grant | The grant file is still installed by hand |
| Not this file | Cache folder paths, and the archive deposit workflow | Those stay on the storage and privilege requirements |

| Includes | Excludes |
|----------|----------|
| Which host this family name means, and what folder-backup does on it | A second cache chain; a C compiler install; a hard stop that lists every platform |

| Surface | What you open | What for |
|---------|---------------|----------|
| `folder-backup` | the ship unit | backup, restore, and the numbered boards |
| `folder-backup about` | storage lines | the cache folder this process chose |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Back up a folder | The archive is staged in this login's cache, then deposited when this host's privilege law allows it | `folder-backup backup /path/to/project` |
| See the cache | about names the folder in use, the preferred folder, and the fallbacks | `folder-backup about` |

## 2. Core Rules / Requirements (Mandatory)

1. This file is the only folder-backup owner of the other-Linux family label.
2. The cited detect, from sibling project tn5250-cli, requirement `requirement-other-linux.md`, accepts the host when `uname -s` is `Linux`, the Debian requirement does not claim the host, the Ubuntu requirement does not claim the host, Alpine is not detected, Fedora and Red Hat Enterprise Linux are not detected, Termux is not detected, and macOS is not detected.
3. Termux is `TERMUX_VERSION` set. Alpine is `/etc/os-release` `ID=alpine`. Fedora is `ID=fedora`. Red Hat Enterprise Linux is `ID=rhel`. macOS is `uname -s` `Darwin`. This situation must not claim those hosts.
4. An Ubuntu release outside 22.04, 24.04, and 26.04, and a Debian release outside 12 and 13, are this situation when `uname -s` is `Linux` and the sibling's mismatch rules do not stop them. Debian 11 is this situation. A Debian or Ubuntu identity mismatch is the sibling's stop. This product does not implement that stop, and this file does not claim the mismatched host as other Linux.
5. `ID=centos`, `ID=rocky`, `ID=almalinux`, `ID=amzn`, and `ID=ol` stay this situation. `ID_LIKE` does not by itself select Debian, Ubuntu, Fedora, or Red Hat Enterprise Linux. A derivative that uses `dnf` and whose `ID` is not `fedora` and not `rhel` stays here.
6. The sibling refuses BSD, Git Bash, and Windows from this situation. This product does not implement that refusal. A BSD `uname` makes `util_cache_host_kind` return `linux`. That return is the cache kind. It is not a claim that BSD is other Linux.
7. On a host that is this family, the cache chain is the Linux chain. Narrow archive deposit stays `requirement-three-layer-privilege-model`. This file does not call `apt-get`, `apk`, `dnf`, `pacman`, or `zypper`.

### 2.1 Implementation Notes (this product)

| Item | Value |
|------|--------|
| **Product** | `folder-backup` |
| **Family** | Other Linux, as the sibling defines the remainder |
| **Cited detect** | `uname -s` `Linux`, and none of the named families |
| **Ship unit today** | Cache kind `linux` for every `uname` that is not Git Bash and not Darwin |
| **BSD** | Not this family. Cache kind may still be `linux`. No refuse message |
| **Deposit** | `/var/backup/folder-backup` when the three-layer grant applies |
| **Honesty** | Label is law. No platform-list refusal is implemented |

### 2.2 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Other Linux is the remainder, not a silent synonym for every `uname`.
- **Principle 2 – Intentional**: CentOS, Rocky, Alma, Amazon Linux, and Oracle Linux stay here even when they use `dnf`.
- **Principle 13 – Multi environment**: One backup behavior for that remainder. No per-distro package install.

## Under command line for normal user only

This family is a Linux host, not a command line for normal user only. Termux is `requirement-termux`. Git Bash and Windows cmd are `requirement-windows-git-bash`.

**This requirement:** folder-backup does not install packages on other Linux. It does not call `pkg`. Archive deposit stays the three-layer requirement. Dedicated system user privilege stays unused.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The family name is a label. The ship unit's live split stays the three cache kinds.
- **Intentional:** Detection pairs are cited from the sibling so two products name the same host the same way.
- **Anti-fragile:** A host that matches no family still runs. This file does not add a refuse path.
- **Over-protect:** Cache paths stay on the storage requirement. Deposit stays on the privilege requirement.
- **Principle 10 – Least privilege**: No package-manager sudo on this remainder.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Copy the sibling's compiler install, CMake configure, or payload copy into this product.
2. Replace `util_cache_host_kind` with the sibling's detect pair. That function is a reusable cache classifier.
3. Add a second cache chain in this file.
4. Add `payload_platform` to `about` or `--json about`.
5. Exit non-zero with a platform list when no family matches, unless that stop is implemented and tested. It is not implemented.
6. Write this product's rules into sibling project tn5250-cli.
7. Treat `ID_LIKE` as a selector for Debian, Ubuntu, Alpine, Fedora, or Red Hat Enterprise Linux.
8. Refuse BSD, Git Bash, or Windows from folder-backup with the sibling's platform list. That stop is not this product's behavior.
9. Treat cache kind `linux` as proof that the host is other Linux.

**Violating this rule mixes a compiler product into a backup tool, or invents a host stop the ship unit does not have.**

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-shell-cli-storage.md` | Cache chain and persistence (`requirement-shell-cli-storage`) |
| `docs/requirements/requirement-three-layer-privilege-model.md` | Narrow archive deposit on a Linux host (`requirement-three-layer-privilege-model`) |
| `docs/requirements/requirement-folder-archive-backup.md` | Backup and restore operations |
| `src/folder-backup` | Ship unit. `util_cache_host_kind` is the live host split |
| Sibling project tn5250-cli, requirement `requirement-other-linux.md` | Other-Linux detection remainder. Not this product's backup behavior |
| `docs/requirements/requirement-debian.md` | Debian 12 and 13 are not this remainder |
| `docs/requirements/requirement-ubuntu.md` | Ubuntu 22.04, 24.04, and 26.04 are not this remainder |
| `docs/requirements/requirement-alpine.md` | `ID=alpine` is not this remainder |
| `docs/requirements/requirement-fedora-redhat.md` | `ID=fedora` and `ID=rhel` are not this remainder |
| `docs/requirements/requirement-termux.md` | A set `TERMUX_VERSION` is not this remainder |
| `docs/requirements/requirement-macos.md` | Darwin is not this remainder |

## Design-time verification

| TP family / ID | What it proves | Status |
|----------------|----------------|--------|
| TP-CLI-12 | Cache kind `linux` uses the Linux chain | have — does not prove the other-Linux remainder |
| RQ-OTHER-LINUX refuse | No platform-list refusal in the ship unit | law only — not a test gate |

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`

## Terminologies

Copied substance for the words this requirement uses. No harness paths.

### Command line for normal user only

**Definition:** A command line for normal user only is a POSIX-like shell whose privilege ceiling is normal user privilege. Typical instances are Termux, Git Bash, and Windows cmd. There is no usable root or sudo host change and no dedicated system account for this login. When the ship unit detects this kind of shell, it must not implement admin privilege or dedicated system user privilege: no in-tool sudo, no apt or dnf wrap, no /etc destination, no useradd, and no switch to a dedicated system user.

**Human daily-life explanation:** A command line for normal user only is a keyboard that only has your keys. Termux on a phone, Git Bash on Windows, and Windows cmd / Command Prompt are this kind of room: you can tidy your own drawer; you cannot borrow the building site key or put on a dedicated-operator badge.

**Daily-life example:** On Termux you run pkg as yourself. On Git Bash you run git as yourself. On Windows cmd you type as yourself. None of those rooms should grow a sudo apt or a hidden system-user switch.

### Git Bash

**Definition:** Git Bash is an instance of command line for normal user only: the MSYS/MINGW POSIX shell shipped with Git for Windows. Primary glossary detect is the directory /c/ or /c (Windows C: as Git Bash mounts it; default drive /c/). Secondary: MSYSTEM is MINGW* / MSYS* / UCRT* / CLANG*, or uname -s is MINGW* / MSYS*. Exclude WSL (WSL_DISTRO_NAME). On detect, admin privilege and dedicated system user privilege stay unused. Git Bash has no Termux pkg.

**Human daily-life explanation:** Git Bash is a Windows drawer that only opens with your keys. It looks like a Unix shell; it is not a Linux superintendent desk.

**Daily-life example:** You run git and this program as yourself. The program must not grow sudo apt or a dedicated system-user switch because you opened Git Bash.

### Termux

**Definition:** Termux is an instance of command line for normal user only: Android userspace POSIX with this-login PREFIX. Workshop detect stays PREFIX / TERMUX_VERSION / Termux usr tree. On detect, admin privilege and dedicated system user privilege stay unused. Named pkg as this login stays normal user privilege.

**Human daily-life explanation:** Termux is a phone drawer that only opens with your keys.

**Daily-life example:** pkg install as the Termux login is that phone's own package tool. sudo apt and a hidden system-user switch are not.

### Windows cmd

**Definition:** Windows cmd is an instance of command line for normal user only: the Windows-native console family, Command Prompt (cmd.exe) and the same Windows command-line, including PowerShell when it is not Git Bash, Cygwin, or WSL. Typical detect: OS is Windows_NT, or COMSPEC names cmd.exe, after excluding Git Bash (MSYSTEM / MINGW / MSYS), Cygwin (uname CYGWIN*), and WSL (WSL_DISTRO_NAME or uname Linux). On detect, admin privilege and dedicated system user privilege stay unused. Windows cmd has no Termux pkg and no Unix sudo or apt.

**Human daily-life explanation:** Windows cmd is a Windows drawer that only opens with your keys. It is the ordinary Command Prompt / Windows command-line. It is not a Linux superintendent desk and it is not Git Bash.

**Daily-life example:** You type commands in Command Prompt or PowerShell as yourself. The program must not grow sudo apt or a dedicated system-user switch because you opened Windows cmd.

## 6. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-14 | Active 1.0.0 | Family label for folder-backup. Detection pairs cited from sibling project tn5250-cli, requirement `requirement-other-linux.md`. No payload build. Cache chain stays on the storage requirement. |

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
