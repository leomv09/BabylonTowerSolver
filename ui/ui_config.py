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

class AppGTK:
    """ Class that handles the graphic user interface components. """
    def __init__(self):
        """ Initializes the components.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.start_matrix = [['*', '-', '-', '-'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y']]
        self.end_matrix = [['*', '-', '-', '-'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y']]
        self.current_index_row_0 = 0
        self.current_index_row_1 = 0
        self.current_index_row_2 = 0
        self.current_index_row_3 = 0
        self.current_index_row_4 = 0
        self.movement_index = 0
        self.solution_grids_index = 0
        self.indexes = [self.current_index_row_0, self.current_index_row_1, self.current_index_row_2, self.current_index_row_3, self.current_index_row_4]
        self.matrix_1_selected_color = ""
        self.matrix_2_selected_color = ""
        self.matrix_1_red_counter = 0
        self.matrix_1_green_counter = 0
        self.matrix_1_blue_counter = 0
        self.matrix_1_yellow_counter = 0
        self.matrix_1_wildcard_counter = 0
        self.matrix_2_red_counter = 0
        self.matrix_2_green_counter = 0
        self.matrix_2_blue_counter = 0
        self.matrix_2_yellow_counter = 0
        self.matrix_2_wildcard_counter = 0
        self.cw_toy_images = []
        self.sw_toy_images = []

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

        self.connect_windows_signals()
        self.set_start_window_buttons()
        self.set_configuration_window_buttons()
        self.set_solution_window_buttons()
        self.set_configuration_window_images()

        if(self.cw_start_button):
            self.cw_start_button.connect("clicked", self.start_solution_window, self.solution_window, self.configuration_window)


    def connect_windows_signals(self):
        """ Connects the quit signail to the windows.
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
        if(self.loading_window):
            self.loading_window.connect("destroy", gtk.Widget.destroy)
        if(self.user_manual_window):
            self.user_manual_window.connect("destroy", gtk.Widget.destroy)

    def set_start_window_buttons(self):
        """ Obtains all the buttons from the start window XML file.
        sw = start window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.create_configuration_button = self.start_window_builder.get_object("menu_button_create_config")
        self.open_file_dialog = self.start_window_builder.get_object("file_chooser_button")
        self.load_file_button = self.start_window_builder.get_object("load_file_button")
        self.set_filter()
        self.load_file_button.connect("clicked", self.open_config_from_file)
        if(self.create_configuration_button):
            self.create_configuration_button.connect("clicked", self.start_configuration_window, self.configuration_window, self.main_window)

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
            self.load_configuration_matrix(self.start_matrix)
            self.load_configuration_matrix(self.end_matrix, 5)
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
        #Selection Colors
        self.cw_matrix_1_select_red = self.configuration_window_builder.get_object("select_red_ball_button_1")
        self.cw_matrix_1_select_red.connect("clicked", self.change_selected_color, 1, 'R')
        self.cw_matrix_1_select_green = self.configuration_window_builder.get_object("select_green_ball_button_1")
        self.cw_matrix_1_select_green.connect("clicked", self.change_selected_color, 1, 'G')
        self.cw_matrix_1_select_blue = self.configuration_window_builder.get_object("select_blue_ball_button_1")
        self.cw_matrix_1_select_blue.connect("clicked", self.change_selected_color, 1, 'B')
        self.cw_matrix_1_select_yellow = self.configuration_window_builder.get_object("select_yellow_ball_button_1")
        self.cw_matrix_1_select_yellow.connect("clicked", self.change_selected_color, 1, 'Y')
        self.cw_matrix_1_select_widlcard = self.configuration_window_builder.get_object("select_wildcard_button_1")
        self.cw_matrix_1_select_widlcard.connect("clicked", self.change_selected_color, 1, '*')
        self.cw_matrix_2_select_red = self.configuration_window_builder.get_object("select_red_ball_button_2")
        self.cw_matrix_2_select_red.connect("clicked", self.change_selected_color, 2, 'R')
        self.cw_matrix_2_select_green = self.configuration_window_builder.get_object("select_green_ball_button_2")
        self.cw_matrix_2_select_green.connect("clicked", self.change_selected_color, 2, 'G')
        self.cw_matrix_2_select_blue = self.configuration_window_builder.get_object("select_blue_ball_button_2")
        self.cw_matrix_2_select_blue.connect("clicked", self.change_selected_color, 2, 'B')
        self.cw_matrix_2_select_yellow = self.configuration_window_builder.get_object("select_yellow_ball_button_2")
        self.cw_matrix_2_select_yellow.connect("clicked", self.change_selected_color, 2, 'Y')
        self.cw_matrix_2_select_widlcard = self.configuration_window_builder.get_object("select_wildcard_button_2")
        self.cw_matrix_2_select_widlcard.connect("clicked", self.change_selected_color, 2, '*')

        #Matrix buttons
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
        #Matrix 2
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

    def show_next_solution(self, widget):
        if(not self.movement_index + 1 > len(self.movements)-1):
            self.movement_index += 1
            self.print_step()
        if(not self.solution_grids_index +1 > len(self.solution_grids)-1):
            self.solution_grids_index +=1
            self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def show_previous_solution(self, widget):
        if(not self.movement_index - 1 < 0):
            self.movement_index -=1
            self.print_step()
        if(not self.solution_grids_index - 1 < 0):
            self.solution_grids_index -=1
            self.paint_solution_matrix(self.solution_grids, self.solution_grids_index)

    def show_user_manual(self):
        content_label = self.user_manual_window.get_object("content_label")
        content_label.set_text(utilities.readFile("user_manual.txt"))

    def change_selected_color(self, widget, matrix_id, color_id):
        if(matrix_id == 1):
            self.matrix_1_selected_color = utilities.get_matrix_image_name(color_id)
            self.cw_matrix_1_selected_color.set_from_file(self.matrix_1_selected_color)
        else:
            self.matrix_2_selected_color = utilities.get_matrix_image_name(color_id)
            self.cw_matrix_2_selected_color.set_from_file(self.matrix_2_selected_color)

    def put_selected_color(self, widget, matrix_id, image_object, row, col):
        if matrix_id == 1:
            selected_color = utilities.get_operation_name(self.matrix_1_selected_color)
            if selected_color == 'R':
                if self.matrix_1_red_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('R'))
                    self.matrix_1_red_counter += 1
            elif selected_color == 'G':
                if self.matrix_1_green_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('G'))
                    self.matrix_1_green_counter += 1
            elif selected_color == 'B':
                if self.matrix_1_blue_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('B'))
                    self.matrix_1_blue_counter += 1
            elif selected_color == 'Y':
                if self.matrix_1_yellow_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('Y'))
                    self.matrix_1_yellow_counter += 1
            elif selected_color == '*':
                if self.matrix_1_wildcard_counter < 1:
                    image_object.set_from_file(utilities.get_matrix_image_name('*'))
                    self.matrix_1_wildcard_counter += 1
            self.start_matrix[row][col] = selected_color

        else:
            selected_color = utilities.get_operation_name(self.matrix_2_selected_color)
            if selected_color == 'R':
                if self.matrix_2_red_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('R'))
                    self.matrix_2_red_counter += 1
            if selected_color == 'G':
                if self.matrix_2_green_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('G'))
                    self.matrix_2_green_counter += 1
            if selected_color == 'B':
                if self.matrix_2_blue_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('B'))
                    self.matrix_2_blue_counter += 1
            if selected_color == 'Y':
                if self.matrix_2_yellow_counter < 4:
                    image_object.set_from_file(utilities.get_matrix_image_name('Y'))
                    self.matrix_2_yellow_counter += 1
            if selected_color == '*':
                if self.matrix_2_wildcard_counter < 1:
                    image_object.set_from_file(utilities.get_matrix_image_name('*'))
                    self.matrix_2_wildcard_counter += 1
            self.end_matrix[row][col] = selected_color

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
        self.matrix_1_red_counter = 0
        self.matrix_1_green_counter = 0
        self.matrix_1_blue_counter = 0
        self.matrix_1_yellow_counter = 0
        self.matrix_1_wildcard_counter = 0


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
        self.matrix_2_red_counter = 0
        self.matrix_2_green_counter = 0
        self.matrix_2_blue_counter = 0
        self.matrix_2_yellow_counter = 0
        self.matrix_2_wildcard_counter = 0



    def start_configuration_window(self, widget, config_window, parent_window):
        """ Shows the configuration window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if(config_window and parent_window):
            #self.load_configuration_matrix(self.start_matrix)
            #self.load_configuration_matrix(self.end_matrix, 5)
            config_window.show()

    def start_solution_window(self, widget, solution_window, parent_window):
        """ Shows the solution window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if(solution_window and parent_window):
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
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball1"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball2"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball3"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball4"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball5"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball6"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball7"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball8"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball9"))
        self.cw_toy_images.append(self.configuration_window_builder.get_object("ball10"))


    def set_solution_window_images(self):
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball1"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball2"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball3"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball4"))
        self.sw_toy_images.append(self.solution_window_builder.get_object("ball5"))


    def load_configuration_matrix(self, matrix, number=0):
        index = 0
        for operation_set in matrix:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = self.cw_toy_images[index+number]
            gtk_object.set_from_file('img/'+image)
            index += 1

    def load_solution_matrix(self):
        index = 0
        for operation_set in self.solution_grids[0]:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = self.sw_toy_images[index]
            gtk_object.set_from_file('img/'+image)
            index += 1
        self.print_step()


    def configuration_move_right_row(self, widget, id, matrix_number=1):
        if(matrix_number == 1):
            count = len(self.start_matrix[id]) - 1
            last = self.start_matrix[id].pop(count)
            self.start_matrix[id].insert(0, last)
            self.paint_matrix(self.start_matrix, self.cw_toy_images)
        else:
            count = len(self.end_matrix[id]) - 1
            last = self.end_matrix[id].pop(count)
            self.end_matrix[id].insert(0, last)
            self.paint_matrix(self.end_matrix, self.cw_toy_images, 5)

    def configuration_move_left_row(self, widget, id, matrix_number=1):
        if(matrix_number == 1):
            first = self.start_matrix[id].pop(0)
            self.start_matrix[id].append(first)
            self.paint_matrix(self.start_matrix, self.cw_toy_images)
        else:
            first = self.end_matrix[id].pop(0)
            self.end_matrix[id].append(first)
            self.paint_matrix(self.end_matrix, self.cw_toy_images, 5)


    def move_upward(self, widget, matrix_number=1):
        if(matrix_number == 1):
            if(utilities.has_upward_moves(self.start_matrix)):
                self.start_matrix = utilities.move_upward(self.start_matrix)
                self.paint_matrix(self.start_matrix, self.cw_toy_images)
            else:
                print("No moves")
        else:
            if(utilities.has_upward_moves(self.end_matrix)):
                self.end_matrix = utilities.move_upward(self.end_matrix)
                self.paint_matrix(self.end_matrix, self.cw_toy_images, 5)
            else:
                print("No moves")


    def move_downward(self, widget, matrix_number=1):
        if(matrix_number == 1):
            if(utilities.has_downward_moves(self.start_matrix)):
                self.start_matrix = utilities.move_downward(self.start_matrix)
                self.paint_matrix(self.start_matrix, self.cw_toy_images)
            else:
                print("No moves")
        else:
            if(utilities.has_downward_moves(self.end_matrix)):
                self.end_matrix = utilities.move_downward(self.end_matrix)
                self.paint_matrix(self.end_matrix, self.cw_toy_images, 5)
            else:
                print("No moves")


    def paint_matrix(self, matrix, images, id=0):
        index = 0
        print("\n")
        for operation_set in matrix:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = images[index+id]
            gtk_object.set_from_file('img/'+image)
            index += 1
            print(operation_set)

    def paint_solution_matrix(self, matrix, id=0):
        index = 0
        print("\n")
        for operation_set in matrix[id]:
            image = utilities.get_image_name(operation_set[0])
            gtk_object = self.sw_toy_images[index]
            gtk_object.set_from_file('img/'+image)
            index += 1
            print(operation_set)

    def print_step(self):
        if (self.movements):
            text = utilities.get_movement_description(self.movements[self.movement_index])
            self.description_label.set_text(text)
