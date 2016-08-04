# note - on OSX, requires framework build of python/2.7 to run, as this
# application requires access to the screen (this may only apply to systems
# running Mavericks or later)


# This script for a graphical user interface is intended to serve as a template for future, complex
# graphical user interfaces; primarily intended to be used as a simplified front-end of wx.Widgets,
# allow for easy setup of dynamic hiding that might involve cross-communication between objects of
# assorted placement in the hierarchy of parent-child objects.


######
#
#  Some license info here
#
######
import  wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

# global dictionary in which we store data
myDict = {}

# utf-encoded angstroms unit, for use in labels on the GUI
angstrom = u'\u212B'.encode('utf-8')

# general class for wx.Panel objects
class Panel(wx.Panel):

  def __init__(self,parent):
    # initialize the panel with a grid accessible to other methods
    wx.Panel.__init__(self,parent);
    self.grid = wx.GridBagSizer(hgap=5,vgap=5);

    # some panels are initialized as members of a notebook, while others are directly
    # assigned to the frame; this is handled here

    # we record whether this panel is a notebook; whether it has a friend (an accompanying
    # panel, which is neither a child nor parent, but will be shown whenever this panel appears);
    # whether it has a parent; whether it has a child; whether it has widgets;

    # note that all panels have a parent; top level panels have the frame as their parent object,
    # which in turn has the window as its parent
    self._isNotebook = False;
    self._hasSibling = False;
    self._hasParent = True;
    self._hasChild = False;
    self._hasWidgets = False;

    # a given panel may be a member of one notebook;
    # a given panel may have multiple siblings;
    # a given panel may have one parent;
    # a given panel may have multiple children;
    self._notebookName = [];
    self._siblings = [];
    self._parent = wx.
    self._children = [];
    self._widgets = [];


  def addWidget():
    # when adding a widget, we consider the grid position it will be added to, as well
    # as the flags which will be implemented when placing the widget on the grid

    pass

    # destroy an object of type aWidget
  def deleteWidget():
    pass

  def bindToFunction():
    pass


# this class will be used as the parent panel for any notebook-type pages;
# likely that these Notebook objects will be the direct children of the frame, rather than an
# object of the Panel class
class Notebook(wx.Panel):
  def __init__(self,parent, *args, **kwargs):
    wx.Panel.__init__(self,parent)
    thisNotebook = wx.Notebook(self)
    self.listOfPageObjs = []
    self.pageObjs = []
    # somehow make this work... need to pass panel class objects and call, e.g., panelObj(thisNotebook)
    for index, item in enumerate(args):
      self.listOfPageObjs.append(str(item))
      self.pageObjs.append(item(thisNotebook))

      ## need their names here
      thisNotebook.AddPage(self.pageObjs[index],objName)
      # need to pass in their names as well, which will show up as the labels

    # add a sizer to the notebook
    thisSizer=wx.BoxSizer()
    thisSizer.Add(thisNotebook,1,wx.EXPAND)
    self.SetSizer(thisSizer)
  pass


## we only need one frame for the GUI; holds all the panels/notebooks
class aFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self,None,title="Cassandra Input File Editor v1.2")
    self.SetInitialSize((900,620))


  pass

class aWidget:
  def __init__(self,name,coords,widgetType,span=(1,1),label=None,labelPosition=None,**kwargs):
    # note that we use **kwargs to pass in information that may be specific to certain type
    # of widget; e.g., text widget vs button vs ... etc.
    # **kwargs is a list of KeyWord ARGumentS (kwargs)  of arbitrary length
    # note that, by default, there is no label (and no label position <(int,int)> provided
    self.name = name #string
    self.coords = coords #tuple of coords: "(integer, integer)"
    self.widgetType = widgetType # button, textwidget, label, etc.

    # default behavior of span is (1,1) if not specified;
    self.span = span

    if label:
      self.label = label
      try:
        self.labelPosition = labelPosition
      except:
        print "Error: label %s specified, but no label position tuple (int,int) given! " %label

    # here we create the actual widget object? I think..
    if self.widgetType is "staticText":
      pass
    elif self.widgetType is "button":
      pass
    elif self.widgetType is "textWidget":
      pass

  def instantiateWidget(self):
    pass


    # consider handling for a 'display' widget - one that displays the current value of another widget
    # that may not otherwise have a displayable value, e.g. a button (direct example: simulation directory)



# consider - how to control show/hide without explicitly coding it?
# answer: make it its own class with data structures and handling etc. auto-contruct a tree of relational hierarchies
# that is created after passing information in via instantiation with the 'aWidget' class
# note that this would need access to instantaneous values and would need to check those values in between events
# i.e., during loop. ... how?

##########################################
##########################################
# This is the actual script, where
# object creation begins.
# To add a new widget,
# add it below this point after
# creating whatever base objects your
# widget will require
##########################################
##########################################

app = wx.App(False)
thisFrame = aFrame()

#### the first panel
firstPanelObj = Panel(thisFrame)

# some widgets
firstPanelNames = ["runName", "simulationDirectory", "ensemble", "numberOfSpecies"]
firstPanelLabels = ["Run Name: ", "Simulation Directory: ", "Ensemble: ", "Number of Species: "]
firstPanelCoords = [(3,3), (4,3), (5,3), (6,3)]
firstPanelSpans = [(1,1), (1,1), (1,1), (1,1)]
firstPanelWidgetTypes = ["textWidget", "button", "choice", "choice"]
widgetsOne = []

for index, item in enumerate(firstPanelNames):
  widgetsOne.append(aWidget(name = firstPanelNames[index], coords = firstPanelCoords[index], \
                            widgetType = firstPanelWidgetTypes[index], span = firstPanelSpans[index],\
                            label = firstPanelLabels[index], labelPosition = "left"))

for index, item in enumerate(widgetsOne):
  print item.name

  #def __init__(self,name,coords,span=(1,1),widgetType,label=None,labelPosition=None,**kwargs):















thisFrame.Show()
app.MainLoop()







