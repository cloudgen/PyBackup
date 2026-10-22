# PyBackup proof.
# HelloTui features that must stay: path label, clock, wide columns, thirteen
# languages, system-log 31-33, language 41-53, self-management 82-87, Exit 9,
# pip argv, about page shape, empty argv help off a terminal.
# Folder-backup features: backup, restore, retention, dest guard, four-command
# JSON grant, submit without mkdir, menu rows 1 and 5.
import json
import os
import stat
import subprocess
import tempfile
import unittest
from datetime import datetime

from PyBackup.archive import (
    Settings,
    apply_retention,
    backup,
    count_tree,
    refuse_restore_dest,
    restore,
)
from PyBackup.cli import Cli
from PyBackup.menu_language import MenuLanguage
from PyBackup.menu_painter import MenuPainter
from PyBackup.self_management import SelfManage
from PyBackup.storage import DomainError
from PyBackup.sudoers import generate, print_sudoers, remove_draft, submit
from PyBackup.tui import Tui


def _settings(root):
    os.environ["BACKUP_ROOT"] = root
    os.environ["BACKUP_NOTATION"] = "PyBackup"
    os.environ["MAX_DAILY_BACKUPS"] = "5"
    os.environ["MAX_TOTAL_BACKUPS"] = "30"
    return Settings(version="1.0.0")


