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

# import the needed modules
import wx, os

# global dictionary in which we store data
myDict = {}

#********************************************************************************
# Custom classes wrapping wxWidgets objects
#********************************************************************************

class wxFrame(wx.Frame):
    # note to others: we pass another class (an instance of Frame) to this wx.Frame derived class;
    # the ambiguity of parent in the class __init__ vs the wx.Frame.__init__ is due to parent in the
    # wx.Frame.__init__ function being a /keyword/ argument, rather than a python convention, as is used
    # in the class __init__ function.  The wx.Frame.__init__ parent argument /must/ be a wx.Window object,
    # or simply value "None", which is what we usually use

    # __init__ takes the implicit self argument as usual
    # and 'sibling' here is an instance of our 'Frame' class defined immediately below this class.
    # 'sibling' holds all the necessary data needed to define a wx.Frame object.
    def __init__(self,sibling):
        wx.Frame.__init__(self,parent=sibling._parent,title=sibling._title)
        self.SetInitialSize(sibling._size)

# we define our own Frame() class, because we don't instantly want to create an actual wx.Frame object yet
class Frame:

    # a static class object we can access using Frame._register[index] - we don't access this via an instance of
    # the class; we can also iterate over it, looking for instances with specific data
    _register = []
    _typeName = "Frame"

      # implicit argument self
      # parent: typically None, but if a frame is spawned dynamically it may be useful to pass the relevant object
      # title: string displayed at the top of the frame (the name)
      # size: integer tuple (e.g., (100,100)) specifying the size of the frame in pixels
    def __init__(self, parent, title, size, **kwargs):
        self._parent = parent;
        self._title = title;
        self._size = size;

        # an instance variable holding other instances that are children of this instance
        self._children = []


    def initObj(self):

        # make an instance of the frame, that is a derived class of the wx.Frame class
        self._obj = wxFrame(self)
        Frame._register.append(self)

        # iterate over this instance's children and initialize them.
        for obj in self._children:
            obj.initObj();

        # we have now instantiated all of the objects on this frame; show the frame
        self._obj.Show()


# a wxNotebook class
class wxNotebook(wx.Notebook):
    # the implicit self argument, as usual
    # and 'sibling' - the instance of 'Notebook' class (defined below) holding all
    # necessary data needed to define the wx.Notebook
    def __init__(self,sibling):

        # create the wx.Notebook object
        wx.Notebook(sibling._parent._obj)

        # an empty list, where we list append the Panel objects that serve as pages
        self._pages = [];

        # for all objects denoted as children of our Notebook class,
        # instantiate their object, append that object to the pages list
        # and use the wx.Notebook.AddPage() function to add the page
        for index, item in enumerate(sibling._children):
            item.initObj();
            self._pages.append(item._obj)
            self.AddPage(self._pages[index], item._name);

        # sizer stuff
        self.NBSizer = wx.BoxSizer();
        self.NBSizer.Add(self,1,wx.EXPAND)
        sibling._parent._obj.SetSizer(self.NBSizer)

# our notebook class that collates information before making a wx.Notebook notebook
class Notebook:
    # the implicit self argument
    # parent panel object
    # the pages to be added to this notebook
    # and the names of the pages
    _register = []
    _typeName = "Notebook"

    def __init__(self,parent, **kwargs):
        # instantiate the notebook
        self._parent = parent;
        # an instance variable holding other instances that are children of this instance
        self._children = [];
        self._pages = [];
        # append this instance to a list belonging to the parent, so that the parent knows
        parent._children.append(self);

    def initObj(self):

        # our wxNotebook method initiates the instantiation of the self._children objects
        self._obj = wx.Notebook(self._parent._obj)

        # create a wxNotebook instance and store it in self._obj;  pass 'self' as the argument
        # i.e., we pass this instance of Notebook as the 'sibling' argument (the wxNotebook 'self' is implicit)
        ##self._obj = wxNotebook(self)
        for index, item in enumerate(self._children):
            item.initObj();
            self._pages.append(item._obj);
            self._obj.AddPage(self._pages[index], item._name);
        self.NBSizer = wx.BoxSizer();
        self.NBSizer.Add(self._obj, 1, wx.EXPAND)
        self._parent._obj.SetSizer(self.NBSizer)
        Notebook._register.append(self)

    def customBehavior():
        pass

    # i think this has to be incorporated in the wxNotebook class, rather than here;
    def OnPageChanging(self,event):
        oldPage = event.GetOldSelection()
        newPage = event.GetSelection()

        customBehavior()

class wxPanel(wx.Panel):
    def __init__(self,sibling):
        wx.Panel.__init__(self,parent=sibling._parent._obj);
        self._needsSizer = True;
        for obj in sibling._children:
            if obj._typeName == "Notebook":
                self._needsSizer = False;
                break
        if self._needsSizer:
            self.grid = wx.GridBagSizer(hgap=5,vgap=5);
            self.SetSizer(self.grid);

        # call the init methods of the objects, which then places wxWidget objects in the self._widgets variable for
        # each Widget class instance
        # a panel holding a notebook will never have a widget - its a dummy panel
        # if it does, this is where an error will be thrown!
        for child in sibling._children:
            if child._typeName == "Widget":
                child.initObj(self);
                self.grid.Add(child._obj, pos=child._pos, span=child._span, flag=child._gridFlags)
                # if the base child widget object is a label, it won't have a function
                if ((child._function is not None) and (child._wxEvt is not None)):
                    self.Bind(child._wxEvt,child._function,child._obj)
                if child._label is not None:
                    # we know that this will be a label;
                    child._labelObj = wx.StaticText(self,label=child._label)
                    self.grid.Add(child._labelObj,child._labelPos, child._labelSpan)
                if (child._hasSlave):
                    self.Bind(child._wxEvt, child.masterFunction, child._obj)
                # some objects are initially hidden; here, we hide them.
                if (child._initHide):
                    child._obj.Hide()
                    if (child._label is not None):
                        child._labelObj.Hide()
        self.Layout()

