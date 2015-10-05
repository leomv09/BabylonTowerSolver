import sys
import pygtk

pygtk.require("2.0")
import gtk
import utilities
import file
import os.path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import core.babylon_node
import core.astar

class NestedDialog(object):
    def __init__(self, dialog):
        self.dialog = dialog
        self.response_var = None

    def run(self):
        self._run()
        return self.response_var

    def _run(self):
        self.dialog.show()
        self.dialog.connect("response", self._response)
        gtk.main()

    def _response(self, dialog, response):
        self.response_var = response
        self.dialog.destroy()
        gtk.main_quit()

class AppGTK:
    """ Class that handles the graphic user interface components. """

    def __init__(self):
        """ Initializes the components.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.start_matrix = [['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*']]
        self.end_matrix = [['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*']]
        self.current_index_row_0 = 0
        self.current_index_row_1 = 0
        self.current_index_row_2 = 0
        self.current_index_row_3 = 0
        self.current_index_row_4 = 0
        self.movement_index = 0
        self.solution_grids_index = 0
        self.indexes = [self.current_index_row_0, self.current_index_row_1, self.current_index_row_2,
                        self.current_index_row_3, self.current_index_row_4]

        self.matrix_info = {
            1: {
                "selected_color": "",
                "red_counter": 0,
                "green_counter": 0,
                "blue_counter": 0,
                "yellow_counter": 0,
                "blocked_counter": 0,
                "wildcard_counter": 20,
                "matrix": self.start_matrix
            },
            2: {
                "selected_color": "",
                "red_counter": 0,
                "green_counter": 0,
                "blue_counter": 0,
                "yellow_counter": 0,
                "blocked_counter": 0,
                "wildcard_counter": 20,
                "matrix": self.end_matrix
            }
        }

        self.color_counter = {
            'R': "red_counter",
            'G': "green_counter",
            'B': "blue_counter",
            'Y': "yellow_counter",
            '-': "blocked_counter",
            '*': "wildcard_counter"
        }

        self.color_amount = {
            'R': 4,
            'G': 4,
            'B': 4,
            'Y': 4,
            '-': 3,
            '*': 20
        }

        self.cw_toy_images = []
        self.sw_toy_images = []
        self.current_face = 0
        """ Create the builder for each window """
        self.start_window_builder = gtk.Builder()
        self.configuration_window_builder = gtk.Builder()
        self.solution_window_builder = gtk.Builder()
        self.loading_window_builder = gtk.Builder()
        self.user_manual_window_builder = gtk.Builder()

        """ Obtain the glade file for each window """
        self.start_window_builder.add_from_file("start_window.glade")
        self.configuration_window_builder.add_from_file("configuration_window.glade")
        self.solution_window_builder.add_from_file("solution_window.glade")
        self.loading_window_builder.add_from_file("loading_window.glade")
        self.user_manual_window_builder.add_from_file("user_manual.glade")

        """ Get the main components from the XML file """
        self.main_window = self.start_window_builder.get_object("main_window")
        self.configuration_window = self.configuration_window_builder.get_object("main_window")
        self.solution_window = self.solution_window_builder.get_object("main_window")
        self.loading_window = self.loading_window_builder.get_object("main_window")
        self.user_manual_window = self.user_manual_window_builder.get_object("main_window")
        self.description_label = self.solution_window_builder.get_object("steps_description_label")
        self.help_label = self.user_manual_window_builder.get_object("help_content")

        self.connect_windows_signals()
        self.set_start_window_buttons()
        self.set_configuration_window_buttons()
        self.set_solution_window_buttons()
        self.set_configuration_window_images()

        if (self.cw_start_button):
            self.cw_start_button.connect("clicked", self.start_solution_window, self.solution_window,
                                         self.configuration_window)

    def connect_windows_signals(self):
        """ Connects the quit signail to the windows.
        parameters:
            [AppGTK] self -- the self instance.
        """
        if (self.main_window):
            self.main_window.connect("destroy", gtk.main_quit)
            self.main_window.show()
        if (self.configuration_window):
            self.configuration_window.connect("destroy", gtk.Widget.destroy)
        if (self.solution_window):
            self.solution_window.connect("destroy", gtk.Widget.destroy)
        if (self.loading_window):
            self.loading_window.connect("destroy", gtk.Widget.destroy)
        if (self.user_manual_window):
            self.user_manual_window.connect("destroy", gtk.Widget.destroy)

    def set_start_window_buttons(self):
        """ Obtains all the buttons from the start window XML file.
        sw = start window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.help = self.start_window_builder.get_object("ayuda")
        self.create_configuration_button = self.start_window_builder.get_object("menu_button_create_config")
        self.open_file_dialog = self.start_window_builder.get_object("file_chooser_button")
        self.set_filter()
        self.open_file_dialog.connect("file-set", self.open_config_from_file)
        if (self.create_configuration_button):
            self.create_configuration_button.connect("clicked", self.start_configuration_window,
                                                     self.configuration_window, self.main_window)
        if self.help:
            self.help.connect("clicked", self.show_user_manual, self.user_manual_window, self.main_window)

    def set_filter(self):
        filter = gtk.FileFilter()
        filter.set_name("Text files")
        filter.add_pattern("*.txt")
        self.open_file_dialog.add_filter(filter)

    def open_config_from_file(self, widget):
        file_name = self.open_file_dialog.get_filename()
        if (file_name):
            start, end = file.load(file_name)
            self.start_matrix = start
            self.end_matrix = end
            self.load_configuration_matrix(self.start_matrix, 1)
            self.load_configuration_matrix(self.end_matrix, 2)
            self.configuration_window.show()

    def set_configuration_window_buttons(self):
        """ Obtains all the buttons from the configuration window XML file.
        cw = configuration window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.cw_start_button = self.configuration_window_builder.get_object("start_button")
        self.cw_matrix_1_selected_color = self.configuration_window_builder.get_object("selected_color_1")
        self.cw_matrix_2_selected_color = self.configuration_window_builder.get_object("selected_color_2")
        self.cw_matrix_1_clear_button = self.configuration_window_builder.get_object("clean_button_1")
        self.cw_matrix_2_clear_button = self.configuration_window_builder.get_object("clean_button_2")
        self.cw_matrix_1_clear_button.connect("clicked", self.clear_matrix_1)
        self.cw_matrix_2_clear_button.connect("clicked", self.clear_matrix_2)
        # Selection Colors
        self.cw_matrix_1_select_red = self.configuration_window_builder.get_object("select_red_ball_button_1")
        self.cw_matrix_1_select_red.connect("clicked", self.change_selected_color, 1, 'R')
        self.cw_matrix_1_select_green = self.configuration_window_builder.get_object("select_green_ball_button_1")
        self.cw_matrix_1_select_green.connect("clicked", self.change_selected_color, 1, 'G')
        self.cw_matrix_1_select_blue = self.configuration_window_builder.get_object("select_blue_ball_button_1")
        self.cw_matrix_1_select_blue.connect("clicked", self.change_selected_color, 1, 'B')
        self.cw_matrix_1_select_yellow = self.configuration_window_builder.get_object("select_yellow_ball_button_1")
        self.cw_matrix_1_select_yellow.connect("clicked", self.change_selected_color, 1, 'Y')
        self.cw_matrix_1_select_widlcard = self.configuration_window_builder.get_object("select_wildcard_button_1")
        self.cw_matrix_1_select_widlcard.connect("clicked", self.change_selected_color, 1, '-')
        self.cw_matrix_2_select_red = self.configuration_window_builder.get_object("select_red_ball_button_2")
        self.cw_matrix_2_select_red.connect("clicked", self.change_selected_color, 2, 'R')
        self.cw_matrix_2_select_green = self.configuration_window_builder.get_object("select_green_ball_button_2")
        self.cw_matrix_2_select_green.connect("clicked", self.change_selected_color, 2, 'G')
        self.cw_matrix_2_select_blue = self.configuration_window_builder.get_object("select_blue_ball_button_2")
        self.cw_matrix_2_select_blue.connect("clicked", self.change_selected_color, 2, 'B')
        self.cw_matrix_2_select_yellow = self.configuration_window_builder.get_object("select_yellow_ball_button_2")
        self.cw_matrix_2_select_yellow.connect("clicked", self.change_selected_color, 2, 'Y')
        self.cw_matrix_2_select_widlcard = self.configuration_window_builder.get_object("select_wildcard_button_2")
        self.cw_matrix_2_select_widlcard.connect("clicked", self.change_selected_color, 2, '-')

        # Matrix buttons
        self.cw_matrix_1_0_0 = self.configuration_window_builder.get_object("matrix_1_0_0")
        self.cw_ball_1_0_0 = self.configuration_window_builder.get_object("ball_1_0_0")
        self.cw_matrix_1_0_0.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_0_0, 0, 0)
        self.cw_matrix_1_0_1 = self.configuration_window_builder.get_object("matrix_1_0_1")
        self.cw_ball_1_0_1 = self.configuration_window_builder.get_object("ball_1_0_1")
        self.cw_matrix_1_0_1.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_0_1, 0, 1)
        self.cw_matrix_1_0_2 = self.configuration_window_builder.get_object("matrix_1_0_2")
        self.cw_ball_1_0_2 = self.configuration_window_builder.get_object("ball_1_0_2")
        self.cw_matrix_1_0_2.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_0_2, 0, 2)
        self.cw_matrix_1_0_3 = self.configuration_window_builder.get_object("matrix_1_0_3")
        self.cw_ball_1_0_3 = self.configuration_window_builder.get_object("ball_1_0_3")
        self.cw_matrix_1_0_3.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_0_3, 0, 3)
        self.cw_matrix_1_1_0 = self.configuration_window_builder.get_object("matrix_1_1_0")
        self.cw_ball_1_1_0 = self.configuration_window_builder.get_object("ball_1_1_0")
        self.cw_matrix_1_1_0.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_1_0, 1, 0)
        self.cw_matrix_1_1_1 = self.configuration_window_builder.get_object("matrix_1_1_1")
        self.cw_ball_1_1_1 = self.configuration_window_builder.get_object("ball_1_1_1")
        self.cw_matrix_1_1_1.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_1_1, 1, 1)
        self.cw_matrix_1_1_2 = self.configuration_window_builder.get_object("matrix_1_1_2")
        self.cw_ball_1_1_2 = self.configuration_window_builder.get_object("ball_1_1_2")
        self.cw_matrix_1_1_2.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_1_2, 1, 2)
        self.cw_matrix_1_1_3 = self.configuration_window_builder.get_object("matrix_1_1_3")
        self.cw_ball_1_1_3 = self.configuration_window_builder.get_object("ball_1_1_3")
        self.cw_matrix_1_1_3.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_1_3, 1, 3)
        self.cw_matrix_1_2_0 = self.configuration_window_builder.get_object("matrix_1_2_0")
        self.cw_ball_1_2_0 = self.configuration_window_builder.get_object("ball_1_2_0")
        self.cw_matrix_1_2_0.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_2_0, 2, 0)
        self.cw_matrix_1_2_1 = self.configuration_window_builder.get_object("matrix_1_2_1")
        self.cw_ball_1_2_1 = self.configuration_window_builder.get_object("ball_1_2_1")
        self.cw_matrix_1_2_1.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_2_1, 2, 1)
        self.cw_matrix_1_2_2 = self.configuration_window_builder.get_object("matrix_1_2_2")
        self.cw_ball_1_2_2 = self.configuration_window_builder.get_object("ball_1_2_2")
        self.cw_matrix_1_2_2.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_2_2, 2, 2)
        self.cw_matrix_1_2_3 = self.configuration_window_builder.get_object("matrix_1_2_3")
        self.cw_ball_1_2_3 = self.configuration_window_builder.get_object("ball_1_2_3")
        self.cw_matrix_1_2_3.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_2_3, 2, 3)
        self.cw_matrix_1_3_0 = self.configuration_window_builder.get_object("matrix_1_3_0")
        self.cw_ball_1_3_0 = self.configuration_window_builder.get_object("ball_1_3_0")
        self.cw_matrix_1_3_0.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_3_0, 3, 0)
        self.cw_matrix_1_3_1 = self.configuration_window_builder.get_object("matrix_1_3_1")
        self.cw_ball_1_3_1 = self.configuration_window_builder.get_object("ball_1_3_1")
        self.cw_matrix_1_3_1.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_3_1, 3, 1)
        self.cw_matrix_1_3_2 = self.configuration_window_builder.get_object("matrix_1_3_2")
        self.cw_ball_1_3_2 = self.configuration_window_builder.get_object("ball_1_3_2")
        self.cw_matrix_1_3_2.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_3_2, 3, 2)
        self.cw_matrix_1_3_3 = self.configuration_window_builder.get_object("matrix_1_3_3")
        self.cw_ball_1_3_3 = self.configuration_window_builder.get_object("ball_1_3_3")
        self.cw_matrix_1_3_3.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_3_3, 3, 3)
        self.cw_matrix_1_4_0 = self.configuration_window_builder.get_object("matrix_1_4_0")
        self.cw_ball_1_4_0 = self.configuration_window_builder.get_object("ball_1_4_0")
        self.cw_matrix_1_4_0.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_4_0, 4, 0)
        self.cw_matrix_1_4_1 = self.configuration_window_builder.get_object("matrix_1_4_1")
        self.cw_ball_1_4_1 = self.configuration_window_builder.get_object("ball_1_4_1")
        self.cw_matrix_1_4_1.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_4_1, 4, 1)
        self.cw_matrix_1_4_2 = self.configuration_window_builder.get_object("matrix_1_4_2")
        self.cw_ball_1_4_2 = self.configuration_window_builder.get_object("ball_1_4_2")
        self.cw_matrix_1_4_2.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_4_2, 4, 2)
        self.cw_matrix_1_4_3 = self.configuration_window_builder.get_object("matrix_1_4_3")
        self.cw_ball_1_4_3 = self.configuration_window_builder.get_object("ball_1_4_3")
        self.cw_matrix_1_4_3.connect("clicked", self.put_selected_color, 1, self.cw_ball_1_4_3, 4, 3)
        # Matrix 2
        self.cw_matrix_2_0_0 = self.configuration_window_builder.get_object("matrix_2_0_0")
        self.cw_ball_2_0_0 = self.configuration_window_builder.get_object("ball_2_0_0")
        self.cw_matrix_2_0_0.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_0_0, 0, 0)
        self.cw_matrix_2_0_1 = self.configuration_window_builder.get_object("matrix_2_0_1")
        self.cw_ball_2_0_1 = self.configuration_window_builder.get_object("ball_2_0_1")
        self.cw_matrix_2_0_1.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_0_1, 0, 1)
        self.cw_matrix_2_0_2 = self.configuration_window_builder.get_object("matrix_2_0_2")
        self.cw_ball_2_0_2 = self.configuration_window_builder.get_object("ball_2_0_2")
        self.cw_matrix_2_0_2.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_0_2, 0, 2)
        self.cw_matrix_2_0_3 = self.configuration_window_builder.get_object("matrix_2_0_3")
        self.cw_ball_2_0_3 = self.configuration_window_builder.get_object("ball_2_0_3")
        self.cw_matrix_2_0_3.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_0_3, 0, 3)
        self.cw_matrix_2_1_0 = self.configuration_window_builder.get_object("matrix_2_1_0")
        self.cw_ball_2_1_0 = self.configuration_window_builder.get_object("ball_2_1_0")
        self.cw_matrix_2_1_0.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_1_0, 1, 0)
        self.cw_matrix_2_1_1 = self.configuration_window_builder.get_object("matrix_2_1_1")
        self.cw_ball_2_1_1 = self.configuration_window_builder.get_object("ball_2_1_1")
        self.cw_matrix_2_1_1.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_1_1, 1, 1)
        self.cw_matrix_2_1_2 = self.configuration_window_builder.get_object("matrix_2_1_2")
        self.cw_ball_2_1_2 = self.configuration_window_builder.get_object("ball_2_1_2")
        self.cw_matrix_2_1_2.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_1_2, 1, 2)
        self.cw_matrix_2_1_3 = self.configuration_window_builder.get_object("matrix_2_1_3")
        self.cw_ball_2_1_3 = self.configuration_window_builder.get_object("ball_2_1_3")
        self.cw_matrix_2_1_3.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_1_3, 1, 3)
        self.cw_matrix_2_2_0 = self.configuration_window_builder.get_object("matrix_2_2_0")
        self.cw_ball_2_2_0 = self.configuration_window_builder.get_object("ball_2_2_0")
        self.cw_matrix_2_2_0.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_2_0, 2, 0)
        self.cw_matrix_2_2_1 = self.configuration_window_builder.get_object("matrix_2_2_1")
        self.cw_ball_2_2_1 = self.configuration_window_builder.get_object("ball_2_2_1")
        self.cw_matrix_2_2_1.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_2_1, 2, 1)
        self.cw_matrix_2_2_2 = self.configuration_window_builder.get_object("matrix_2_2_2")
        self.cw_ball_2_2_2 = self.configuration_window_builder.get_object("ball_2_2_2")
        self.cw_matrix_2_2_2.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_2_2, 2, 2)
        self.cw_matrix_2_2_3 = self.configuration_window_builder.get_object("matrix_2_2_3")
        self.cw_ball_2_2_3 = self.configuration_window_builder.get_object("ball_2_2_3")
        self.cw_matrix_2_2_3.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_2_3, 2, 3)
        self.cw_matrix_2_3_0 = self.configuration_window_builder.get_object("matrix_2_3_0")
        self.cw_ball_2_3_0 = self.configuration_window_builder.get_object("ball_2_3_0")
        self.cw_matrix_2_3_0.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_3_0, 3, 0)
        self.cw_matrix_2_3_1 = self.configuration_window_builder.get_object("matrix_2_3_1")
        self.cw_ball_2_3_1 = self.configuration_window_builder.get_object("ball_2_3_1")
        self.cw_matrix_2_3_1.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_3_1, 3, 1)
        self.cw_matrix_2_3_2 = self.configuration_window_builder.get_object("matrix_2_3_2")
        self.cw_ball_2_3_2 = self.configuration_window_builder.get_object("ball_2_3_2")
        self.cw_matrix_2_3_2.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_3_2, 3, 2)
        self.cw_matrix_2_3_3 = self.configuration_window_builder.get_object("matrix_2_3_3")
        self.cw_ball_2_3_3 = self.configuration_window_builder.get_object("ball_2_3_3")
        self.cw_matrix_2_3_3.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_3_3, 3, 3)
        self.cw_matrix_2_4_0 = self.configuration_window_builder.get_object("matrix_2_4_0")
        self.cw_ball_2_4_0 = self.configuration_window_builder.get_object("ball_2_4_0")
        self.cw_matrix_2_4_0.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_4_0, 4, 0)
        self.cw_matrix_2_4_1 = self.configuration_window_builder.get_object("matrix_2_4_1")
        self.cw_ball_2_4_1 = self.configuration_window_builder.get_object("ball_2_4_1")
        self.cw_matrix_2_4_1.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_4_1, 4, 1)
        self.cw_matrix_2_4_2 = self.configuration_window_builder.get_object("matrix_2_4_2")
        self.cw_ball_2_4_2 = self.configuration_window_builder.get_object("ball_2_4_2")
        self.cw_matrix_2_4_2.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_4_2, 4, 2)
        self.cw_matrix_2_4_3 = self.configuration_window_builder.get_object("matrix_2_4_3")
        self.cw_ball_2_4_3 = self.configuration_window_builder.get_object("ball_2_4_3")
        self.cw_matrix_2_4_3.connect("clicked", self.put_selected_color, 2, self.cw_ball_2_4_3, 4, 3)


    def set_solution_window_buttons(self):
        """ Obtains all the buttons from the solution XML file
        sw = solution window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.sow_next_solution_button = self.solution_window_builder.get_object("next_solution_button")
        self.sow_previous_solution_button = self.solution_window_builder.get_object("previous_solution_button")
        self.sow_next_solution_button.connect("clicked", self.show_next_solution)
        self.sow_previous_solution_button.connect("clicked", self.show_previous_solution)
        self.sow_rotate_left_button = self.solution_window_builder.get_object("rotate_left_button")
        self.sow_rotate_left_button.connect("clicked", self.rotate_left)
        self.sow_rotate_right_button = self.solution_window_builder.get_object("rotate_right_button")
        self.sow_rotate_right_button.connect("clicked", self.rotate_right)

    def show_next_solution(self, widget):
        if (not self.movement_index + 1 > len(self.movements) - 1):
            self.movement_index += 1
            self.print_step()
        if (not self.solution_grids_index + 1 > len(self.solution_grids) - 1):
            self.solution_grids_index += 1
            self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def show_previous_solution(self, widget):
        if (not self.movement_index - 1 < 0):
            self.movement_index -= 1
            self.print_step()
        if (not self.solution_grids_index - 1 < 0):
            self.solution_grids_index -= 1
            self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def rotate_left(self, widget):
        self.current_face = (self.current_face+1) % 4
        self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def rotate_right(self, widget):
        self.current_face = (self.current_face-1) % 4
        self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def show_user_manual(self, widget, help_window, parent_window):
        """ Shows the configuration window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if help_window and parent_window:
            self.help_label.set_text(utilities.read_file("user_manual.txt"))
            help_window.show()

    def change_selected_color(self, widget, matrix_id, color_id):
        self.matrix_info[matrix_id]["selected_color"] = utilities.get_matrix_image_name(color_id)
        if (matrix_id == 1):
            self.cw_matrix_1_selected_color.set_from_file(self.matrix_info[matrix_id]["selected_color"])
        else:
            self.cw_matrix_2_selected_color.set_from_file(self.matrix_info[matrix_id]["selected_color"])

    def put_selected_color(self, widget, matrix_id, image_object, row, col):
        if row < 0 or row > 4 or col < 0 or col > 3:
            return

        selected_color = utilities.get_operation_name(self.matrix_info[matrix_id]["selected_color"])
        selected_counter = self.color_counter[selected_color]

        current_color = self.matrix_info[matrix_id]["matrix"][row][col]
        current_counter = self.color_counter[current_color]

        if current_color == selected_color:
            self.matrix_info[matrix_id][current_counter] -= 1
            self.matrix_info[matrix_id]["matrix"][row][col] = "*"
            image_object.clear()

        elif self.matrix_info[matrix_id][selected_counter] < self.color_amount[selected_color]:
            if selected_color == '-' and row != 0:
                return

            if current_color != '*':
                self.matrix_info[matrix_id][current_counter] -= 1

            image_object.set_from_file(utilities.get_matrix_image_name(selected_color))
            self.matrix_info[matrix_id][selected_counter] += 1
            self.matrix_info[matrix_id]["matrix"][row][col] = selected_color

    def clear_matrix_1(self, widget):
        self.cw_ball_1_0_0.set_from_file(None)
        self.cw_ball_1_0_1.set_from_file(None)
        self.cw_ball_1_0_2.set_from_file(None)
        self.cw_ball_1_0_3.set_from_file(None)
        self.cw_ball_1_1_0.set_from_file(None)
        self.cw_ball_1_1_1.set_from_file(None)
        self.cw_ball_1_1_2.set_from_file(None)
        self.cw_ball_1_1_3.set_from_file(None)
        self.cw_ball_1_2_0.set_from_file(None)
        self.cw_ball_1_2_1.set_from_file(None)
        self.cw_ball_1_2_2.set_from_file(None)
        self.cw_ball_1_2_3.set_from_file(None)
        self.cw_ball_1_3_0.set_from_file(None)
        self.cw_ball_1_3_1.set_from_file(None)
        self.cw_ball_1_3_2.set_from_file(None)
        self.cw_ball_1_3_3.set_from_file(None)
        self.cw_ball_1_4_0.set_from_file(None)
        self.cw_ball_1_4_1.set_from_file(None)
        self.cw_ball_1_4_2.set_from_file(None)
        self.cw_ball_1_4_3.set_from_file(None)
        self.matrix_info[1]["red_counter"] = 0
        self.matrix_info[1]["green_counter"] = 0
        self.matrix_info[1]["blue_counter"] = 0
        self.matrix_info[1]["yellow_counter"] = 0
        self.matrix_info[1]["blocked_counter"] = 0
        self.matrix_info[1]["wildcard_counter"] = 20
        self.start_matrix = [['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*']]
        self.matrix_info[1]["matrix"] = self.start_matrix

    def clear_matrix_2(self, widget):
        self.cw_ball_2_0_0.set_from_file(None)
        self.cw_ball_2_0_1.set_from_file(None)
        self.cw_ball_2_0_2.set_from_file(None)
        self.cw_ball_2_0_3.set_from_file(None)
        self.cw_ball_2_1_0.set_from_file(None)
        self.cw_ball_2_1_1.set_from_file(None)
        self.cw_ball_2_1_2.set_from_file(None)
        self.cw_ball_2_1_3.set_from_file(None)
        self.cw_ball_2_2_0.set_from_file(None)
        self.cw_ball_2_2_1.set_from_file(None)
        self.cw_ball_2_2_2.set_from_file(None)
        self.cw_ball_2_2_3.set_from_file(None)
        self.cw_ball_2_3_0.set_from_file(None)
        self.cw_ball_2_3_1.set_from_file(None)
        self.cw_ball_2_3_2.set_from_file(None)
        self.cw_ball_2_3_3.set_from_file(None)
        self.cw_ball_2_4_0.set_from_file(None)
        self.cw_ball_2_4_1.set_from_file(None)
        self.cw_ball_2_4_2.set_from_file(None)
        self.cw_ball_2_4_3.set_from_file(None)
        self.matrix_info[2]["red_counter"] = 0
        self.matrix_info[2]["green_counter"] = 0
        self.matrix_info[2]["blue_counter"] = 0
        self.matrix_info[2]["yellow_counter"] = 0
        self.matrix_info[2]["blocked_counter"] = 0
        self.matrix_info[2]["wildcard_counter"] = 20
        self.end_matrix = [['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*'], ['*', '*', '*', '*']]
        self.end_matrix[2]["matrix"] = self.end_matrix

    def start_configuration_window(self, widget, config_window, parent_window):
        """ Shows the configuration window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if (config_window and parent_window):
            # self.load_configuration_matrix(self.start_matrix)
            # self.load_configuration_matrix(self.end_matrix, 5)
            config_window.show()

    def show_dialog(self, message):
        dialog = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
            gtk.BUTTONS_OK, message)
        nested_dialog = NestedDialog(dialog)
        nested_dialog.run()

    def start_solution_window(self, widget, solution_window, parent_window):
        """ Shows the solution window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if (solution_window and parent_window):
            if not utilities.is_valid_configuration(self.start_matrix):
                self.show_dialog("Configuracion inicial invalida")
                return

            if not utilities.is_valid_configuration(self.end_matrix):
                self.show_dialog("Configuracion final invalida")
                return

            print("\nStart matrix")
            print(self.start_matrix)
            print("\nEnd matrix")
            print(self.end_matrix)
            print("\n")
            self.loading_window.show()
            start = core.babylon_node.BabylonNode(self.start_matrix)
            goal = core.babylon_node.BabylonNode(self.end_matrix)
            algorithm = core.astar.AStar()
            nodes = algorithm.nodes_between(start, goal)
            self.movements = [node.movement for node in nodes[1:]] if len(nodes) > 1 else []
            self.solution_grids = [node.grid for node in nodes]
            print("\nSolution:\n")
            print(self.solution_grids)
            print("\nMovements:\n")
            print(self.movements)
            self.set_solution_window_images();
            self.load_solution_matrix()
            solution_window.show()
            self.loading_window.destroy()
            parent_window.destroy()

    def set_configuration_window_images(self):
        self.cw_toy_images_1 =[[self.cw_ball_1_0_0, self.cw_ball_1_0_1, self.cw_ball_1_0_2, self.cw_ball_1_0_3],
                              [self.cw_ball_1_1_0, self.cw_ball_1_1_1, self.cw_ball_1_1_2, self.cw_ball_1_1_3],
                              [self.cw_ball_1_2_0, self.cw_ball_1_2_1, self.cw_ball_1_2_2, self.cw_ball_1_2_3],
                              [self.cw_ball_1_3_0, self.cw_ball_1_3_1, self.cw_ball_1_3_2, self.cw_ball_1_3_3],
                              [self.cw_ball_1_4_0, self.cw_ball_1_4_1, self.cw_ball_1_4_2, self.cw_ball_1_4_3]]

        self.cw_toy_images_2 =[[self.cw_ball_2_0_0, self.cw_ball_2_0_1, self.cw_ball_2_0_2, self.cw_ball_2_0_3],
                              [self.cw_ball_2_1_0, self.cw_ball_2_1_1, self.cw_ball_2_1_2, self.cw_ball_2_1_3],
                              [self.cw_ball_2_2_0, self.cw_ball_2_2_1, self.cw_ball_2_2_2, self.cw_ball_2_2_3],
                              [self.cw_ball_2_3_0, self.cw_ball_2_3_1, self.cw_ball_2_3_2, self.cw_ball_2_3_3],
                              [self.cw_ball_2_4_0, self.cw_ball_2_4_1, self.cw_ball_2_4_2, self.cw_ball_2_4_3]]

    def set_solution_window_images(self):
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball1"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball2"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball3"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball4"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball5"))

    def load_configuration_matrix(self, matrix, matrix_id):
        i = 0
        j = 0
        array = self.cw_toy_images_1
        if(matrix_id == 2):
            array = self.cw_toy_images_2
        for i in range(0, 5):
            for j in range(0, 4):
                self.matrix_info[matrix_id][self.color_counter[matrix[i][j]]] += 1
                image = utilities.get_matrix_image_name(matrix[i][j])
                gtk_object = array[i][j]
                gtk_object.set_from_file(image)

    def load_solution_matrix(self):
        index = 0
        for operation_set in self.solution_grids[0]:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = self.sw_toy_images[index]
            gtk_object.set_from_file('img/' + image)
            index += 1
        self.print_step()


    def paint_matrix(self, matrix, images, id=0):
        index = 0
        print("\n")
        for operation_set in matrix:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = images[index + id]
            gtk_object.set_from_file('img/' + image)
            index += 1
            print(operation_set)

    def paint_solution_matrix(self, matrix, id=0):
        index = 0
        print("\n")
        for operation_set in matrix[id]:
            image = utilities.get_image_name(operation_set[self.current_face])
            gtk_object = self.sw_toy_images[index]
            gtk_object.set_from_file('img/' + image)
            index += 1
            print(operation_set)

    def print_step(self):
        if (self.movements):
            text = utilities.get_movement_description(self.movements[self.movement_index])
            self.description_label.set_text(text)
