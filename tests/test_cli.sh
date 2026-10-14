# =============================================================================
# tests/test_cli.sh — CLI surface
# Channel verbs are listed. version-check / self-update use a non-empty
# unreachable URL (127.0.0.1 only). A non-interactive line with no command
# copies this file (self-install). No live GitHub fetch.
# =============================================================================
# Primary REQs: requirement-shell-cli-interface, requirement-shell-cli-default-interaction,
# requirement-shell-output-requirements, requirement-shell-cli-storage
# TP family: TP-CLI-*
# =============================================================================

# shellcheck source=helpers.sh
. "${TESTS_ROOT}/helpers.sh"

run_test_cli() {
    t_header "CLI surface (TP-CLI)"

    require_cmd sh
    require_cmd grep
    require_cmd tar

    # Isolate HOME/cache so about/version do not mkdir on the live login.
    ci_isolated_env

    # TP-CLI-01 syntax
    sh -n "${SCRIPT}"
    assert_eq "TP-CLI-01 sh -n ship unit" 0 "$?"

    # TP-CLI-02 version human
    _out=$(sh "${SCRIPT}" version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-02 version exit 0" 0 "$_ec"
    assert_contains "TP-CLI-02 version mentions app" "$_out" "${APP_NAME}"
    assert_contains "TP-CLI-02 version mentions VERSION" "$_out" "${PRODUCT_VERSION}"

    # TP-CLI-03 version json
    _out=$(sh "${SCRIPT}" --json version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-03 version --json exit 0" 0 "$_ec"
    assert_contains "TP-CLI-03 type version" "$_out" '"type":"version"'
    assert_contains "TP-CLI-03 app field" "$_out" "\"app\":\"${APP_NAME}\""
    assert_contains "TP-CLI-03 version field" "$_out" "\"version\":\"${PRODUCT_VERSION}\""

    # TP-CLI-04 help lists local lifecycle, selfmanaged channel verbs, and domain
    _out=$(sh "${SCRIPT}" help 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-04 help exit 0" 0 "$_ec"
    assert_contains "TP-CLI-04 help install" "$_out" "install"
    assert_contains "TP-CLI-04 help uninstall" "$_out" "uninstall"
    assert_contains "TP-CLI-04 help where-is-me" "$_out" "where-is-me"
    assert_contains "TP-CLI-04 help backup" "$_out" "backup"
    assert_contains "TP-CLI-04 help restore" "$_out" "restore"
    assert_contains "TP-CLI-04 help print-sudoers" "$_out" "print-sudoers"
    assert_contains "TP-CLI-04 help install-script" "$_out" "print-sudoers-install-script"
    assert_contains "TP-CLI-04 help remove-project-sudoers" "$_out" "remove-project-sudoers"
    assert_contains "TP-CLI-04 help submit-sudoer-request" "$_out" "submit-sudoer-request"
    assert_contains "TP-CLI-04 help generate-sudoer-request" "$_out" "generate-sudoer-request"
    assert_contains "TP-CLI-04 help public inbound" "$_out" "/var/sudoer-cli/sudoer-request"
    assert_contains "TP-CLI-04 help --update" "$_out" "--update"
    assert_contains "TP-CLI-04 help --add" "$_out" "--add"
    assert_contains "TP-CLI-04 help SUDOER_PUBLIC_ROOT" "$_out" "SUDOER_PUBLIC_ROOT"
    assert_contains "TP-CLI-04 help hard-disk default" "$_out" "hard-disk"
    assert_contains "TP-CLI-04 help --json" "$_out" "--json"
    assert_contains "TP-CLI-04 help menu" "$_out" "Numbered boards: client-side, language, sudoers, self-management, and Exit"
    assert_contains "TP-CLI-04 help names Japanese" "$_out" "77 Japanese"
    assert_contains "TP-CLI-04 help names Korean" "$_out" "78 Korean"
    assert_contains "TP-CLI-04 help names FOLDER_BACKUP_LANG" "$_out" "FOLDER_BACKUP_LANG"
    assert_contains "TP-CLI-04 help main" "$_out" "Same as menu"
    assert_contains "TP-CLI-04 help self-install" "$_out" "self-install"
    assert_contains "TP-CLI-04 help self-update" "$_out" "self-update"
    assert_contains "TP-CLI-04 help self-uninstall" "$_out" "self-uninstall"
    assert_contains "TP-CLI-04 help version-check" "$_out" "version-check"
    assert_contains "TP-CLI-04 help SCRIPT_URL channel" "$_out" "SCRIPT_URL"
    assert_not_contains "TP-CLI-04 no CHECKSUM" "$_out" "CHECKSUM"

    # TP-CLI-17 help lists test-purpose grant-emit under a heading apart
    assert_contains "TP-CLI-17 work heading" "$_out" "Work commands:"
    assert_contains "TP-CLI-17 grant heading" "$_out" "Grant and draft setup (tests and review):"
    _work=$(printf '%s' "$_out" | sed -n '/Work commands:/,/Grant and draft setup/p')
    _grant=$(printf '%s' "$_out" | sed -n '/Grant and draft setup (tests and review):/,/Global Options:/p')
    assert_contains "TP-CLI-17 work has backup" "$_work" "backup"
    assert_contains "TP-CLI-17 work has restore" "$_work" "restore"
    assert_contains "TP-CLI-17 work has remove-project-sudoers" "$_work" "remove-project-sudoers"
    assert_contains "TP-CLI-17 work has submit-sudoer-request" "$_work" "submit-sudoer-request"
    assert_not_contains "TP-CLI-17 work omits print-sudoers row" "$_work" "print-sudoers ["
    assert_not_contains "TP-CLI-17 work omits generate-sudoer-request row" "$_work" "generate-sudoer-request ["
    assert_contains "TP-CLI-17 grant has print-sudoers" "$_grant" "print-sudoers"
    assert_contains "TP-CLI-17 grant has print-sudoers-install-script" "$_grant" "print-sudoers-install-script"
    assert_contains "TP-CLI-17 grant has generate-sudoer-request" "$_grant" "generate-sudoer-request"
    assert_not_contains "TP-CLI-17 grant omits backup operand" "$_grant" "backup <folder>"

    # TP-CLI-05 help json (short structured note — not a long human dump)
    _out=$(sh "${SCRIPT}" --json help 2>/dev/null)
    assert_eq "TP-CLI-05 help --json exit 0" 0 "$?"
    assert_contains "TP-CLI-05 help json success" "$_out" '"type":"success"'
    assert_contains "TP-CLI-05 help json command" "$_out" '"command":"help"'
    assert_contains "TP-CLI-05 help json note" "$_out" '"note"'
    assert_not_contains "TP-CLI-05 help json not human Usage" "$_out" "Usage:"

    # TP-CLI-06 about json domain + cache folders, no channel
    _out=$(sh "${SCRIPT}" --json about 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-06 about --json exit 0" 0 "$_ec"
    assert_contains "TP-CLI-06 type about" "$_out" '"type":"about"'
    assert_contains "TP-CLI-06 cache_used" "$_out" '"cache_used"'
    assert_contains "TP-CLI-06 cache_preferred field" "$_out" '"cache_preferred"'
    assert_contains "TP-CLI-06 cache_preferred path" "$_out" '"cache_preferred":"/dev/shm/cache/cache-'"${APP_NAME}"'-'
    assert_contains "TP-CLI-06 cache_fallback field" "$_out" '"cache_fallback"'
    assert_contains "TP-CLI-06 cache_fallback_2" "$_out" '"cache_fallback_2"'
    assert_contains "TP-CLI-06 cache_fallback leaf" "$_out" "cache-${APP_NAME}"
    assert_contains "TP-CLI-06 effective_storage" "$_out" '"effective_storage"'
    assert_contains "TP-CLI-06 persistence_storage field" "$_out" '"persistence_storage"'
    assert_contains "TP-CLI-06 persistence_storage leaf" "$_out" "/.local/${APP_NAME}"
    assert_contains "TP-CLI-06 backup_notation" "$_out" '"backup_notation"'
    assert_contains "TP-CLI-06 deposit_dir" "$_out" '"deposit_dir"'
    assert_contains "TP-CLI-06 sudoer_cli" "$_out" '"sudoer_cli"'
    assert_contains "TP-CLI-06 sudoer_adm" "$_out" '"sudoer_adm"'
    assert_contains "TP-CLI-06 sudoer_inbound" "$_out" '"sudoer_inbound"'
    assert_contains "TP-CLI-06 host_sudoers_present" "$_out" '"host_sudoers_present"'
    assert_contains "TP-CLI-06 restore_host_default" "$_out" '"restore_host_default"'
    assert_not_contains "TP-CLI-06 no CHECKSUM" "$_out" "CHECKSUM"
    assert_not_contains "TP-CLI-06 no SCRIPT_URL" "$_out" "SCRIPT_URL"

    _hout=$(sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-06 human Cache folder used" "$_hout" "Cache folder used:"
    assert_contains "TP-CLI-06 human Cache folder preferred" "$_hout" "Cache folder (preferred):"
    assert_contains "TP-CLI-06 human Cache folder 1st fallback" "$_hout" "Cache folder (1st fallback):"
    assert_contains "TP-CLI-06 human Cache folder 2nd fallback" "$_hout" "Cache folder (2nd fallback):"
    assert_contains "TP-CLI-06 human Persistence storage" "$_hout" "Persistence storage:"
    assert_contains "TP-CLI-06 human Persistence path leaf" "$_hout" "/.local/${APP_NAME}"
    assert_not_contains "TP-CLI-06 no Storage (effective) label" "$_hout" "Storage (effective)"
    assert_not_contains "TP-CLI-06 no Storage (fallback) label" "$_hout" "Storage (fallback)"
    assert_not_contains "TP-CLI-06 no Cache folder (live) label" "$_hout" "Cache folder (live)"

    # TP-CLI-07 off-TTY empty argv = CLI self-install (copy; not help; not the boards)
    _out=$(SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-07 empty argv exit 0" 0 "$_ec"
    assert_file_exists "TP-CLI-07 empty argv installed binary" "${CI_USER_BIN}/${APP_NAME}"
    assert_contains "TP-CLI-07 empty argv self-install banner" "$_out" "Starting self-install"
    assert_contains "TP-CLI-07 empty argv copies the local script" "$_out" "Installing from local script"
    assert_not_contains "TP-CLI-07 empty argv is not help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-07 empty argv not numbered list" "$_out" "9. Exit"
    _mode=$(stat -c '%a' "${CI_USER_BIN}/${APP_NAME}" 2>/dev/null || stat -f '%OLp' "${CI_USER_BIN}/${APP_NAME}" 2>/dev/null || echo "")
    case "${_mode}" in
        700|0700) t_pass "TP-CLI-07 local dest mode 0700" ;;
        *) t_fail "TP-CLI-07 local dest mode 0700, got '${_mode}'" ;;
    esac
    _out=$(SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" 2>&1)
    assert_eq "TP-CLI-07 second empty argv exit 0" 0 "$?"
    assert_contains "TP-CLI-07 second empty argv already installed" "$_out" "already installed"
    rm -f "${CI_USER_BIN}/${APP_NAME}"

    # TP-CLI-08 unknown command fail-closed
    _err=$(sh "${SCRIPT}" no-such-command 2>&1 >/dev/null)
    _ec=$?
    assert_eq "TP-CLI-08 unknown exit 1" 1 "$_ec"
    assert_contains "TP-CLI-08 unknown error text" "$_err" "Unknown command"

    _err=$(sh "${SCRIPT}" --json no-such-command 2>&1 >/dev/null)
    _ec=$?
    assert_eq "TP-CLI-08 unknown --json exit 1" 1 "$_ec"
    assert_contains "TP-CLI-08 unknown --json type" "$_err" '"type":"out_error"'

    # TP-CLI-09 quiet suppresses version info
    _out=$(sh "${SCRIPT}" --quiet version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-09 quiet version exit 0" 0 "$_ec"
    _trim=$(printf '%s' "$_out" | tr -d ' \t\n\r')
    if [ -z "$_trim" ]; then
        t_pass "TP-CLI-09 quiet suppresses human version"
    else
        t_fail "TP-CLI-09 quiet expected empty stdout, got '$(_trunc "$_out")'"
    fi

    # TP-CLI-10 selfmanaged channel verbs are routed. Offline URL must not install.
    _offurl="http://127.0.0.1:9/folder-backup-offline"
    _err=$(SCRIPT_URL="${_offurl}" sh "${SCRIPT}" self-update 2>&1 >/dev/null)
    assert_eq "TP-CLI-10 self-update exit 1" 1 "$?"
    assert_not_contains "TP-CLI-10 self-update is routed" "$_err" "Unknown command"
    assert_contains "TP-CLI-10 self-update fetch failure" "$_err" "Failed to fetch"

    _err=$(SCRIPT_URL="${_offurl}" sh "${SCRIPT}" version-check 2>&1 >/dev/null)
    assert_eq "TP-CLI-10 version-check exit 1" 1 "$?"
    assert_not_contains "TP-CLI-10 version-check is routed" "$_err" "Unknown command"
    assert_contains "TP-CLI-10 version-check fetch failure" "$_err" "Failed to fetch"

    _err=$(sh "${SCRIPT}" self-uninstall 2>&1 >/dev/null)
    assert_eq "TP-CLI-10 self-uninstall absent exit 0" 0 "$?"
    assert_not_contains "TP-CLI-10 self-uninstall is routed" "$_err" "Unknown command"

    # TP-CLI-20 do-not-capture-read: no $() of a prompt helper in the ship unit
    _cap=$(grep -n '$(prompt_' "${SCRIPT}" | grep -v ':[[:space:]]*#' || true)
    if [ -z "${_cap}" ]; then
        t_pass "TP-CLI-20 no command substitution of prompt helpers"
    else
        t_fail "TP-CLI-20 captured prompt helper: ${_cap}"
    fi

    # TP-CLI-11 set -u HOME unset still works for version
    _out=$(env -u HOME sh "${SCRIPT}" version 2>/dev/null)
    _ec=$?
    assert_eq "TP-CLI-11 env -u HOME version exit 0" 0 "$_ec"
    assert_contains "TP-CLI-11 env -u HOME version text" "$_out" "${PRODUCT_VERSION}"

    # TP-CLI-12 cache isolation under temp HOME (per login + process id)
    ci_isolated_env
    _login=$(id -un 2>/dev/null || echo "unknown")
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" sh "${SCRIPT}" --json about 2>/dev/null)
    assert_contains "TP-CLI-12 isolated about has app in cache" "$_out" "${APP_NAME}"
    _pref=$(printf '%s' "$_out" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _pid="${_pref##*-}"
    case "${_pref}" in
        /dev/shm/cache/cache-"${APP_NAME}"-"${_login}"-[0-9]*)
            t_pass "TP-CLI-12 cache_preferred is shm login process leaf"
            ;;
        *) t_fail "TP-CLI-12 cache_preferred unexpected: '${_pref:-empty}'" ;;
    esac
    _fb=$(printf '%s' "$_out" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_fallback 1st" "/tmp/cache/cache-${APP_NAME}-${_login}-${_pid}" "${_fb}"
    _fb2=$(printf '%s' "$_out" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_fallback 2nd" "${CI_HOME}/.cache/cache-${APP_NAME}-${_pid}" "${_fb2}"
    _used=$(printf '%s' "$_out" | sed -n 's/.*"cache_used":"\([^"]*\)".*/\1/p' | head -n1)
    _eff=$(printf '%s' "$_out" | sed -n 's/.*"effective_storage":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 cache_used matches effective" "${_eff}" "${_used}"
    if [ -n "$_eff" ] && [ -d "$_eff" ] && [ ! -h "$_eff" ]; then
        t_pass "TP-CLI-12 effective cache directory exists"
    else
        t_fail "TP-CLI-12 effective cache missing: '${_eff:-empty}'"
    fi
    case "${_eff}" in
        /dev/shm/"${APP_NAME}"|/dev/shm/"${APP_NAME}"-*)
            t_fail "TP-CLI-12 effective cache must not be ram-drive project shape: '${_eff}'"
            ;;
        *) t_pass "TP-CLI-12 effective cache is not a ram-drive project shape" ;;
    esac
    _perm=$(command ls -ld "${_eff}" 2>/dev/null | cut -c1-10)
    assert_eq "TP-CLI-12 cache leaf mode 0700" "drwx------" "${_perm}"
    if [ -O "${_eff}" ]; then
        t_pass "TP-CLI-12 cache leaf owned by this login"
    else
        t_fail "TP-CLI-12 cache leaf not owned by this login: '${_eff}'"
    fi
    _err=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" FOLDER_BACKUP_CACHE_SKIP=preferred \
        sh "${SCRIPT}" about 2>&1 >/dev/null)
    assert_not_contains "TP-CLI-12 silent cache fallback" "${_err}" "fallback"
    assert_not_contains "TP-CLI-12 silent cache fallback error" "${_err}" "Cannot create cache"
    _skip=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" FOLDER_BACKUP_CACHE_SKIP=preferred \
        sh "${SCRIPT}" --json about 2>/dev/null)
    _skip_eff=$(printf '%s' "$_skip" | sed -n 's/.*"effective_storage":"\([^"]*\)".*/\1/p' | head -n1)
    _skip_fb=$(printf '%s' "$_skip" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 skipped preferred uses 1st fallback" "${_skip_fb}" "${_skip_eff}"
    _gb=$(HOME="${CI_HOME}" FOLDER_BACKUP_CACHE_HOST=gitbash sh "${SCRIPT}" --json about 2>/dev/null)
    _gb_pref=$(printf '%s' "$_gb" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _gb_pid="${_gb_pref##*-}"
    assert_eq "TP-CLI-12 gitbash preferred" "/tmp/cache/cache-${APP_NAME}-${_login}-${_gb_pid}" "${_gb_pref}"
    _gb_fb=$(printf '%s' "$_gb" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 gitbash 1st fallback" "${CI_HOME}/AppData/Local/Temp/cache-${APP_NAME}-${_gb_pid}" "${_gb_fb}"
    _gb_fb2=$(printf '%s' "$_gb" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 gitbash no 2nd fallback" "" "${_gb_fb2}"
    _mac=$(HOME="${CI_HOME}" FOLDER_BACKUP_CACHE_HOST=mac sh "${SCRIPT}" --json about 2>/dev/null)
    _mac_pref=$(printf '%s' "$_mac" | sed -n 's/.*"cache_preferred":"\([^"]*\)".*/\1/p' | head -n1)
    _mac_pid="${_mac_pref##*-}"
    assert_eq "TP-CLI-12 mac preferred" "/tmp/cache/cache-${APP_NAME}-${_login}-${_mac_pid}" "${_mac_pref}"
    _mac_fb=$(printf '%s' "$_mac" | sed -n 's/.*"cache_fallback":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 mac 1st fallback" "${CI_HOME}/Library/Caches/cache-${APP_NAME}-${_mac_pid}" "${_mac_fb}"
    _mac_fb2=$(printf '%s' "$_mac" | sed -n 's/.*"cache_fallback_2":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 mac 2nd fallback" "${CI_HOME}/cache/cache-${APP_NAME}-${_mac_pid}" "${_mac_fb2}"
    _hum_l=$(HOME="${CI_HOME}" sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 linux about used" "${_hum_l}" "Cache folder used:"
    assert_contains "TP-CLI-12 linux about preferred path" "${_hum_l}" "/dev/shm/cache/cache-${APP_NAME}-${_login}-"
    assert_contains "TP-CLI-12 linux about 2nd path" "${_hum_l}" "/.cache/cache-${APP_NAME}-"
    _hum_gb=$(HOME="${CI_HOME}" FOLDER_BACKUP_CACHE_HOST=gitbash sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 gitbash about 1st" "${_hum_gb}" "AppData/Local/Temp/cache-${APP_NAME}-"
    assert_not_contains "TP-CLI-12 gitbash about omits 2nd" "${_hum_gb}" "Cache folder (2nd fallback)"
    _hum_mac=$(HOME="${CI_HOME}" FOLDER_BACKUP_CACHE_HOST=mac sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-12 mac about 1st" "${_hum_mac}" "Library/Caches/cache-${APP_NAME}-"
    assert_contains "TP-CLI-12 mac about 2nd path" "${_hum_mac}" "Cache folder (2nd fallback): ${CI_HOME}/cache/cache-${APP_NAME}-"
    _pers=$(printf '%s' "$_out" | sed -n 's/.*"persistence_storage":"\([^"]*\)".*/\1/p' | head -n1)
    assert_eq "TP-CLI-12 persistence_storage path" "${CI_HOME}/.local/${APP_NAME}" "$_pers"
    if [ -n "$_pers" ] && [ -d "$_pers" ]; then
        t_pass "TP-CLI-12 persistence storage directory exists"
    else
        t_fail "TP-CLI-12 persistence storage missing: '${_pers:-empty}'"
    fi
    case "${_pers}" in
        */.local/bin|*/.local/bin/) t_fail "TP-CLI-12 persistence must not be USER_BIN: '${_pers}'" ;;
        *) t_pass "TP-CLI-12 persistence is not the install bin directory" ;;
    esac
    ci_cleanup_env

    # TP-CLI-15 named menu / self-management off a terminal stop.
    # A line with no command is TP-CLI-07 / TP-CLI-23 (self-install), not this block.
    _out=$(sh "${SCRIPT}" menu 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 menu off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 menu off-TTY needs a terminal" "$_out" "menu needs a terminal"
    assert_not_contains "TP-CLI-15 menu off-TTY is not help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-15 menu off-TTY not the numbered list" "$_out" "9. Exit"

    _out=$(sh "${SCRIPT}" main 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 main off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 main off-TTY needs a terminal" "$_out" "menu needs a terminal"
    assert_not_contains "TP-CLI-15 main off-TTY is not help" "$_out" "Usage:"

    _out=$(sh "${SCRIPT}" --json menu 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 menu --json off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 menu --json off-TTY JSON error" "$_out" '"type":"out_error"'
    assert_contains "TP-CLI-15 menu --json off-TTY message" "$_out" "menu needs a terminal"
    assert_not_contains "TP-CLI-15 menu --json off-TTY not JSON help" "$_out" '"type":"success"'
    assert_not_contains "TP-CLI-15 menu --json off-TTY not numbered list" "$_out" "9. Exit"

    _out=$(sh "${SCRIPT}" --quiet menu 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 menu --quiet off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 menu --quiet off-TTY needs a terminal" "$_out" "menu needs a terminal"
    assert_not_contains "TP-CLI-15 menu --quiet off-TTY is not help" "$_out" "Usage:"

    _out=$(sh "${SCRIPT}" self-management 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 self-management off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 self-management off-TTY needs a terminal" "$_out" "self-management needs a terminal"
    assert_not_contains "TP-CLI-15 self-management off-TTY is not help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-15 self-management off-TTY not the board" "$_out" "61. install:"

    _out=$(sh "${SCRIPT}" --json self-management 2>&1)
    _ec=$?
    assert_eq "TP-CLI-15 self-management --json off-TTY exit 1" 1 "$_ec"
    assert_contains "TP-CLI-15 self-management --json off-TTY JSON error" "$_out" '"type":"out_error"'
    assert_contains "TP-CLI-15 self-management --json off-TTY message" "$_out" "self-management needs a terminal"
    assert_not_contains "TP-CLI-15 self-management --json off-TTY not JSON help" "$_out" '"type":"success"'
    assert_not_contains "TP-CLI-15 self-management --json off-TTY not the board" "$_out" "61. install:"

    assert_contains "TP-CLI-15 help lists menu" "$(sh "${SCRIPT}" help 2>/dev/null)" "Numbered boards: client-side, language, sudoers, self-management, and Exit"
    assert_contains "TP-CLI-15 help lists main" "$(sh "${SCRIPT}" help 2>/dev/null)" "Same as menu"
    assert_contains "TP-CLI-15 help says a pipe places this program" "$(sh "${SCRIPT}" help 2>/dev/null)" "a pipe places this program"

    # TP-CLI-23 a switch is not a verb. Isolate bins so this does not place
    # into the login that is running the suite.
    ci_isolated_env
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" --quiet 2>&1)
    assert_eq "TP-CLI-23 --quiet exit 0" 0 "$?"
    assert_file_exists "TP-CLI-23 --quiet placed binary" "${CI_USER_BIN}/${APP_NAME}"
    assert_not_contains "TP-CLI-23 --quiet is not help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-23 --quiet is not the boards" "$_out" "9. Exit"
    ci_cleanup_env

    ci_isolated_env
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" --json 2>&1)
    assert_eq "TP-CLI-23 --json exit 0" 0 "$?"
    assert_file_exists "TP-CLI-23 --json placed binary" "${CI_USER_BIN}/${APP_NAME}"
    assert_contains "TP-CLI-23 --json success" "$_out" '"type":"out_success"'
    assert_not_contains "TP-CLI-23 --json is not help" "$_out" "Usage:"
    assert_not_contains "TP-CLI-23 --json is not the boards" "$_out" "9. Exit"
    ci_cleanup_env

    ci_isolated_env
    _out=$(HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" --debug 2>&1)
    assert_eq "TP-CLI-23 non-TTY --debug exit 0" 0 "$?"
    assert_file_exists "TP-CLI-23 non-TTY --debug placed binary" "${CI_USER_BIN}/${APP_NAME}"
    assert_contains "TP-CLI-23 non-TTY --debug self-install banner" "$_out" "Starting self-install"
    assert_not_contains "TP-CLI-23 non-TTY --debug is not help" "$_out" "Usage:"
    ci_cleanup_env

    _out=$(sh "${SCRIPT}" --debug version 2>/dev/null)
    assert_contains "TP-CLI-23 --debug version stays version" "$_out" "version ${PRODUCT_VERSION}"
    assert_not_contains "TP-CLI-23 --debug version is not self-install" "$_out" "Starting self-install"

    if command -v python3 >/dev/null 2>&1; then
        _esc=$(printf '\033')
        _out=$(PTY_IN="9" ci_pty_run)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 TTY empty argv client row" "$_plain" "1. client-side: this login's folders: pack and restore"
        assert_contains "TP-CLI-13 TTY empty argv sudoers row" "$_plain" "5. sudoers: Grant and drafts"
        assert_contains "TP-CLI-13 TTY empty argv server hidden" "$_plain" "server-side is not available: this program does not run a host service. Number 2 stays reserved."
        assert_contains "TP-CLI-13 TTY empty argv self row" "$_plain" "6. self-management: this CLI install, version, update, uninstall"
        assert_contains "TP-CLI-13 TTY empty argv language row" "$_plain" "7. language: display language for this menu"
        assert_contains "TP-CLI-13 TTY empty argv Exit 9" "$_plain" "9. Exit"
        assert_not_contains "TP-CLI-13 TTY empty argv no server row" "$_plain" "2. server-side"
        assert_contains "TP-CLI-13 TTY empty argv ident token" "$_plain" "${APP_NAME}(${PRODUCT_VERSION})"
        assert_not_contains "TP-CLI-13 TTY empty argv hides generate row" "$_plain" "generate-sudoer-request:"
        assert_not_contains "TP-CLI-13 TTY empty argv no backup on front" "$_plain" "11. backup:"

        _out=$(PTY_IN="9" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 TTY menu client row" "$_plain" "1. client-side: this login's folders: pack and restore"
        assert_contains "TP-CLI-13 TTY menu sudoers row" "$_plain" "5. sudoers: Grant and drafts"
        assert_contains "TP-CLI-13 TTY menu self row" "$_plain" "6. self-management: this CLI install, version, update, uninstall"
        assert_contains "TP-CLI-13 TTY menu language row" "$_plain" "7. language: display language for this menu"
        assert_contains "TP-CLI-13 TTY menu Exit 9" "$_plain" "9. Exit"
        _out=$(PTY_IN="9" ci_pty_run main)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 TTY main client row" "$_plain" "1. client-side: this login's folders: pack and restore"
        assert_contains "TP-CLI-13 TTY main sudoers row" "$_plain" "5. sudoers: Grant and drafts"
        assert_contains "TP-CLI-13 TTY main Exit 9" "$_plain" "9. Exit"
        _out=$(PTY_IN="$(printf '%s\n' 'backup' '/tmp/does-not-exist-fb-menu')" ci_pty_run menu)
        assert_contains "TP-CLI-13 TTY typed backup uses typed folder" "$_out" "Source is not a directory: /tmp/does-not-exist-fb-menu"
        assert_not_contains "TP-CLI-13 TTY typed backup path not polluted by prompt" "$_out" "Source is not a directory: Folder to pack:"
        _out=$(PTY_IN="$(printf '%s\n' '12' '9')" ci_pty_run menu)
        assert_contains "TP-CLI-13 TTY pick 12 not a menu choice" "$_out" "Not a menu choice"
        _out=$(PTY_IN="$(printf '%s\n' '1' '0' '9')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 TTY client backup row" "$_plain" "11. backup: Pack a named folder into a dated gzip archive under /var/backup/folder-backup"
        assert_contains "TP-CLI-13 TTY client restore row" "$_plain" "12. restore: Put an archive back onto the hard-disk projects tree"
        assert_not_contains "TP-CLI-13 TTY client has no sudoers row" "$_plain" "17. sudoers:"
        _out=$(PTY_IN="$(printf '%s\n' '1' 'sudoers' '0' '9')" ci_pty_run menu)
        assert_contains "TP-CLI-13 TTY client sudoers word is not a row" "$_out" "Not a menu choice 'sudoers'"
        _out=$(PTY_IN="$(printf '%s\n' '5' '0' '9')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 TTY front sudoers row" "$_plain" "5. sudoers: Grant and drafts"
        assert_contains "TP-CLI-13 TTY sudoers submit row" "$_plain" "52. submit-sudoer-request: Hand the JSON grant to the approval queue"
        assert_contains "TP-CLI-13 TTY sudoers remove row" "$_plain" "55. remove-project-sudoers: Remove the local grant draft only"
        assert_contains "TP-CLI-13 TTY sudoers hides test commands" "$_plain" "test commands are not available: type generate-sudoer-request, print-sudoers, or print-sudoers-install-script. Numbers 51, 53, and 54 stay reserved."
        assert_not_contains "TP-CLI-13 TTY sudoers omits generate row" "$_plain" "51. generate-sudoer-request:"
        assert_not_contains "TP-CLI-13 TTY sudoers omits old 172 row" "$_plain" "172. submit-sudoer-request:"
        assert_contains "TP-CLI-13 TTY sudoers Back 0" "$_plain" "0. Back"
        assert_not_contains "TP-CLI-13 TTY sudoers has no Back 8" "$_plain" "8. Back"
        _front5=$(printf '%s\n' "$_plain" | grep -c "5. sudoers:" || true)
        if [ "${_front5}" -ge 2 ]; then
            t_pass "TP-CLI-13 sudoers Back returns to the front"
        else
            t_fail "TP-CLI-13 sudoers Back did not return to the front (count=${_front5})"
        fi
        _err=$(sh "${SCRIPT}" sudoers 2>&1 >/dev/null)
        assert_eq "TP-CLI-13 sudoers not a live command" 1 "$?"
        assert_contains "TP-CLI-13 sudoers unknown" "$_err" "Unknown command"
        # AC-4: five names are live dispatcher tokens. Do not run handlers
        # against the host inbound — bare submit-sudoer-request enqueues
        # /var/sudoer-cli when sudoer-cli + production trust are present.
        ci_isolated_env
        _live13=$(ci_snapshot_live_sudoer_inbound)
        for _verb in generate-sudoer-request submit-sudoer-request print-sudoers print-sudoers-install-script remove-project-sudoers; do
            _err=$(HOME="${CI_HOME}" \
                GLOBAL_BIN="${CI_GLOBAL_BIN}" \
                USER_BIN="${CI_USER_BIN}" \
                SUDOER_CLI="${CI_HOME}/no-such-sudoer-cli" \
                SUDOER_QUEUE_INBOUND="${CI_SUDOER_INBOUND}" \
                SUDOER_PUBLIC_ROOT="${CI_HOME}/var-sudoer-cli-absent" \
                sh "${SCRIPT}" "${_verb}" 2>&1 >/dev/null) || true
            assert_not_contains "TP-CLI-13 ${_verb} is a live command" "$_err" "Unknown command"
        done
        ci_assert_no_live_sudoer_enqueue "TP-CLI-13 did not enqueue live sudoer inbound" "${_live13}"
        ci_cleanup_env

        _out=$(PTY_IN="9" ci_pty_run --json menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-14 TTY menu --json still numbered list" "$_plain" "9. Exit"
        assert_contains "TP-CLI-14 TTY menu --json client row" "$_plain" "1. client-side: this login's folders"
        assert_not_contains "TP-CLI-14 TTY menu --json ignores JSON help" "$_out" '"type":"success"'

        _out=$(PTY_IN="$(printf '%s\n' '6' '0' '9')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-13 self board install" "$_plain" "61. install: Copy this program into your bin or /usr/local/bin"
        assert_contains "TP-CLI-13 self board version is about" "$_plain" "62. version: Show version and detailed diagnostics (about)"
        assert_contains "TP-CLI-13 self board self-install" "$_plain" "67. self-install: Copy this file, or download it when the shell is a pipe"
        assert_contains "TP-CLI-13 self board back" "$_plain" "0. Back"
        assert_not_contains "TP-CLI-13 self board no where-is-me row" "$_plain" "where-is-me:"

        _out=$(PTY_IN="0" ci_pty_run --json self-management)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-14 TTY self-management --json still the board" "$_plain" "61. install:"
        assert_not_contains "TP-CLI-14 TTY self-management --json ignores JSON help" "$_out" '"type":"success"'

        ci_isolated_env
        _out=$(PTY_IN="9" SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" ci_pty_run --json)
        assert_file_exists "TP-CLI-23 TTY --json placed binary" "${CI_USER_BIN}/${APP_NAME}"
        assert_contains "TP-CLI-23 TTY --json success" "$_out" '"type":"out_success"'
        assert_not_contains "TP-CLI-23 TTY --json is not the boards" "$_out" "9. Exit"
        ci_cleanup_env

        ci_isolated_env
        _out=$(PTY_IN="9" ci_pty_run --debug)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-23 TTY --debug shows the front" "$_plain" "1. client-side:"
        if [ -e "${CI_USER_BIN}/${APP_NAME}" ]; then
            t_fail "TP-CLI-23 TTY --debug placed a binary"
        else
            t_pass "TP-CLI-23 TTY --debug does not place"
        fi
        ci_cleanup_env

        _out=$(PTY_IN="9" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_not_contains "TP-CLI-16 no help row" "$_plain" "help: Show this help"
        assert_not_contains "TP-CLI-16 no install row" "$_plain" "install: Copy this program"
        assert_not_contains "TP-CLI-16 no uninstall row" "$_plain" "uninstall: Remove the managed binary"
        assert_not_contains "TP-CLI-16 no where-is-me row" "$_plain" "where-is-me: Show running"
        assert_not_contains "TP-CLI-16 no version row" "$_plain" "version: Show version and detailed diagnostics"
        assert_not_contains "TP-CLI-16 no about row" "$_plain" "about: Show diagnostics"
        assert_not_contains "TP-CLI-16 no print-sudoers row" "$_plain" "print-sudoers: Write a grant file"
        assert_not_contains "TP-CLI-16 no install-script row" "$_plain" "print-sudoers-install-script: Write an admin script"
        assert_not_contains "TP-CLI-16 no generate row" "$_plain" "generate-sudoer-request: Write a local JSON grant"
        assert_not_contains "TP-CLI-16 no submit on main" "$_plain" "submit-sudoer-request: Hand the JSON grant"
        assert_not_contains "TP-CLI-16 no remove on main" "$_plain" "remove-project-sudoers: Remove the local grant"
        assert_not_contains "TP-CLI-16 no menu row" "$_plain" "menu: Show the numbered list"
        assert_not_contains "TP-CLI-16 no main row" "$_plain" "main: Same numbered list"
        assert_not_contains "TP-CLI-16 no self-install row" "$_plain" "self-install:"
        assert_not_contains "TP-CLI-16 no self-update row" "$_plain" "self-update:"
        assert_not_contains "TP-CLI-16 no self-uninstall row" "$_plain" "self-uninstall:"
        assert_not_contains "TP-CLI-16 no version-check row" "$_plain" "version-check:"
        assert_contains "TP-CLI-16 front category self-management" "$_plain" "6. self-management:"

        # TP-CLI-18 — default CLI main menu style (product alias of portable TP-CLI-17)
        _out=$(PTY_IN="9" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-18 TTY ident token" "$_plain" "${APP_NAME}(${PRODUCT_VERSION})"
        assert_contains "TP-CLI-18 TTY header bold name" "$_out" "${_esc}[1m${APP_NAME}${_esc}[0m"
        assert_contains "TP-CLI-18 TTY header italic version" "$_out" "(${_esc}[3m${PRODUCT_VERSION}${_esc}[0m)"
        assert_contains "TP-CLI-18 TTY explain SGR 3;37" "$_out" "${_esc}[3;37m"
        assert_contains "TP-CLI-18 TTY short name bold" "$_out" "1. ${_esc}[1mclient-side${_esc}[0m: "
        assert_contains "TP-CLI-18 TTY Exit unstyled" "$_plain" "9. Exit"
        _out=$(PTY_IN="$(printf '%s\n' '5' '0' '9')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-18 TTY submenu ident token" "$_plain" "${APP_NAME}(${PRODUCT_VERSION})"
        assert_contains "TP-CLI-18 TTY submenu title" "$_plain" "sudoers (grant and drafts)"
        assert_contains "TP-CLI-18 TTY submenu header bold name" "$_out" "${_esc}[1m${APP_NAME}${_esc}[0m"
        assert_contains "TP-CLI-18 TTY submenu short bold" "$_out" "52. ${_esc}[1msubmit-sudoer-request${_esc}[0m: "
        assert_contains "TP-CLI-18 TTY front sudoers short bold" "$_out" "5. ${_esc}[1msudoers${_esc}[0m: "
        _out=$(PTY_IN="$(printf '%s\n' '12' '9')" ci_pty_run menu)
        assert_contains "TP-CLI-19 invalid choice retries" "$_out" "Not a menu choice '12'"
        _plain=$(ci_strip_ansi "$_out")
        _front_n=$(printf '%s\n' "$_plain" | grep -c "1. client-side:" || true)
        if [ "${_front_n}" -ge 2 ]; then
            t_pass "TP-CLI-19 invalid choice reprints this board"
        else
            t_fail "TP-CLI-19 invalid choice did not reprint the front board (count=${_front_n})"
        fi
        _out=$(PTY_IN="$(printf '\n')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-21 empty Enter shows the front" "$_plain" "9. Exit"
        assert_not_contains "TP-CLI-21 empty Enter is not a bad choice" "$_out" "Not a menu choice"
        _front_n=$(printf '%s\n' "$_plain" | grep -c "1. client-side:" || true)
        if [ "${_front_n}" -eq 1 ]; then
            t_pass "TP-CLI-21 empty Enter leaves the front"
        else
            t_fail "TP-CLI-21 empty Enter did not leave the front (count=${_front_n})"
        fi
        _out=$(PTY_IN="$(printf '%s\n' '6' '' '9')" ci_pty_run menu)
        _plain=$(ci_strip_ansi "$_out")
        assert_contains "TP-CLI-21 empty on self is Back" "$_plain" "61. install:"
        assert_contains "TP-CLI-21 empty on self returns to the front" "$_plain" "9. Exit"
        assert_not_contains "TP-CLI-21 empty on self is not a bad choice" "$_out" "Not a menu choice"
        _out=$(PTY_IN="$(printf '%s\n' '6' '62' '9')" ci_pty_run menu)
        assert_contains "TP-CLI-21 row 62 runs about" "$_out" "Cache folder used"
        assert_not_contains "TP-CLI-21 row 62 is not the thin version line" "$_out" "version ${PRODUCT_VERSION}"
        _out=$(PTY_IN="$(printf '%s\n' 'version' '9')" ci_pty_run menu)
        assert_contains "TP-CLI-21 typed version runs about" "$_out" "Cache folder used"
        assert_not_contains "TP-CLI-21 typed version is not the thin version line" "$_out" "version ${PRODUCT_VERSION}"
        _plain=$(ci_strip_ansi "$_out")
        _front_n=$(printf '%s\n' "$_plain" | grep -c "1. client-side:" || true)
        if [ "${_front_n}" -ge 2 ]; then
            t_pass "TP-CLI-21 finished leaf redisplays the front board"
        else
            t_fail "TP-CLI-21 finished leaf did not redisplay the front board (count=${_front_n})"
        fi
        _off=$(sh "${SCRIPT}" menu 2>/dev/null)
        assert_not_contains "TP-CLI-18 off-TTY menu no explain CSI" "$_off" "${_esc}[3;37m"
        assert_not_contains "TP-CLI-18 off-TTY menu no ident CSI" "$_off" "${_esc}[1m${APP_NAME}"
        ci_isolated_env
        _empty=$(SCRIPT_URL="http://127.0.0.1:9/folder-backup-offline" sh "${SCRIPT}" 2>/dev/null)
        assert_not_contains "TP-CLI-18 off-TTY empty argv no explain CSI" "$_empty" "${_esc}[3;37m"
        rm -f "${CI_USER_BIN}/${APP_NAME}"
        ci_cleanup_env
    else
        t_skip "TP-CLI-13 TTY menu (no python3 for PTY)"
        t_skip "TP-CLI-13 TTY sudoers submenu (no python3 for PTY)"
        t_skip "TP-CLI-14 TTY menu --json (no python3 for PTY)"
        t_skip "TP-CLI-16 TTY exclusions (no python3 for PTY)"
        t_skip "TP-CLI-18 TTY menu look (no python3 for PTY)"
        t_skip "TP-CLI-18 TTY submenu header (no python3 for PTY)"
    fi

    # TP-CLI-24 menu 7 language. Unset the suite pin so the file can win.
    ci_isolated_env
    _out=$(printf '%s\n' '7' '0' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 open language then Back exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 front language long" "$_out" "display language for this menu"
    assert_contains "TP-CLI-24 language row 71" "$_out" "71."
    assert_contains "TP-CLI-24 language English" "$_out" "English"
    assert_contains "TP-CLI-24 language row 72" "$_out" "72."
    assert_contains "TP-CLI-24 language Traditional Chinese" "$_out" "繁體中文"
    assert_contains "TP-CLI-24 language row 73" "$_out" "73."
    assert_contains "TP-CLI-24 language Spanish" "$_out" "Español"
    assert_contains "TP-CLI-24 language Spanish long" "$_out" "use Spanish for this menu"
    assert_contains "TP-CLI-24 language row 74" "$_out" "74."
    assert_contains "TP-CLI-24 language French" "$_out" "Français"
    assert_contains "TP-CLI-24 language French long" "$_out" "use French for this menu"
    assert_contains "TP-CLI-24 language row 75" "$_out" "75."
    assert_contains "TP-CLI-24 language German" "$_out" "Deutsch"
    assert_contains "TP-CLI-24 language German long" "$_out" "use German for this menu"
    assert_contains "TP-CLI-24 language row 76" "$_out" "76."
    assert_contains "TP-CLI-24 language Simplified Chinese" "$_out" "简体中文"
    assert_contains "TP-CLI-24 language Simplified Chinese long" "$_out" "use Simplified Chinese for this menu"
    assert_contains "TP-CLI-24 language row 77" "$_out" "77."
    assert_contains "TP-CLI-24 language Japanese" "$_out" "日本語"
    assert_contains "TP-CLI-24 language Japanese long" "$_out" "use Japanese for this menu"
    assert_contains "TP-CLI-24 language row 78" "$_out" "78."
    assert_contains "TP-CLI-24 language Korean" "$_out" "한국어"
    assert_contains "TP-CLI-24 language Korean long" "$_out" "use Korean for this menu"
    assert_contains "TP-CLI-24 language Back" "$_out" "0. Back"
    assert_file_missing "TP-CLI-24 Back does not write language" "${CI_HOME}/.local/${APP_NAME}/language"
    _out=$(printf '%s\n' '7' '72' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose Traditional Chinese exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 Traditional Chinese saved" "$_out" "選單語言是繁體中文"
    assert_contains "TP-CLI-24 front redraws in Traditional Chinese" "$_out" "用戶端"
    assert_contains "TP-CLI-24 Traditional Chinese Exit" "$_out" "9. 離開"
    assert_contains "TP-CLI-24 Traditional Chinese prompt" "$_out" "請輸入編號，或輸入指令名稱："
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is zh-Hant" "zh-Hant" "${_lang}"
    _mode=$(stat -c '%a' "${CI_HOME}/.local/${APP_NAME}/language" 2>/dev/null || stat -f '%OLp' "${CI_HOME}/.local/${APP_NAME}/language")
    assert_eq "TP-CLI-24 language file mode 600" "600" "${_mode}"
    _out=$(printf '%s\n' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    assert_contains "TP-CLI-24 next run stays Traditional Chinese" "$_out" "用戶端"
    assert_not_contains "TP-CLI-24 next run is not English client-side" "$_out" "client-side"
    _out=$(printf '%s\n' '7' '71' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose English exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 English saved" "$_out" "Menu language is English"
    assert_contains "TP-CLI-24 front redraws in English" "$_out" "client-side"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is en" "en" "${_lang}"
    _out=$(printf '%s\n' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    assert_contains "TP-CLI-24 next run stays English" "$_out" "client-side"
    assert_not_contains "TP-CLI-24 next run is not Traditional Chinese client" "$_out" "用戶端"
    _out=$(printf '%s\n' '7' '73' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose Spanish exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 Spanish saved" "$_out" "El idioma del menú es español"
    assert_contains "TP-CLI-24 Spanish Exit" "$_out" "9. Salir"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is es" "es" "${_lang}"
    _out=$(printf '%s\n' '7' '74' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose French exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 French saved" "$_out" "La langue du menu est le français"
    assert_contains "TP-CLI-24 French Exit" "$_out" "9. Quitter"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is fr" "fr" "${_lang}"
    _out=$(printf '%s\n' '7' '75' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose German exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 German saved" "$_out" "Die Menüsprache ist Deutsch"
    assert_contains "TP-CLI-24 German Exit" "$_out" "9. Beenden"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is de" "de" "${_lang}"
    _out=$(printf '%s\n' '7' '76' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose Simplified Chinese exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 Simplified Chinese saved" "$_out" "菜单语言是简体中文"
    assert_contains "TP-CLI-24 front redraws in Simplified Chinese" "$_out" "客户端"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is zh-Hans" "zh-Hans" "${_lang}"
    _out=$(printf '%s\n' '7' '77' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose Japanese exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 Japanese saved" "$_out" "メニューの言語は日本語"
    assert_contains "TP-CLI-24 Japanese Exit" "$_out" "9. 終了"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is ja" "ja" "${_lang}"
    _out=$(printf '%s\n' '7' '78' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    _ec=$?
    assert_eq "TP-CLI-24 choose Korean exit 0" 0 "$_ec"
    assert_contains "TP-CLI-24 Korean saved" "$_out" "메뉴 언어는 한국어"
    assert_contains "TP-CLI-24 Korean Exit" "$_out" "9. 종료"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 file is ko" "ko" "${_lang}"
    printf '%s\n' 'nope' > "${CI_HOME}/.local/${APP_NAME}/language"
    _out=$(printf '%s\n' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 env -u FOLDER_BACKUP_LANG sh "${SCRIPT}" 2>&1)
    assert_contains "TP-CLI-24 unrecognized file is English" "$_out" "client-side"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 unrecognized file is left as written" "nope" "${_lang}"
    printf '%s\n' 'en' > "${CI_HOME}/.local/${APP_NAME}/language"
    _out=$(printf '%s\n' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 FOLDER_BACKUP_LANG=zh-Hant sh "${SCRIPT}" 2>&1)
    assert_contains "TP-CLI-24 FOLDER_BACKUP_LANG overrides the file" "$_out" "用戶端"
    printf '%s\n' 'en' > "${CI_HOME}/.local/${APP_NAME}/language"
    _out=$(printf '%s\n' '9' | HOME="${CI_HOME}" USER_BIN="${CI_USER_BIN}" GLOBAL_BIN="${CI_GLOBAL_BIN}" TTY=1 FOLDER_BACKUP_LANG=es sh "${SCRIPT}" 2>&1)
    assert_contains "TP-CLI-24 FOLDER_BACKUP_LANG=es overrides the file" "$_out" "idioma"
    _lang=$(head -n 1 "${CI_HOME}/.local/${APP_NAME}/language" | tr -d '\r')
    assert_eq "TP-CLI-24 FOLDER_BACKUP_LANG does not rewrite the file" "en" "${_lang}"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Japanese help heading" "$_out" "使い方:"
    assert_not_contains "TP-CLI-24 Japanese help is not Usage" "$_out" "Usage:"
    _out=$(FOLDER_BACKUP_LANG=ko sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Korean help heading" "$_out" "사용법:"
    assert_not_contains "TP-CLI-24 Korean help is not Usage" "$_out" "Usage:"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-24 Japanese about title" "$_out" "概要 / 診断"
    assert_contains "TP-CLI-24 Japanese about cache" "$_out" "使用中のキャッシュフォルダ"
    assert_not_contains "TP-CLI-24 Japanese about is not About / Diagnostics" "$_out" "About / Diagnostics"
    _out=$(FOLDER_BACKUP_LANG=ko sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-24 Korean about title" "$_out" "개요 / 진단"
    assert_contains "TP-CLI-24 Korean about cache" "$_out" "사용 중인 캐시 폴더"
    assert_not_contains "TP-CLI-24 Korean about is not About / Diagnostics" "$_out" "About / Diagnostics"
    _out=$(FOLDER_BACKUP_LANG=en sh "${SCRIPT}" help 2>/dev/null)
    assert_contains "TP-CLI-24 English help still says Usage" "$_out" "Usage:"
    assert_contains "TP-CLI-24 English help names Japanese" "$_out" "77 Japanese"
    assert_contains "TP-CLI-24 English help names Korean" "$_out" "78 Korean"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Japanese work heading" "$_out" "作業コマンド:"
    assert_contains "TP-CLI-24 Japanese grant heading" "$_out" "認可と下書き（試験と確認）:"
    assert_contains "TP-CLI-24 Japanese help keeps backup" "$_out" "backup"
    assert_not_contains "TP-CLI-24 Japanese help has no Work commands" "$_out" "Work commands:"
    assert_not_contains "TP-CLI-24 Japanese help has no Grant heading" "$_out" "Grant and draft setup (tests and review):"
    assert_not_contains "TP-CLI-24 Japanese help has no Global Options" "$_out" "Global Options:"
    assert_not_contains "TP-CLI-24 Japanese help has no Environment heading" "$_out" "Environment:"
    assert_not_contains "TP-CLI-24 Japanese help has no Examples heading" "$_out" "Examples:"
    assert_not_contains "TP-CLI-24 Japanese help has no Machine-readable JSON" "$_out" "Machine-readable JSON"
    assert_not_contains "TP-CLI-24 Japanese help has no you can read" "$_out" "you can read without sudo"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-24 Japanese useful heading" "$_out" "便利なコマンド:"
    assert_contains "TP-CLI-24 Japanese preferred cache label" "$_out" "キャッシュフォルダ（優先）"
    assert_not_contains "TP-CLI-24 Japanese about has no Useful commands" "$_out" "Useful commands:"
    assert_not_contains "TP-CLI-24 Japanese about has no English preferred" "$_out" "Cache folder (preferred):"
    assert_not_contains "TP-CLI-24 Japanese about has no Machine-readable output" "$_out" "Machine-readable output"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" about --json 2>/dev/null)
    assert_contains "TP-CLI-24 Japanese JSON about keeps cache_used" "$_out" "cache_used"
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" version 2>&1)
    assert_contains "TP-CLI-24 Japanese version stays English" "$_out" "folder-backup version "
    _out=$(FOLDER_BACKUP_LANG=ja sh "${SCRIPT}" help --json 2>/dev/null)
    assert_contains "TP-CLI-24 Japanese JSON help message" "$_out" "説明は人が読むモードにあります"
    assert_not_contains "TP-CLI-24 Japanese JSON help is not the English message" "$_out" "Help text available"
    _out=$(FOLDER_BACKUP_LANG=ko sh "${SCRIPT}" about 2>/dev/null)
    assert_contains "TP-CLI-24 Korean useful heading" "$_out" "유용한 명령:"
    _out=$(FOLDER_BACKUP_LANG=zh-Hant sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Traditional Chinese work heading" "$_out" "工作指令："
    _out=$(FOLDER_BACKUP_LANG=zh-Hans sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Simplified Chinese work heading" "$_out" "工作命令："
    _out=$(FOLDER_BACKUP_LANG=es sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 Spanish work heading" "$_out" "Comandos de trabajo:"
    _out=$(FOLDER_BACKUP_LANG=fr sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 French work heading" "$_out" "Commandes de travail :"
    _out=$(FOLDER_BACKUP_LANG=de sh "${SCRIPT}" help 2>&1)
    assert_contains "TP-CLI-24 German work heading" "$_out" "Arbeitsbefehle:"
    _body=$(awk '/^app_menu_text\(\)/{p=1} /^app_cmd_menu_language\(\)/{p=0} p' "${SCRIPT}" | tr '[:upper:]' '[:lower:]')
    assert_not_contains "TP-CLI-24 app_menu_text has no read" "${_body}" "read"
    unset _out _ec _lang _mode _body
    ci_cleanup_env
}
