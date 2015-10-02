import sys
import pygtk
pygtk.require("2.0")
import gtk


class AppGTK:
    """ Class that handle the graphic user interface. """
    def __init__(self):
        """ Initializes the components.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.start_window_builder = gtk.Builder()
        self.configuration_window_builder = gtk.Builder()
        self.solution_window_builder = gtk.Builder()
        
        self.start_window_builder.add_from_file("start_window.glade")
        self.configuration_window_builder.add_from_file("configuration_window.glade")
        self.solution_window_builder.add_from_file("solution_window.glade")
        
        self.main_window = self.start_window_builder.get_object("main_window")
        self.configuration_window = self.configuration_window_builder.get_object("main_window")
        self.solution_window = self.solution_window_builder.get_object("main_window")
        
        self.connect_windows_signals()
        self.set_start_window_buttons()
        self.set_configuration_window_buttons()
        
    def connect_windows_signals(self):
        """ Connects the quit signail of the windows.
        parameters:
            [AppGTK] self -- the self instance.
        """
        if(self.main_window):
            self.main_window.connect("destroy", gtk.main_quit)
            self.main_window.show()
        if(self.configuration_window):
            self.configuration_window.connect("destroy", gtk.Widget.destroy)
        if(self.solution_window):
            self.solution_window.connect("destroy", gtk.Widget.destroy)

    def set_start_window_buttons(self):
        """ Obtains all the buttons from the start window XML file.
        sw = solution window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.create_configuration_button = self.start_window_builder.get_object("menu_button_create_config")
        if(self.create_configuration_button):
            self.create_configuration_button.connect("clicked", self.start_configuration_window, self.configuration_window, self.main_window)
            
    def set_configuration_window_buttons(self):
        """ Obtains all the buttons from the configuration window XML file.
        cw = configuration window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.cw_upward_button = self.configuration_window_builder.get_object("upward_button")
        self.cw_downward_button = self.configuration_window_builder.get_object("downward_button")
        self.cw_start_button = self.configuration_window_builder.get_object("start_button")
        
        self.cw_backward_button1 = self.configuration_window_builder.get_object("backward_button1")
        self.cw_backward_button2 = self.configuration_window_builder.get_object("backward_button2")
        self.cw_backward_button3 = self.configuration_window_builder.get_object("backward_button3")
        self.cw_backward_button4 = self.configuration_window_builder.get_object("backward_button4")
        self.cw_backward_button5 = self.configuration_window_builder.get_object("backward_button5")
        
        self.cw_forward_button1 = self.configuration_window_builder.get_object("forward_button1")
        self.cw_forward_button2 = self.configuration_window_builder.get_object("forward_button2")
        self.cw_forward_button3 = self.configuration_window_builder.get_object("forward_button3")
        self.cw_forward_button4 = self.configuration_window_builder.get_object("forward_button4")
        self.cw_forward_button5 = self.configuration_window_builder.get_object("forward_button5")
    
    def set_solution_window_buttons:
        """ Obtains all the buttons from the solution XML file
        sw = solution window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.sow_upward_button = self.start_window_builder.get_object("upward_button")
        self.sow_downward_button = self.start_window_builder.get_object("downward_button")
        
        self.sow_backward_button1 = self.start_window_builder.get_object("backward_button1")
        self.sow_backward_button2 = self.start_window_builder.get_object("backward_button2")
        self.sow_backward_button3 = self.start_window_builder.get_object("backward_button3")
        self.sow_backward_button4 = self.start_window_builder.get_object("backward_button4")
        self.sow_backward_button5 = self.start_window_builder.get_object("backward_button5")
        
        self.sow_forward_button1 = self.start_window_builder.get_object("forward_button1")
        self.sow_forward_button2 = self.start_window_builder.get_object("forward_button2")
        self.sow_forward_button3 = self.start_window_builder.get_object("forward_button3")
        self.sow_forward_button4 = self.start_window_builder.get_object("forward_button4")
        self.sow_forward_button5 = self.start_window_builder.get_object("forward_button5")
        
    
    
    def start_configuration_window(self, widget, config_window, parent_window):
        """ Shows the configuration window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if(config_window and parent_window):
            config_window.show()



