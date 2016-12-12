#********************************************************************************
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
#   Created by Brian Keene on 8 September 2016
#
#   Revision history:
#
#
#********************************************************************************
# note - on OSX, requires framework build of python/2.7 to run, as this
# application requires access to the screen (this might only apply to systems
# running Mavericks or later)

# This script for a graphical user interface is intended to serve as a template for
# graphical user interfaces; primarily intended to be used as a simplified
# front-end of wx.Widgets, and to allow for easy setup of dynamic hiding that
# might involve cross-communication between objects of assorted placement in
# the hierarchy of parent-child objects.  Allows for an OOP creation of a GUI,
# with emphasis on easy modification in the accompanying script.

# import the needed modules
import wx, os

# global dictionary in which we store data
myDict = {}

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
        wx.Notebook(sibling._parent._obj)
        self._pages = [];
        for index, item in enumerate(sibling._children):
            item.initObj();
            self._pages.append(item._obj)
            self.AddPage(self._pages[index], item._name);
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
        self._initValue = kwargs.get('value',"")
        self._function = kwargs.get('function',None)
        self._wxEvt = None
        self._hasMaster = False; # default this to false; changed if the setMaster() function is called on self
        self._hasSlave = False;
        # these will be instantiated during the creation of the parent object
        self._labelObj = None;
        self._obj = None;

        # Hide most objects at first; that way, they only show if they are told to show,
        # and otherwise will hide when told to hide
        # implement this /after/ we have connected all the show/hide funcitonality
        self._initHide = False;

        # TODO: have the Panel's grid.Add() method use these flags when instantiating the widget
        self._gridFlags = (wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.EXPAND | wx.ALIGN_CENTER)

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
            self._obj = wx.TextCtrl(parentInstance,value=self._initValue,name=self._name)
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


