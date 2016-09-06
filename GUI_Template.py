# note - on OSX, requires framework build of python/2.7 to run, as this
# application requires access to the screen (this might only apply to systems
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
import wx, os
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

# global dictionary in which we store data
myDict = {}

class Frame(wx.Frame):
    # note to others: we pass another class (an instance of MainFrame) to this wx.Frame derived class;
    # the ambiguity of parent in the class __init__ vs the wx.Frame.__init__ is due to parent in the
    # wx.Frame.__init__ function being a /keyword/ argument, rather than a python convention, as is used
    # in the class __init__ funciton.  The wx.Frame.__init__ parent argument /must/ be a wx.Window object,
    # or simply value "None", which is what we usually use
    def __init__(self,parent):
        wx.Frame.__init__(self,parent=parent._windowObj,title = parent._title, size = parent._size)
        self.Show()


# we define our own MainFrame() class, because we don't instantly want to create an actual wx.Frame object yet
class MainFrame:
  _register = []
    # implicit argument self
    # parent: typically None, but if a frame is spawned dynamically it may be useful to pass the relevant object
    # title: string displayed at the top of the frame (the name)
    # size: integer tuple (e.g., (100,100)) specifying the size of the frame
  def __init__(self, parent, title, size, **kwargs):
      self._parent = parent;
      self._title = title;
      self._size = size;
      self._windowObj = kwargs.get("windowObj",None)


  def initFrame(self):

      # make an instance of the frame, that is an derived class of the wx.Frame class
      self._frame = Frame(self)

# this class will be used as the parent panel for any notebook-type pages;
# likely that these Notebook objects will be the direct children of the frame, rather than an
# object of the Panel class

# TODO: this needs to be refined, heavily
class Notebook(wx.Panel):
    # the implicit self argument
    # parent panel object
    # the pages to be added to this notebook
    # and the names of the pages
  def __init__(self,parent,pages):
    # instantiate the notebook
    thisNotebook = wx.Notebook(self, parent)
    self.listOfPageObjs = []
    self.pageObjs = []

    for index, item in enumerate(pages):
      self.listOfPageObjs.append(str(item))
      self.pageObjs.append(item(thisNotebook))

      ## need their names here
      # we should be able to obtain them via a wx() method
      thisNotebook.AddPage(self.pageObjs[index],objName)

    # add a sizer to the notebook
    thisSizer=wx.BoxSizer()
    thisSizer.Add(thisNotebook,1,wx.EXPAND)
    self.SetSizer(thisSizer)

    self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
  # we can define this dynamically (per-instance of the object)
  # and outside of the class
  def customBehavior():
    pass

  def OnPageChanging(self,event):
    oldPage = event.GetOldSelection()
    newPage = event.GetSelection()

    customBehavior()

class Panel(wx.Panel):
    def __init__(self,parent,wxObj):
        # again, in the wx.Panel.__init__ function call, parent is a keyword argument that takes a wx object
        wx.Panel.__init__(self,parent=wxObj);

# in this class, we collate all the information we'll need to make a well-defined wx.Panel object
class BasePanel:

  def __init__(self,parent):
    # on initialization, the panel should be initialized ...
    wx.Panel.__init__(self,parent);

    # a grid object, on which widgets will be placed
    self.grid = wx.GridBagSizer(hgap=5,vgap=5);

    # we record whether this panel is a notebook; whether it has a friend ;
    # whether it has a parent; whether it has a child; whether it has widgets;

    # note that all panels have a parent; top level panels have the frame as their parent object,
    # which in turn has the window as its parent
    self._isNotebook = False;
    self._hasFriend = False;
    self._hasParent = True;
    self._hasChild = False;
    self._hasWidgets = False;

    # a given panel may be a member of one notebook;
    # a given panel may have multiple siblings;
    # a given panel may have one parent;
    # a given panel may have multiple children;
    self._notebookName = [];
    self._friends = [];

    # TODO: pseudocode; change this
    #self._parent = wx.GetName(parent);
    # end todo

    self._children = [];
    self._widgets = [];


  def addWidget(widget):
    # when adding a widget, we consider the grid position it will be added to, as well
    # as the flags which will be implemented when placing the widget on the grid

    #first, we need to get the information from the widget

    # TODO: un-pseudocode this;
    #some pseudocode of what we need from the widget when we instantiate it
    #widgetName = wx.GetName(widget);
    #widgetID = wx.GetID();
    #widgetCoords = wx.GetCoords(widget);
    #widgetSpan = wx.GetSpan(widget);
    #widgetFlags = wx.GetFlags(widget);

    # should the widget already be bound to a function? consider this (TODO)
    #self.grid.Add(widget.
    pass

    # destroy an object of type Widget
  def deleteWidget():
    pass

  def bindToFunction():
    # ehhhh... we might have already done this in the widget class. could be better that way.
    pass

# TODO: consider, what other information is general to all widgets? are there any objects here now
# that might be considered extraneous to the majority of them? reduce waste
class Widget:
  def __init__(self,name,coords,widgetType,span=(1,1),parent=None,label=None,labelPosition=None,**kwargs):
    # note that we use **kwargs to pass in information that may be specific to certain type
    # of widget; e.g., text widget vs button vs ... etc.
    # **kwargs is a list of KeyWord ARGumentS (kwargs)  of arbitrary length
    # note that, by default, there is no label (and no label position <(int,int)> provided
    self._name = name; #string
    self._coords = coords; #tuple of coords: "(integer, integer)"
    self._widgetType = widgetType; # button, textwidget, label, etc.
    self._parent = parent;
    # default behavior of span is (1,1) if not specified;
    self._span = span

    if label:
      self.label = label
      try:
        self.labelPosition = labelPosition
      except:
        print "Error: label %s specified, but no label position tuple (int,int) given! " %label

      #  if self._widgetType is "staticText":
      pass
    elif self._widgetType is "button":
      pass
    elif self._widgetType is "textWidget":
      pass

  def instantiateWidget(self):
    self._parent.addWidget(self)

  def makeWidget(self):
    pass