class TestHelloTuiFeatures(unittest.TestCase):
    """Features copied from HelloTui and left in place."""

    def test_front_keeps_hellotui_rows_and_adds_backup_menu(self):
        painter = MenuPainter(home=tempfile.mkdtemp(prefix="pbhome_"))
        rows = painter.display_rows("front")
        numbers = [row[0] for row in rows]
        kinds = [row[3] for row in rows]
        self.assertEqual(numbers, [1, 3, 4, 5, 8, 9])
        self.assertEqual(
            kinds,
            ["client-side", "system-log", "language", "sudoers", "self-management", "exit"],
        )
        self.assertNotIn(2, numbers)
        self.assertNotIn("hello", kinds)

    def test_system_log_language_and_self_numbers_unchanged(self):
        painter = MenuPainter(home=tempfile.mkdtemp(prefix="pbhome_"))
        self.assertEqual([row[0] for row in painter.display_rows("log")], [31, 32, 33, 0])
        self.assertEqual(
            [row[3] for row in painter.display_rows("log")],
            ["view-log", "clear-log", "log-folder", "back"],
        )
        self.assertEqual([row[0] for row in painter.display_rows("self")], [82, 83, 84, 85, 86, 87, 0])
        lang = painter.display_rows("lang")
        self.assertEqual(lang[0][0], 41)
        self.assertEqual(lang[-2][0], 53)
        self.assertEqual(lang[-1][3], "back")
        self.assertEqual(len(MenuLanguage.CODES), 13)

    def test_client_and_sudoers_boards(self):
        painter = MenuPainter(home=tempfile.mkdtemp(prefix="pbhome_"))
        client = painter.display_rows("client")
        sudo = painter.display_rows("sudoers")
        self.assertEqual([row[0] for row in client], [11, 12, 0])
        self.assertEqual([row[3] for row in client], ["backup", "restore", "back"])
        self.assertEqual([row[0] for row in sudo], [52, 55, 0])
        self.assertNotIn(51, [row[0] for row in sudo])
        self.assertNotIn(53, [row[0] for row in sudo])
        self.assertNotIn(54, [row[0] for row in sudo])
        front = painter.unavailable_sentences("front")[0]
        self.assertIn("server-side is not available", front)
        self.assertIn("Number 2 stays reserved", front)
        hidden = painter.unavailable_sentences("sudoers")[0]
        self.assertEqual(
            hidden,
            "test commands are not available: type generate-sudoer-request, "
            "print-sudoers, or print-sudoers-install-script. "
            "Numbers 51, 53, and 54 stay reserved.",
        )
        self.assertEqual(
            front,
            "server-side is not available: this program does not run a host service. "
            "Number 2 stays reserved.",
        )
        client_explain = client[0][2]
        self.assertIn("/var/backup/PyBackup", client_explain)
        self.assertIsNone(painter.language.token_kind("hello", "front"))

    def test_shell_languages_keep_hellotui_rows_and_translate_the_band(self):
        os.environ["PYBACKUP_LANG"] = "zh-Hant"
        try:
            painter = MenuPainter(home=tempfile.mkdtemp(prefix="pbhome_"))
            front = painter.display_rows("front")
            self.assertEqual(front[0][1], "用戶端")
            self.assertEqual(front[1][1], "系統日誌")
            self.assertEqual(front[4][2], "版本、關於，以及 pip 生命週期")
            self.assertEqual(front[3][2], "授權與草稿")
            update = [row for row in painter.display_rows("self") if row[3] == "self-update"][0]
            self.assertEqual(update[2], "用 pip 升級此套件")
            self.assertIn("伺服器端無法使用", painter.unavailable_sentences("front")[0])
            self.assertIn("編號 2 保留", painter.unavailable_sentences("front")[0])
            self.assertIn("51", painter.unavailable_sentences("sudoers")[0])
            self.assertEqual(painter.display_rows("client")[0][1], "backup")
            app = Cli()
            text = app.help_text()
            self.assertIn("工作指令：", text)
            self.assertIn("授權與草稿設定（測試與檢視）：", text)
            self.assertLess(text.index("工作指令："), text.index("授權與草稿設定"))
            self.assertIn("backup <source-folder>", text)
        finally:
            os.environ.pop("PYBACKUP_LANG", None)

    def test_path_label_clock_and_wide_columns(self):
        self.assertEqual(MenuPainter.PATH_LABEL_EN, "Path")
        self.assertEqual(MenuPainter.PATH_LABEL_ZH_HANT, "路徑")
        self.assertEqual(MenuPainter.FRAME_TOP_LEFT, "╭")
        self.assertEqual(MenuPainter.CARET_BLOCK, "█")
        self.assertEqual(MenuPainter.display_width("路徑"), 4)
        self.assertEqual(MenuPainter.display_width("╭─╮"), 3)
        home = tempfile.mkdtemp(prefix="pbhome_")
        os.environ.pop("PYBACKUP_LANG", None)
        painter = MenuPainter(home=home)
        painter.clock_text = lambda: "14:05:09"
        line = painter.path_line()
        self.assertTrue(line.startswith("Path: "))
        self.assertTrue(line.endswith("14:05:09"))
        self.assertNotIn("路徑", line)
        session = Tui()
        session.painter = MenuPainter(home=home)
        session.painter.clock_text = lambda: "14:05:09"
        for text in (
            session.front_lines()[0],
            session.self_lines()[0],
            session.log_lines()[0],
            session.language_lines()[0],
            session.client_lines()[0],
            session.sudoers_lines()[0],
        ):
            self.assertTrue(text.startswith("Path: "), text)
            self.assertTrue(text.endswith("14:05:09"), text)

    def test_language_env_does_not_write_the_leaf(self):
        home = tempfile.mkdtemp(prefix="pbhome_")
        os.environ["HOME"] = home
        os.environ["PYBACKUP_LANG"] = "zh-Hant"
        language = MenuLanguage(home=home)
        self.assertEqual(language.code(), "zh-Hant")
        self.assertEqual(language.path_label(), "路徑")
        self.assertFalse(os.path.exists(language.leaf_path()))
        os.environ.pop("PYBACKUP_LANG", None)

    def test_pip_lifecycle_unchanged(self):
        tool = SelfManage("PyBackup", "1.0.0")
        self.assertEqual(tool.argv_for("self-update")[-3:], ["install", "--upgrade", "PyBackup"])
        self.assertEqual(tool.argv_for("self-install")[1:4], ["-m", "pip", "install"])
        self.assertNotIn("curl", tool.argv_for("version-check"))
        self.assertNotIn("sudo", tool.argv_for("self-uninstall"))

    def test_empty_argv_off_a_terminal_is_help(self):
        self.assertIn("backup", Cli.PRODUCT_VERBS)
        self.assertNotIn("hello", Cli.PRODUCT_VERBS)
        self.assertNotIn("sudoers", Cli.PRODUCT_VERBS)
        original = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: False)
        try:
            self.assertFalse(Cli.opens_text_screen(["backup", "/tmp"]))
            self.assertFalse(Cli.opens_text_screen(["self-update"]))
            self.assertFalse(Cli.opens_text_screen([]))
            app = Cli()
            code = app.run([])
            self.assertEqual(code, 0)
        finally:
            Cli.stdout_is_tty = original

    def test_help_splits_work_and_grant_emit(self):
        os.environ["PYBACKUP_LANG"] = "en"
        app = Cli()
        text = app.help_text()
        os.environ.pop("PYBACKUP_LANG", None)
        self.assertIn("Work commands:", text)
        self.assertIn("Grant and draft setup (tests and review):", text)
        self.assertLess(text.index("Work commands:"), text.index("Grant and draft setup"))
        self.assertIn("backup <source-folder>", text)
        self.assertIn("generate-sudoer-request", text)

    def test_unknown_and_force_and_sudoers_word(self):
        app = Cli()
        self.assertEqual(app.run(["no-such-verb"]), 1)
        self.assertEqual(app.run(["self-uninstall"]), 1)
        self.assertEqual(app.run(["sudoers"]), 1)
        self.assertEqual(app.run(["version"]), 0)