# in this class, we collate all the information we'll need to make a well-defined wx.Panel object
class Panel:
    # what do we require from the user to instantiate a base panel object?
    # make an iterable list of panel instances; make sure methods only access this /after/
    # the main frame has added all objects (i.e., at the end of th user's GUI script!)
    _register = []

    # all instances of this class have the _typeName = "Panel"
    _typeName = "Panel"

    def __init__(self, parent,**kwargs):

        # a list of widget objects, from our widgets class, that identify this panel as their parent panel
        # note that we do /not/ need more information, as this has the instanced objects; we can call their methods
        # directly from here! Very convenient.
        self._widgets = [];

        # panel must have parent object on which it is displayed
        self._parent = parent;

        # a list of the instances that have this instance of the Panel class as their parent
        self._children = []
        parent._children.append(self);

        # we use a name if this panel is a child of a Notebook object; in this case, the name is
        # displayed atop the notebook
        self._name = kwargs.get("name",None)

    def initObj(self):
        # we initialize the panel, which then refers to all of the panel's widgets' methods for their instantiation
        self._obj = wxPanel(self);

        # append this instance to the class register, so that we may iterate over the class instances if needed
        Panel._register.append(self);

        # iterate over self._children, and initialize objects that are /not/ of the type widget; these will
        # be initialized in the wxPanel class!
        for obj in self._children:
            if (obj._typeName != "Widget"):
                obj.initObj()

    def deleteWidget():
        pass

    def bindToFunction():
         # ehhhh... we might have already done this in the widget class. could be better that way.
        pass

