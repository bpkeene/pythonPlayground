#********************************************************************************
#   Cassandra - An open source atomistic Monte Carlo software package
#   developed at the University of Notre Dame.
#   http://cassandra.nd.edu
#   Prof. Edward Maginn <ed@nd.edu>
#   Copyright (2013) University of Notre Dame du Lac
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#********************************************************************************
#
#   Created by Brian Keene on February 4, 2015
#
#   Revision history:
#   23 July 2015 - (BK) rewrote
#   8 September 2016 - (BK) implemented template resources
#
#********************************************************************************

# import the resources from GUI_Template
from GUI_Template import *

######################################################################################
# SECTION 1: Creation of the main frame object and accompanying panels
######################################################################################
#
# MainFrame: the top level window that holds all objects
# TopPanel: the top level panel that we can put other widgets/notebooks etc on
# TopNotebook: holds the other panels in the style that we want
# PanelOne: the "Basic Information" panel
# PanelTwo: the "Interaction Parameters" panel
# PanelThree: the "Probabilities Information" panel
# PanelFour: the "File Handling" panel
#
######################################################################################

# change 'size' to any tuple of integers; this variable denotes the size, in
# pixels, that the frame (GUI) will appear on the user's screen
size = (900,620);
MainFrame = Frame(None,"Cassandra Input File Editor v1.2",size);

TopPanel = Panel(MainFrame);
TopNotebook = Notebook(TopPanel);

PanelOne = Panel(TopNotebook,name="Basic Information");
PanelTwo = Panel(TopNotebook,name="Interaction Parameters");
PanelThree = Panel(TopNotebook,name="Probabilities Information");
PanelFour = Panel(TopNotebook,name="File Handling");
######################################################################################





######################################################################################
# SECTION 2: Creation of subnotebooks
######################################################################################
#
# The main panels have smaller sections in them that allow for easier navigation
# of the GUI.  Here, we create notebooks to hold these sections, and provide
# names for the panels that will then appear on the bar atop the notebooks or
# panels.
#
# PanelOneNotebook: holds subpanels of "Basic Information"
# PanelTwoNotebook: holds subpanels of "Interaction Parameters"
# PanelThreeNotebook: holds subpanels of "Probabilities Information"
# PanelFourNotebook: holds subpanels of "File Handling"
#
# PanelOnePageOne: a subpanel of PanelOneNotebook, titled "Page 1"
# PanelOnePageTwo: a subpanel of PanelOneNotebook, titled "Page 2"
# and etc. for the remaining notebooks and subpanels.
#
#######################################################################################

# create the notebooks that will hold the subpanels
PanelOneNotebook = Notebook(PanelOne);
PanelTwoNotebook = Notebook(PanelTwo);
PanelThreeNotebook = Notebook(PanelThree);
PanelFourNotebook = Notebook(PanelFour);

# the pages of the panel one notebook, "Basic Information"
PanelOnePageOne = Panel(PanelOneNotebook,name="Page 1")
PanelOnePageTwo = Panel(PanelOneNotebook,name="Page 2")

# the pages of the panel two notebook, "Interaction Parameters"
PanelTwoIntramolecular = Panel(PanelTwoNotebook,name="Intramolecular")
PanelTwoIntermolecular = Panel(PanelTwoNotebook,name="Intermolecular")

# the pages of the panel three notebook, "Probabilities Information"
PanelThreeTranslation = Panel(PanelThreeNotebook,name="Translation")
PanelThreeRotation = Panel(PanelThreeNotebook,name="Rotation")
PanelThreeRegrowth = Panel(PanelThreeNotebook,name="Regrowth")
PanelThreeVolume = Panel(PanelThreeNotebook,name="Volume")
PanelThreeInsertion = Panel(PanelThreeNotebook,name="Insertion")
PanelThreeSwap = Panel(PanelThreeNotebook,name="Swap")

# the pages of the panel four notebook, "File Handling"
PanelFourMoleculeFiles = Panel(PanelFourNotebook,name="Molecule Files")
PanelFourFragmentFiles = Panel(PanelFourNotebook,name="Fragment Files")
PanelFourInputFile = Panel(PanelFourNotebook,name="Input File")
PanelFourOutputFile = Panel(PanelFourNotebook,name="Output File")

######################################################################################




######################################################################################
# SECTION 3.2: Definition of Global Functions for Widgets
######################################################################################
# Widgets (and graphical user interfaces) are event-based applications.
# The widgets process user input - clicks, keyboard strokes, etc. -
# and translate these into responses determined by the function(s) to which
# the widget and other sibling or parent objects are bound.
# Here, we define global default functions;
# Individual widgets can use different functions and be bound to them;
# These are provided for ease of use
######################################################################################

# proof of concept - define a function in this script, bind and use in the template
# to print out to terminal what we type in the text widget.

# default behavior for text widget objects
def defaultTextFunction(event):
    obj = event.GetEventObject();
    objKeyword = str(obj._sibling)
    val = str(event.GetString())

    print objname, val



######################################################################################
# SECTION 4.1: Addition of widgets to PanelOnePageOne
######################################################################################
# PanelOnePageOne is the panel to which the graphical user interface opens.
# This panel is special in that it incorporates some navigational restrictions,
# based on the current values of the widgets on the page! These restrictions are
# enforced by (syntax here)
#
# PanelOnePageOne:
#       - Run Name text
#       - Directory dialog (button)
#       - Ensemble choice
#       - Number of Species choice
#       - Create Input file button
#
######################################################################################

# lists of options for the choice widgets on this panel
numberOfSpeciesChoices = ["","1","2","3","4","5","6"]
ensembleChoices = ["", "NVT_MC","NVT_MIN","NPT_MC","GCMC","GEMC","GEMC_NPT"]

# the text widget asking for the run name
runNameWidget = Widget(PanelOnePageOne,widgetType="text",name="runName", pos=(3,2), \
        label="Run Name: ", labelPos=(3,1))

# a button (with label) from which the user may select the simulation directory
simulationDirectoryWidget = Widget(PanelOnePageOne,widgetType="button", name="Select Directory", \
        pos=(4,2), label="Simulation Directory: ", labelPos=(4,1))

# a choice widget (drop down menu) from which the user may select one of Cassandra's ensembles
ensembleWidget = Widget(PanelOnePageOne,widgetType="choice",name="# Sim_Type", \
        pos=(5,2), label="Ensemble: ", labelPos=(5,1),choices=ensembleChoices)

# a choice widget from which the number of species in simulation may be selected
numberOfSpeciesWidget = Widget(PanelOnePageOne,widgetType="choice",name="", \
        pos=(6,2), label="Number of Species: ",labelPos=(6,1),choices=numberOfSpeciesChoices)

# a button which creates the input file in the simulation directory
makeInputFileWidget = Widget(PanelOnePageOne,widgetType="button",name="Create Input File", \
        pos=(12,2))

# a string we place on the panel
string1= "Have you completed all prompts on all pages? "
staticText1 = Widget(PanelOnePageOne,widgetType="static",name=string1,\
        pos=(11,1),span=(1,3))

# another string
string2 ="If so, click here:"
staticText2 = Widget(PanelOnePageOne,widgetType="static",name=string2, \
        pos=(12,1),span=(1,1))

# set the functions to which these widgets will respond; some of them will be standard,
# others are specific to a given widget

######################################################################################

# initiate the event loop, and instruct the main frame to show!
# this causes a cascade of instantiations - at this point, all objects must be declared.
if __name__ == "__main__":
    app = wx.App()
    MainFrame.initObj()
    app.MainLoop()


