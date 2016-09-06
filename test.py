# proof of concept importing the template and setting up the GUI in a process
# similar to lammps input file script

from GUI_Template import *

# utf-encoded angstroms unit, for use in labels on the GUI

# the size of the main frame - adjust here to change size of the GUI on the screen;
# must be an integer tuple
size = (640,480);
# the main frame is a bet special; we can't actually create the object until the app is finished
thisFrame = MainFrame(None,"Hello World",size);


# let's try adding a simple panel with the first few widgets;
# first, we'll need to make the panel, then the notebook, then the other panels...
# and then we place the widgets on that bottom panel

# let's make some pseudocode; ideally, the only thing the next person maintaining should have to do
# is provide arguments (including the variable name of the parent object) and some preliminary information



#topLevelPanel = Panel(*args)
#topLevelNotebook = Notebook(*args)
#PanelOneA = Panel(*args)
#fakeWidget
# don't we need names for all the widgets though? I think so..

# initiate the event loop, and instruct the main frame to show!
if __name__ == "__main__":
    app = wx.App()
    thisFrame.initFrame()
    app.MainLoop()