#class wxWidget:
#    def __init__(self,sibling):
#        self._widget = None;
#        if sibling._
class Widget:
    _register = []
    _typeName = "Widget"

    # for all Widget objects, we need the parent object, widgetType, name, and position
    def __init__(self,parent,widgetType,name,pos,**kwargs):
        # note that we use **kwargs to pass in information that may be specific to certain type
        # of widget; e.g., text widget vs button vs ... etc.
        # **kwargs is a list of KeyWord ARGumentS (kwargs)  of arbitrary length
        # note that, by default, there is no label (and no label position <(int,int)> provided

        #####################
        # Required arguments, for all widget types
        #####################
        self._parent = parent; # parent object, typically an instance of Panel
        self._widgetType = widgetType; # button, textwidget, label, etc.
        self._name = name; #string
        self._pos = pos; #tuple of coords: "(integer, integer)"


        #####################
        # Required arguments, for some widget types
        #####################

        # required for choice widgets
        self._choices = kwargs.get('choices',None)

        ############################
        # optional arguments
        # we can specify a label (if so, must specify a position)
        # the spans of the label and widget default to (1,1)
        # if a widget can use an initial value (e.g., a text control), it defaults to an empty string
        # if a widget is to be bound to a function, must specify this explicitly or bind to it later
        ############################
        self._label = kwargs.get('label',None)
        self._labelPos = kwargs.get('labelPos',None)
        # default behavior of span is (1,1) if not specified
        self._span = kwargs.get('span',(1,1))
        self._labelSpan = kwargs.get('labelSpan',(1,1))
        self._size = kwargs.get('size',None)
        self._style = kwargs.get('style',None)
        self._initValue = kwargs.get('value',"")
        self._function = kwargs.get('function',None)
        self._wxEvt = None
        self._hasMaster = False; # default this to false; changed if the setMaster() function is called on self
        self._hasSlave = False;
        self._fontOptions = kwargs.get('fontOptions',None)


        # these will be instantiated during the creation of the parent object
        self._labelObj = None;
        self._obj = None;

        # Hide most objects at first; that way, they only show if they are told to show,
        # and otherwise will hide when told to hide
        # implement this /after/ we have connected all the show/hide funcitonality
        self._initHide = False;

        # TODO: have the Panel's grid.Add() method use these flags when instantiating the widget
        self._gridFlags = (wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.EXPAND | wx.ALIGN_CENTER)

        # default the dictionary keyword for data storage to 'None';
        # we require the programmer to specify explicitly under what keyword to store the data
        # this can be accessed via the 'setDictKwarg()' method, defined below
        self._dictKwarg = None

        # append the object to the list of children in the parent instance
        parent._children.append(self)

        # the master widget - this is a /Widget/ instance
        self._masters = []

        # denotes messages from master that instruct self to Hide()
        # these should be strings
        self._hideWhen = []

        # widgets to which self is master; note that this is set implicitly via setMaster, when
        # other widgets denotes self as master
        # this is a /Widget/ instance (not a wx object)
        self._slaves = []
        Widget._register.append(self); # append this instance to the class register
    # allows the function to which the widget will be bound to be set after construction of the widget instance
    # we allow the function to be defined according to whatever parameters the user inputs; no implicit self

    def masterFunction(self,event):
        # pass the value of this widget to slaved widgets
        message = str(event.GetString())
        for slave in self._slaves:
            slave.evaluateMessage(message);


    def evaluateMessage(self,message):
        # this is used by the interface to loop over child widgets
        # in the event that a chosen selection hides multiple levels of the parent-child hierarchy.
        # continues until exhaustion
        if message in self._hideWhen:
            self._obj.Hide()
            if (self._labelObj is not None):
                self._labelObj.Hide()
            self._parent._obj.Layout()
        else:
            self._obj.Show()
            if (self._labelObj is not None):
                self._labelObj.Show()
            self._parent._obj.Layout()

    def setMaster(self, master, hideWhen):
        self._masters.append(master)

        # assume hideWhen is in the form of an array
        for instruction in hideWhen:
            self._hideWhen.append(instruction)

        # append self to master._slaves[]
        master._slaves.append(self);
        self._hasMaster = True;

        if master._hasSlave == False:
            master._hasSlave = True;

    def setDictKwarg(self,keyword):
        self._dictKwarg = keyword;

    def setFunction(self,function):
        self._function = function;

    def setGridFlags(self,flags):
        self._gridFlags = flags;

    def setInitHide(self,boolean):
        self._initHide = boolean;

    # maybe the user wants to attach labels later; allow them to do so here
    def setLabel(self,label,labelPos,**kwargs):
        self._label = label;
        self._labelPos = labelPos;
        self._labelSpan = kwargs.get('labelSpan',(1,1))

    # this is a bottom level object; it requires a parentInstance on initialization
    def initObj(self,parentInstance):
        # for each, initialize the wx object in self._obj, and inform the class what kind of wx event to
        # expect in self._wxEvt
       #self._obj = wxWidget(self)

        if (self._widgetType == "text"):
            if (self._style is None):
                self._obj = wx.TextCtrl(parentInstance,value=self._initValue,name=self._name)
                self._wxEvt = wx.EVT_TEXT
            else:
                self._obj = wx.TextCtrl(parentInstance,value='',size=self._size, \
                        name = self._name,style = self._style)
                self._wxEvt = wx.EVT_TEXT

    # need to add all types of widgets here; remember to overload necessary parameters for each via kwargs.get()
        elif (self._widgetType == "choice"):
            #choicesList
            if (self._choices is None):
                raise ValueError('%s has no choices!  Please specify choices for the choice widget.' %(self._name))
            self._obj = wx.Choice(parentInstance,-1,choices=self._choices,name=self._name)
            self._wxEvt = wx.EVT_CHOICE

        # more types of widgets to be implemented
        elif (self._widgetType == "button"):
            if (self._name is None):
                raise ValueError('%s has no name! The name of the button is displayed on the button, and \n\
                is required!' %(self._name))
            self._obj = wx.Button(parentInstance,label=self._name, name=self._name)
            self._wxEvt = wx.EVT_BUTTON


        elif (self._widgetType == "static"):
            self._obj = wx.StaticText(parentInstance,label=self._name, name=self._name)
            self._wxEvt = None
           # if (self._fontOptions is not None):
           #     self._obj.SetFont(wx.Font(self._fontOptions))

        # all widgets with which we interact will store there data in the global dictionary;
        # access to this dictionary is controlled by the _dictKwarg attribute
        # this attribute must be appended to the wxWidget object, because I can't figure out
        # how to refer back to the base Widget class instance once we make the wxWidget swig object
        self._obj.__setattr__("_dictKwarg", self._dictKwarg)

# utf-8 encoding of the Angstrom unit symbol; useful to have here
angstrom = u'\u212B'.encode('utf-8')

# the maximum number of species we will allow the user to specify using the GUI
maxNumberOfSpecies = 6

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

# default behavior for text widget objects
def defaultTextFunction(event):

    # ask the GUI what object received the event
    obj = event.GetEventObject();

    # we added the dictKwarg as an attribute to the wxObject on instantiation, presumably
    # so, get the keyword that we will use for the dictionary
    objKeyword = obj._dictKwarg

    # get the value of the event
    val = str(event.GetString())

    # raise a value error if the value of object keyword is None --
    # this means that someone forgot to assign dictionary keyword to this widget, and therefore
    # the data won't be stored anywhere, so it won't be written to the input file!
    noKeywordAlert = "No dictionary keyword specified for this widget - your data isn't being stored!"
    if (objKeyword is None):
        raise ValueError(noKeywordAlert)

    # otherwise, everything went ok and we'll put the value in the dictionary
    if (val):
       myDict[objKeyword] = val

    # this will throw a KeyError if an empty value is attempted to be written to file at the end
    # -- in any case, we don't need to worry about it
    # this cleans up our dictionary if the user decides they don't need to use the value after all
    if not val:
        if objKeyword in myDict.keys():
            del myDict[objKeyword]

    print objKeyword, val

# default behavior for our choice widget objects
# this is essentially identical to our text widget function, but we make a distinction for clarity
def defaultChoiceFunction(event):

    # ask the GUI what object received the event
    obj = event.GetEventObject();

    # get the keyword associated with this object
    objKeyword = obj._dictKwarg

    # get the value of the event
    val = str(event.GetString())

    noKeywordAlert = "No dictionary keyword specified for this widget - your data isn't being stored!"
    if (objKeyword is None):
        raise ValueError(noKeywordAlert)

    # otherwise, everything went ok and we'll put the value in the dictionary
    if (val):
       myDict[objKeyword] = val

    if not val:
        del myDict[objKeyword]

    print objKeyword, val


