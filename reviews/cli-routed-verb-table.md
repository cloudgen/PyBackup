# CLI routed-verb table — folder-backup

**Product:** folder-backup  
**Ship unit:** `src/folder-backup`  
**Dispatcher:** `app_main`  
**Scan date:** 2026-09-30 (menu contract re-checked for 1.23.0)  
**Mode:** full (label + purpose refresh)  
**Copied / re-checked:** 13 live copied · 2 re-checked (`menu`/`main` now routed) · 1 not-yet-wired  

Inventory from dispatcher case, not help. Human-readable is `{{short-descript}}: {{explain}}` (short-descript = routed-verb).

## Live

| verb | handler | privilege | last modified date | purpose | human-readable |
|------|---------|-----------|--------------------|---------|----------------|
| version | `app_version` | you | missing | diagnostics | version: Show the local version |
| about | `app_about` | you | 2026-08-03 | diagnostics | about: Show diagnostics including sudoers trust tier |
| help | `app_help` | you | missing | diagnostics | help: Show this help |
| install | `inst_local_install` | you | 2026-08-09 | self-managed | install: Copy this program into your bin or /usr/local/bin |
| uninstall | `inst_local_uninstall` | you | 2026-08-03 | self-managed | uninstall: Remove the managed binary (not the host grant) |
| where-is-me | `app_where_is_me` | you | 2026-08-03 | self-managed | where-is-me: Show running and install paths |
| self-install | `inst_self_install` | you | 2026-09-30 | self-managed | self-install: Copy this file, or download it when the shell is a pipe |
| version-check | `ver_check` | you | 2026-09-30 | self-managed | version-check: Compare this version with the channel |
| self-update | `inst_self_update` | you | 2026-09-30 | self-managed | self-update: Replace the placed binary from the channel |
| self-uninstall | `inst_self_uninstall` | you | 2026-09-30 | self-managed | self-uninstall: Remove the channel-placed binary |
| self-management | `app_default_self_loop` → `app_cmd_menu_self` | you | 2026-09-30 | self-managed | self-management: On a terminal, numbered self-management board (61-67). Off a terminal, stops: self-management needs a terminal |
| backup | `fb_backup` | you (deposit needs change-the-computer after admin grant) | 2026-08-12 | operational | backup: Pack a named folder into a dated gzip archive under /var/backup/folder-backup |
| restore | `fb_restore` | you (stage fetch may need change-the-computer) | 2026-08-03 | operational | restore: Put an archive back onto the hard-disk projects tree |
| print-sudoers | `fb_print_sudoers` | you | 2026-08-14 | test-purpose | print-sudoers: Write a grant file an admin can install |
| print-sudoers-install-script | `fb_print_sudoers_install_script` | you | 2026-08-09 | test-purpose | print-sudoers-install-script: Write an admin script to install or remove the grant |
| remove-project-sudoers | `fb_remove_project_sudoers` | you | 2026-08-09 | operational | remove-project-sudoers: Remove the local grant draft only |
| generate-sudoer-request | `fb_generate_sudoer_request` | you | 2026-08-17 | test-purpose | generate-sudoer-request: Write a local JSON grant you can read without sudo |
| submit-sudoer-request | `fb_submit_sudoer_request` | you | 2026-08-17 | operational | submit-sudoer-request: Hand the JSON grant to the approval queue |
| menu | `app_cmd_menu` (`app_main_menu` aliases it) | you | 2026-09-30 | operational | menu: Numbered boards: client-side, language, sudoers, self-management, and Exit (same boards as a TTY empty run; off a terminal, stops: menu needs a terminal) |
| main | `app_cmd_menu` | you | 2026-09-30 | operational | main: Same as menu |

## Not-yet-wired

| verb | handler | privilege | last modified date | purpose | human-readable | status |
|------|---------|-----------|--------------------|---------|----------------|--------|
| setup | — | — | — | — | — | forbidden (not this CLI; sibling inbound setup) |

Do not list `menu` / `main` as choices on their own menu.

A TTY **front** board prints category rows, not the flat work list. folder-backup is **case 2**. **`sudoers` and `language` are not live dispatcher tokens.** Front rows are **1** client-side, **5** sudoers, **6** self-management, **7** language, **9** Exit. Number **2** stays reserved (no host service). Client rows are **11** backup, **12** restore, **0** Back. Language rows are **71**–**78**. The sudoers board prints **52** submit-sudoer-request and **55** remove-project-sudoers. Test-purpose verbs stay off every numbered board; **51** / **53** / **54** stay reserved. The self board prints **61**–**67** (local `install` and channel place are both shown). Row **62** and a typed `version` on a board run `about`. Argv `version` stays `app_version`. `uninstall` and `where-is-me` stay typed. A finished leaf redisplays the front. An empty line on the front leaves. Child Back is **0**. Off a terminal, `menu` and `self-management` stop.

**Front:** client-side, sudoers, self-management, language, Exit. **Client:** backup, restore. **Sudoers board:** submit-sudoer-request, remove-project-sudoers. **Self board:** install, version, about, version-check, self-update, self-uninstall, self-install.

## Honesty

Dispatcher tokens on 2026-09-30: version, about, help, install, uninstall, where-is-me, self-install, version-check, self-update, self-uninstall, self-management, backup, restore, print-sudoers, print-sudoers-install-script, remove-project-sudoers, generate-sudoer-request, submit-sudoer-request, menu, main. Empty argv is **not** a token: on a real terminal it calls `app_cmd_menu`; a pipe, `--quiet`, or `--json` with no command calls `inst_self_install`. Named `menu` and `self-management` off a terminal stop. Channel verbs are live and sit on the self board (front row **6**), not as front rows. `install` is the local copy and self row **61**. This product classifies `print-sudoers`, `print-sudoers-install-script`, and `generate-sudoer-request` as **test-purpose** (off every numbered board; numbers reserved). **`sudoers` is not a dispatcher token.**
