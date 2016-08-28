# proof of concept importing the template and setting up the GUI in a process
# similar to lammps input file script

from GUI_Template import *


app = wx.App(False)
thisFrame = Frame();

firstPanelObj = Panel(thisFrame)

runName = Widget("runName",(5,1),text);
runName.instantiateWidget(firstPanelObj)
#firstPanelNames = ["runName", "simulationDirectory", "ensemble", "numberOfSpecies"]
#firstPanelLabels = ["Run Name: ", "Simulation Directory: ", "Ensemble: ", "Number of Species: "]
#firstPanelCoords = [(3,3), (4,3), (5,3), (6,3)]
#firstPanelSpans = [(1,1), (1,1), (1,1), (1,1)]
#firstPanelWidgetTypes = ["textWidget", "button", "choice", "choice"]
#widgetsOne = []
#for index, item in enumerate(firstPanelNames):
#  widgetsOne.append(Widget(name = firstPanelNames[index], coords = firstPanelCoords[index], \
#                            widgetType = firstPanelWidgetTypes[index], span = firstPanelSpans[index],\
#                            label = firstPanelLabels[index], labelPosition = "left"))




# here try to print the objects we've added to the Panel object
#for child in firstPanelObj.__subclasses__():
    #print child.name
thisFrame.Show()
app.MainLoop()

