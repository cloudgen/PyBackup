# =============================================================================
# Menu language for the text menu.
# requirement-python-cli-language — codes, the language leaf, and menu copy.
# requirement-python-oop — class MenuLanguage.
# =============================================================================
from __future__ import annotations

import os


class MenuLanguage:
    """The thirteen menu languages, the saved code, and the words the menu prints.

    English is the default when the leaf is missing, empty, or not one of the
    codes. LANG is not read. PYBACKUP_LANG wins at startup and does not write
    the leaf. A menu pick writes the leaf and updates this process.
    """

    CODES = (
        ("en", "English", 41),
        ("zh-Hans", "简体中文", 42),
        ("zh-Hant", "繁體中文", 43),
        ("es", "Español", 44),
        ("ar", "العربية", 45),
        ("fr", "Français", 46),
        ("pt", "Português", 47),
        ("ru", "Русский", 48),
        ("de", "Deutsch", 49),
        ("ja", "日本語", 50),
        ("ko", "한국어", 51),
        ("nl", "Nederlands", 52),
        ("el", "Ελληνικά", 53),
    )
    BLOCK_FIRST = 40
    BLOCK_LAST = 59
    APP_DIR = "PyBackup"
    LEAF_NAME = "language"

    def __init__(self, logger=None, home=None) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuLanguage")
        if home is None:
            home = os.environ.get("HOME", "")
        self.home = home
        self._code = "en"
        self.load()

    def codes(self) -> tuple:
        return tuple(code for code, _name, _number in self.CODES)

    def endonym(self, code: str) -> str:
        for item, name, _number in self.CODES:
            if item == code:
                return name
        return ""

    def number_for(self, code: str) -> int | None:
        for item, _name, number in self.CODES:
            if item == code:
                return number
        return None

    def code_for_number(self, number: int) -> str | None:
        for code, _name, item in self.CODES:
            if item == number:
                return code
        return None

    def leaf_path(self) -> str:
        """The language leaf. Empty when this process has no home directory."""
        if not self.home:
            return ""
        return os.path.join(self.home, ".local", self.APP_DIR, self.LEAF_NAME)

    def code(self) -> str:
        return self._code

    def load(self) -> None:
        """Pick the code for this process. Does not write the leaf.

        PYBACKUP_LANG wins when it is one of the thirteen codes. Otherwise the
        first line of the leaf is used. A missing, empty, or other line is English.
        An other line is not rewritten.
        """
        forced = os.environ.get("PYBACKUP_LANG", "")
        if forced in self.codes():
            self._code = forced
            return
        self._code = self._read_leaf()

    def _read_leaf(self) -> str:
        path = self.leaf_path()
        if not path or not os.path.isfile(path):
            return "en"
        try:
            with open(path, "r", encoding="utf-8") as handle:
                line = handle.readline()
        except OSError:
            return "en"
        line = line.replace("\r", "").strip()
        if line in self.codes():
            return line
        return "en"

    def save(self, code: str) -> str:
        """Write one code and switch this process. A failed write keeps the old code.

        The message is in the language that is current after a success, and in
        the language that was current before a failed write.
        """
        if code not in self.codes():
            return self.text("save_failed")
        path = self.leaf_path()
        if not path:
            return self.text("save_failed")
        previous = self._code
        try:
            folder = os.path.dirname(path)
            os.makedirs(folder, mode=0o700, exist_ok=True)
            os.chmod(folder, 0o700)
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            try:
                os.write(descriptor, (code + "\n").encode("utf-8"))
            finally:
                os.close(descriptor)
            os.chmod(path, 0o600)
        except OSError:
            self._code = previous
            return self.text("save_failed")
        self._code = code
        return self.text("saved")

    def text(self, key: str) -> str:
        block = _TEXTS.get(self._code) or _TEXTS["en"]
        found = block.get(key)
        if found is None:
            found = _TEXTS["en"].get(key, "")
        return found

    def path_label(self) -> str:
        """The path-line word for the selected code. The directory is not translated."""
        return self.text("path")

    def lang_long(self, endonym: str) -> str:
        return self.text("lang_long").format(name=endonym)

    def row_short(self, kind: str, english: str) -> str:
        key = _SHORT_KEY.get(kind)
        if key is None:
            return english
        return self.text(key)

    def row_long(self, kind: str, english: str) -> str:
        key = _LONG_KEY.get(kind)
        if key is None:
            return english
        return self.text(key)

    def token_kind(self, token: str, layer: str) -> str | None:
        """A typed word that is not the row currently on screen.

        The language board accepts the code tokens. The front board accepts
        every category short. Leaf verbs stay the English token on the row.
        """
        if layer == "lang":
            code = _LANG_TOKENS.get(token)
            if code is not None:
                return "set-" + code
            return None
        if layer == "front":
            return _FRONT_TOKENS.get(token)
        return None


