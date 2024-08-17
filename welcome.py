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
    _p,
    lrun,
    lp,
    app_store,
    links_store,
)
from bredos.utilities import debounce
from os import path

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject  # type: ignore

class WelcomeApp(Adw.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app) -> None:
        self.create_action("about", self.on_about_action)

    def do_activate(self) -> None:
        """Callback for the app.activate signal."""

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
    
    header_bar: Adw.HeaderBar = Gtk.Template.Child()
    home_grid: Gtk.GridView = Gtk.Template.Child()
    apps_grid: Gtk.GridView = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        # Create a selection model
        home_selection_model = Gtk.NoSelection(model=links_store)
        apps_selection_model = Gtk.NoSelection(model=app_store)

        # Create a factory for creating widgets
        factory = Gtk.SignalListItemFactory()

        def create_widget(factory, list_item):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            icon = Gtk.Image()
            icon.set_pixel_size(48)
            label = Gtk.Label()
            button = Gtk.Button()
            button.set_child(box)
            button.set_hexpand(True)
            button.set_vexpand(True)
            box.append(icon)
            box.append(label)
            list_item.set_child(button)

        def bind_widget(factory, list_item):
            button = list_item.get_child()
            box = button.get_child()
            icon = box.get_first_child()
            label = box.get_last_child()

            app_item = list_item.get_item()
            icon.set_from_icon_name(app_item.icon_name)
            label.set_label(app_item.label)

            @debounce(0.5)
            def on_button_clicked(button):
                lrun(app_item.command)

            button.connect("clicked", on_button_clicked)

        factory.connect("setup", create_widget)
        factory.connect("bind", bind_widget)

        self.home_grid.set_factory(factory)
        self.home_grid.set_model(home_selection_model)
        self.apps_grid.set_factory(factory)
        self.apps_grid.set_model(apps_selection_model)

