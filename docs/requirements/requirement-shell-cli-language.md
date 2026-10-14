**file**: docs/requirements/requirement-shell-cli-language.md  
**Status**: Active (Version 1.2.0)  
**Area**: shell  
**Key**: `requirement-shell-cli-language`  
**Optional RQ-ID**: `RQ-SHELL-CLI-LANGUAGE`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **product Single Source of Truth** for the **display language** of folder-backup’s numbered boards and for human `help` and human `about`.

The eight codes, the child numbers **71**–**78**, the saved-language lines, the failed-write lines, the choose-prompt, Back, Exit, and the language-board longs follow the sibling **sshd-cli** language law **1.3.1**, adapted to this menu. This product has no server board. Sudoers prints only **52** and **55**. English explains stay this product’s sentences (`requirement-shell-cli-default-interaction`, `requirement-shell-cli-sudoers-submenu`).

### 1.1 Human-facing

**In one sentence:** On a real terminal, pick **7** and then **71**–**78** to choose the menu language; the choice is kept under this login and the front board comes back in that language.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Open language and pick a number | `folder-backup` then `7` then `72` |
| The other role | A script can force one run without writing the file | `FOLDER_BACKUP_LANG=ja folder-backup help` |
| Not this file | Which front rows exist, and the English board text | `requirement-shell-cli-default-interaction` |

| Includes | Excludes |
|----------|----------|
| Eight codes and front row **7** | A ninth code |
| File `${HOME}/.local/folder-backup/language` | Putting that file in the cache folder or under `/var/backup` |
| `FOLDER_BACKUP_LANG` for this run only | `language` as an argv verb |

| Surface | What you open | What for |
|---------|---------------|----------|
| Front row **7** | language board | store one code |
| `folder-backup help` | command | human help follows the code |
| `folder-backup about` | command | human about follows the code |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Keep Traditional Chinese | The file becomes `zh-Hant` and the front redraws | `7` then `72` |
| Look without saving | Back does not write the file | `7` then `0` |
| Force one run | The file stays as it was | `FOLDER_BACKUP_LANG=es folder-backup` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Codes

| Code | Row | Short on every board |
|------|-----|----------------------|
| `en` | **71** | `English` |
| `zh-Hant` | **72** | `繁體中文` |
| `es` | **73** | `Español` |
| `fr` | **74** | `Français` |
| `de` | **75** | `Deutsch` |
| `zh-Hans` | **76** | `简体中文` |
| `ja` | **77** | `日本語` |
| `ko` | **78** | `한국어` |

`en` is the default. **MUST NOT** invent a ninth code. Shorts stay those endonyms in every UI language.

### 2.2 Where the choice is stored

1. The leaf is `${HOME}/.local/${APP_NAME}/language`, inside persistence from `requirement-shell-cli-storage`. **MUST NOT** put it in the cache folder. **MUST NOT** put it under `/var/backup`.
2. The file is one line, one of the eight codes, then a newline. Mode **0600**. A trailing CR is ignored. Only the first line is read.
3. A missing file, an empty file, or any other first line means English. **MUST NOT** rewrite the file in that case.
4. `app_lang_load` sets `APP_LANG` **once**, at the start of `app_main`, after persistence is resolved and before the zero-cli-verb split. **MUST NOT** call it again in that process. A later call would let `FOLDER_BACKUP_LANG` cover a pick just saved. `app_cmd_menu` does not call it.
5. When `FOLDER_BACKUP_LANG` is one of the eight codes, that value wins at process start. It does not write the file. A menu pick still writes the file and sets `APP_LANG` for the rest of that process.
6. `app_lang_save` writes the line and sets `APP_LANG` only after the write succeeds. A code outside the eight returns failure and leaves `APP_LANG` unchanged. A failed write warns in the language that was current before the failure, then the front board still returns.

### 2.3 Menu numbers

Front **7** opens `app_cmd_menu_language`. **71** stores `en`. **72** stores `zh-Hant`. **73** stores `es`. **74** stores `fr`. **75** stores `de`. **76** stores `zh-Hans`. **77** stores `ja`. **78** stores `ko`. A successful pick prints the saved-language line, then the front board redisplays in that language. **0** / empty / EOF is Back and does not write the file. An invalid choice uses `out_error` and reprints this board.

