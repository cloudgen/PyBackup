# Requirements index

**Product:** PyBackup (Python text-menu CLI — command `py-backup`; folder tar.gz backup with narrow sudo deposit)  
**Workspace state:** Specialized product law (left genesis); **software-development** class. **Python ship unit** `src/PyBackup` version **1.0.0**, bootstrap **HelloTui → PyBackup** (user order 2026-10-22: keep HelloTui features, specialize folder-backup). A terminal with no command opens the text menu. No terminal with no command prints help and returns 0. Pip lifecycle is `python -m pip` (rows **82**–**87**). There is no `curl | sh` channel on `py-backup`.  
**Shell reference:** `src/folder-backup` release **1.26.0** remains on disk. Its requirements below stay the behavioral record of that file. Where a shell row disagrees with a `requirement-python-*` row, **`py-backup` follows the Python row**. Do not delete the shell rows. Do not edit HelloTui.  
**Project repository:** https://github.com/cloudgen/PyBackup (`git@github.com:cloudgen/PyBackup.git`)  
**Updated:** 2026-10-22

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law. Python ship unit uses setuptools. Shell reference residual stays for `src/folder-backup`. No dest approver | class | Active (1.1.6) | `requirement-class-software-dev.md` | 2026-10-22 |
| requirement-python-tui | Text menu: path and clock, rows 1 client-side, 3 system-log, 4 language, 5 sudoers, 8 self-management, 9 Exit. Three-row band under the box | python | Active (1.0.1) | `requirement-python-tui.md` | 2026-10-22 |
| requirement-python-cli-interface | `py-backup` verbs, empty argv, help split, pip lifecycle | python | Active (1.0.1) | `requirement-python-cli-interface.md` | 2026-10-22 |
| requirement-python-cli-language | Thirteen codes 41–53, leaf `~/.local/PyBackup/language`, `PYBACKUP_LANG` | python | Active (1.0.1) | `requirement-python-cli-language.md` | 2026-10-22 |
| requirement-python-about | About page: identity, domain fields, cache labels, host check, star box | python | Active (1.0.1) | `requirement-python-about.md` | 2026-10-22 |
| requirement-python-cli-logging | ChronicleLogger constructed inside `def main` | python | Active (1.0.1) | `requirement-python-cli-logging.md` | 2026-10-22 |
| requirement-python-error-handling | `ERROR:` plus `Next:` ; DomainError ; fail closed | python | Active (1.0.1) | `requirement-python-error-handling.md` | 2026-10-22 |
| requirement-python-oop | Class homes for the text menu and the domain modules | python | Active (1.0.1) | `requirement-python-oop.md` | 2026-10-22 |
| requirement-python-packaging | `pyproject.toml`, version 1.0.0, console script `py-backup` | python | Active (1.0.1) | `requirement-python-packaging.md` | 2026-10-22 |
| requirement-python-coding-style | Python style for this package | python | Active (1.0.1) | `requirement-python-coding-style.md` | 2026-10-22 |
| requirement-python-project-structure | `src/PyBackup` layout | python | Active (1.0.1) | `requirement-python-project-structure.md` | 2026-10-22 |
| requirement-python-readme | Product README shape for PyBackup | python | Active (1.0.1) | `requirement-python-readme.md` | 2026-10-22 |
| requirement-bootstrap-chain | Bootstrap chain. Shell record A=selfmanaged → B=folder-backup (channel kept). Python chain A=HelloTui → B=PyBackup (pip; empty off-terminal is help) | architecture | Active (2.5.0) | `requirement-bootstrap-chain.md` | 2026-10-22 |
| requirement-project-folder | Project layout (`src/`), install bins, `/var/backup` deposit; scratch leaf per login and per process | architecture | Active (1.0.1) | `requirement-project-folder.md` | 2026-09-27 |
| requirement-three-layer-privilege-model | Type 0 + narrow Type 1 deposit; sudoers emit + **install-script** handoff; **per-user** fragment names; **trust tiers** (S13); submit workflow + inbound fidelity + **host-probe add/update** + **independent generate** (readable dest); fragment **MUST** be `backup *` / `restore *` **and** `--json` twins; privilege paths do not download; staging cache is per login and per process | architecture | Active (1.12.1) | `requirement-three-layer-privilege-model.md` | 2026-09-30 |
| requirement-sudoer-json-file | **JSON sudoer file** SSOT: four command objects. Shell sample stays `folder-backup` (compact JSON Gap on that file). Python emit is service `PyBackup` and path `GLOBAL_BIN/py-backup` | architecture | Active (1.4.2) | `requirement-sudoer-json-file.md` | 2026-10-22 |
| requirement-folder-archive-backup | **Backup/restore ops SSOT**: backup + verify + **restore**; archive files are regular-file members (verbose type `-` and `h`); dest whitelist **W-ETC-USER** `/etc/{{username}}` (never `/etc/passwd`); stage root is the per-login per-process cache | backup | Active (1.3.1) | `requirement-folder-archive-backup.md` | 2026-10-22 |
| requirement-folder-archive-backup-retention-total | **Total retention**: max **30** archives per project basename; prune oldest after successful deposit | backup | Active (1.0.0) | `requirement-folder-archive-backup-retention-total.md` | 2026-08-12 |
| requirement-folder-archive-backup-retention-daily | **Daily retention**: max **5** archives per basename per calendar day; prune oldest same-day `N` | backup | Active (1.0.0) | `requirement-folder-archive-backup-retention-daily.md` | 2026-08-12 |
| requirement-shell-cli-interface | Shell CLI interface (commands, flags, dispatch, modes); channel verbs `self-install` / `version-check` / `self-update` / `self-uninstall` / `self-management`; local `install` stays copy mode 0755; non-interactive zero-cli-verb is `inst_self_install`; named `menu` off a terminal stops; submit `--add`/`--update`; **generate-sudoer-request**; **`menu`/`main` routed**; interactive zero-cli-verb = numbered boards; test-purpose grant-emit listed apart and off numbered boards (**have**); English headings stay exact and other codes translate them; grant/draft verbs live; family **sudoers** is front **5** and is not dispatched; front **7** language is not dispatched; about cache used / preferred / 1st / 2nd | shell | Active (1.13.0) | `requirement-shell-cli-interface.md` | 2026-10-14 |
| requirement-shell-cli-zero-arguments | Interactive zero-cli-verb = numbered boards; non-interactive zero-cli-verb = `inst_self_install` (not help, not local `install`); named menu stop is default-interaction | shell | Active (1.2.1) | `requirement-shell-cli-zero-arguments.md` | 2026-09-30 |
| requirement-shell-cli-default-interaction | Claimed TTY numbered boards on an **interactive** zero-cli-verb and `menu`/`main`; front **1** / hidden **2** / **5** sudoers / **6** self-management / **7** language / **9**; client **11**/**12**; self **61**–**67** (row **62** runs about); child Back **0**; empty front line leaves; named menu off a terminal stops; front hide sentence says server-side is not available; sudoers **body** on sudoers-submenu REQ; language **body** on language REQ; non-interactive place is zero-arguments; **implemented** | shell | Active (1.13.0) | `requirement-shell-cli-default-interaction.md` | 2026-10-14 |
| requirement-shell-cli-language | Eight menu languages; front **7** / children **71**–**78**; persistence leaf `language`; `FOLDER_BACKUP_LANG` wins for one run and does not write the file; human `help` and human `about` follow `APP_LANG`; JSON about and argv `version` stay English; front hide sentence says not available | shell | Active (1.2.0) | `requirement-shell-cli-language.md` | 2026-10-14 |
| requirement-shell-cli-sudoers-submenu | Front **5** sudoers board; printed rows **52** and **55**; **51**/**53**/**54** reserved; hide sentence matches the front not-available shape; `sudoers` not dispatched; header and longs follow `APP_LANG`; English strings stay the table; Back **0** returns to the front | shell | Active (1.5.0) | `requirement-shell-cli-sudoers-submenu.md` | 2026-10-14 |
| requirement-shell-local-self-management | Local install / uninstall / where-is-me; **mode 0755** multi-user; channel verbs live beside this pair; `install` is also self-board row **61**; a pipe is not this `install` | shell | Active (1.3.3) | `requirement-shell-local-self-management.md` | 2026-10-14 |
| requirement-shell-output-requirements | Central `out_*` output SSOT; identity token + numbered-row ink (bold short name); parent selfmanaged | shell | Active (1.1.2) | `requirement-shell-output-requirements.md` | 2026-09-30 |
| requirement-operator-readable-error | Operator-facing error **wording** (human-intro style: what happened / next step) | shell | Active (1.0.0) | `requirement-operator-readable-error.md` | 2026-08-17 |
| requirement-shell-script-coding | POSIX `/bin/sh` coding-style specialize-in home (without it, portable lessons arrive raw); own-or-point | shell | Active (1.0.0) | `requirement-shell-script-coding.md` | 2026-09-06 |
| requirement-shell-sudo-command | In-tool sudo wrap + studied allow table (`backup *` / `restore *` / `--json` twins); wrap **Gap** | shell | Active (1.0.1) | `requirement-shell-sudo-command.md` | 2026-10-22 |
| requirement-shell-modular-function-design | Single-file modular prefixes (`out_`/`inst_`/`app_`/`fb_`); language helpers `app_lang_load` / `app_lang_save` / `app_menu_text` / `app_cmd_menu_language`; parent selfmanaged | shell | Active (1.0.2) | `requirement-shell-modular-function-design.md` | 2026-09-30 |
| requirement-shell-idempotency | Re-run safety; archive next-N no overwrite | shell | Active | `requirement-shell-idempotency.md` | 2026-08-03 |
| requirement-shell-interactive-vs-noninteractive | Interactive vs non-interactive / confirm policy; `prompt_ask` → `PROMPT_ASK_VALUE`; off-TTY zero-cli-verb is self-install; named menu off a terminal stops | shell | Active (1.1.3) | `requirement-shell-interactive-vs-noninteractive.md` | 2026-09-30 |
| requirement-shell-cli-storage | Per-login per-process cache folder **and** persistence `${HOME}/.local/folder-backup`; language leaf `language` mode 0600 (not cache, not `/var/backup`); leaf mode 0700; silent tier miss; English about labels Cache folder used / preferred / 1st / 2nd + Persistence storage stay exact; other codes translate those human labels; JSON field names stay English; both cache env pairs accepted | shell | Active (1.5.1) | `requirement-shell-cli-storage.md` | 2026-09-30 |
| requirement-domain-folder-backup | Domain **surface** SSOT (four pillars). Shell record stays. Python subsection names `py-backup`, deposit `/var/backup/PyBackup`, and `normal_user_only()`. Menu numbers for the Python command are `requirement-python-tui` | domain | Active (1.6.13) | `requirement-domain-folder-backup.md` | 2026-10-22 |
| requirement-windows-git-bash | Git Bash family label plus the Windows cmd peer; cache kind `gitbash` is implemented (`MSYSTEM` or `uname`); sibling detect pair is not the cache gate; normal user privilege; no `pkg`; no payload | shell | Active (1.0.0) | `requirement-windows-git-bash.md` | 2026-10-14 |
| requirement-debian | Debian 12 bookworm and 13 trixie label, cited from sibling tn5250-cli; cache kind `linux`; no `apt-get`; os-release branch not implemented | shell | Active (1.0.0) | `requirement-debian.md` | 2026-10-14 |
| requirement-ubuntu | Ubuntu 22.04 jammy, 24.04 noble, 26.04 resolute label, cited from sibling tn5250-cli; cache kind `linux`; no `apt-get`; os-release branch not implemented | shell | Active (1.0.0) | `requirement-ubuntu.md` | 2026-10-14 |
| requirement-other-linux | Other Linux remainder label, cited from sibling tn5250-cli; cache kind `linux` is not proof of this remainder; no package install; no platform-list refusal | shell | Active (1.0.0) | `requirement-other-linux.md` | 2026-10-14 |
| requirement-alpine | Alpine `ID=alpine` label, cited from sibling tn5250-cli; cache kind `linux`; no `apk`; os-release branch not implemented | shell | Active (1.0.0) | `requirement-alpine.md` | 2026-10-14 |
| requirement-fedora-redhat | Fedora `ID=fedora` and RHEL `ID=rhel` label, cited from sibling tn5250-cli; CentOS/Rocky/Alma/Amazon/Oracle stay other Linux; no `dnf` | shell | Active (1.0.0) | `requirement-fedora-redhat.md` | 2026-10-14 |
| requirement-termux | Termux `TERMUX_VERSION` label, cited from sibling tn5250-cli; ship unit cache kind stays `linux`; normal user privilege; no `pkg`; no sudoers fragment | shell | Active (1.0.0) | `requirement-termux.md` | 2026-10-14 |
| requirement-macos | macOS Darwin label; cache kind `mac` is implemented; no `brew`; `/var/backup` is not the macOS store; deposit is not branched on Darwin | shell | Active (1.0.0) | `requirement-macos.md` | 2026-10-14 |

## Channel (kept from selfmanaged — user order 2026-09-30)

| Surface | Status on folder-backup |
|---------|-------------------------|
| `self-install` / `version-check` / `self-update` / `self-uninstall` / `self-management` | **Present.** On the self-management board (front row **6**, rows **64**–**67**). A non-interactive zero-cli-verb calls `inst_self_install`. Not front-board rows. |
| `SCRIPT_URL` | **Present.** Composed from `REPO_USER` / `REPO_NAME` / `SCRIPT_RELPATH`. Help prints it. |
| Non-interactive zero-cli-verb | **CLI self-install** (`inst_self_install`). Not local `install`. Not help. |
| `install` | **Local copy** (`inst_local_install`, mode 0755). Not an alias of `self-install`. Also self-board row **61**. |
| Separate `.sha256` requirement file | **No file.** The ship unit still honors optional `CHECKSUM` on download. |

**Install mode:** **dual.** Checkout copy is `install` (mode 0755). Online place is the pipe one-liner (`self-install`: local 0700, global 0755). A terminal with no command is the numbered boards.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for folder-backup.  
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.  
3. Product source comments cite **only** these live requirement files — never templates/skills as behavioral authority.  
4. This versioned surface lists **requirement rows only** — do not dump templates / skills / terminologies / incidents path inventories here.  
5. Keep Status and Path in sync with each file’s header when status changes.  
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).  
7. **Domain SSOT:** exactly one Active `requirement-domain-*` (`requirement-domain-folder-backup`).  
8. **Shell reference only:** do not drop the channel verbs from `src/folder-backup`. **Python command `py-backup`:** user order 2026-10-22 replaces that channel with HelloTui pip rows. Empty argv off a terminal is help, not `self-install`.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
