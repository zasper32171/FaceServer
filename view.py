import tkinter


class View(tkinter.Tk):

    def __init__(self):

        tkinter.Tk.__init__(self)
        self._manager = None

    def set_manager(self, manager):

        self._manager = manager

    def start(self):

        pass

    def stop(self):

        pass
