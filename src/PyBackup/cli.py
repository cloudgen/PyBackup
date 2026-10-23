#!/usr/bin/env python
# =============================================================================
# PyBackup CLI — HelloTui text menu plus folder backup.
# Law keys: requirement-python-cli-interface, requirement-python-cli-default-interaction,
#           requirement-python-cli-logging, requirement-python-tui, requirement-python-oop,
#           requirement-python-about, requirement-domain-folder-backup,
#           requirement-folder-archive-backup, requirement-python-error-handling,
#           requirement-sudoer-json-file
# Specialized from HelloTui. HelloTui itself is not modified.
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# def main writes ChronicleLogger(...). This module does not construct it
# at import time and does not re-export it.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import sys

from .about_page import AboutPage
from .archive import Settings, backup, restore
from .check_system import CheckSystem
from .self_management import SelfManage
from .storage import DomainError
from .sudoers import (
    generate,
    print_install_script,
    print_sudoers,
    remove_draft,
    submit,
)
from .tui import Tui


class Cli:
    """Parser, dispatch, verbs, and the tty gate. One class in this file.

    Identity, verb lists, and suffix sets are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    HelloTui pip lifecycle, about, language, and system-log stay on this class.
    """

    from . import __version__ as VERSION

    APP_NAME = "PyBackup"
    CONSOLE_NAME = "py-backup"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "backup",
        "restore",
        "remove-project-sudoers",
        "submit-sudoer-request",
        "print-sudoers",
        "print-sudoers-install-script",
        "generate-sudoer-request",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    WORK_VERBS = (
        "backup",
        "restore",
        "remove-project-sudoers",
        "submit-sudoer-request",
    )
    TEST_VERBS = (
        "print-sudoers",
        "print-sudoers-install-script",
        "generate-sudoer-request",
    )
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    FORCE_VERBS = ("self-uninstall", "restore", "remove-project-sudoers")
    AUTHOR_NAME = "cloudgen"
    AUTHOR_EMAIL = "wongcf22@gmail.com"
    HOMEPAGE = "https://github.com/cloudgen/PyBackup"
    LAST_UPDATE = "2026-10-22"
    DOWNLOAD_URL = ""
    BASIC_USAGE = "py-backup backup <source-folder>"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli.VERSION
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli.VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli.VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.tui = Tui(self, logger=logger)

    def settings(self, json_out=False):
        found = Settings(version=Cli.VERSION)
        found.json = json_out
        return found

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, backup, restore, the grant verbs, and the pip verbs
        do not draw the screen. Empty argv and about do, when stdout is a terminal.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdout_is_tty():
            return False
        verb = None
        for token in argv:
            if token.startswith("-"):
                continue
            if verb is None:
                verb = token
                continue
            return False
        if verb == "about":
            return True
        return verb is None

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def help_text(self):
        """Work commands, then grant-emit testers, then the pip lifecycle.

        English headings stay exact. The saved menu language translates those
        two headings and keeps the split. Command tokens stay Latin.
        requirement-domain-folder-backup pillar C.
        """
        from .menu_language import MenuLanguage

        language = MenuLanguage()
        work = language.text("help_work")
        grant = language.text("help_grant")
        return (
            "{0} — pack a folder into a dated gzip archive and restore it.\n"
            "With no arguments on a terminal, opens the text menu.\n"
            "With no arguments and no terminal, prints this help and stops.\n"
            "\n"
            "{1}\n"
            "  backup <source-folder>\n"
            "      Create tar.gz, deposit under the backup notation, verify counts.\n"
            "  restore <archive|prefix> [dest]\n"
            "      Restore an archive. Default dest is the hard-disk projects tree.\n"
            "      Flags: --force --disk --ram\n"
            "  remove-project-sudoers [path]\n"
            "      Delete the local grant draft only. Not /etc. --force skips the question.\n"
            "  submit-sudoer-request [file]\n"
            "      Queue a JSON grant via sudoer-cli. Default action is update when\n"
            "      this user's host fragment exists, otherwise add. No /etc write.\n"
            "      No inbound mkdir.\n"
            "\n"
            "{2}\n"
            "  print-sudoers [path]\n"
            "      Emit the project-sudoers-file draft. Does not write /etc.\n"
            "  print-sudoers-install-script [path]\n"
            "      Write an admin script for install, uninstall, replace, and status.\n"
            "  generate-sudoer-request [path]\n"
            "      Write a compact JSON grant this login can read.\n"
            "      Flags: --add --update --allow-test-local\n"
            "\n"
            "These three test commands are not on a numbered row.\n"
            "Numbers 51, 53, and 54 stay reserved. sudoers is not a typed command.\n"
            "\n"
            "Environment: BACKUP_ROOT, BACKUP_NOTATION, PROJECTS_ROOT, RAM_ROOT,\n"
            "RESTORE_HOST_DEFAULT, MAX_DAILY_BACKUPS, MAX_TOTAL_BACKUPS.\n"
            "Archive as this login. Deposit and a root-owned restore need an\n"
            "allowlisted sudo after an admin installs the fragment.\n"
            "\n"
            "Self-management (pip, not a downloaded shell script):\n"
            "  version-check    python -m pip index versions {0}\n"
            "  self-update      python -m pip install --upgrade {0}\n"
            "  self-install     python -m pip install {0}\n"
            "  self-uninstall   python -m pip uninstall -y {0}   (needs --force)\n"
            "Empty arguments do not install or update.\n"
            "\n"
            "Examples:\n"
            "  py-backup\n"
            "  py-backup backup /path/to/project\n"
            "  py-backup generate-sudoer-request --allow-test-local\n"
            "  py-backup submit-sudoer-request ~/.config/PyBackup/sudoer-request-$USER.json\n"
            "  py-backup print-sudoers-install-script --allow-test-local\n"
        ).format(Cli.APP_NAME, work, grant)

    def build_parser(self):
        """One product verb plus the operands that verb needs."""
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.help_text(),
        )
        parser.add_argument("verb", nargs="?", default=None, metavar="verb")
        parser.add_argument("operands", nargs="*", metavar="operand")
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(Cli.APP_NAME, Cli.VERSION),
        )
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--json", action="store_true")
        parser.add_argument("--disk", action="store_true")
        parser.add_argument("--ram", action="store_true")
        parser.add_argument("--add", action="store_true")
        parser.add_argument("--update", action="store_true")
        parser.add_argument("--allow-test-local", action="store_true")
        parser.add_argument("--purpose", default="")
        return parser

    def _page(self, text):
        print(text)
        return 0

    def _unknown_verb(self, token):
        names = ", ".join(Cli.PRODUCT_VERBS)
        return self.report_error(
            "Unknown verb '{0}'.".format(token),
            "{0} help — verbs: {1}".format(Cli.CONSOLE_NAME, names),
        )

    def _domain(self, func, *args, **kwargs):
        try:
            return self._page(func(*args, **kwargs))
        except DomainError as exc:
            return self.report_error(exc.message, exc.nxt)

    def _action_flag(self, args):
        if args.add and args.update:
            return self.report_error(
                "--add and --update cannot both be set.",
                "{0} generate-sudoer-request --add".format(Cli.CONSOLE_NAME),
            )
        if args.add:
            return "add"
        if args.update:
            return "update"
        return ""

    def _ask(self, tui, screen, model, title, lines):
        if screen is None or model is None:
            return None
        text = tui.read_key(screen, model, lines, title=title)
        if text is None:
            return None
        return text.strip()

    def run_menu_kind(self, kind, tui, screen, model):
        """A numbered row or a typed token on the open screen."""
        try:
            settings = self.settings(False)
            if kind == "backup":
                source = self._ask(tui, screen, model, "backup", ["Folder to pack:"])
                if not source:
                    return None
                return backup(source, settings)
            if kind == "restore":
                spec = self._ask(tui, screen, model, "restore", ["Archive or project prefix:"])
                if not spec:
                    return None
                dest = self._ask(
                    tui, screen, model, "restore",
                    ["Destination (empty uses the hard-disk projects tree):"],
                )
                if dest is None:
                    return None
                return restore(spec, dest, settings, force=False)
            if kind == "generate-sudoer-request":
                dest = self._ask(
                    tui, screen, model, "generate-sudoer-request",
                    ["JSON path (empty uses ~/.config/PyBackup):"],
                )
                if dest is None:
                    return None
                return generate(settings, dest)
            if kind == "print-sudoers":
                dest = self._ask(
                    tui, screen, model, "print-sudoers",
                    ["Draft path (empty uses ~/.config/PyBackup):"],
                )
                if dest is None:
                    return None
                return print_sudoers(settings, dest)
            if kind == "print-sudoers-install-script":
                return print_install_script(settings)
            if kind == "submit-sudoer-request":
                src = self._ask(
                    tui, screen, model, "submit-sudoer-request",
                    ["JSON file (empty writes a fresh grant):"],
                )
                if src is None:
                    return None
                return submit(settings, src)
            if kind == "remove-project-sudoers":
                path = self._ask(
                    tui, screen, model, "remove-project-sudoers",
                    ["Draft path (empty removes the only draft):"],
                )
                if path is None:
                    return None
                answer = self._ask(
                    tui, screen, model, "remove-project-sudoers",
                    ["Remove the local draft? (y/n)"],
                )
                return remove_draft(path, force=False, confirm=(answer or "").lower() in ("y", "yes"))
            return None
        except DomainError as exc:
            return "ERROR: {0}\nNext: {1}".format(exc.message, exc.nxt)

    def _dispatch(self, args):
        """One product verb, the front board, or a fail-closed stop."""
        verb = args.verb
        if args.force and verb not in Cli.FORCE_VERBS:
            return self.report_error(
                "--force is only for self-uninstall, restore, and remove-project-sudoers.",
                "{0} help".format(Cli.CONSOLE_NAME),
            )
        if args.disk and args.ram:
            return self.report_error(
                "--disk and --ram cannot both be set.",
                "{0} restore <archive> --disk".format(Cli.CONSOLE_NAME),
            )
        action = self._action_flag(args)
        if isinstance(action, int):
            return action
        if verb == "about":
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "version":
            return self._page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not args.force:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
                )
            return self.self_manage.emit(verb)
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb)
        settings = self.settings(args.json)
        ops = list(args.operands)
        if verb == "backup":
            if not ops:
                if not self.stdout_is_tty():
                    return self.report_error(
                        "backup needs a source folder.",
                        "{0} backup <source-folder>".format(Cli.CONSOLE_NAME),
                    )
                asked = self.tui.ask_lines("backup", ["Folder to pack:"])
                if asked is None or not str(asked).strip():
                    return 1
                ops = [str(asked).strip()]
            return self._domain(backup, ops[0], settings)
        if verb == "restore":
            if not ops and self.stdout_is_tty():
                asked = self.tui.ask_lines("restore", ["Archive or project prefix:"])
                if asked is None or not str(asked).strip():
                    return 1
                ops = [str(asked).strip()]
            spec = ops[0] if ops else ""
            dest = ops[1] if len(ops) > 1 else ""
            host = "ram-drive" if args.ram else ("hard-disk" if args.disk else "")
            return self._domain(restore, spec, dest, settings, args.force, host)
        if verb == "generate-sudoer-request":
            dest = ops[0] if ops else ""
            return self._domain(
                generate, settings, dest, action, args.allow_test_local, args.purpose,
            )
        if verb == "print-sudoers":
            dest = ops[0] if ops else ""
            return self._domain(print_sudoers, settings, dest, args.allow_test_local)
        if verb == "print-sudoers-install-script":
            dest = ops[0] if ops else ""
            return self._domain(print_install_script, settings, dest, args.allow_test_local)
        if verb == "submit-sudoer-request":
            src = ops[0] if ops else ""
            return self._domain(
                submit, settings, src, action, args.allow_test_local, args.purpose,
            )
        if verb == "remove-project-sudoers":
            path = ops[0] if ops else ""
            return self._domain(remove_draft, path, args.force, False)
        if verb == "sudoers":
            return self.report_error(
                "sudoers is a menu, not a command.",
                "{0}".format(Cli.CONSOLE_NAME),
            )
        if verb is not None:
            return self._unknown_verb(verb)
        if not self.stdout_is_tty():
            self.build_parser().print_help()
            return 0
        opened = self.tui.open_text_menu()
        if opened == "missing":
            return 1
        return 0

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        parser = self.build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            code = exc.code
            if code is None or code == 0:
                return 0
            return int(code)
        if args.verb == "help":
            parser.print_help()
            return 0
        return self._dispatch(args)


def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    from PyBackup import __version__

    screen = Cli.opens_text_screen(argv)
    logger = ChronicleLogger(
        logname=Cli.APP_NAME,
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())