_SHORT_KEY = {
    "language": "language_short",
    "system-log": "system_log_short",
    "self-management": "self_short",
    "exit": "exit_short",
    "back": "back_short",
    "client-side": "client_short",
}

_LONG_KEY = {
    "client-side": "client_long",
    "sudoers": "sudoers_long",
    "backup": "backup_long",
    "restore": "restore_long",
    "submit-sudoer-request": "submit_long",
    "remove-project-sudoers": "remove_long",
    "language": "language_long",
    "system-log": "system_log_long",
    "self-management": "self_long",
    "exit": "exit_long",
    "back": "back_long",
    "view-log": "view_long",
    "clear-log": "clear_long",
    "log-folder": "folder_long",
    "version": "version_long",
    "about": "about_long",
    "version-check": "version_check_long",
    "self-update": "self_update_long",
    "self-uninstall": "self_uninstall_long",
    "self-install": "self_install_long",
}

_LANG_TOKENS = {
    "english": "en",
    "en": "en",
    "English": "en",
    "simplified-chinese": "zh-Hans",
    "zh-hans": "zh-Hans",
    "zh-Hans": "zh-Hans",
    "简体中文": "zh-Hans",
    "traditional-chinese": "zh-Hant",
    "zh-hant": "zh-Hant",
    "zh-Hant": "zh-Hant",
    "繁體中文": "zh-Hant",
    "spanish": "es",
    "es": "es",
    "Español": "es",
    "español": "es",
    "arabic": "ar",
    "ar": "ar",
    "العربية": "ar",
    "عربي": "ar",
    "french": "fr",
    "fr": "fr",
    "Français": "fr",
    "français": "fr",
    "portuguese": "pt",
    "pt": "pt",
    "Português": "pt",
    "português": "pt",
    "portugues": "pt",
    "russian": "ru",
    "ru": "ru",
    "Русский": "ru",
    "русский": "ru",
    "german": "de",
    "de": "de",
    "Deutsch": "de",
    "deutsch": "de",
    "japanese": "ja",
    "ja": "ja",
    "日本語": "ja",
    "korean": "ko",
    "ko": "ko",
    "한국어": "ko",
    "dutch": "nl",
    "nl": "nl",
    "Nederlands": "nl",
    "nederlands": "nl",
    "greek": "el",
    "el": "el",
    "Ελληνικά": "el",
    "ελληνικά": "el",
}

_FRONT_TOKENS = {
    "language": "language",
    "語言": "language",
    "语言": "language",
    "idioma": "language",
    "langue": "language",
    "Sprache": "language",
    "sprache": "language",
    "言語": "language",
    "언어": "language",
    "لغة": "language",
    "язык": "language",
    "taal": "language",
    "γλώσσα": "language",
    "system-log": "system-log",
    "系统日志": "system-log",
    "系統日誌": "system-log",
    "registro": "system-log",
    "journal": "system-log",
    "Systemprotokoll": "system-log",
    "システムログ": "system-log",
    "시스템 로그": "system-log",
    "registo": "system-log",
    "системный журнал": "system-log",
    "systeemlog": "system-log",
    "αρχείο καταγραφής": "system-log",
    "سجل النظام": "system-log",
    "self-management": "self-management",
    "自我管理": "self-management",
    "autogestión": "self-management",
    "autogestion": "self-management",
    "autogestão": "self-management",
    "Selbstverwaltung": "self-management",
    "selbstverwaltung": "self-management",
    "自己管理": "self-management",
    "자기관리": "self-management",
    "إدارة ذاتية": "self-management",
    "самоуправление": "self-management",
    "zelfbeheer": "self-management",
    "αυτοδιαχείριση": "self-management",
    "client-side": "client-side",
    "用戶端": "client-side",
    "客户端": "client-side",
    "cliente": "client-side",
    "client": "client-side",
    "Client": "client-side",
    "クライアント": "client-side",
    "클라이언트": "client-side",
    "sudoers": "sudoers",
    "Exit": "exit",
    "离开": "exit",
    "離開": "exit",
    "Salir": "exit",
    "خروج": "exit",
    "Quitter": "exit",
    "Sair": "exit",
    "Выход": "exit",
    "Beenden": "exit",
    "終了": "exit",
    "종료": "exit",
    "Afsluiten": "exit",
    "Έξοδος": "exit",
}