class TestBackup(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="pbak_")
        self.root = tempfile.mkdtemp(prefix="pbroot_")
        self._env = {
            name: os.environ.get(name)
            for name in (
                "HOME", "BACKUP_ROOT", "BACKUP_NOTATION", "PROJECTS_ROOT",
                "MAX_DAILY_BACKUPS", "MAX_TOTAL_BACKUPS", "TERMUX_VERSION",
                "PREFIX", "MSYSTEM",
            )
        }
        os.environ["HOME"] = self.home
        os.environ.pop("TERMUX_VERSION", None)
        os.environ.pop("MSYSTEM", None)
        os.environ["PREFIX"] = "/usr"
        self.settings = _settings(self.root)

    def tearDown(self):
        for name, value in self._env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def _source(self):
        folder = os.path.join(self.home, "alpha")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "note.txt"), "w", encoding="utf-8") as handle:
            handle.write("hello\n")
        link = os.path.join(folder, "link.txt")
        if not os.path.lexists(link):
            os.symlink("note.txt", link)
        return folder

    def test_symlink_is_not_a_regular_file(self):
        folder = self._source()
        entries, files = count_tree(folder)
        self.assertEqual(files, 1)
        self.assertGreater(entries, files)

    def test_backup_names_verifies_and_does_not_keep_the_stage(self):
        folder = self._source()
        text = backup(folder, self.settings)
        self.assertIn("Backup complete:", text)
        self.assertIn("archive_files=1", text)
        day = datetime.now().strftime("%Y%m%d")
        dest = os.path.join(self.root, "PyBackup", "alpha-{0}-1.tar.gz".format(day))
        self.assertTrue(os.path.isfile(dest))
        self.assertEqual(stat.S_IMODE(os.stat(dest).st_mode), 0o640)
        self.assertIn("mode=", text)

    def test_second_archive_does_not_overwrite(self):
        folder = self._source()
        backup(folder, self.settings)
        backup(folder, self.settings)
        day = datetime.now().strftime("%Y%m%d")
        dep = os.path.join(self.root, "PyBackup")
        self.assertTrue(os.path.isfile(os.path.join(dep, "alpha-{0}-1.tar.gz".format(day))))
        self.assertTrue(os.path.isfile(os.path.join(dep, "alpha-{0}-2.tar.gz".format(day))))

    def test_daily_retention_keeps_five(self):
        dep = os.path.join(self.root, "PyBackup")
        os.makedirs(dep)
        day = "20261022"
        for n in range(1, 7):
            path = os.path.join(dep, "alpha-{0}-{1}.tar.gz".format(day, n))
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("x")
        result = apply_retention("alpha", dep, day, self.settings)
        left = sorted(os.listdir(dep))
        self.assertEqual(len(left), 5)
        self.assertNotIn("alpha-20261022-1.tar.gz", left)
        self.assertEqual(result["daily_removed"], 1)

    def test_total_retention_keeps_thirty(self):
        dep = os.path.join(self.root, "PyBackup")
        os.makedirs(dep)
        for n in range(1, 32):
            path = os.path.join(dep, "alpha-20261001-{0}.tar.gz".format(n))
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("x")
        result = apply_retention("alpha", dep, "20261022", self.settings)
        self.assertEqual(len(os.listdir(dep)), 30)
        self.assertEqual(result["total_removed"], 1)
        self.assertFalse(os.path.exists(os.path.join(dep, "alpha-20261001-1.tar.gz")))

    def test_restore_round_trip_and_refuse_passwd(self):
        folder = self._source()
        backup(folder, self.settings)
        day = datetime.now().strftime("%Y%m%d")
        dest = os.path.join(self.home, "out", "alpha")
        text = restore(
            "alpha-{0}-1.tar.gz".format(day),
            dest,
            self.settings,
            force=False,
        )
        self.assertIn("Restore complete:", text)
        self.assertTrue(os.path.isfile(os.path.join(dest, "note.txt")))
        self.assertTrue(os.path.islink(os.path.join(dest, "link.txt")))
        with self.assertRaises(DomainError):
            refuse_restore_dest("/etc/passwd", self.settings)
        with self.assertRaises(DomainError):
            restore("alpha", "/etc/passwd", self.settings, force=True)

    def test_nonempty_restore_needs_force(self):
        folder = self._source()
        backup(folder, self.settings)
        dest = os.path.join(self.home, "busy")
        os.makedirs(dest)
        with open(os.path.join(dest, "keep.txt"), "w", encoding="utf-8") as handle:
            handle.write("stay\n")
        with self.assertRaises(DomainError) as caught:
            restore("alpha", dest, self.settings, force=False)
        self.assertIn("not empty", caught.exception.message)

    def test_missing_source_and_termux_fail_closed(self):
        with self.assertRaises(DomainError):
            backup(os.path.join(self.home, "missing"), self.settings)
        os.environ["TERMUX_VERSION"] = "0.118"
        with self.assertRaises(DomainError) as caught:
            backup(self._source(), self.settings)
        self.assertIn("does not wrap sudo", caught.exception.message)
        os.environ.pop("TERMUX_VERSION", None)
        os.environ["MSYSTEM"] = "MINGW64"
        with self.assertRaises(DomainError) as caught:
            backup(self._source(), self.settings)
        self.assertIn("does not wrap sudo", caught.exception.message)

    def test_cli_backup(self):
        folder = self._source()
        app = Cli()
        code = app.run(["backup", folder])
        self.assertEqual(code, 0)
        original = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: False)
        try:
            code = app.run(["backup"])
            self.assertEqual(code, 1)
        finally:
            Cli.stdout_is_tty = original