Typed `language`, `語言`, `语言`, `idioma`, `langue`, `Sprache`, `sprache`, `言語`, and `언어` on the front open this board. The language board accepts:

| Row | Typed tokens |
|-----|----------------|
| **71** | `english`, `en`, `English` |
| **72** | `traditional-chinese`, `zh-hant`, `zh-Hant`, `繁體中文` |
| **73** | `spanish`, `es`, `Español`, `español` |
| **74** | `french`, `fr`, `Français`, `français` |
| **75** | `german`, `de`, `Deutsch`, `deutsch` |
| **76** | `simplified-chinese`, `zh-hans`, `zh-Hans`, `简体中文` |
| **77** | `japanese`, `ja`, `日本語` |
| **78** | `korean`, `ko`, `한국어` |

`language` is **not** an argv verb. `folder-backup language` stays unknown.

The front board also accepts the displayed category short: `client-side`, `用戶端`, `客户端`, `cliente`, `client`, `Client`, `クライアント`, `클라이언트` for row **1**; `self-management`, `自我管理`, `autogestión`, `autogestion`, `Selbstverwaltung`, `selbstverwaltung`, `自己管理`, `자기관리` for row **6**. The sudoers short stays `sudoers` in every language. Exit words `離開`, `离开`, `Salir`, `Quitter`, `Beenden`, `終了`, and `종료` leave the front. Back words `返回`, `Atrás`, `Retour`, `Zurück`, `戻る`, and `뒤로` are Back on a child board.

### 2.4 What follows the language

**MUST** follow `APP_LANG` on the front, client, language, self-management, and sudoers boards. That covers the layer title, the category shorts, every long description, Back, Exit, the choose-prompt, the unknown-choice line, and the hide sentences.

**MUST** keep each leaf short as the English verb in every language (`backup`, `restore`, `install`, `submit-sudoer-request`, and the other leaf tokens).

English board sentences stay the tables in `requirement-shell-cli-default-interaction` and `requirement-shell-cli-sudoers-submenu`. When `APP_LANG=en` those sentences are exact, including `Grant and drafts` and `sudoers (grant and drafts)`. Other codes translate those sentences and keep command names, flags, paths, and numbers in Latin spelling.

**MUST** follow `APP_LANG` for human `help` and human `about`: section headings and the prose after command tokens, flags, paths, and environment names. When `APP_LANG=en` that prose is exact. When `APP_LANG` is one of the other seven codes, that prose is that language. **MUST NOT** leave a human help or about sentence in English for those seven codes, except the Latin tokens, flags, paths, and environment names, and the machine status tokens below.

JSON `about` field names and values stay English. Argv `version` stays English (`folder-backup version VERSION`). Operational command output, data-picker prompts, and `out_die` lines that are not a menu unknown-choice stay English.

JSON `help` user-facing strings follow the code. The message contains the four letters r, e, a, d in a row, so it is a `case` arm in `app_help`. The note does not, so it is `app_menu_text` key `help_json_note`.

Any other sentence that contains those four letters (a lowercase scan; `already`, `thread`, `spread`, `ready`, and `readable` count) stays a `case` arm in `app_help` or `app_about`. Every other human help or about sentence is the matching `help_*` or `about_*` arm of `app_menu_text`. This requirement does not paste that function.

Machine status tokens stay Latin in about values: `production`, `test_local`, `unmanaged`, `sudo_n_ok`, `sudo_needs_auth_or_denied`, `no_sudo`, `not_found`, `true`, `false`. When a stored version or shell value equals the English words `not found` or `unknown`, the printed word follows `APP_LANG`. The installed sentence, the yes/no sentence, and the execution-context sentence are full translated sentences.

