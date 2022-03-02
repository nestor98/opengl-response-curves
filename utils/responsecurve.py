import csv
import numpy as np
import math
import os

from OpenGL.GL import *

import dearpygui.dearpygui as dpg


class ResponseCurve:

    def __init__(self, path):
        """
        path is the path to the curve.csv
        """
        self.load(path)
        self.waiting_send=False

    def load(self, path):
        with open(path, mode='r') as csv_curve:
            self.name = os.path.splitext(os.path.basename(path))[0]
            csv_reader = csv.reader(csv_curve)
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # First row are the wavelengths
                    # TODO: im usually assuming the range is the same for all the
                    # cameras (true for these csvs)
                    self.c_wl_samples = len(row)
                    self.c_wl_min = row[0]
                    self.c_wl_min = float(self.c_wl_min)
                    self.c_wl_max = row[self.c_wl_samples-1]
                    self.c_wl_max = float(self.c_wl_max)
                    print("Curve spectrum: {}..{} nm ({} samples).\n".format(self.c_wl_min,self.c_wl_max,self.c_wl_samples))
                if line_count == 1: # X or R values
                    a_values = row
                if line_count == 2: # Y or G values
                    b_values = row
                if line_count == 3: # Z or B values
                    c_values = row
                line_count += 1
            if (len(a_values) != self.c_wl_samples or len(b_values) != self.c_wl_samples or len(c_values) != self.c_wl_samples):
                print("ERROR: There must be {} values in second, thrid and fourth rows.".format(self.c_wl_samples))
                sys.exit(2)

            self.curve = np.vstack((a_values, b_values, c_values)).astype(np.float32)


    def send_curve(self, uniform_location):
        """ sends the curve data to opengl """
        glUniform3fv(uniform_location, self.curve.shape[1], self.curve.T)

    def check_send_curve(self, uniform_location):
        """ sends the curve only if it has changed """
        if self.waiting_send:
            self.waiting_send=False
            self.send_curve(uniform_location)

    # ----------------------------------------------------------------------
    # From here, just GUI:
    def file_callback(self, sender, app_data):
        """
        sender will have the dpg key for the widget that called this (we dont care)
        app_data is a dictionary with the returned info (with the path)
        """
        path = app_data['file_path_name']
        self.load(path) # load the new curve
        self.update_gui() # update the plot
        self.waiting_send=True # cant directly send as this is asynchronous

    def update_gui(self, onlyData=False):
        """ updates the plot after changing the curves """
        if onlyData:
            dpg.set_value("x_series", [self.datax, self.curve[0,:]])
            dpg.set_value("y_series", [self.datax, self.curve[1,:]])
            dpg.set_value("z_series", [self.datax, self.curve[2,:]])
        else:
            dpg.delete_item("curveplot", children_only=False)
            self.add_curve_plot()

    def add_curve_plot(self):
        """ adds the plot of the 3 curves """
        with dpg.plot(label=self.name, height=400, width=400, anti_aliased=True, tag="curveplot", parent="curve_window"):
            # optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="wavelength")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

            # series belong to a y axis
            # print(self.curve[0,:])
            dpg.add_line_series(self.datax, self.curve[2,:], label="B curve", parent="y_axis", id="z_series")
            dpg.add_line_series(self.datax, self.curve[0,:], label="R curve", parent="y_axis", id="x_series")
            dpg.add_line_series(self.datax, self.curve[1,:], label="G curve", parent="y_axis", id="y_series")


    def setup_gui(self):
        """ sets up the gui """
        dpg.create_context()

        with dpg.file_dialog(directory_selector=False, show=False, height=300, default_path="response-curves", callback=self.file_callback, tag="file_dialog_id"):
            dpg.add_file_extension(".csv")

        self.datax = np.linspace(self.c_wl_min, self.c_wl_max, self.c_wl_samples)

        window_tag = "curve_window"
        with dpg.window(label="Settings", tag=window_tag):
            dpg.add_button(label="Change response curve", callback=lambda: dpg.show_item("file_dialog_id"))
            # this will contain the plot
        # created/updatet by this:
        # self.add_curve_plot()

        dpg.create_viewport(title='Settings', width=450, height=550)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return window_tag
