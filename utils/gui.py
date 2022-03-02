

import dearpygui.dearpygui as dpg

class GuiHandler:

    def __init__(self):
        self.queue = {}



    def send_vars(self, shader):
        for key in self.queue:
            shader.set(key, self.queue[key])

        self.queue.clear()


    def exposureCB(self, sender, data):
        self.queue["exposure"] = data

    def guiCallBack(self, sender, data, key="exposure"):
        self.queue[key] = data


    def add_slider_exposure(self, parent=0, max_value=100.0, default_value=1.0, format="exposure = %.1f"):
        dpg.add_slider_float(parent=parent, max_value=max_value,
                            default_value=default_value, format=format,
                            callback=self.exposureCB)
        self.queue["exposure"] = float(default_value)

    def add_slider_float(self, parent=0, max_value=100.0, default_value=1.0, format="exposure = %.1f", key="exposure"):
        dpg.add_slider_float(parent=parent, max_value=max_value,
                            default_value=default_value, format=format,
                            callback=lambda s, d: self.guiCallBack(s,d,key=key))
        self.queue[key] = float(default_value)