English usage heading stays `Usage:`. Other usage headings: `用法：` (zh-Hant and zh-Hans), `Uso:`, `Utilisation :`, `Verwendung:`, `使い方:`, `사용법:`. English about title stays `About / Diagnostics`. Japanese about title is `概要 / 診断`. Korean about title is `개요 / 진단`. English cache label stays `Cache folder used: ` (the source ends with one space). Japanese cache label is `使用中のキャッシュフォルダ: `. Korean cache label is `사용 중인 캐시 폴더: `. The two Chinese cache labels end on the fullwidth colon and have no trailing space. English cache preferred, 1st fallback, 2nd fallback, and persistence labels stay `Cache folder (preferred): `, `Cache folder (1st fallback): `, `Cache folder (2nd fallback): `, and `Persistence storage:` with the English spacing. The other seven codes translate those labels. JSON names `cache_used`, `cache_preferred`, `cache_fallback`, `cache_fallback_2`, and `persistence_storage` stay English.

Help and about section headings:

| Heading | en | zh-Hant | zh-Hans | es | fr | de | ja | ko |
|---------|----|---------|----------|----|----|----|----|-----|
| Self-management | `Self-management (full channel, any login):` | `自我管理（完整通道，任何登入）：` | `自我管理（完整通道，任何登录）：` | `Autogestión (canal completo, cualquier inicio):` | `Autogestion (canal complet, toute session) :` | `Selbstverwaltung (voller Kanal, jede Anmeldung):` | `自己管理（完全なチャネル、どのログインでも）:` | `자기관리 (전체 채널, 어떤 로그인이든):` |
| Install and self-care | `Install and self-care (your own login):` | `安裝與自我維護（你自己的登入）：` | `安装与自我维护（你自己的登录）：` | `Instalación y cuidado propio (su propio inicio):` | `Installation et entretien (votre propre session) :` | `Installation und eigene Pflege (Ihre eigene Anmeldung):` | `インストールと自己手入れ（自分のログイン）:` | `설치와 자기 정비 (자신의 로그인):` |
| Work | `Work commands:` | `工作指令：` | `工作命令：` | `Comandos de trabajo:` | `Commandes de travail :` | `Arbeitsbefehle:` | `作業コマンド:` | `작업 명령:` |
| Grant | `Grant and draft setup (tests and review):` | `授權與草稿設定（測試與檢視）：` | `授权与草稿设置（测试与查看）：` | `Concesión y borradores (pruebas y revisión):` | `Autorisation et brouillons (essais et relecture) :` | `Freigabe und Entwürfe (Tests und Prüfung):` | `認可と下書き（試験と確認）:` | `허가와 초안 (시험과 검토):` |
| Options | `Global Options:` | `全域選項：` | `全局选项：` | `Opciones globales:` | `Options globales :` | `Globale Optionen:` | `全体オプション:` | `전역 옵션:` |
| Environment | `Environment:` | `環境：` | `环境：` | `Entorno:` | `Environnement :` | `Umgebung:` | `環境:` | `환경:` |
| Examples | `Examples:` | `範例：` | `示例：` | `Ejemplos:` | `Exemples :` | `Beispiele:` | `例:` | `예:` |
| About useful | `Useful commands:` | `常用指令：` | `常用命令：` | `Comandos útiles:` | `Commandes utiles :` | `Nützliche Befehle:` | `便利なコマンド:` | `유용한 명령:` |

Sentences kept as `case` arms because they contain those four letters:

| Arm | en | zh-Hant | zh-Hans | es | fr | de | ja | ko |
|-----|----|---------|----------|----|----|----|----|-----|
| JSON help message | `Help text available in human-readable mode. Run without --json.` | `說明文字在人類可讀模式。請不要加 --json。` | `说明文字在人可读模式。请不要加 --json。` | `El texto de ayuda está en el modo para personas. Ejecute sin --json.` | `Le texte d'aide est dans le mode pour les personnes. Lancez sans --json.` | `Der Hilfetext steht im Modus für Menschen. Starten Sie ohne --json.` | `説明は人が読むモードにあります。--json を付けずに実行してください。` | `도움말 문장은 사람이 읽는 모드에 있습니다. --json 없이 실행하세요.` |
| `--json` flag | `Machine-readable JSON (implies --quiet)` | `機器可處理的 JSON（同時視為 --quiet）` | `机器可处理的 JSON（同时视为 --quiet）` | `JSON para máquinas (implica --quiet)` | `JSON pour les machines (implique --quiet)` | `JSON für Maschinen (schließt --quiet ein)` | `機械向け JSON（--quiet を含む）` | `기계용 JSON(--quiet 포함)` |
| Generate continuation | `you can read without sudo. Does not write /etc or inbound.` | `不必用 sudo 就能查看。不會寫入 /etc 或 inbound。` | `不必用 sudo 就能查看。不会写入 /etc 或 inbound。` | `se puede ver sin sudo. No escribe /etc ni inbound.` | `visible sans sudo. N'écrit pas /etc ni inbound.` | `ohne sudo sichtbar. Schreibt nicht nach /etc oder inbound.` | `sudo なしで内容を見られます。/etc と inbound には書きません。` | `sudo 없이 내용을 볼 수 있습니다. /etc 나 inbound 에는 쓰지 않습니다.` |
| About `--json` blurb | `Machine-readable output` | `機器可處理的輸出` | `机器可处理的输出` | `salida para máquinas` | `sortie pour les machines` | `Ausgabe für Maschinen` | `機械向けの出力` | `기계용 출력` |

English help **MUST** name `77 Japanese` and `78 Korean`.

Saved line (printed after a successful save, so it is in the new language):

| Code | Saved |
|------|--------|
| `en` | `Menu language is English` |
| `zh-Hant` | `選單語言是繁體中文` |
| `es` | `El idioma del menú es español` |
| `fr` | `La langue du menu est le français` |
| `de` | `Die Menüsprache ist Deutsch` |
| `zh-Hans` | `菜单语言是简体中文` |
| `ja` | `メニューの言語は日本語` |
| `ko` | `메뉴 언어는 한국어` |

Failed write:

| Code | Failed write |
|------|----------------|
| `en` | `Could not save the menu language` |
| `zh-Hant` | `無法儲存選單語言` |
| `es` | `No se pudo guardar el idioma del menú` |
| `fr` | `Impossible d'enregistrer la langue du menu` |
| `de` | `Die Menüsprache konnte nicht gespeichert werden` |
| `zh-Hans` | `无法保存菜单语言` |
| `ja` | `メニューの言語を保存できませんでした` |
| `ko` | `메뉴 언어를 저장하지 못했습니다` |

Back and Exit:

| Code | Back | Exit |
|------|------|------|
| `en` | `0. Back` | `9. Exit` |
| `zh-Hant` | `0. 返回` | `9. 離開` |
| `zh-Hans` | `0. 返回` | `9. 离开` |
| `es` | `0. Atrás` | `9. Salir` |
| `fr` | `0. Retour` | `9. Quitter` |
| `de` | `0. Zurück` | `9. Beenden` |
| `ja` | `0. 戻る` | `9. 終了` |
| `ko` | `0. 뒤로` | `9. 종료` |

Choose-prompt. Every source string ends with one space.

| Code | Source string |
|------|----------------|
| `en` | `Choose a number, or type the command name: ` |
| `zh-Hant` | `請輸入編號，或輸入指令名稱： ` |
| `es` | `Elija un número, o escriba el nombre del comando: ` |
| `fr` | `Choisissez un numéro, ou saisissez le nom de la commande : ` |
| `de` | `Wählen Sie eine Nummer, oder geben Sie den Befehlsnamen ein: ` |
| `zh-Hans` | `请输入编号，或输入指令名称： ` |
| `ja` | `番号を入力するか、コマンド名を入力してください: ` |
| `ko` | `번호를 입력하거나 명령 이름을 입력하세요: ` |

Menu boards print that prompt with `out_msg_n` and then `read -r` into `_prompt_line` in the current shell. **MUST NOT** pass it through `prompt_line` (that helper appends another colon). Field prompts (a backup path, an archive) stay `prompt_line`.

Language-board longs:

| UI | Row | Long |
|----|-----|------|
| `en` | **71** | `use English for this menu` |
| `en` | **72** | `use Traditional Chinese for this menu` |
| `en` | **73** | `use Spanish for this menu` |
| `en` | **74** | `use French for this menu` |
| `en` | **75** | `use German for this menu` |
| `en` | **76** | `use Simplified Chinese for this menu` |
| `en` | **77** | `use Japanese for this menu` |
| `en` | **78** | `use Korean for this menu` |
| `zh-Hant` | **71** | `這個選單改用英文` |
| `zh-Hant` | **72** | `這個選單改用繁體中文` |
| `zh-Hant` | **73** | `這個選單改用西班牙文` |
| `zh-Hant` | **74** | `這個選單改用法文` |
| `zh-Hant` | **75** | `這個選單改用德文` |
| `zh-Hant` | **76** | `這個選單改用簡體中文` |
| `zh-Hant` | **77** | `這個選單改用日文` |
| `zh-Hant` | **78** | `這個選單改用韓文` |
| `es` | **71** | `usar inglés en este menú` |
| `es` | **72** | `usar chino tradicional en este menú` |
| `es` | **73** | `usar español en este menú` |
| `es` | **74** | `usar francés en este menú` |
| `es` | **75** | `usar alemán en este menú` |
| `es` | **76** | `usar chino simplificado en este menú` |
| `es` | **77** | `usar japonés en este menú` |
| `es` | **78** | `usar coreano en este menú` |
| `fr` | **71** | `utiliser l'anglais pour ce menu` |
| `fr` | **72** | `utiliser le chinois traditionnel pour ce menu` |
| `fr` | **73** | `utiliser l'espagnol pour ce menu` |
| `fr` | **74** | `utiliser le français pour ce menu` |
| `fr` | **75** | `utiliser l'allemand pour ce menu` |
| `fr` | **76** | `utiliser le chinois simplifié pour ce menu` |
| `fr` | **77** | `utiliser le japonais pour ce menu` |
| `fr` | **78** | `utiliser le coréen pour ce menu` |
| `de` | **71** | `Englisch für dieses Menü verwenden` |
| `de` | **72** | `Traditionelles Chinesisch für dieses Menü verwenden` |
| `de` | **73** | `Spanisch für dieses Menü verwenden` |
| `de` | **74** | `Französisch für dieses Menü verwenden` |
| `de` | **75** | `Deutsch für dieses Menü verwenden` |
| `de` | **76** | `Vereinfachtes Chinesisch für dieses Menü verwenden` |
| `de` | **77** | `Japanisch für dieses Menü verwenden` |
| `de` | **78** | `Koreanisch für dieses Menü verwenden` |
| `zh-Hans` | **71** | `这个菜单改用英文` |
| `zh-Hans` | **72** | `这个菜单改用繁体中文` |
| `zh-Hans` | **73** | `这个菜单改用西班牙文` |
| `zh-Hans` | **74** | `这个菜单改用法文` |
| `zh-Hans` | **75** | `这个菜单改用德文` |
| `zh-Hans` | **76** | `这个菜单改用简体中文` |
| `zh-Hans` | **77** | `这个菜单改用日文` |
| `zh-Hans` | **78** | `这个菜单改用韩文` |
| `ja` | **71** | `このメニューを英語にする` |
| `ja` | **72** | `このメニューを繁体字中国語にする` |
| `ja` | **73** | `このメニューをスペイン語にする` |
| `ja` | **74** | `このメニューをフランス語にする` |
| `ja` | **75** | `このメニューをドイツ語にする` |
| `ja` | **76** | `このメニューを簡体字中国語にする` |
| `ja` | **77** | `このメニューを日本語にする` |
| `ja` | **78** | `このメニューを韓国語にする` |
| `ko` | **71** | `이 메뉴를 영어로` |
| `ko` | **72** | `이 메뉴를 번체 중국어로` |
| `ko` | **73** | `이 메뉴를 스페인어로` |
| `ko` | **74** | `이 메뉴를 프랑스어로` |
| `ko` | **75** | `이 메뉴를 독일어로` |
| `ko` | **76** | `이 메뉴를 간체 중국어로` |
| `ko` | **77** | `이 메뉴를 일본어로` |
| `ko` | **78** | `이 메뉴를 한국어로` |

