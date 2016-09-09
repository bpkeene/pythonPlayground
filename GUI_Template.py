# note - on OSX, requires framework build of python/2.7 to run, as this
# application requires access to the screen (this might only apply to systems
# running Mavericks or later)


# This script for a graphical user interface is intended to serve as a template for future, complex
# graphical user interfaces; primarily intended to be used as a simplified front-end of wx.Widgets,
# allow for easy setup of dynamic hiding that might involve cross-communication between objects of
# assorted placement in the hierarchy of parent-child objects.
# Allows for an OOP creation of a GUI, with emphasis on easy modification in the accompanying script.

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

class wxFrame(wx.Frame):
    # note to others: we pass another class (an instance of MainFrame) to this wx.Frame derived class;
    # the ambiguity of parent in the class __init__ vs the wx.Frame.__init__ is due to parent in the
    # wx.Frame.__init__ function being a /keyword/ argument, rather than a python convention, as is used
    # in the class __init__ funciton.  The wx.Frame.__init__ parent argument /must/ be a wx.Window object,
    # or simply value "None", which is what we usually use
    def __init__(self,sibling):
        wx.Frame.__init__(self,parent=sibling._windowObj,title = sibling._title, size = sibling._size)

# we define our own MainFrame() class, because we don't instantly want to create an actual wx.Frame object yet
class Frame:

    # a static class object we can access using MainFrame._register[index] - we don't access this via an instance of
    # the class; we can also iterate over it, looking for objects with
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
        self._windowObj = kwargs.get("windowObj",None)

        # an instance variable holding other instances that are children of this instance
        self._children = []


    def initObj(self):

        # make an instance of the frame, that is an derived class of the wx.Frame class
        self._obj = wxFrame(self)
        Frame._register.append(self)

        # iterate over this instance's children and initialize them.
        for obj in self._children:
            obj.initObj();
        self._obj.Show()


# this class will be used as the parent panel for any notebook-type pages;
# likely that these Notebook objects will be the direct children of the frame, rather than an
# object of the Panel class
# or is it an object of the notebook class?
#class wxNotebook:
#
#    # an implicit self argument
#    # and the parent instance to which this notebook will be added
#    def __init__(self,sibling):
#        self._obj = wx.Notebook(sibling._parent._obj);
#
#        self._children = [];
#        for index, obj in enumerate(sibling._children):
#            # call the init() methods of the child objects;
#            # and then we want to append the wx instances of the child objects
#            # after that, we want to head to
#            obj.initObj();
#            self._children.append(obj._obj)
#            self._obj.AddPage(self._children[index], obj._name)


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

        # our wxNotebook method initiates the instantation of the self._children objects
        self._obj = wx.Notebook(self._parent._obj)
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
        print sibling._name
        wx.Panel.__init__(self,parent=sibling._parent._obj);
        self.grid = wx.GridBagSizer(hgap=5,vgap=5);
        self.SetSizer(self.grid);

        # call the init methods of the objects, which then places wxWidget objects in the self._widgets variable for
        # each Widget class instance
        for obj in sibling._children:
            if obj._typeName == "Widget":
                obj.init();
                self.grid.Add(obj._widget, pos=obj._pos, span=obj._span)
                # call the self.Bind() functionality here

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

class Widget:
    _register = []
    _typeName = "Widget"


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

        # a buffer value - holds the data immediately prior to the widget's most recent interaction
        # for choice widgets, this will be a complete value; for textwidgets, it will be string = str[:-2]
        self._buffer = ""

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

