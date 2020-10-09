#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GdkX11, Gdk, Gtk, GLib


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
        Application menu main window
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Application Selector")

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(css)

        scroll_container = Gtk.ScrolledWindow()
        scroll_container.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.app_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        scroll_container.add(self.app_container)
        self.add(scroll_container)

        self.get_style_context().add_class("window")
        self.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

# TODO read system apps
# TODO read user apps
# TODO make list of categories
# TODO sort apps into categories
# TODO display categories
# TODO show corresponding apps as buttons under categories
# TODO run corresponding app when clicking a button


if __name__ == "__main__":
    win = LcarsdeApplicationStarter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
