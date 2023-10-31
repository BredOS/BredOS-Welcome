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

import gettext
import welcome_support
from welcome_support import (
    _,
)
from os import path

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio

class WelcomeApp(Adw.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app) -> None:
        self.create_action("about", self.on_about_action)

    def do_activate(self) -> None:
        """Callback for the app.activate signal."""

        _ = setup_translations()
        
        global win
        win = self.props.active_window
        if not win:
            win = WelcomeWindow(application=self)
            self.win = win
        win.present()

    def on_preferences_action(self, widget, _) -> None:
        """Callback for the app.preferences action."""
        pass

    def on_about_action(self, widget, py) -> None:
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="BredOS Welcome",
            application_icon="org.bredos.welcome",
            developer_name="BredOS",
            version="0.0.1",
            developers=["Panda"],
            designers=["Panda", "DustyDaimler"],
            copyright="© 2023 BredOS",
            comments=_("Welcome to BredOS!"),
            license_type=Gtk.License.GPL_3_0,
            website="https://BredOS.org",
        )
        about.present()

    def create_action(self, name, callback, shortcuts=None) -> None:
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

@Gtk.Template(resource_path="/org/bredos/welcome/ui/window.ui")
class WelcomeWindow(Adw.Window):
    __gtype_name__ = "WelcomeWindow"
    
    header_bar = Gtk.Template.Child()
    # header_bar: Gtk.HeaderBar = Gtk.Template.Child()
    # stack: Adw.ViewStack = Gtk.Template.Child()
    # switcher_bar: Adw.ViewSwitcherBar = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def setup_translations(lang: object = None) -> gettext.GNUTranslations:
    """
    Setup translations

        Does the following:
        - Loads the translations from the locale folder
        - Sets the translations for the gettext module

        Returns:  A gettext translation object
        :rtype: object
    """
    lang_path = path.join(path.dirname(__file__), "locale")
    # Load translations
    if lang is not None:
        gettext.bindtextdomain("bakery", lang_path)
        gettext.textdomain("bakery")
        translation = gettext.translation("bakery", lang_path, languages=[lang])
        translation.install()
        return translation.gettext  # type: ignore
    else:
        gettext.bindtextdomain("bakery", lang_path)
        gettext.textdomain("bakery")
        return gettext.gettext  # type: ignore
    
