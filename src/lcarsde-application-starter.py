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
    font-family: 'Ubuntu Condensed', sans-serif;
    font-weight: 600;
    font-size: 24px;
    color: #f90;
}
.line-end {
    min-width: 20px;
    background-color: #99F;
    background: #99F; /* for Ubuntu */
    outline-style: none;
    border-width: 0;
    box-shadow: none;
    padding: 0;
    margin: 0;
}
.line-end--left {
    border-radius: 20px 0 0 20px;
}
.line-end--right {
    border-radius: 0 20px 20px 0;
}
.window {
    background-color: #000;
}
'''


def sort_dict_by_key(data):
    new_dict = {}
    for key in sorted(data.keys()):
        new_dict[key] = data[key]
    return new_dict


class CategoryLabel(Gtk.Box):
    def __init__(self, label, css_provider):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        line_end_left = Gtk.Label()
        line_end_left.get_style_context().add_class("line-end")
        line_end_left.get_style_context().add_class("line-end--left")
        line_end_left.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.add(line_end_left)

        category_label = Gtk.Label(label=label)
        category_label.get_style_context().add_class("category")
        category_label.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.add(category_label)

        line_end_right = Gtk.Label()
        line_end_right.get_style_context().add_class("line-end")
        line_end_right.get_style_context().add_class("line-end--right")
        line_end_right.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.add(line_end_right)


class LcarsdeApplicationStarter(Gtk.Window):
    """
    Application selector main window
    """
    PREFERRED_CATEGORIES = ["System", "Game", "Network", "Office", "Settings", "AudioVideo", "Development", "Graphics",
                            "Utility"]

    def __init__(self):
        Gtk.Window.__init__(self, title="Application Selector")
        self.set_wmclass("Application Selector", "Application Selector")

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
        no_display = False
        for line in data_lines:
            if line.startswith("Name="):
                name = line[5:][0:18]
            elif line.startswith("Categories="):
                categories = line[11:]
            elif line.startswith("Exec="):
                exe = line[5:]
            elif line.startswith("NoDisplay="):
                no_display = line[10:].lower() == "true"

            if name is not None and categories is not None and exe is not None:
                break

        if not name or no_display:
            return

        if not categories:
            categories = "Utility"

        categories = list(categories.split(";"))
        category = self.get_category(categories).strip()
        if category == "":
            category = "Utility"

        if category not in self.applications.keys():
            self.applications[category] = list()

        self.applications[category].append((name, exe))

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
        for category, apps in sort_dict_by_key(self.applications).items():
            category_label = CategoryLabel(category, self.css_provider)
            self.app_container.add(category_label)

            apps.sort(key=lambda e: e[0])
            flow_box = Gtk.FlowBox(homogeneous=True)
            for app in apps:
                button = Gtk.Button(label=app[0])
                flow_box.add(button)

            self.app_container.add(flow_box)

    @staticmethod
    def start_application(widget):
        pass


if __name__ == "__main__":
    win = LcarsdeApplicationStarter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
