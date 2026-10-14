# Requirement ↔ test matrix — folder-backup

**Updated:** 2026-10-14 (1.26.0)  
**Product VERSION:** 1.26.0  
**Suite:** `tests/run.sh` (1.26.0: PASS=610 FAIL=0 SKIP=2)

| Requirement key | Area | TP families | Coverage notes |
|-----------------|------|-------------|----------------|
| requirement-class-software-dev | class | TP-CLI-01, TP-CLI-11 | Syntax + stack residual; channel verbs kept |
| requirement-bootstrap-chain | architecture | TP-CLI-04, TP-CLI-07, TP-CLI-10, TP-CLI-23 | Channel verbs listed; offline version-check / self-update fail closed; a script with no command copies (`inst_self_install`) and does not fetch |
| requirement-project-folder | architecture | TP-LC-01, TP-FOLDER-BACKUP-06 | src ship unit; deposit path naming |
| requirement-three-layer-privilege-model | architecture | TP-FOLDER-BACKUP-01, **01b**, 01c, 02, 05, **14**, **15**, **15b**, **19**, **20**, **21**, **21b**, **22e**, **23**, **23b**, **23c**, **24**, **24b**, **24c**, **24d**, **26**, **26b**; **27 todo** | Trust tiers **S13**; submit workflow AC-16–22; independent generate AC-23/24; inbound fidelity; host-probe add/update; other-user dest ignored; **backup \*** emit AC-25; `--json` twins AC-26 (text have; compact JSON Gap) |
| requirement-sudoer-json-file | architecture | TP-FOLDER-BACKUP-**22**, **22b**, **22c**, **22d**, **22e**, **22f**, **24**, **24c**, **24d**, **26**, **26b**; **27 todo** | JSON grant is `folder-backup` backup/restore plus `*` **and** `--json` twins (AC-26); compact JSON emit **Gap**; pretty emit + inbound body keep both verbs; independent generate dest readable; OS-tool submit refuse |
| requirement-folder-archive-backup | backup | TP-FOLDER-BACKUP-03..08, 10..13, **16**, **28** | Source/name/deposit/verify/next-N/**restore** + dest whitelist W-ETC-USER; archive files exclude symlinks (ops SSOT) |
| requirement-folder-archive-backup-retention-total | backup | TP-FOLDER-BACKUP-17, 17b, **17c** | Max **30** per basename; oldest-first prune; failed backup does not prune |
| requirement-folder-archive-backup-retention-daily | backup | TP-FOLDER-BACKUP-18, 18b, **18c** | Max **5** per basename per day; lowest-`N` same-day prune; failed backup does not prune |
| requirement-shell-cli-interface | shell | TP-CLI-* | Commands, flags, dispatch (incl. new sudoers verbs); **menu/main** TP-CLI-13..16; test-purpose grant-emit apart (**TP-CLI-17 have**) |
| requirement-shell-script-coding | shell | (indirect) | Specialize-in home; own-or-point |
| requirement-shell-sudo-command | shell | TP-FOLDER-BACKUP-01, 01c, 26; **27 todo** | Studied allow table; wrap Gap |
| requirement-shell-cli-zero-arguments | shell | TP-CLI-07, **23** | **Active 1.2.1** — interactive boards; non-interactive `inst_self_install`; `--quiet` / `--json` / non-TTY `--debug` place; TTY `--debug` does not; named menu stop is default-interaction |
| requirement-shell-cli-default-interaction | shell | TP-CLI-07, **13**, **14**, **15**, **16**, **18**, **19**, **21**, **23**, **24** | **Active 1.13.0** — interactive zero-cli-verb = numbered boards; non-interactive place is zero-arguments; named `menu` / `self-management` off a terminal stop; empty front line leaves; row **62** and typed `version` run `about`; front **1**/**5**/**6**/**7**/**9**; front hide sentence says server-side is not available; client **11**/**12**; self **61**–**67**; sudoers body on sudoers-submenu REQ; language body on language REQ; bold short name; finished leaf redisplays the front |
| requirement-shell-cli-language | shell | TP-CLI-**24**, **04**, **13** | **Active 1.2.0** — eight codes **71**–**78**; file mode 0600; env does not rewrite; human help and about follow the code; JSON about and argv version stay English; English front row **7**; front hide sentence says not available |
| requirement-shell-cli-sudoers-submenu | shell | TP-CLI-**13**, **16**, **18** | **Active 1.5.0** — front **5**; printed **52**/**55**; **51**/**53**/**54** reserved; hide sentence matches the front not-available shape; `sudoers` not dispatched; header follows `APP_LANG`; Back **0** returns to the front |
| requirement-shell-local-self-management | shell | TP-LC-* (incl. **09/10** mode) | install/uninstall/where-is-me; **0755** multi-user; global preferred for elev |
| requirement-shell-output-requirements | shell | TP-CLI-03,05,08,09, **18** | JSON / quiet / errors; identity token + numbered-row ink |
| requirement-operator-readable-error | shell | TP-FOLDER-BACKUP-**25**, **25b**, **25c** | Operator-facing `[ERROR]` wording (what happened / next step / no jargon-only) |
| requirement-shell-modular-function-design | shell | (indirect) | `fb_print_sudoers*`, `fb_remove_project_sudoers`, deposit/restore |
| requirement-shell-idempotency | shell | TP-LC-03,07 · TP-FOLDER-BACKUP-06,08 | Re-install; next-N |
| requirement-shell-interactive-vs-noninteractive | shell | TP-LC-05 · TP-FOLDER-BACKUP-15 · **15b** | Uninstall / remove-project-sudoers confirm; multi-draft non-interactive path required |
| requirement-shell-cli-storage | shell | TP-CLI-06 · TP-CLI-12 · TP-CLI-**24** · domain staging | Per-login per-process cache (law **1.5.1**); silent tier miss; leaf mode 0700; persistence `${HOME}/.local/folder-backup/`; language leaf mode 0600; human cache labels follow the code; JSON names stay English |
| requirement-domain-folder-backup | domain | TP-FOLDER-BACKUP-01,02,09,14,15,19,20,**21**,**21b**,**23**,**23b**,**24** · TP-CLI-04,06 | Surface verbs/help/about; submit public inbound; generate-sudoer-request; host-probe add/update |
| requirement-windows-git-bash | shell | TP-CLI-**12** | **Active 1.0.0** — cache kind `gitbash` have. Sibling `OSTYPE` pair and a privilege skip are law only |
| requirement-debian | shell | TP-CLI-**12** | **Active 1.0.0** — Debian 12/13 label. Cache kind `linux` have. os-release branch is law only |
| requirement-ubuntu | shell | TP-CLI-**12** | **Active 1.0.0** — Ubuntu 22.04/24.04/26.04 label. Cache kind `linux` have. os-release branch is law only |
| requirement-other-linux | shell | TP-CLI-**12** | **Active 1.0.0** — remainder label. Cache kind `linux` is not proof of this remainder. No platform-list refusal |
| requirement-alpine | shell | TP-CLI-**12** | **Active 1.0.0** — `ID=alpine` label. Cache kind `linux` have. os-release branch is law only |
| requirement-fedora-redhat | shell | TP-CLI-**12** | **Active 1.0.0** — `ID=fedora` or `ID=rhel`. Cache kind `linux` have. os-release branch is law only |
| requirement-termux | shell | TP-CLI-**12** | **Active 1.0.0** — `TERMUX_VERSION` label. Ship unit cache kind stays `linux`. No `pkg`. Privilege skip is law only |
| requirement-macos | shell | TP-CLI-**12** | **Active 1.0.0** — Darwin cache kind `mac` have. No `brew`. Deposit is not branched on Darwin |

**Checklist / mold (harness, not product suite):** **S11–S12** elev tables (when claimed); **S13** trust tier; **S14** emit; **S15** convert/inbound; **S16** independent generate dest — agent path `SK-CREATE-SUDOERS-FILE` / `CL-CREATE-SUDOERS-SECURITY`. Operator errors: `SK-OPERATOR-READABLE-ERROR` / `CL-OPERATOR-READABLE-ERROR`.

**Kept (user order 2026-09-30):** channel verbs, automatic SHA-256 companion on download, terminal numbered boards, non-interactive zero-cli-verb as `inst_self_install`, local `install` as the 0755 copy. Do not drop those without an owner order.
