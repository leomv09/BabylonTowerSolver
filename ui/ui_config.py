import sys
import pygtk
pygtk.require("2.0")
import gtk


class AppGTK:
    def __init__(self):
        builder = gtk.Builder()
        builder2 = gtk.Builder()
        builder.add_from_file("start_window.glade")
        builder2.add_from_file("configuration_window.glade")
        self.main_window = builder.get_object("main_window")
        self.configuration_window = builder2.get_object("main_window")
        self.create_button = builder.get_object("menu_button_create_config")
        self.connect_signals()
        
    def connect_signals(self):
        if(self.main_window):
            self.main_window.connect("destroy", gtk.main_quit)
            self.main_window.show()
        if(self.create_button):
            self.create_button.connect("clicked", self.start_configuration_window, self.configuration_window, self.main_window)
        if(self.configuration_window):
            self.configuration_window.connect("destroy", gtk.main_quit)
            
    def start_configuration_window(self, widget, config_window, parent_window):
        if(config_window and parent_window):
            config_window.show()
            ##parent_window.destroy()



