#!/usr/bin/env python3

import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


css = b'''
.select_button {
    font-family: 'Ubuntu Condensed', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #000;
    text-shadow: none;
    background-color: #99F;
    background: #99F; /* for Ubuntu */
    outline-style: none;
    border-radius: 0;
    border-width: 0;
    box-shadow: none;
    padding: 2px 3px;
    margin: 0;
}
.close_button {
    background-color: #C66;
    background: #C66; /* for Ubuntu */
    outline-style: none;
    border-radius: 0 20px 20px 0;
    border-width: 0;
    box-shadow: none;
    padding: 0;
    margin: 0;
}
.category {
    color: #f90;
}
.spacer {
    background-color: #99C;
    outline-style: none;
    border-radius: 0;
    padding: 0;
    margin: 0 40px 0 0;
}
.window {
    background-color: #000;
}
'''


class LcarsdeApplicationStarter(Gtk.Window):
    """
    Application selector main window
    """
    PREFERRED_CATEGORIES = ["System", "Game", "Network", "Office", "Settings", "AudioVideo", "Development", "Graphics",
                            "Utility"]

    def __init__(self):
        Gtk.Window.__init__(self, title="Application Selector")

        self.applications = {}
        self.load_system_applications()
        self.load_user_applications()

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(css)

        scroll_container = Gtk.ScrolledWindow()
        scroll_container.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.app_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.display_apps()

        scroll_container.add(self.app_container)
        self.add(scroll_container)

        self.get_style_context().add_class("window")
        self.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def add_application(self, app_data):
        data_lines = app_data.splitlines()
        name = None
        categories = None
        exe = None
        for line in data_lines:
            if line.startswith("Name="):
                name = line[5:]
            elif line.startswith("Categories="):
                categories = line[11:]
            elif line.startswith("Exec="):
                exe = line[5:]

            if name is not None and categories is not None and exe is not None:
                break

        if not categories:
            categories = "Utility"

        categories = list(categories.split(";"))
        category = self.get_category(categories).strip()
        if category == "":
            category = "Utility"

        if category not in self.applications.keys():
            self.applications[category] = set()

        self.applications[category].add((name, exe))

    def get_category(self, categories):
        for preferred_category in self.PREFERRED_CATEGORIES:
            if preferred_category in categories:
                return preferred_category
        return categories[0]

    def load_applications(self, app_directory):
        app_files = [os.path.join(app_directory, f)
                     for f in os.listdir(app_directory)
                     if os.path.isfile(os.path.join(app_directory, f))]
        app_data = set()
        for file_path in app_files:
            try:
                with open(file_path, 'r') as file:
                    app_data.add(file.read())
            except FileNotFoundError:
                print("Unable to load {0}".format(file_path))

        for d in app_data:
            self.add_application(d)

    def load_system_applications(self):
        self.load_applications("/usr/share/applications")

    def load_user_applications(self):
        path = "{0}/.local/share/applications".format(os.environ.get('HOME'))
        self.load_applications(path)

    def display_apps(self):
        for category, apps in self.applications.items():
            category_label = Gtk.Label(label=category)
            category_label.get_style_context().add_class("category")
            category_label.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
            self.app_container.add(category_label)

    @staticmethod
    def start_application(widget):
        pass


if __name__ == "__main__":
    win = LcarsdeApplicationStarter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