######################################################################################
# SECTION 4.1: Addition of widgets to PanelOnePageOne (Basic Information / Page One)
######################################################################################
# PanelOnePageOne is the panel to which the graphical user interface opens.
# This panel is special in that it incorporates some navigational restrictions,
# based on the current values of the widgets on the page! These restrictions are
# enforced by (syntax here) TODO
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
numberOfSpeciesChoices = [""]
# iterative over global variable 'maxNumberOfSpecies' to add options to the choice widget
for i in range(maxNumberOfSpecies):
    numberOfSpeciesChoices.append("%s" %(i+1))

ensembleChoices = ["", "NVT_MC","NVT_MIN","NPT_MC","GCMC","GEMC","GEMC_NPT"]

# the text widget asking for the run name
runNameWidget = Widget(PanelOnePageOne,widgetType="text", name = "",pos=(3,2), \
        label="Run Name: ", labelPos=(3,1))

# a button (with label) from which the user may select the simulation directory
simulationDirectoryWidget = Widget(PanelOnePageOne,widgetType="button", name="Select Directory", \
        pos=(4,2), label="Simulation Directory: ", labelPos=(4,1))

simulationDirectoryDisplay = Widget(PanelOnePageOne,widgetType="text",name="displaySimDir", \
        pos=(4,3), span = (1,2),style=wx.TE_READONLY,size=(200,-1))

# a choice widget (drop down menu) from which the user may select one of Cassandra's ensembles
ensembleWidget = Widget(PanelOnePageOne,widgetType="choice",name="# Sim_Type", \
        pos=(5,2), label="Ensemble: ", labelPos=(5,1),choices=ensembleChoices)

# a choice widget from which the number of species in simulation may be selected
numberOfSpeciesWidget = Widget(PanelOnePageOne,widgetType="choice",name="", \
        pos=(6,2), label="Number of Species: ",labelPos=(6,1),choices=numberOfSpeciesChoices)

# a button which creates the input file in the simulation directory
makeInputFileWidget = Widget(PanelOnePageOne,widgetType="button",name="Create Input File", \
        pos=(12,2))

# our string indicating that further navigation of the GUI requires our above prompts to be answered
# P.S., if anyone can figure out how to make this bold, kudos
string0 = "Please provide the following information before continuing."

provideInformationText = Widget(PanelOnePageOne,widgetType="static",name=string0, \
        pos=(1,2),span=(1,4))

# a string we place on the panel
string1= "Have you completed all prompts on all pages? "
staticText1 = Widget(PanelOnePageOne,widgetType="static",name=string1,\
        pos=(11,1),span=(1,4))

# another string
string2 ="If so, click here:"
staticText2 = Widget(PanelOnePageOne,widgetType="static",name=string2, \
        pos=(12,1),span=(1,1))


##########
# Set dictionary keyword for widgets which have functionality (for the most part, everything
# other than labels); also, special case: we don't need anything for the 'create input file' button
# since it writes the file, rather than storing anything
##########
runNameWidget.setDictKwarg("runName")
simulationDirectoryWidget.setDictKwarg("simDir")
numberOfSpeciesWidget.setDictKwarg("numSpecies")
ensembleWidget.setDictKwarg("ensemble")

#################################################
# definition of custom functions for this panel
#################################################

def simDirFunction(event):
    # retrieve the object that was interacted with on the GUI
    # for this function, we know it was the simulation directory button
    obj = event.GetEventObject();

    # obj can be used approximately interchangeably with 'self' at this point
    # this is the syntax for creating a directory dialog with wxPython
    dlg = wx.DirDialog(obj,"Select Simulation Directory", \
            style = wx.DD_DEFAULT_STYLE)

    # once the user has navigated to the appropriate directory and pressed OK,
    if dlg.ShowModal() == wx.ID_OK:
        val = dlg.GetPath()
    else:
        val = ''

    # process the data
    directoryName = os.path.split(val)
    if val:
        myDict['displaySimDir'] = directoryName[1]
        strToDisplay = "/" + myDict['displaySimDir'] + "/"
    else:
        myDict['displaySimDir'] = ''
        strToDisplay = myDict['displaySimDir']

    # it will then store the relative path that the user has selected
    simulationDirectoryDisplay._obj.SetValue((strToDisplay))
    objKeyword = obj._dictKwarg

    noKeywordAlert = "No dictionary keyword specified for this widget - your data isn't being stored!"
    if (objKeyword is None):
        raise ValueError(noKeywordAlert)

    # otherwise, everything went ok and we'll put the value in the dictionary
    if (val):
       myDict[objKeyword] = val

    if not val:
        del myDict[objKeyword]

    print objKeyword, val

def createInputFileFunction(event):
    # TODO super dooper important, pretty much the reason for the whole thing
    pass

#################################################
# set the functions to which these widgets will respond; some of them will be standard,
# others are specific to a given widget
runNameWidget.setFunction(defaultTextFunction)
simulationDirectoryWidget.setFunction(simDirFunction)
numberOfSpeciesWidget.setFunction(defaultChoiceFunction)
ensembleWidget.setFunction(defaultChoiceFunction)
makeInputFileWidget.setFunction(createInputFileFunction)



# show/hide dynamics
#
# on PanelOnePageOne, we only have master widgets - these widgets are /always/
# displayed.  So, there isn't much to be done!


# initially, all widgets  are hidden; specify here that we show these objects.
# since this is the first panel, we can actually iterate over all objects created thus far
for widget in Widget._register:
    widget.setInitHide(False)