Front language long: `display language for this menu` (en), `這個選單的顯示語言`, `idioma de este menú`, `langue d'affichage de ce menu`, `Anzeigesprache dieses Menüs`, `这个菜单的显示语言`, `このメニューの表示言語`, `이 메뉴의 표시 언어`. Category short: `language` / `語言` / `idioma` / `langue` / `Sprache` / `语言` / `言語` / `언어`.

### 2.5 Call shape

`app_lang_load`, `app_lang_save`, and `app_menu_text` do not contain `read` (a lowercase scan of those four letters in a row). A command substitution around them is allowed. `app_cmd_menu_language` contains `read -r` and **MUST** be called in the current shell from the front board’s language arm. **MUST NOT** wrap that function in `$()` or backticks.

`app_menu_text` prints the chosen string on stdout with no newline. A missing key prints the key. An unknown `APP_LANG` falls back to English. The caller passes the string to `out_*`.

### 2.6 Worked samples

English front (markdown emphasis stands in for TTY ink; the choose-prompt’s trailing space is omitted here):

```text
[INFO] **folder-backup**(*VERSION*) — numbered list
[INFO] server-side is not available: this program does not run a host service. Number 2 stays reserved.
1. **client-side**: *this login's folders: pack and restore*
5. **sudoers**: *Grant and drafts*
6. **self-management**: *this CLI install, version, update, uninstall*
7. **language**: *display language for this menu*
9. Exit
Choose a number, or type the command name:
```

Traditional Chinese front after **72**:

```text
[INFO] **folder-backup**(*VERSION*) — 編號清單
[INFO] 伺服器端無法使用：這個程式不執行主機服務。編號 2 保留。
1. **用戶端**: *這個登入的資料夾：打包與還原*
5. **sudoers**: *授權與草稿*
6. **自我管理**: *這個 CLI 的安裝、版本、更新、移除*
7. **語言**: *這個選單的顯示語言*
9. 離開
請輸入編號，或輸入指令名稱：
```

Japanese help opens with `使い方:` and the work heading `作業コマンド:`. It does not print `Usage:` or `Work commands:`. Korean about opens with `개요 / 診断` and the useful heading `유용한 명령:`.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A bad file stays English and is not rewritten. Env does not clobber a pick in the same process.
- **Intentional:** Eight codes, one file, one env name.
- **Anti-fragile:** Back does not write. A failed write still returns to the front.
- **Over-protect:** `language` is not a dispatcher token. The language leaf is not cache and not `/var/backup`.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add a ninth language code, or drop one of the eight.
2. Store the language leaf in the cache folder or under `/var/backup`.
3. Call `app_lang_load` again after a menu pick in the same process.
4. Let `FOLDER_BACKUP_LANG` rewrite the language file.
5. Dispatch `language` from `app_main`.
6. Put `read` inside `app_menu_text`, or call `app_cmd_menu_language` through `$()`.
7. Pass the menu choose-prompt through `prompt_line`.
8. Change English `Grant and drafts` or `sudoers (grant and drafts)` while translating other codes.
9. Translate leaf shorts (`backup`, `install`, `submit-sudoer-request`, and the rest).
10. Leave human help or about prose in English when `APP_LANG` is one of the other seven codes, except Latin tokens, flags, paths, environment names, and the machine status tokens in §2.4.

