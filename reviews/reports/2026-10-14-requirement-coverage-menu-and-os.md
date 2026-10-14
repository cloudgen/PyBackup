# Requirement sufficient check — menu numbers and OS families

**Date:** 2026-10-14
**Product:** folder-backup
**Ship unit:** `src/folder-backup` **1.26.0**
**Suite:** `sh tests/run.sh` — PASS=610 FAIL=0 SKIP=2

## Claim

- ID: **C-menu-567**
- Text: The front board lists client-side **1**, sudoers **5**, self-management **6**, language **7**, and Exit **9**. Language children are **71**–**78**. Sudoers prints **52** and **55** and reserves **51**, **53**, and **54**. Self-management is **61**–**67**. Eight OS family labels cite sibling project tn5250-cli and do not add a compiler install.

## SSOT preflight

- Identity: **aligned**. `APP_NAME` is `folder-backup`. `VERSION` is `1.26.0`.
- Registry: **31** Active requirement files and **0** Withdrawn. The eight new files are `requirement-windows-git-bash`, `requirement-debian`, `requirement-ubuntu`, `requirement-other-linux`, `requirement-alpine`, `requirement-fedora-redhat`, `requirement-termux`, and `requirement-macos`.
- Notes: The first suite run in this change failed **TP-CLI-24** because the language board printed **52** and **55** for Traditional Chinese and German. Those two rows are **72** and **75**. The rerun is the count above.

## Registered law

| Key | Version | What it now says |
|-----|---------|------------------|
| `requirement-shell-cli-default-interaction` | 1.13.0 | Front **1** / **5** / **6** / **7** / **9**. Self **61**–**67**. |
| `requirement-shell-cli-language` | 1.2.0 | Front **7**. Children **71**–**78**. |
| `requirement-shell-cli-sudoers-submenu` | 1.5.0 | Front **5**. Printed **52** and **55**. Reserved **51**, **53**, **54**. |
| `requirement-shell-cli-interface` | 1.13.0 | Sudoers and language are not dispatched. Self board is front **6**. |
| `requirement-windows-git-bash` | 1.0.0 | Cache kind `gitbash` is implemented. Sibling detect pair is not the cache gate. |
| `requirement-debian` | 1.0.0 | Debian 12 and 13 label. No `apt-get`. os-release branch is not implemented. |
| `requirement-ubuntu` | 1.0.0 | Ubuntu 22.04, 24.04, and 26.04 label. No `apt-get`. |
| `requirement-other-linux` | 1.0.0 | Remainder label. No platform-list refusal. |
| `requirement-alpine` | 1.0.0 | `ID=alpine` label. No `apk`. |
| `requirement-fedora-redhat` | 1.0.0 | `ID=fedora` or `ID=rhel`. No `dnf`. |
| `requirement-termux` | 1.0.0 | `TERMUX_VERSION` label. Cache kind stays `linux`. No `pkg`. |
| `requirement-macos` | 1.0.0 | Darwin cache kind `mac` is implemented. No `brew`. Deposit is not branched on Darwin. |

## Live surfaces

- Front print order is **1**, **5**, **6**, **7**, **9**. Cases are `7|language`, `5|sudoers`, `6|self-management`.
- Language rows are **71** through **78**. Picks **72** and **75** store Traditional Chinese and German.
- Sudoers rows stay **52** and **55**.
- `util_cache_host_kind` still returns `linux`, `gitbash`, or `mac`. It does not read `/etc/os-release` or `TERMUX_VERSION`.

## Proof

`sh tests/run.sh` reported PASS=610 FAIL=0 SKIP=2. **TP-CLI-13** checks the front rows and the sudoers board. **TP-CLI-24** checks language **71**–**78** and a saved pick. **TP-CLI-12** checks the Linux, Git Bash, and Mac cache chains.

## Gaps

- The Debian, Ubuntu, Alpine, Fedora, and RHEL labels are not a branch in the ship unit.
- Termux and Git Bash law says normal user privilege. The ship unit does not skip `util_sudo` from `TERMUX_VERSION` or from cache kind `gitbash`.
- macOS is not the primary deposit host. `BACKUP_ROOT` still defaults to `/var/backup` on Darwin.
- Elevated deposit proofs **TP-FOLDER-BACKUP-07** and **08** stay skipped when this login has no sudoers deposit.

## Verdict

**Sufficient with Gaps.** The numbered boards match the new law and the suite is green. The OS files name the sibling families and record what this program actually does. They do not pretend the os-release labels are implemented.
