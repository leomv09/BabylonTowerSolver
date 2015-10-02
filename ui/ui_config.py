import sys
import pygtk
pygtk.require("2.0")
import gtk
import utilities
import file_parser
import os.path, sys
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
        self.startMatrix1 = [['*', '-', '-', '-'], ['B', 'R', 'Y', 'G'], ['B', 'Y', 'R', 'G'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y']]
        self.startMatrix2 = [['*', '-', '-', '-'], ['B', 'R', 'Y', 'G'], ['B', 'Y', 'R', 'G'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y']]
        self.current_index_row_0 = 0
        self.current_index_row_1 = 0
        self.current_index_row_2 = 0
        self.current_index_row_3 = 0
        self.current_index_row_4 = 0
        self.movement_index = 0
        self.solution_grids_index = 0
        self.indexes = [self.current_index_row_0, self.current_index_row_1, self.current_index_row_2, self.current_index_row_3, self.current_index_row_4]
        
        self.cw_toy_images = []
        self.sw_toy_images = []
        
        self.start_window_builder = gtk.Builder()
        self.configuration_window_builder = gtk.Builder()
        self.solution_window_builder = gtk.Builder()
        self.loading_window_builder = gtk.Builder()
        self.user_manual_window_builder = gtk.Builder()
        
        self.start_window_builder.add_from_file("start_window.glade")
        self.configuration_window_builder.add_from_file("configuration_window.glade")
        self.solution_window_builder.add_from_file("solution_window.glade")
        self.loading_window_builder.add_from_file("loading_window.glade")
        self.user_manual_window_builder.add_from_file("user_manual.glade")
        
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
        if(file_name):
            data = file_parser.parse_file(file_name)
            self.startMatrix1 = data
            self.load_congiguration_matrix(self.startMatrix1)
            self.load_congiguration_matrix(self.startMatrix2, 5)
            self.configuration_window.show()
            
    def set_configuration_window_buttons(self):
        """ Obtains all the buttons from the configuration window XML file.
        cw = configuration window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.cw_upward_button = self.configuration_window_builder.get_object("upward_button")
        self.cw_upward_button2 = self.configuration_window_builder.get_object("upward_button2")
        self.cw_upward_button.connect("clicked", self.move_upward)
        self.cw_upward_button2.connect("clicked", self.move_upward, 2)
        self.cw_downward_button = self.configuration_window_builder.get_object("downward_button")
        self.cw_downward_button2 = self.configuration_window_builder.get_object("downward_button2")
        self.cw_downward_button.connect("clicked", self.move_downward)
        self.cw_downward_button2.connect("clicked", self.move_downward, 2)
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

        self.cw_forward_button1.connect("clicked", self.configuration_move_right_row, 0, 1)
        self.cw_forward_button2.connect("clicked", self.configuration_move_right_row, 1, 1)
        self.cw_forward_button3.connect("clicked", self.configuration_move_right_row, 2, 1)
        self.cw_forward_button4.connect("clicked", self.configuration_move_right_row, 3, 1)
        self.cw_forward_button5.connect("clicked", self.configuration_move_right_row, 4, 1)

        self.cw_backward_button1.connect("clicked", self.configuration_move_left_row, 0, 1)
        self.cw_backward_button2.connect("clicked", self.configuration_move_left_row, 1, 1)
        self.cw_backward_button3.connect("clicked", self.configuration_move_left_row, 2, 1)
        self.cw_backward_button4.connect("clicked", self.configuration_move_left_row, 3, 1)
        self.cw_backward_button5.connect("clicked", self.configuration_move_left_row, 4, 1)

        self.cw_backward_button6 = self.configuration_window_builder.get_object("backward_button6")
        self.cw_backward_button7 = self.configuration_window_builder.get_object("backward_button7")
        self.cw_backward_button8 = self.configuration_window_builder.get_object("backward_button8")
        self.cw_backward_button9 = self.configuration_window_builder.get_object("backward_button9")
        self.cw_backward_button10 = self.configuration_window_builder.get_object("backward_button10")
        
        self.cw_forward_button6 = self.configuration_window_builder.get_object("forward_button6")
        self.cw_forward_button7 = self.configuration_window_builder.get_object("forward_button7")
        self.cw_forward_button8 = self.configuration_window_builder.get_object("forward_button8")
        self.cw_forward_button9 = self.configuration_window_builder.get_object("forward_button9")
        self.cw_forward_button10 = self.configuration_window_builder.get_object("forward_button10")

        self.cw_forward_button6.connect("clicked", self.configuration_move_right_row, 0, 2)
        self.cw_forward_button7.connect("clicked", self.configuration_move_right_row, 1, 2)
        self.cw_forward_button8.connect("clicked", self.configuration_move_right_row, 2, 2)
        self.cw_forward_button9.connect("clicked", self.configuration_move_right_row, 3, 2)
        self.cw_forward_button10.connect("clicked", self.configuration_move_right_row, 4, 2)

        self.cw_backward_button6.connect("clicked", self.configuration_move_left_row, 0, 2)
        self.cw_backward_button7.connect("clicked", self.configuration_move_left_row, 1, 2)
        self.cw_backward_button8.connect("clicked", self.configuration_move_left_row, 2, 2)
        self.cw_backward_button9.connect("clicked", self.configuration_move_left_row, 3, 2)
        self.cw_backward_button10.connect("clicked", self.configuration_move_left_row, 4, 2)
    
    def set_solution_window_buttons(self):
        """ Obtains all the buttons from the solution XML file
        sw = solution window.
        parameters:
            [AppGTK] self -- the self instance.
        """
        self.sow_upward_button = self.solution_window_builder.get_object("upward_button")
        self.sow_downward_button = self.solution_window_builder.get_object("downward_button")
        
        self.sow_backward_button1 = self.solution_window_builder.get_object("backward_button1")
        self.sow_backward_button2 = self.solution_window_builder.get_object("backward_button2")
        self.sow_backward_button3 = self.solution_window_builder.get_object("backward_button3")
        self.sow_backward_button4 = self.solution_window_builder.get_object("backward_button4")
        self.sow_backward_button5 = self.solution_window_builder.get_object("backward_button5")
        
        self.sow_forward_button1 = self.solution_window_builder.get_object("forward_button1")
        self.sow_forward_button2 = self.solution_window_builder.get_object("forward_button2")
        self.sow_forward_button3 = self.solution_window_builder.get_object("forward_button3")
        self.sow_forward_button4 = self.solution_window_builder.get_object("forward_button4")
        self.sow_forward_button5 = self.solution_window_builder.get_object("forward_button5")

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
        
    
    def start_configuration_window(self, widget, config_window, parent_window):
        """ Shows the configuration window.
        parameters:
            [AppGTK] self -- the self instance.
            [gtk.Widget] widget -- the widget event.
            [gtk.Object] config_window -- The configuration window object.
            [gtk.Object] config_window -- The start window object(parent).
        """
        if(config_window and parent_window):
            self.load_congiguration_matrix(self.startMatrix1)
            self.load_congiguration_matrix(self.startMatrix2, 5)
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
            self.loading_window.show()
            start = core.babylon_node.BabylonNode(self.startMatrix1)
            goal = core.babylon_node.BabylonNode(self.startMatrix2)
            algorithm = core.astar.AStar()
            self.movements = algorithm.movements_between(start, goal)
            self.solution_grids = algorithm.grids_between(start, goal)
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


    def load_congiguration_matrix(self, matrix, number=0):
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
            count = len(self.startMatrix1[id]) - 1
            last = self.startMatrix1[id].pop(count)
            self.startMatrix1[id].insert(0, last)
            self.paint_matrix(self.startMatrix1, self.cw_toy_images)
        else:
            count = len(self.startMatrix2[id]) - 1
            last = self.startMatrix2[id].pop(count)
            self.startMatrix2[id].insert(0, last)
            self.paint_matrix(self.startMatrix2, self.cw_toy_images, 5)

    def configuration_move_left_row(self, widget, id, matrix_number=1):
        if(matrix_number == 1):
            first = self.startMatrix1[id].pop(0)
            self.startMatrix1[id].append(first)
            self.paint_matrix(self.startMatrix1, self.cw_toy_images)
        else:
            first = self.startMatrix2[id].pop(0)
            self.startMatrix2[id].append(first)
            self.paint_matrix(self.startMatrix2, self.cw_toy_images, 5)


    def move_upward(self, widget, matrix_number=1):
        if(matrix_number == 1):
            if(utilities.has_upward_moves(self.startMatrix1)):
                self.startMatrix1 = utilities.move_upward(self.startMatrix1)
                self.paint_matrix(self.startMatrix1, self.cw_toy_images)
            else:
                print("No moves")
        else:
            if(utilities.has_upward_moves(self.startMatrix2)):
                self.startMatrix2 = utilities.move_upward(self.startMatrix2)
                self.paint_matrix(self.startMatrix2, self.cw_toy_images, 5)
            else:
                print("No moves")

                
    def move_downward(self, widget, matrix_number=1):
        if(matrix_number == 1):
            if(utilities.has_downward_moves(self.startMatrix1)):
                self.startMatrix1 = utilities.move_downward(self.startMatrix1)
                self.paint_matrix(self.startMatrix1, self.cw_toy_images)
            else:
                print("No moves")
        else:
            if(utilities.has_downward_moves(self.startMatrix2)):
                self.startMatrix2 = utilities.move_downward(self.startMatrix2)
                self.paint_matrix(self.startMatrix2, self.cw_toy_images, 5)
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
        text = utilities.get_movement_description(self.movements[self.movement_index])
        self.description_label.set_text(text)
        
                