# after we define more objects, we won't want to do that..

######################################################################################
# SECTION 4.2: Addition of widgets to PanelOnePageTwo (Basic Information/Page Two)
######################################################################################
# PanelOnePageTwo asks for other basic information about the simulation, some of
# which might be dependent on the selected ensemble or the number of species.
#
# PanelOnePageTwo:
#       - Temperature
#       - Mixing Rule
#       - Minimum Cutoff
#       - Pair storage
#       - Random Number seeds (Seed 1 and Seed 2)
#       - Pressure
#       - Box information (cubic/non-cubic, length or h-matrix), for boxes 1 and 2
#       - CBMC parameters
#       - Chemical potential
#       - accompanying labels for all of the above named prompts
#
######################################################################################

# lists of choices for choice widgets
mixingRulesChoices = ["","Lorentz-Berthelot","Geometric"]
pairStorageChoices = ["","TRUE","FALSE"] #TODO check if Cassandra's I/O is all caps
boxShapeChoices = ["", "CUBIC","NON-CUBIC"]

# temperature: label and text widget
temperatureWidget = Widget(PanelOnePageTwo,widgetType="text",name="temperature", \
                    pos=(1,2), label="Temperature (K): ", labelPos=(1,1))

# mixing rule: label and choice widget
mixingRuleWidget = Widget(PanelOnePageTwo, widgetType="choice",name="mixing", \
        pos=(2,2), label="Mixing Rule: ", labelPos=(2,1), choices = mixingRulesChoices)

# minimum cutoff: label and text widget
cutoffWidget = Widget(PanelOnePageTwo, widgetType="text",name="rcutoff", \
        pos=(3,2), label="Cutoff (%s): " %(angstrom), labelPos=(3,1))

# Pair storage: label and choice widget
pairStorageWidget = Widget(PanelOnePageTwo,widgetType="choice",name="pairStorage", \
        pos=(4,2), label = "Pair Storage: ", labelPos = (4,1), choices=pairStorageChoices)

# seed 1: label and text widget
seed1Widget = Widget(PanelOnePageTwo, widgetType="text", name = "seed1", \
        pos=(5,2), label = "Seed 1: ", labelPos=(5,1))

# seed 2: label and text widget
seed2Widget = Widget(PanelOnePageTwo, widgetType="text", name = "seed2", \
        pos=(6,2), label = "Seed 2: ", labelPos=(6,1))

# "Box Information" label
boxInfoLabel = Widget(PanelOnePageTwo, widgetType="static", name = "Box Information", \
        pos=(9,1))

# "Box Shape" label
boxShapeLabel = Widget(PanelOnePageTwo, widgetType="static", name = "Box Shape",\
        pos=(9,2))

# Box 1: label and choice widget
box1ShapeChoice = Widget(PanelOnePageTwo, widgetType="choice", name = "Box1 Shape", \
        pos=(10,2), label = "Box 1: ", labelPos = (10,1), choices = boxShapeChoices)

# Box 2: label and choice widget
box2ShapeChoice = Widget(PanelOnePageTwo, widgetType="choice", name = "Box2 Shape", \
        pos=(11,2), label = "Box 2: ", labelPos = (11,1), choices = boxShapeChoices)

# Box 1 H-Matrix Frame Button (## IMPORTANT - objects added to frame below!)
box1HMatrix = Widget(PanelOnePageTwo, widgetType="button", name = "Create H Matrix", \
        pos=(10,4))

# Box 2 H-Matrix Frame Button (## IMPORTANT - objects added to frame below!)
box2HMatrix = Widget(PanelOnePageTwo, widgetType="button", name = "Create H Matrix", \
        pos=(11,4))

# "CBMC" label
CBMCLabel = Widget(PanelOnePageTwo, widgetType="static", name="CBMC Parameters", \
        pos=(13,1))

# "Trial Insertions" label and text widget
trialInsertionWidget = Widget(PanelOnePageTwo, widgetType="text", name="trialInsertions", \
        pos=(14,2), label="Trial Insertions: ", labelPos=(14,1))

# "Rotational Bias" label and text widget
rotationalBiasWidget = Widget(PanelOnePageTwo, widgetType="text", name="rotationalBias", \
        pos=(15,2), label="Rotational Bias: ", labelPos=(15,1))

# "Trial orientations" label and text widget
trialOrientationsWidget = Widget(PanelOnePageTwo, widgetType="text", name="trialOrientations", \
        pos=(16,2), label="Trial Orientations: ", labelPos=(16,1))

# "Cutoff (%angstrom) Box 1:" label and text widget
CBMCCutoffBox1 = Widget(PanelOnePageTwo, widgetType="text", name="cbmcCutoffB1", \
        pos=(17,2), label="Cutoff (%s) Box 1: " %(angstrom), labelPos=(17,1))

# "Cutoff (%angstrom) Box 2:" label and text widget
CBMCCutoffBox2 = Widget(PanelOnePageTwo, widgetType="text", name="cbmcCutoffB2", \
        pos=(18,2), label="Cutoff (%s) Box 2: " %(angstrom), labelPos=(18,1))

# "Chemical Potential (kJ/mol)" label
chemicalPotentialLabel = Widget(PanelOnePageTwo, widgetType = "static", \
        name="Chemical Potential (kJ/mol)", pos=(1,5), span=(1,2))

# our label for species 1
chemicalPotentialS1Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 1: ", pos =(2,5))

