import sys
import pygtk
pygtk.require("2.0")
import gtk


class AppGTK:
    def __init__(self):
        start_window_builder = gtk.Builder()
        configuration_window_builder = gtk.Builder()
        solution_window_builder = gtk.Builder()
        
        start_window_builder.add_from_file("start_window.glade")
        configuration_window_builder.add_from_file("configuration_window.glade")
        solution_window_builder.add_from_file("solution_window.glade")
        
        self.main_window = start_window_builder.get_object("main_window")
        self.configuration_window = configuration_window_builder.get_object("main_window")
        self.create_button = start_window_builder.get_object("menu_button_create_config")
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



