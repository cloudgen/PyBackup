**file**: docs/requirements/requirement-termux.md
**Status**: Active (Version 1.0.0)
**Area**: shell
**Key**: `requirement-termux`
**ID**: RQ-TERMUX
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement owns the Termux family label for folder-backup.

Family labels cite detection pairs from sibling project tn5250-cli. Those pairs name the host. They do not import that project's compiler install, CMake build, or payload copy. folder-backup backs up and restores folder archives. It does not build a curses client.

The ship unit's live host split is `util_cache_host_kind` in `src/folder-backup`. It returns `linux`, `gitbash`, or `mac`. Force with `FOLDER_BACKUP_CACHE_HOST` or `SELFMANAGED_CACHE_HOST`. Git Bash for that function is a non-empty `MSYSTEM`, or `uname -s` matching `MINGW*` or `MSYS*`. Mac is `uname -s` `Darwin`. Every other `uname` returns `linux`, including Termux, Debian, Ubuntu, Alpine, Fedora, Red Hat Enterprise Linux, other Linux, and a BSD `uname`. The function does not read `/etc/os-release` and does not read `TERMUX_VERSION`. It does not refuse a host. Cache paths stay on `docs/requirements/requirement-shell-cli-storage.md`. This file must not invent a second chain. This product does not compile a C payload, does not install compiler packages, and does not report `payload_platform`.

### 1.1 Human-facing

**In one sentence:** This requirement owns the Termux family label for folder-backup.

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

1. This file is the only folder-backup owner of the Termux family label.
2. The cited detect, from sibling project tn5250-cli, requirement `requirement-termux-cli-coding.md`, accepts the host when `TERMUX_VERSION` is set and not empty. In that sibling the check runs after the Git Bash pair and the Darwin check, and before Debian, Ubuntu, Alpine, Fedora, Red Hat Enterprise Linux, and other Linux. `uname -s` reporting `Linux` does not make Termux into other Linux or Alpine. Darwin is not Termux.
3. `util_cache_host_kind` does not read `TERMUX_VERSION`. On Termux, `uname -s` is `Linux`, so the function returns `linux`. The cache chain that runs is the Linux chain, including the note on `requirement-shell-cli-storage` that a Termux cache root may be `noexec`. Cache remains scratch only. This program must not run a program from the cache root.
4. Termux is a command line for normal user only. This product must not install a sudoers fragment for this login, must not call in-tool `sudo` to mutate the host, must not call `pkg`, and must not call `apt-get`, `apk`, `dnf`, or `brew`. The numbered sudoers board may still display on a terminal. Choosing a row must not wrap `sudo` and must not write `/etc`.
5. The ship unit does not yet skip `util_sudo` when `TERMUX_VERSION` is set. That skip is not added by this requirement. Deposit into `/var/backup/folder-backup` is the Linux host store. It is not a Termux store. This file does not order a new refuse path.

### 2.1 Implementation Notes (this product)

| Item | Value |
|------|--------|
| **Product** | `folder-backup` |
| **Family** | Termux |
| **Cited detect** | `TERMUX_VERSION` set and not empty |
| **Ship unit today** | Does not read `TERMUX_VERSION`. Cache kind `linux` |
| **Cache** | Linux chain. May be `noexec`. Scratch only |
| **Privilege ceiling** | Normal user privilege. No `pkg`. No sudoers fragment. No in-tool sudo for host mutation |
| **Deposit** | Not a Termux store. The ship unit does not branch deposit on `TERMUX_VERSION` |
| **Honesty** | Label and ceiling are law. The `TERMUX_VERSION` read is not implemented |

### 2.2 Why This Requirement Exists (CIAO)

- **Principle 9 – Privilege layers**: A phone userspace does not gain admin privilege because `uname` says Linux.
- **Principle 10 – Least privilege**: `pkg` is not a folder-backup install step. This product has no compiler packages to fetch.
- **Principle 1 – Caution**: Say that the cache function still returns `linux`.

## Under command line for normal user only

When `TERMUX_VERSION` is set, this program runs as a command line for normal user only. Admin privilege and dedicated system user privilege stay unused.

**This requirement:** no in-tool `sudo` for host mutation, no sudoers fragment, no `/etc` destination, no `useradd`, and no `pkg`. Git Bash and Windows cmd are not Termux and must not gain `pkg` from this file. The ship unit's cache function does not perform this detect. Backup deposit is not retargeted here.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The family name is a label. The ship unit's live split stays the three cache kinds.
- **Intentional:** Detection pairs are cited from the sibling so two products name the same host the same way.
- **Anti-fragile:** A host that matches no family still runs. This file does not add a refuse path.
- **Over-protect:** Cache paths stay on the storage requirement. Deposit stays on the privilege requirement.
- **Principle 21 – Dual policies**: The sibling's `pkg install -y` line stays in that project.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Copy the sibling's compiler install, CMake configure, or payload copy into this product.
2. Replace `util_cache_host_kind` with the sibling's detect pair. That function is a reusable cache classifier.
3. Add a second cache chain in this file.
4. Add `payload_platform` to `about` or `--json about`.
5. Exit non-zero with a platform list when no family matches, unless that stop is implemented and tested. It is not implemented.
6. Write this product's rules into sibling project tn5250-cli.
7. Treat `ID_LIKE` as a selector for Debian, Ubuntu, Alpine, Fedora, or Red Hat Enterprise Linux.
8. Call `pkg` from folder-backup because the sibling installs compiler packages that way.
9. Treat cache kind `linux` as proof the host is not Termux.

**Violating this rule mixes a compiler product into a backup tool, or invents a host stop the ship unit does not have.**

## 5. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-shell-cli-storage.md` | Cache chain and persistence (`requirement-shell-cli-storage`) |
| `docs/requirements/requirement-three-layer-privilege-model.md` | Narrow archive deposit on a Linux host (`requirement-three-layer-privilege-model`) |
| `docs/requirements/requirement-folder-archive-backup.md` | Backup and restore operations |
| `src/folder-backup` | Ship unit. `util_cache_host_kind` is the live host split |
| Sibling project tn5250-cli, requirement `requirement-termux-cli-coding.md` | Termux `TERMUX_VERSION` detection. Not this product's backup behavior. This product does not call `pkg` |
| `docs/requirements/requirement-other-linux.md` | Other Linux must not claim a set `TERMUX_VERSION` |
| `docs/requirements/requirement-windows-git-bash.md` | Git Bash and Windows cmd. No `pkg` |

## Design-time verification

| TP family / ID | What it proves | Status |
|----------------|----------------|--------|
| TP-CLI-12 | A Linux `uname` uses the Linux cache chain. Termux is that `uname` today | have — `TERMUX_VERSION` is not asserted |
| RQ-TERMUX privilege | No `pkg` and no sudoers fragment on Termux | law only — ship unit does not read `TERMUX_VERSION` |

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
| 2026-10-14 | Active 1.0.0 | Family label for folder-backup. Detection pairs cited from sibling project tn5250-cli, requirement `requirement-termux-cli-coding.md`. No payload build. Cache chain stays on the storage requirement. |

**Last Updated**: 2026-10-14
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