# our labels for species 2-6 (same process)..
chemicalPotentialS2Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 2: ", pos =(3,5))
chemicalPotentialS3Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 3: ", pos =(4,5))
chemicalPotentialS4Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 4: ", pos =(5,5))
chemicalPotentialS5Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 5: ", pos =(6,5))
chemicalPotentialS6Label = Widget(PanelOnePageTwo, widgetType = "static", \
        name = "Species 6: ", pos =(7,5))

# Chemical potential prompts, for species 1-6 (## IMPORTANT -
# if support for more than 6 species within the GUI is desired, must change that here)

# the text widgets for species 1-6
chemicalPotentialS1Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (2,6))
chemicalPotentialS2Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (3,6))
chemicalPotentialS3Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (4,6))
chemicalPotentialS4Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (5,6))
chemicalPotentialS5Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (6,6))
chemicalPotentialS6Widget = Widget(PanelOnePageTwo, widgetType = "text", \
        name = "", pos = (7,6))

#### H-Matrix Frame objects & functions \TODO
def destroyHMatrix(event):

    # the user clicked 'Done', so destroy the Frame and its objects

    # first, we get the object that received the event (the "Done" button)
    obj = event.GetEventObject()

    # get the object obj's parent frame
    # obj is the "Done" button, whose parent is the Panel, whose parent is the Frame;
    # we call the Close() function on the Frame object (i.e., destroy the top level object).
    frameToBeClosed = obj.GetParent().GetParent()
    frameToBeClosed.Close();

def hMatrixFunction(event):

    # get the button from which the event originated
    obj = event.GetEventObject()

    # get the dictionary keyword argument assigned to the H-Matrix Button
    objKeyword = obj._dictKwarg

    # objKeyword is either 'hmatrix box 1' or 'hmatrix box 2'
    # so, splice the objKeyword and store the last index (either '1' or '2') in a new variable
    thisBox = str(objKeyword[-1])

    # now we need to spawn a frame
    hMatrixFrame = Frame(None,"H Matrix",(360,300))
    hMatrixPanel = Panel(hMatrixFrame)

    # place the widgets on the frame
    # first, an instructional label:
    instructionsStringHMatrix = "Enter your H-Matrix vectors below."
    instructionsHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = instructionsStringHMatrix, pos = (1,1), span = (1,4))

    # now, more static widget labels - our x, y, and z director vectors
    xTopLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "x", pos = (2,2))
    yTopLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "y", pos = (2,3))
    zTopLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "z", pos = (2,4))

    # and x, y, z labels on the sides
    xSideLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "x", pos = (3,1))
    ySideLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "y", pos = (4,1))
    zSideLabelHMatrix = Widget(hMatrixPanel, widgetType = "static", \
            name = "z", pos = (5,1))

    # the text widgets forming the h-matrix
    #   xx    xy     xz
    #   yx    yy     yz
    #   zx    zy     zz

    xxHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (3,2))
    xyHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (3,3))
    xzHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (3,4))

    yxHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (4,2))
    yyHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (4,3))
    yzHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (4,4))

    zxHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (5,2))
    zyHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (5,3))
    zzHMatrixTextWidget = Widget(hMatrixPanel, widgetType = "text", \
            name = "", pos = (5,4))

    # also, this is a Frame object, not a dialog (as with the simulation directory button)
    # therefore, we need to add a button that destroys the frame when the user is done entering
    # the information

    doneButtonHMatrix = Widget(hMatrixPanel, widgetType = "button", \
            name = "Done", pos = (7,4))

    # we now have all of our widgets on the panel; assign dictionary keyword arguments
    # to the relevant widgets (the widgets that will store or access data in dictionary 'myDict')
    # for the h-matrix text widgets, assign it as the director vector  and the box number
    xxHMatrixTextWidget.setDictKwarg("xx %s" %thisBox)
    xyHMatrixTextWidget.setDictKwarg("xy %s" %thisBox)
    xzHMatrixTextWidget.setDictKwarg("xz %s" %thisBox)
    yxHMatrixTextWidget.setDictKwarg("yx %s" %thisBox)
    yyHMatrixTextWidget.setDictKwarg("yy %s" %thisBox)
    yzHMatrixTextWidget.setDictKwarg("yz %s" %thisBox)
    zxHMatrixTextWidget.setDictKwarg("zx %s" %thisBox)
    zyHMatrixTextWidget.setDictKwarg("zy %s" %thisBox)
    zzHMatrixTextWidget.setDictKwarg("zz %s" %thisBox)

    # these will all use the default text function
    xxHMatrixTextWidget.setFunction(defaultTextFunction)
    xyHMatrixTextWidget.setFunction(defaultTextFunction)
    xzHMatrixTextWidget.setFunction(defaultTextFunction)
    yxHMatrixTextWidget.setFunction(defaultTextFunction)
    yyHMatrixTextWidget.setFunction(defaultTextFunction)
    yzHMatrixTextWidget.setFunction(defaultTextFunction)
    zxHMatrixTextWidget.setFunction(defaultTextFunction)
    zyHMatrixTextWidget.setFunction(defaultTextFunction)
    zzHMatrixTextWidget.setFunction(defaultTextFunction)

    # assign the 'close' functionality to the 'Done' button
    doneButtonHMatrix.setFunction(destroyHMatrix)

    # initialize all the objects.
    hMatrixFrame.initObj()

    # now that we have all the objects instantiated, we can work with the wxWidgets objects

    # we wish to populate the text widgets with their values if the user re-opens
    # the window; so, look in myDict for the _dictKwarg assigned to each text widget; if it is
    # in the dictionary, set the value of the textwidget to that value;
    # else, set the value to an empty string

    # there isn't a very elegant way to handle this; just copy and paste the same code for each widget
    # we need to work with the wxWidget objects directly; access via ._obj syntax
    if (("xx %s" %(thisBox)) in myDict.keys()):
        xxHMatrixTextWidget._obj.SetValue(myDict["xx %s" %thisBox])
    else:
        xxHMatrixTextWidget._obj.SetValue('')
    if (("xy %s" %(thisBox)) in myDict.keys()):
        xyHMatrixTextWidget._obj.SetValue(myDict["xy %s" %thisBox])
    else:
        xyHMatrixTextWidget._obj.SetValue('')
    if (("xz %s" %(thisBox)) in myDict.keys()):
        xzHMatrixTextWidget._obj.SetValue(myDict["xz %s" %thisBox])
    else:
        xzHMatrixTextWidget._obj.SetValue('')

    # and for our y[x,y,z] text widgets...
    if (("yx %s" %(thisBox)) in myDict.keys()):
        yxHMatrixTextWidget._obj.SetValue(myDict["yx %s" %thisBox])
    else:
        yxHMatrixTextWidget._obj.SetValue('')
    if (("yy %s" %(thisBox)) in myDict.keys()):
        yyHMatrixTextWidget._obj.SetValue(myDict["yy %s" %thisBox])
    else:
        yyHMatrixTextWidget._obj.SetValue('')
    if (("yz %s" %(thisBox)) in myDict.keys()):
        yzHMatrixTextWidget._obj.SetValue(myDict["yz %s" %thisBox])
    else:
        yzHMatrixTextWidget._obj.SetValue('')

    # and for our z[x,y,z] text widgets...
    if (("zx %s" %(thisBox)) in myDict.keys()):
        zxHMatrixTextWidget._obj.SetValue(myDict["zx %s" %thisBox])
    else:
        zxHMatrixTextWidget._obj.SetValue('')
    if (("zy %s" %(thisBox)) in myDict.keys()):
        zyHMatrixTextWidget._obj.SetValue(myDict["zy %s" %thisBox])
    else:
        zyHMatrixTextWidget._obj.SetValue('')
    if (("zz %s" %(thisBox)) in myDict.keys()):
        zzHMatrixTextWidget._obj.SetValue(myDict["zz %s" %thisBox])
    else:
        zzHMatrixTextWidget._obj.SetValue('')

    # and that concludes the hMatrix panels.  note that this handles both
    # the box 1 and box 2 h matrix stuff.