_TEXTS = {
    "en": {
        "path": "Path",
        "language_short": "language",
        "language_long": "display language for this menu",
        "system_log_short": "system-log",
        "system_log_long": "view, clear, and the log folder",
        "self_short": "self-management",
        "self_long": "version, about, and pip lifecycle",
        "exit_short": "Exit",
        "exit_long": "leave",
        "back_short": "Back",
        "back_long": "return to the main menu",
        "client_short": "client-side",
        "client_long": "this login's folders: pack and restore",
        "sudoers_long": "Grant and drafts",
        "backup_long": "Pack a named folder into a dated gzip archive under /var/backup/PyBackup",
        "restore_long": "Put an archive back onto the hard-disk projects tree",
        "submit_long": "Hand the JSON grant to the approval queue",
        "remove_long": "Remove the local grant draft only",
        "band_front": "server-side is not available: this program does not run a host service. Number 2 stays reserved.",
        "band_sudoers": "test commands are not available: type generate-sudoer-request, print-sudoers, or print-sudoers-install-script. Numbers 51, 53, and 54 stay reserved.",
        "title_client": "client-side",
        "title_sudoers": "sudoers",
        "help_work": "Work commands:",
        "help_grant": "Grant and draft setup (tests and review):",
        "view_long": "list a log file and show it",
        "clear_long": "empty one log file",
        "folder_long": "show the log folder",
        "version_long": "show the installed version",
        "about_long": "version and this computer",
        "version_check_long": "compare this install with pip",
        "self_update_long": "upgrade this package with pip",
        "self_uninstall_long": "remove this package with pip",
        "self_install_long": "install this package with pip",
        "title_main": "main menu",
        "title_language": "language",
        "title_log": "system-log",
        "title_self": "self-management",
        "invalid": "That choice is not on this list. Pick a listed number.",
        "saved": "Menu language is English",
        "save_failed": "Could not save the menu language",
        "lang_long": "use {name} for this menu",
    },
    "zh-Hans": {
        "path": "路径",
        "language_short": "语言",
        "language_long": "此菜单的显示语言",
        "system_log_short": "系统日志",
        "system_log_long": "查看、清空，以及日志文件夹",
        "self_short": "自我管理",
        "self_long": "版本、关于，以及 pip 生命周期",
        "exit_short": "离开",
        "exit_long": "离开",
        "back_short": "返回",
        "back_long": "返回主菜单",
        "client_short": "客户端",
        "client_long": "这个登录的文件夹：打包与还原",
        "sudoers_long": "授权与草稿",
        "backup_long": "把具名文件夹打包成带日期的 gzip 归档，放在 /var/backup/PyBackup",
        "restore_long": "把归档放回硬盘上的项目树",
        "submit_long": "把 JSON 授权交给核准队列",
        "remove_long": "只移除本机的授权草稿",
        "band_front": "服务器端无法使用：这个程序不运行主机服务。编号 2 保留。",
        "band_sudoers": "测试命令无法使用：请输入 generate-sudoer-request、print-sudoers 或 print-sudoers-install-script。编号 51、53、54 保留。",
        "title_client": "客户端",
        "title_sudoers": "sudoers",
        "help_work": "工作命令：",
        "help_grant": "授权与草稿设置（测试与查看）：",
        "view_long": "列出日志文件并显示",
        "clear_long": "清空一个日志文件",
        "folder_long": "显示日志文件夹",
        "version_long": "显示已安装的版本",
        "about_long": "版本，以及这台计算机",
        "version_check_long": "用 pip 比较此安装",
        "self_update_long": "用 pip 升级此包",
        "self_uninstall_long": "用 pip 移除此包",
        "self_install_long": "用 pip 安装此包",
        "title_main": "主菜单",
        "title_language": "语言",
        "title_log": "系统日志",
        "title_self": "自我管理",
        "invalid": "这个选择不在列表上。请挑选列出的号码。",
        "saved": "菜单语言是简体中文",
        "save_failed": "无法保存菜单语言",
        "lang_long": "此菜单使用{name}",
    },
    "zh-Hant": {
        "path": "路徑",
        "language_short": "語言",
        "language_long": "這個選單的顯示語言",
        "system_log_short": "系統日誌",
        "system_log_long": "查看、清空，以及日誌資料夾",
        "self_short": "自我管理",
        "self_long": "版本、關於，以及 pip 生命週期",
        "exit_short": "離開",
        "exit_long": "離開",
        "back_short": "返回",
        "back_long": "返回主選單",
        "client_short": "用戶端",
        "client_long": "這個登入的資料夾：打包與還原",
        "sudoers_long": "授權與草稿",
        "backup_long": "把具名資料夾打包成帶日期的 gzip 封存，放在 /var/backup/PyBackup",
        "restore_long": "把封存放回硬碟上的專案樹",
        "submit_long": "把 JSON 授權交給核准佇列",
        "remove_long": "只移除本機的授權草稿",
        "band_front": "伺服器端無法使用：這個程式不執行主機服務。編號 2 保留。",
        "band_sudoers": "測試指令無法使用：請輸入 generate-sudoer-request、print-sudoers 或 print-sudoers-install-script。編號 51、53、54 保留。",
        "title_client": "用戶端",
        "title_sudoers": "sudoers",
        "help_work": "工作指令：",
        "help_grant": "授權與草稿設定（測試與檢視）：",
        "view_long": "列出日誌檔並顯示",
        "clear_long": "清空一個日誌檔",
        "folder_long": "顯示日誌資料夾",
        "version_long": "顯示已安裝的版本",
        "about_long": "版本，以及這台電腦",
        "version_check_long": "用 pip 比較此安裝",
        "self_update_long": "用 pip 升級此套件",
        "self_uninstall_long": "用 pip 移除此套件",
        "self_install_long": "用 pip 安裝此套件",
        "title_main": "主選單",
        "title_language": "語言",
        "title_log": "系統日誌",
        "title_self": "自我管理",
        "invalid": "這個選擇不在清單上。請挑選列出的號碼。",
        "saved": "選單語言是繁體中文",
        "save_failed": "無法儲存選單語言",
        "lang_long": "這個選單使用{name}",
    },
    "es": {
        "path": "Ruta",
        "language_short": "idioma",
        "language_long": "idioma de este menú",
        "system_log_short": "registro",
        "system_log_long": "ver, vaciar y la carpeta de registro",
        "self_short": "autogestión",
        "self_long": "versión, acerca de y el ciclo de pip",
        "exit_short": "Salir",
        "exit_long": "salir",
        "back_short": "Atrás",
        "back_long": "volver al menú principal",
        "client_short": "cliente",
        "client_long": "carpetas de este inicio: empaquetar y restaurar",
        "sudoers_long": "concesión y borradores",
        "backup_long": "Empaquetar una carpeta con nombre en un gzip con fecha bajo /var/backup/PyBackup",
        "restore_long": "Devolver un archivo al árbol de proyectos del disco",
        "submit_long": "Entregar la concesión JSON a la cola de aprobación",
        "remove_long": "Quitar solo el borrador local de la concesión",
        "band_front": "servidor no está disponible: este programa no ejecuta un servicio del equipo. El número 2 queda reservado.",
        "band_sudoers": "los comandos de prueba no están disponibles: escriba generate-sudoer-request, print-sudoers o print-sudoers-install-script. Los números 51, 53 y 54 quedan reservados.",
        "title_client": "cliente",
        "title_sudoers": "sudoers",
        "help_work": "Comandos de trabajo:",
        "help_grant": "Concesión y borradores (pruebas y revisión):",
        "view_long": "listar un archivo de registro y mostrarlo",
        "clear_long": "vaciar un archivo de registro",
        "folder_long": "mostrar la carpeta de registro",
        "version_long": "mostrar la versión instalada",
        "about_long": "versión y este equipo",
        "version_check_long": "comparar esta instalación con pip",
        "self_update_long": "actualizar este paquete con pip",
        "self_uninstall_long": "quitar este paquete con pip",
        "self_install_long": "instalar este paquete con pip",
        "title_main": "menú principal",
        "title_language": "idioma",
        "title_log": "registro",
        "title_self": "autogestión",
        "invalid": "Esa opción no está en la lista. Elija un número de la lista.",
        "saved": "El idioma del menú es español",
        "save_failed": "No se pudo guardar el idioma del menú",
        "lang_long": "usar {name} en este menú",
    },
    "ar": {
        "path": "المسار",
        "language_short": "لغة",
        "language_long": "لغة العرض لهذه القائمة",
        "system_log_short": "سجل النظام",
        "system_log_long": "عرض ومسح ومجلد السجل",
        "self_short": "إدارة ذاتية",
        "self_long": "الإصدار وحول ودورة pip",
        "exit_short": "خروج",
        "exit_long": "خروج",
        "back_short": "رجوع",
        "back_long": "العودة إلى القائمة الرئيسية",
        "view_long": "سرد ملف سجل وعرضه",
        "clear_long": "إفراغ ملف سجل واحد",
        "folder_long": "عرض مجلد السجل",
        "version_long": "عرض الإصدار المثبّت",
        "about_long": "الإصدار وهذا الجهاز",
        "version_check_long": "قارن هذا التثبيت مع pip",
        "self_update_long": "ترقية هذه الحزمة بـ pip",
        "self_uninstall_long": "إزالة هذه الحزمة بـ pip",
        "self_install_long": "تثبيت هذه الحزمة بـ pip",
        "title_main": "القائمة الرئيسية",
        "title_language": "لغة",
        "title_log": "سجل النظام",
        "title_self": "إدارة ذاتية",
        "invalid": "هذا الاختيار ليس في القائمة. اختر رقماً معروضاً.",
        "saved": "لغة القائمة هي العربية",
        "save_failed": "تعذر حفظ لغة القائمة",
        "lang_long": "استخدام {name} لهذه القائمة",
    },
    "fr": {
        "path": "Chemin",
        "language_short": "langue",
        "language_long": "langue d'affichage de ce menu",
        "system_log_short": "journal",
        "system_log_long": "voir, vider et le dossier du journal",
        "self_short": "autogestion",
        "self_long": "version, à propos et le cycle pip",
        "exit_short": "Quitter",
        "exit_long": "quitter",
        "back_short": "Retour",
        "back_long": "revenir au menu principal",
        "client_short": "client",
        "client_long": "dossiers de cette session : empaqueter et restaurer",
        "sudoers_long": "autorisation et brouillons",
        "backup_long": "Empaqueter un dossier nommé en gzip daté sous /var/backup/PyBackup",
        "restore_long": "Remettre une archive sur l'arbre de projets du disque",
        "submit_long": "Remettre l'autorisation JSON à la file d'approbation",
        "remove_long": "Retirer seulement le brouillon local",
        "band_front": "serveur n'est pas disponible : ce programme ne lance pas un service de l'hôte. Le numéro 2 reste réservé.",
        "band_sudoers": "les commandes de test ne sont pas disponibles : saisissez generate-sudoer-request, print-sudoers ou print-sudoers-install-script. Les numéros 51, 53 et 54 restent réservés.",
        "title_client": "client",
        "title_sudoers": "sudoers",
        "help_work": "Commandes de travail :",
        "help_grant": "Autorisation et brouillons (essais et relecture) :",
        "view_long": "lister un fichier journal et l'afficher",
        "clear_long": "vider un fichier journal",
        "folder_long": "afficher le dossier du journal",
        "version_long": "afficher la version installée",
        "about_long": "version et cet ordinateur",
        "version_check_long": "comparer cette installation avec pip",
        "self_update_long": "mettre à jour ce paquet avec pip",
        "self_uninstall_long": "retirer ce paquet avec pip",
        "self_install_long": "installer ce paquet avec pip",
        "title_main": "menu principal",
        "title_language": "langue",
        "title_log": "journal",
        "title_self": "autogestion",
        "invalid": "Ce choix n'est pas dans la liste. Choisissez un numéro affiché.",
        "saved": "La langue du menu est le français",
        "save_failed": "Impossible d'enregistrer la langue du menu",
        "lang_long": "utiliser {name} pour ce menu",
    },
    "pt": {
        "path": "Caminho",
        "language_short": "idioma",
        "language_long": "idioma deste menu",
        "system_log_short": "registo",
        "system_log_long": "ver, esvaziar e a pasta de registo",
        "self_short": "autogestão",
        "self_long": "versão, acerca de e o ciclo do pip",
        "exit_short": "Sair",
        "exit_long": "sair",
        "back_short": "Voltar",
        "back_long": "voltar ao menu principal",
        "view_long": "listar um ficheiro de registo e mostrá-lo",
        "clear_long": "esvaziar um ficheiro de registo",
        "folder_long": "mostrar a pasta de registo",
        "version_long": "mostrar a versão instalada",
        "about_long": "versão e este computador",
        "version_check_long": "comparar esta instalação com o pip",
        "self_update_long": "atualizar este pacote com o pip",
        "self_uninstall_long": "remover este pacote com o pip",
        "self_install_long": "instalar este pacote com o pip",
        "title_main": "menu principal",
        "title_language": "idioma",
        "title_log": "registo",
        "title_self": "autogestão",
        "invalid": "Essa escolha não está na lista. Escolha um número da lista.",
        "saved": "O idioma do menu é português",
        "save_failed": "Não foi possível guardar o idioma do menu",
        "lang_long": "usar {name} neste menu",
    },
    "ru": {
        "path": "Путь",
        "language_short": "язык",
        "language_long": "язык этого меню",
        "system_log_short": "системный журнал",
        "system_log_long": "просмотр, очистка и папка журнала",
        "self_short": "самоуправление",
        "self_long": "версия, о программе и цикл pip",
        "exit_short": "Выход",
        "exit_long": "выход",
        "back_short": "Назад",
        "back_long": "вернуться в главное меню",
        "view_long": "показать список файлов журнала и открыть один",
        "clear_long": "очистить один файл журнала",
        "folder_long": "показать папку журнала",
        "version_long": "показать установленную версию",
        "about_long": "версия и этот компьютер",
        "version_check_long": "сравнить эту установку с pip",
        "self_update_long": "обновить этот пакет через pip",
        "self_uninstall_long": "удалить этот пакет через pip",
        "self_install_long": "установить этот пакет через pip",
        "title_main": "главное меню",
        "title_language": "язык",
        "title_log": "системный журнал",
        "title_self": "самоуправление",
        "invalid": "Этого пункта нет в списке. Выберите номер из списка.",
        "saved": "Язык меню — русский",
        "save_failed": "Не удалось сохранить язык меню",
        "lang_long": "использовать {name} для этого меню",
    },
    "de": {
        "path": "Pfad",
        "language_short": "Sprache",
        "language_long": "Anzeigesprache für dieses Menü",
        "system_log_short": "Systemprotokoll",
        "system_log_long": "ansehen, leeren und der Protokollordner",
        "self_short": "Selbstverwaltung",
        "self_long": "Version, Info und pip-Lebenszyklus",
        "exit_short": "Beenden",
        "exit_long": "beenden",
        "back_short": "Zurück",
        "back_long": "zurück zum Hauptmenü",
        "client_short": "Client",
        "client_long": "Ordner dieser Anmeldung: packen und wiederherstellen",
        "sudoers_long": "Freigabe und Entwürfe",
        "backup_long": "Einen benannten Ordner als datiertes gzip unter /var/backup/PyBackup packen",
        "restore_long": "Ein Archiv zurück auf den Projektbaum der Festplatte legen",
        "submit_long": "Die JSON-Freigabe an die Freigabe-Warteschlange geben",
        "remove_long": "Nur den lokalen Freigabe-Entwurf entfernen",
        "band_front": "Server ist nicht verfügbar: dieses Programm startet keinen Host-Dienst. Nummer 2 bleibt reserviert.",
        "band_sudoers": "Testbefehle sind nicht verfügbar: geben Sie generate-sudoer-request, print-sudoers oder print-sudoers-install-script ein. Die Nummern 51, 53 und 54 bleiben reserviert.",
        "title_client": "Client",
        "title_sudoers": "sudoers",
        "help_work": "Arbeitsbefehle:",
        "help_grant": "Freigabe und Entwürfe (Tests und Prüfung):",
        "view_long": "eine Protokolldatei auflisten und anzeigen",
        "clear_long": "eine Protokolldatei leeren",
        "folder_long": "den Protokollordner anzeigen",
        "version_long": "die installierte Version anzeigen",
        "about_long": "Version und dieser Computer",
        "version_check_long": "diese Installation mit pip vergleichen",
        "self_update_long": "dieses Paket mit pip aktualisieren",
        "self_uninstall_long": "dieses Paket mit pip entfernen",
        "self_install_long": "dieses Paket mit pip installieren",
        "title_main": "Hauptmenü",
        "title_language": "Sprache",
        "title_log": "Systemprotokoll",
        "title_self": "Selbstverwaltung",
        "invalid": "Diese Wahl steht nicht auf der Liste. Wählen Sie eine angezeigte Nummer.",
        "saved": "Die Menüsprache ist Deutsch",
        "save_failed": "Die Menüsprache konnte nicht gespeichert werden",
        "lang_long": "{name} für dieses Menü verwenden",
    },
    "ja": {
        "path": "パス",
        "language_short": "言語",
        "language_long": "このメニューの表示言語",
        "system_log_short": "システムログ",
        "system_log_long": "表示、消去、ログフォルダ",
        "self_short": "自己管理",
        "self_long": "バージョン、概要、pip のライフサイクル",
        "exit_short": "終了",
        "exit_long": "終了",
        "back_short": "戻る",
        "back_long": "メインメニューに戻る",
        "client_short": "クライアント",
        "client_long": "このログインのフォルダ：まとめて戻す",
        "sudoers_long": "認可と下書き",
        "backup_long": "名前付きフォルダを日付付き gzip にして /var/backup/PyBackup に置く",
        "restore_long": "アーカイブをハードディスクのプロジェクトツリーに戻す",
        "submit_long": "JSON の認可を承認の待ち行列に渡す",
        "remove_long": "ローカルの認可下書きだけを消す",
        "band_front": "サーバーは使えません。このプログラムはホストのサービスを実行しません。番号 2 は予約です。",
        "band_sudoers": "テスト用のコマンドは使えません。generate-sudoer-request、print-sudoers、print-sudoers-install-script と入力します。番号 51、53、54 は予約です。",
        "title_client": "クライアント",
        "title_sudoers": "sudoers",
        "help_work": "作業コマンド:",
        "help_grant": "認可と下書き（試験と確認）:",
        "view_long": "ログファイルを一覧して表示する",
        "clear_long": "ログファイルを1つ空にする",
        "folder_long": "ログフォルダを表示する",
        "version_long": "インストール済みのバージョンを表示する",
        "about_long": "バージョンとこのコンピュータ",
        "version_check_long": "このインストールを pip と比較する",
        "self_update_long": "pip でこのパッケージを更新する",
        "self_uninstall_long": "pip でこのパッケージを削除する",
        "self_install_long": "pip でこのパッケージをインストールする",
        "title_main": "メインメニュー",
        "title_language": "言語",
        "title_log": "システムログ",
        "title_self": "自己管理",
        "invalid": "その選択は一覧にありません。表示された番号を選んでください。",
        "saved": "メニューの言語は日本語",
        "save_failed": "メニューの言語を保存できませんでした",
        "lang_long": "このメニューで{name}を使う",
    },
    "ko": {
        "path": "경로",
        "language_short": "언어",
        "language_long": "이 메뉴의 표시 언어",
        "system_log_short": "시스템 로그",
        "system_log_long": "보기, 비우기, 로그 폴더",
        "self_short": "자기관리",
        "self_long": "버전, 정보, pip 수명 주기",
        "exit_short": "종료",
        "exit_long": "종료",
        "back_short": "뒤로",
        "back_long": "주 메뉴로 돌아가기",
        "client_short": "클라이언트",
        "client_long": "이 로그인의 폴더: 묶고 되돌리기",
        "sudoers_long": "허가와 초안",
        "backup_long": "이름 있는 폴더를 날짜가 있는 gzip 으로 묶어 /var/backup/PyBackup 에 둡니다",
        "restore_long": "아카이브를 하드디스크의 프로젝트 트리에 되돌리기",
        "submit_long": "JSON 허가를 승인 대기열에 넘기기",
        "remove_long": "로컬 허가 초안만 지우기",
        "band_front": "서버는 사용할 수 없습니다. 이 프로그램은 호스트 서비스를 실행하지 않습니다. 번호 2는 예약입니다.",
        "band_sudoers": "테스트 명령은 사용할 수 없습니다. generate-sudoer-request, print-sudoers 또는 print-sudoers-install-script 를 입력하세요. 번호 51, 53, 54 는 예약입니다.",
        "title_client": "클라이언트",
        "title_sudoers": "sudoers",
        "help_work": "작업 명령:",
        "help_grant": "허가와 초안 (시험과 검토):",
        "view_long": "로그 파일을 나열하고 표시합니다",
        "clear_long": "로그 파일 하나를 비웁니다",
        "folder_long": "로그 폴더를 표시합니다",
        "version_long": "설치된 버전을 표시합니다",
        "about_long": "버전과 이 컴퓨터",
        "version_check_long": "이 설치를 pip과 비교합니다",
        "self_update_long": "pip으로 이 패키지를 업그레이드합니다",
        "self_uninstall_long": "pip으로 이 패키지를 제거합니다",
        "self_install_long": "pip으로 이 패키지를 설치합니다",
        "title_main": "주 메뉴",
        "title_language": "언어",
        "title_log": "시스템 로그",
        "title_self": "자기관리",
        "invalid": "그 선택은 목록에 없습니다. 표시된 번호를 고르세요.",
        "saved": "메뉴 언어는 한국어",
        "save_failed": "메뉴 언어를 저장하지 못했습니다",
        "lang_long": "이 메뉴에서 {name} 사용",
    },
    "nl": {
        "path": "Pad",
        "language_short": "taal",
        "language_long": "weergavetaal voor dit menu",
        "system_log_short": "systeemlog",
        "system_log_long": "bekijken, legen en de logmap",
        "self_short": "zelfbeheer",
        "self_long": "versie, info en de pip-levenscyclus",
        "exit_short": "Afsluiten",
        "exit_long": "afsluiten",
        "back_short": "Terug",
        "back_long": "terug naar het hoofdmenu",
        "view_long": "een logbestand tonen en weergeven",
        "clear_long": "één logbestand legen",
        "folder_long": "de logmap tonen",
        "version_long": "de geïnstalleerde versie tonen",
        "about_long": "versie en deze computer",
        "version_check_long": "deze installatie met pip vergelijken",
        "self_update_long": "dit pakket met pip bijwerken",
        "self_uninstall_long": "dit pakket met pip verwijderen",
        "self_install_long": "dit pakket met pip installeren",
        "title_main": "hoofdmenu",
        "title_language": "taal",
        "title_log": "systeemlog",
        "title_self": "zelfbeheer",
        "invalid": "Die keuze staat niet op de lijst. Kies een nummer van de lijst.",
        "saved": "De menutaal is Nederlands",
        "save_failed": "De menutaal kon niet worden opgeslagen",
        "lang_long": "{name} voor dit menu gebruiken",
    },
    "el": {
        "path": "Διαδρομή",
        "language_short": "γλώσσα",
        "language_long": "γλώσσα εμφάνισης για αυτό το μενού",
        "system_log_short": "αρχείο καταγραφής",
        "system_log_long": "προβολή, εκκαθάριση και ο φάκελος καταγραφής",
        "self_short": "αυτοδιαχείριση",
        "self_long": "έκδοση, σχετικά και ο κύκλος του pip",
        "exit_short": "Έξοδος",
        "exit_long": "έξοδος",
        "back_short": "Πίσω",
        "back_long": "επιστροφή στο κύριο μενού",
        "view_long": "λίστα αρχείων καταγραφής και εμφάνιση",
        "clear_long": "εκκένωση ενός αρχείου καταγραφής",
        "folder_long": "εμφάνιση του φακέλου καταγραφής",
        "version_long": "εμφάνιση της εγκατεστημένης έκδοσης",
        "about_long": "έκδοση και αυτός ο υπολογιστής",
        "version_check_long": "σύγκριση αυτής της εγκατάστασης με το pip",
        "self_update_long": "αναβάθμιση αυτού του πακέτου με το pip",
        "self_uninstall_long": "αφαίρεση αυτού του πακέτου με το pip",
        "self_install_long": "εγκατάσταση αυτού του πακέτου με το pip",
        "title_main": "κύριο μενού",
        "title_language": "γλώσσα",
        "title_log": "αρχείο καταγραφής",
        "title_self": "αυτοδιαχείριση",
        "invalid": "Αυτή η επιλογή δεν είναι στη λίστα. Διάλεξε έναν αριθμό της λίστας.",
        "saved": "Η γλώσσα του μενού είναι ελληνικά",
        "save_failed": "Δεν ήταν δυνατή η αποθήκευση της γλώσσας του μενού",
        "lang_long": "χρήση της {name} για αυτό το μενού",
    },
}