class TestSudoers(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="psudo_")
        self._env = {
            name: os.environ.get(name)
            for name in (
                "HOME", "GLOBAL_BIN", "SUDOER_CLI", "SUDOER_ADM_USER",
                "SUDOER_QUEUE_INBOUND", "SUDOER_PUBLIC_ROOT",
            )
        }
        os.environ["HOME"] = self.home
        os.environ["GLOBAL_BIN"] = os.path.join(self.home, "global-bin")
        os.makedirs(os.environ["GLOBAL_BIN"])
        self.settings = Settings(version="1.0.0")

    def tearDown(self):
        for name, value in self._env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def test_generate_has_four_commands_and_refuses_etc(self):
        text = generate(self.settings, allow_test=True)
        self.assertIn("Wrote verified sudoer file", text)
        path = os.path.join(self.home, ".config", "PyBackup", "sudoer-request-{0}.json".format(os.environ.get("USER") or "unknown"))
        # login_name may differ from USER. Find the file.
        folder = os.path.join(self.home, ".config", "PyBackup")
        names = os.listdir(folder)
        self.assertEqual(len(names), 1)
        with open(os.path.join(folder, names[0]), encoding="utf-8") as handle:
            body = json.loads(handle.read())
        args = [item["args"] for item in body["commands"]]
        self.assertEqual(args, [
            ["backup", "*"],
            ["restore", "*"],
            ["--json", "backup", "*"],
            ["--json", "restore", "*"],
        ])
        self.assertTrue(body["commands"][0]["path"].endswith("/py-backup"))
        self.assertNotIn("/bin/tar", json.dumps(body))
        with self.assertRaises(DomainError):
            generate(self.settings, dest="/etc/PyBackup.json", allow_test=True)
        with self.assertRaises(DomainError):
            generate(self.settings, dest="/var/sudoer-cli/sudoer-request/x.json", allow_test=True)

    def test_print_sudoers_does_not_touch_etc(self):
        text = print_sudoers(self.settings, allow_test=True)
        self.assertIn("did not write /etc", text)
        folder = os.path.join(self.home, ".config", "PyBackup")
        with open(os.path.join(folder, os.listdir(folder)[0]), encoding="utf-8") as handle:
            fragment = handle.read()
        self.assertIn("backup *", fragment)
        self.assertIn("--json restore *", fragment)
        self.assertFalse(os.path.exists("/etc/sudoers.d/PyBackup-test-should-not-exist"))

    def test_remove_draft_refuses_etc(self):
        folder = os.path.join(self.home, ".config", "PyBackup")
        os.makedirs(folder)
        path = os.path.join(folder, "sudoers.fragment-me")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("draft\n")
        text = remove_draft(path, force=True, confirm=False)
        self.assertIn("Removed", text)
        self.assertFalse(os.path.exists(path))
        with self.assertRaises(DomainError):
            remove_draft("/etc/sudoers.d/PyBackup-me", force=True, confirm=True)

    def test_submit_does_not_create_inbound(self):
        inbound = os.path.join(self.home, "inbound")
        os.environ["SUDOER_QUEUE_INBOUND"] = inbound
        os.environ["SUDOER_PUBLIC_ROOT"] = os.path.join(self.home, "no-public")
        os.environ["SUDOER_ADM_USER"] = subprocess.check_output(["id", "-un"], text=True).strip()
        generate(self.settings, allow_test=True)
        folder = os.path.join(self.home, ".config", "PyBackup")
        src = os.path.join(folder, os.listdir(folder)[0])
        stub = os.path.join(self.home, "sudoer-cli")
        with open(stub, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\necho fail\nexit 1\n")
        os.chmod(stub, 0o755)
        os.environ["SUDOER_CLI"] = stub
        with self.assertRaises(DomainError) as caught:
            submit(self.settings, src)
        self.assertIn("not found", caught.exception.message)
        self.assertFalse(os.path.isdir(inbound))

    def test_submit_queues_when_inbound_exists(self):
        inbound = os.path.join(self.home, "inbound")
        os.makedirs(inbound, mode=0o755)
        os.environ["SUDOER_QUEUE_INBOUND"] = inbound
        os.environ["SUDOER_ADM_USER"] = subprocess.check_output(["id", "-un"], text=True).strip()
        generate(self.settings, allow_test=True)
        folder = os.path.join(self.home, ".config", "PyBackup")
        src = os.path.join(folder, [name for name in os.listdir(folder) if name.endswith(".json")][0])
        stub = os.path.join(self.home, "sudoer-cli")
        script = """#!/bin/sh
file=""
while [ $# -gt 0 ]; do
  if [ "$1" = "--file" ]; then shift; file=$1; fi
  shift
done
cp "$file" "{inbound}/req-1.json"
printf '%s\\n' '{{"request_id":"req-1.json"}}'
""".format(inbound=inbound)
        with open(stub, "w", encoding="utf-8") as handle:
            handle.write(script)
        os.chmod(stub, 0o755)
        os.environ["SUDOER_CLI"] = stub
        text = submit(self.settings, src)
        self.assertIn("Submitted", text)
        self.assertIn("request_id=req-1.json", text)
        with open(os.path.join(inbound, "req-1.json"), encoding="utf-8") as handle:
            queued = json.loads(handle.read())
        self.assertEqual(len(queued["commands"]), 4)
        self.assertIn("did not write /etc", text)


if __name__ == "__main__":
    unittest.main()