#########################################################
# Set the dictionary kwargs for the widgets on this panel
#########################################################
temperatureWidget.setDictKwarg("temperature")
mixingRuleWidget.setDictKwarg("mixingRule")
cutoffWidget.setDictKwarg("rCutoffLow")
pairStorageWidget.setDictKwarg("pairStorage")
seed1Widget.setDictKwarg("seed1")
seed2Widget.setDictKwarg("seed2")
box1ShapeChoice.setDictKwarg("box1Shape")
box2ShapeChoice.setDictKwarg("box2Shape")
trialInsertionWidget.setDictKwarg("trialInsertions")
rotationalBiasWidget.setDictKwarg("rotationalBias")
trialOrientationsWidget.setDictKwarg("trialOrientations")
CBMCCutoffBox1.setDictKwarg("cbmcCutoffBox1")
CBMCCutoffBox2.setDictKwarg("cbmcCutoffBox2")
box1HMatrix.setDictKwarg("hmatrix box 1")
box2HMatrix.setDictKwarg("hmatrix box 2")
chemicalPotentialS1Widget.setDictKwarg("chemPot S1")
chemicalPotentialS2Widget.setDictKwarg("chemPot S2")
chemicalPotentialS3Widget.setDictKwarg("chemPot S3")
chemicalPotentialS4Widget.setDictKwarg("chemPot S4")
chemicalPotentialS5Widget.setDictKwarg("chemPot S5")
chemicalPotentialS6Widget.setDictKwarg("chemPot S6")

# bind the widgets on this panel to functions as needed
temperatureWidget.setFunction(defaultTextFunction)
mixingRuleWidget.setFunction(defaultChoiceFunction)
cutoffWidget.setFunction(defaultTextFunction)
pairStorageWidget.setFunction(defaultChoiceFunction)
seed1Widget.setFunction(defaultTextFunction)
seed2Widget.setFunction(defaultTextFunction)
box1ShapeChoice.setFunction(defaultChoiceFunction)
box2ShapeChoice.setFunction(defaultChoiceFunction)
trialInsertionWidget.setFunction(defaultTextFunction)
rotationalBiasWidget.setFunction(defaultTextFunction)
trialOrientationsWidget.setFunction(defaultTextFunction)
CBMCCutoffBox1.setFunction(defaultTextFunction)
CBMCCutoffBox2.setFunction(defaultTextFunction)
box1HMatrix.setFunction(hMatrixFunction)
box2HMatrix.setFunction(hMatrixFunction)
chemicalPotentialS1Widget.setFunction(defaultTextFunction)
chemicalPotentialS2Widget.setFunction(defaultTextFunction)
chemicalPotentialS3Widget.setFunction(defaultTextFunction)
chemicalPotentialS4Widget.setFunction(defaultTextFunction)
chemicalPotentialS5Widget.setFunction(defaultTextFunction)
chemicalPotentialS6Widget.setFunction(defaultTextFunction)