**Violating this rule is a critical menu-language regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Front row **7** opens **71**–**78** and **0** Back. **0** does not write the file |
| AC-2 | **72** writes `zh-Hant`, mode **0600**, prints the saved line, and the front redraws with `用戶端` and `9. 離開`. The next run stays that language when `FOLDER_BACKUP_LANG` is unset |
| AC-3 | **71** restores `en`. **73**–**78** store `es`, `fr`, `de`, `zh-Hans`, `ja`, `ko` and print that code’s saved line and Exit word |
| AC-4 | A first line other than the eight codes stays English and is left as written |
| AC-5 | `FOLDER_BACKUP_LANG` overrides the file for that process and does not rewrite the file |
| AC-6 | Human `help` and human `about` follow `APP_LANG`. Japanese help uses `使い方:` and `作業コマンド:`. Korean about uses `개요 / 診断` and `유용한 명령:`. English help still says `Usage:`, `Work commands:`, and `Grant and draft setup (tests and review):`, and names **77** and **78**. JSON about keeps `cache_used`. Argv `version` stays `folder-backup version` |
| AC-7 | `folder-backup language` is unknown. English front text stays the default-interaction table, plus row **7** |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-default-interaction` | Front row **7**; English board text; choice read |
| `requirement-shell-cli-sudoers-submenu` | English sudoers header and rows; copy follows `APP_LANG` |
| `requirement-shell-cli-storage` | Persistence leaf `language`; not cache |
| `requirement-shell-cli-interface` | `language` is not dispatched |
| `requirement-shell-modular-function-design` | Prefix `app_` for the four helpers |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-24** | `tests/test_cli.sh` | **have** — eight codes, file mode, env override, human help and about in each code (AC-1–AC-7) |
| **TP-CLI-04** / **TP-CLI-15** | same | **have** — English help names language and **77** / **78** |
| **TP-CLI-13** | same | **have** — English front includes row **7** and no server row |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## Terminologies

Copied substance for the words this requirement uses.

### CLI main menu numbering

**Definition:** CLI main menu numbering is the portable rule set for integers on a claimed CLI default interaction tree. A command number is unique in the whole tree: a child list must not reuse 1, 2, or 6, or any other parent token. A child command number must start with its parent's number as prefix: 11… under 1, 21… under 2, 51… under 5 when a sudoers family is claimed, 61… under 6, 71… under 7 when a language board is claimed, and 111… under 11. The front board uses small category integers plus Exit 9. Every submenu and data picker uses 0 to go back to the parent list. This term owns which integers, not ink and not the catalog of rows.

**Human daily-life explanation:** CLI main menu numbering is how the café numbers dishes so 11 always means the same plate, even after you walk into a side room. The side-room specials do not start again at 1. They keep the front number as a prefix (11, 111). 0 is the door back to the previous board. 9 on the front board is leaving the café.

**Daily-life example:** Front board 1, client side, opens a second board whose first dish is 11, not another 1. If the kitchen reused 1, nobody would know whether you meant the front door or the first side dish.

### Well-known menu

**Definition:** A well-known menu is the portable numbered TTY membership of well-known CLI verbs, plus the category front rows and front Exit, shared across self-managed products that claim a CLI default interaction. It is the portable subset of a CLI main menu hierarchy table: front board 1 / 2 / 5 / 6 / 7 / 9 and self-management 61…67 under 6. Those integers stay reserved. Which rows a product prints follows the language consider table (shell column versus Python / pip column). Domain numbered rows belong on the full hierarchy table, not this catalog.

**Human daily-life explanation:** A well-known menu is the shared café numbering every similar kitchen agrees on. The front chalkboard has rooms 1, 2, 5 when a sudoers family is claimed, 6 for self-care, and 7 when a language board is claimed, plus 9 to leave. The back-office list under 6 keeps the same dish numbers.

**Daily-life example:** You walk into a shell shop in the family. 6 is self-care. 67 files this tool in the drawer. 61 stocks the pantry when that shop sells extra kits. You walk into a pip shop: 6 is still self-care, 64 and 65 ask the package counter to compare and refresh, and 61 is not "pip install this program."

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-14 | Active 1.2.0 | Front row **7**. Children **71**–**78**. English help names **77** Japanese and **78** Korean. The English front sample and the Traditional Chinese front sample print **1**, **5**, **6**, **7**, **9**. | Terminologies section added.
| 2026-09-30 | Active 1.0.0 | Front **6**, eight codes, persistence leaf, `FOLDER_BACKUP_LANG`. Help and about translate the heading, menu sentence, catalog, title, and cache-used label. |
| 2026-09-30 | Active 1.1.0 | Human `help` and human `about` follow `APP_LANG`. JSON about and argv `version` stay English. Sentences that contain `read` stay `case` arms. |
| 2026-10-10 | Active 1.2.0 | Front worked samples use the not-available hide sentence. |

---

**Last Updated**: 2026-10-14  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
