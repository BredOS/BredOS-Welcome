#! /usr/bin/env python
#
# Copyright 2023 BredOS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
import locale
from bredos.translations import setup_translations
from bredos.logging import (
    setup_logging,
    setup_handler,
    lp,
    lrun,
)
import os

from gi.repository import GObject, Gio  # type: ignore

class Item(GObject.GObject):
    label = GObject.Property(type=str)
    icon_name = GObject.Property(type=str)
    command = GObject.Property()
    check_installed = GObject.Property(type=bool, default=False)

    def __init__(self, label: str, icon_name: str, command: list, check_installed=False):
        super().__init__()
        self.label = label
        self.icon_name = icon_name
        self.command = list(command)
        self.check_installed = check_installed

setup_logging(
    "bredos-welcome",
     os.path.join(os.path.expanduser("~"),".bredos", "welcome", "logs"),
     datetime.now().strftime("WELCOME-%Y-%m-%d-%H-%M-%S.log")
)
setup_handler()
lp("Logger started.")
lp("Setting up translations..")
_, _p = setup_translations("bredos-welcome", locale.getdefaultlocale()[0])
lp("Translations setup.")

app_store = Gio.ListStore(item_type=Item)
links_store = Gio.ListStore(item_type=Item)

app_dict = {
            "Webcord": ("web-browser", ["webcord"], {"check_installed": True}),
            "Software": ("system-software-install", ["gnome-software"], {"check_installed": True}),
            "Terminal": ("utilities-terminal", ["gnome-terminal"], {"check_installed": True}),
}

links_dict = {
            "BredOS Website": ("web-browser", ["xdg-open", "https://bredos.org/"]),
            "BredOS GitHub": ("web-browser", ["xdg-open", "https://github.com/BredOS/"]),
            "BredOS Forum": ("web-browser", ["xdg-open", "https://forum.bredos.org/"]),
            "BredOS Wiki": ("web-browser", ["xdg-open", "https://wiki.bredos.org/"]),
            'BredOS Discord': ("web-browser", ["xdg-open", "https://discord.gg/8Z2K3jZ"]),
}
for label, (icon_name, command, options) in app_dict.items():
            app_item = Item(label=label, icon_name=icon_name, command=command, check_installed=options["check_installed"])
            app_store.append(app_item)

for label, (icon_name, command) in links_dict.items():
            link_item = Item(label=label, icon_name=icon_name, command=command, check_installed=False)
            links_store.append(link_item) 