# show/hide dynamics \TODO


######################################################################################
# SECTION 4.3: Addition of widgets to PanelTwoPageOne (Interaction Parameters /
#                                                      Intermolecular)
######################################################################################
# PanelTwoPageOne (InteractionParameters/Intermolecular) asks for the methods to be
# used to calculate intermolecular potentials - for van der Waals interactions,
# it asks for the functional form (LJ 12-6, or NONE), cut/cut_shift/cut_switch/
# cut_tail; support for the MIE potential is TBD.
# We also ask for the charge style to be used in simulation -
# coulombic functional form, or NONE; calculated using Ewald Summation,
# or a cut.
#
# PanelTwoPageOne:
#       - Box 1 vdW style prompts
#       - Box 2 vdW style prompts
#       - Box 1 charge style prompts
#       - Box 2 charge style prompts
#
######################################################################################

# lists of choices for our various widgets
vdwFunctionalFormChoices = ["","Lennard Jones 12-6","MIE","None"]
vdwTailCorrectionChoices = ["","cut","cut_tail","cut_switch","cut_shift"]
vdwLogicalChoices = ["","TRUE"]

chargeFunctionalFormChoices = ["","Coulombic","None"]
chargeMethodChoices = ["","Ewald","cut"]

# vdw style label

# Box 1 label - vdw style

# Box 2 label - vdw style

# box 1 functional form, vdw style

# box 1 tail correction, vdw style

# box 1 cutoff, vdw style

# box 1 spline off, vdw style

# box 1 logical, vdw style



# box 2 functional form, vdw style

# box 2 tail correction, vdw style

# box 2 cutoff, vdw style

# box 2 spline off, vdw style

# box 2 logical, vdw style



# charge style label

# box 1 label - charge style

# box 2 label - charge style


# box 1 functional form - charge style

# box 1 method - charge style

# box 1 cutoff - charge style

# box 1 accuracy - charge style

# box 2 functional form - charge style

# box 2 method - charge style

# box 2 cutoff - charge style

# box 2 accuracy - charge style



# and functions for the various widgets


# show/hide dynamics


######################################################################################
# SECTION 4.4: Addition of widgets to PanelTwoPageOne (Interaction Parameters /
#                                                      Intramolecular)
######################################################################################

# no lists on this page, nothing to do here!

# "Select a scaling style:" label

# "or enter custom values below." label

# AMBER selection

# CHARMM selection

# efficient way to implement this?
# species 1,2,3,4,5,6 scaling for 1-2, 1-3, 1-4, 1-N interactions



######################################################################################
# SECTION 4.5: Addition of widgets to PanelThreeTranslation
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label

# "Enter the maximum displacement %s allowed for each species in each box below"
# %(angstrom). label

# Move probability widget

# Species 1: label

# Species 2: label

# Species 3: label

# Species 4: label

# Species 5: label

# Species 6: label

# Box 1 label

# Box 2 label

# species 1 box 1 text widget

# species 1 box 2 text widget

# species 2 box 1 text widget

# species 2 box 2 text widget

# species 3 box 1 text widget

# species 3 box 2 text widget

# species 4 box 1 text widget

# species 4 box 2 text widget

# species 5 box 1 text widget

# species 5 box 2 text widget

# species 6 box 1 text widget

# species 6 box 2 text widget



# show/hide functionality


# functions etc.


######################################################################################
# SECTION 4.6: Addition of widgets to PanelThreeRotation
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label

# "Enter the maximum rotational width in degrees for each species in each box below"
# label

# Move probability widget

# Species 1 label
# .....



# Box 1 Label

# box 2 label

# s1 b1 text widget

# s1 b2 text widget

# s2 b1 text widget

# s2 b2 text widget

# ......


# show/hide functionality


# functionality



######################################################################################
# SECTION 4.7: Addition of widgets to PanelThreeRegrowth
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label

# "Enter the relative probablity of regrowth for each species below." label

# "Note that the relative probabilities below must sum to 1." label

# Species 1 textwidget and label

# .... (to 6)


# show/hide functionality


# functionality


######################################################################################
# SECTION 4.8: Addition of widgets to PanelThreeVolume
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label

# Enter the maximum volume displacements in A^3 for the simulation box(es) below."

#


######################################################################################
# SECTION 4.9: Addition of widgets to PanelThreeInsertion
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label




######################################################################################
# SECTION 4.10: Addition of widgets to PanelThreeSwap
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label




######################################################################################
# SECTION 4.10: Addition of widgets to PanelThreeSwap
######################################################################################

# "Please note that the sum of the move probabilities across all move types must
# sum to 1." label





######################################################################################
# SECTION 4.11: Addition of widgets to PanelFourMoleculeFiles
######################################################################################





######################################################################################
# SECTION 4.12: Addition of widgets to PanelFourFragmentFiles
######################################################################################





######################################################################################
# SECTION 4.13: Addition of widgets to PanelFourInputFile
######################################################################################





######################################################################################
# SECTION 4.14: Addition of widgets to PanelFourOutputFile
######################################################################################














######################################################################################

# initiate the event loop, and instruct the main frame to show!
# this causes a cascade of instantiations - at this point, all objects must be declared.
if __name__ == "__main__":
    app = wx.App()
    MainFrame.initObj()
    app.MainLoop()


