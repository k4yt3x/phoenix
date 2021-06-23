#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Phoenix
Creator: K4YT3X
Date Created: June 22, 2021
Last Modified: June 22, 2021

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018-2021 K4YT3X
"""

# built-in imports
# readline is needed for cmd
import cmd
import importlib
import pathlib
import readline
import sys

# third-party imports
from colorama import Fore, Style
from loguru import logger
from rich.console import Console
from rich.table import Table
import colorama


class PhoenixShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.module = None
        self.prompt = "{}phoenix{} > ".format(Fore.YELLOW, Style.RESET_ALL)

    def do_select(self, arg):
        "select a module: select exploit/cve-2019-0193"
        args = arg.split()
        module_path = pathlib.Path.cwd() / "modules" / (args[0] + ".py")
        relative_path = module_path.relative_to(pathlib.Path.cwd() / "modules")

        # check if module exists
        if not module_path.is_file():
            logger.error("the specified module does not exist")
            return

        spec = importlib.util.spec_from_file_location("module.name", str(module_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.module = module.Module(logger)
        logger.success("Successfully loaded {}".format(relative_path))
        self.prompt = "{}phoenix{} [{}{}{}] > ".format(
            Fore.YELLOW, Style.RESET_ALL, Fore.RED, relative_path, Style.RESET_ALL
        )

    def do_info(self, arg):
        "show information about a module: info cve-2019-0193"
        if self.module is None:
            logger.warning("Please select a module first")
            return
        print(self.module.info())

    def do_show(self, arg):
        "show module options: show cve-2019-0193"
        if self.module is None:
            logger.warning("Please select a module first")
            return

        table = Table()

        table.add_column("Key")
        table.add_column("Value")
        table.add_column("Required")

        for key in self.module.options:
            table.add_row(
                key,
                str(self.module.options[key]["value"]),
                str(self.module.options[key]["required"]),
            )

        Console().print(table)

    def do_set(self, arg):
        "set an option for the selected module"
        if self.module is None:
            logger.warning("Please select a module first")
            return

        key = arg.split()[0]
        value = arg.split()[1]
        if key not in self.module.options:
            logger.error("Option does not exist")
            return

        self.module.options[key]["value"] = value

    def do_run(self, arg):
        "execute a module: run cve-2019-0193"
        self.module.run()

    def do_exit(self, arg):
        "exit the Phoenix shell"
        sys.exit(1)

    def do_quit(self, arg):
        "exit the Phoenix shell"
        sys.exit(1)

    def do_EOF(self, arg):
        "exit the Phoenix shell"
        sys.exit(1)


def main():

    colorama.init()

    # remove default sink and use a custom format
    logger.remove(0)
    logger.add(sys.stderr, colorize=True, format="<level>{level}: {message}</level>")

    while True:
        # ignore ^C inputs
        # the program is to be exited with the exit/quit commands
        # or EOF (^D)
        try:
            PhoenixShell().cmdloop()
        except KeyboardInterrupt:
            print()
            logger.warning("Please use EOF or the exit/quit commands to exit")
        except Exception:
            raise


if __name__ == "__main__":
    main()
