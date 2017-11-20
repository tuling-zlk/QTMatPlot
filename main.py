#! /usr/bin/python3

# Stuff to get the window open.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QPushButton, QTreeWidget, QTreeWidgetItem, QGraphicsAnchorLayout, QScrollArea, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

# Matplotlib stuff
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
import seaborn as sns
import h5py
import ast
sns.set_style('ticks')
sns.set_context('paper')
sns.axes_style({'font.family': ['monospace'],
                'font.sans-serif': ['monospace']
                })
sns.set(font='sans-serif', style='ticks')
#sns.set_palette('husl')
sns.set_palette('deep')

# and here http://www.boxcontrol.net/embedding-matplotlib-plot-on-pyqt5-gui.html

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Button Functions
@pyqtSlot()
def button_test():
    print("We're clicking a button, wheee")

# Now, from that other site...
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=7, height=4, dpi=300, num=1, data=None):
        sns.set_style('ticks')
        sns.set_context('paper')
        sns.axes_style({'font.family': ['monospace'],
                        'font.sans-serif': ['monospace']
                        })
        sns.set(font='sans-serif', style='ticks')
        #sns.set_palette('husl')
        sns.set_palette('deep')
        self.data = data
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # We want the axes cleared every time plot() is called


        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)'''

        #self.mpl_connect("scroll_event", self.scrolling)

        self.mpl_dict_lit = '''{
                                'Rows': 2, 
                                'Columns': 4,
                                'dpi': 300,
                                'figsize': {
                                  'width': 7,
                                  'height': 4,
                                 },
                                'Figures': {}
                               }'''
        self.mpl_dict = ast.literal_eval(self.mpl_dict_lit)
        self.fig_dict = '''{ 'type': 'plot', 'data': None }'''
        self.compute_initial_figure()
        self.update_figure()
        ##timer = QtCore.QTimer(self)
        ##timer.timeout.connect(self.update_figure)
        ##timer.start(1000)

    def compute_initial_figure(self):
        self.updateFromDict()

    def plot(self, pd, ax):
        # pd is the plot dictionary
        if pd['data'] != None:
            if pd['type'] == 'plot':
                print("PLOT IT BABY")
                ax.plot(self.translate_location(pd['data']))
                #self.axes

    def updateFromDict(self):
        d = self.mpl_dict
        # Clears the figure before we plot more.
        self.fig.clear()
        self.axes = self.fig.subplots(nrows=int(d['Rows']), ncols=int(d['Columns']))
        self.fig.set_size_inches(float(d['figsize']['width']), float(d['figsize']['height']))
        self.fig.set_dpi(int(d['dpi']))
        # We check to see if we need to update the figures.
        # This should just occur on a rebuild, so if we haven't added anything, don't worry about it.
        print(self.mpl_dict)
        for rows in range(0, int(self.mpl_dict['Rows'])):
            for cols in range(0, int(self.mpl_dict['Columns'])):
                if str((rows, cols)) not in self.mpl_dict['Figures']:
                    self.mpl_dict['Figures'][str((rows,cols))] = ast.literal_eval(self.fig_dict)
                # Throw in the axes object.
                #print(self.mpl_dict['Figures'][(rows,cols)])
                self.plot(self.mpl_dict['Figures'][str((rows,cols))], self.axes[rows,cols])
                



    def updateSize(self, height, width):
        pass

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        # We call this whenever the dictionary is updated.
        self.updateFromDict()
        #l = [np.random.randint(0, 10) for i in range(4)]

        #self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
        FigureCanvas.updateGeometry(self)

    def save_figure(self):
        self.fig.savefig("test.pdf")

    def translate_location(self, location):
        data_loc = None
        location = ast.literal_eval(location)
        print(location, len(location))
        if len(location) == 1:
            data_loc = self.data[location[0]][:]
        elif len(location) == 2:
            try:
                data_loc = self.data[location[0]][:,int(location[1])]
            except:
                data_loc = self.data[location[0]][location[1]][:]
        elif len(location) == 3:
            try:
                data_loc = self.data[location[0]][:,int(location[1]), int(location[2])]
            except:
                data_loc = self.data[location[0]][location[1]][:,int(location[2])]
        elif len(location) == 4:
            print(len(location), location)
            try:
                data_loc = self.data[location[0]][:,int(location[1]), int(location[2]), int(location[3])]
            except:
                data_loc = self.data[location[0]][:,int(location[1]), int(location[2])][location[3]]
        return data_loc


class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Widgets are movable.
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)
        kinetics = h5py.File('direct.h5', 'r')
        dc = MyMplCanvas(self.main_widget, width=10, height=8, dpi=100, data=kinetics)

        # Try the scroll!
        self.scroll = QScrollArea(self.main_widget)
        #self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(False)
        scrollContent = QWidget(self.scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        scrollLayout.addWidget(dc)
        self.scroll.setWidget(scrollContent)
        self.layout.addWidget(self.scroll)

        #self.layout.addWidget(dc)
        self.main_widget.move(250,0)
        self.main_widget.setLayout(self.layout)
        #button = self.newButton(self, "Button!", "Nothing", (100,70), self.button_test, click_args=None)
        testDict = {'0': ['0', '1'], '1': {'A': ['2'], 'B': ['3', '4']}}
        self.save_button = self.newButton(self, "Save", "Saves the Figure", (250,self.height-30), dc.save_figure, click_args=None)
        self.text = self.newTextBox(self, size=(0,0), pos=(self.save_button.button.width()+250, self.height-30), init_text="{}".format(kinetics))
        self.dataTree = self.newTree(self, dict(kinetics), pos=(0, 0), size=(250,self.height/2), col=3, clickable=True, editable=False, function=self.text.showText)
        self.mplTree = self.newTree(self, dc.mpl_dict, pos=(0,self.height/2), size=(250,self.height/2), col=1, function=dc.update_figure)
        #def __init__(self, parent, size, pos, init_text=""):
        #print(dir(layout))
        #layout.addChildWidget(self.dataTree)
        self.show()

    def resizeEvent(self, event):
        # size().height/width should do it.
        self.resizeAll(event.size().height, event.size().width)
        pass

    def resizeAll(self, height, width):
        self.dataTree.tree.resize(self.dataTree.tree.width(), height()/2)
        self.mplTree.tree.setGeometry(0, height()/2, 250, height()/2)
        self.main_widget.setGeometry(250, 0, width()-250, (height()-25))
        self.save_button.button.move(250,height()-30)
        self.text.textBox.setGeometry(self.save_button.button.width()+250, height()-30, width()-250-self.save_button.button.width(), 30)

    def keyPressEvent(self, e):
        # This is our key press handler.  It's mostly just a stub right now.
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def wheelEvent(self, e):
        # This is what happens when we scroll.
        #print(self.tree.data)
        pass

    # Data loading; for now, just do hdf5

    # For displaying data in a tree.
    class newTree():
        def __init__(self, parent, data, pos, col=1, rows=True, size=None, editable=True, clickable=False, function=None):
            self.tree = QTreeWidget(parent)
            self.tree.setColumnCount(col)
            self.parent = parent
            self.col = col
            self.pos = pos
            self.size = size
            #A = QTreeWidgetItem(self.tree, ["A"])
            self.data = data
            if size:
                self.tree.setGeometry(pos[0], pos[1], size[0], size[1])
            self.function = function
            self.editable = editable
            #self.tree.move(pos[0], pos[1])
            # How should we handle this?  Like dictionaries, let's assume.
            self.rows = rows
            self.treeItemKeyDict = {}
            self.updateTree()
            if editable:
                self.tree.itemChanged.connect(self.onItemChanged)
            if clickable:
                self.tree.clicked.connect(self.onClicked)

        def updateData(data):
            self.data = data
            self.updateTree()

        def updateTree(self):
            # Python 3 just uses items, not iteritems.
            #self.tree = QTreeWidget(self.parent)
            #self.tree.setColumnCount(self.col)
            #A = QTreeWidgetItem(self.tree, ["A"])
            if self.size:
                self.tree.setGeometry(self.pos[0], self.pos[1], self.size[0], self.size[1])
            if type(self.data) == dict:
                self.handleDict(self.data, self.tree)

        def handleDict(self, dict_data, tree, key_list=[]):
            # We can actually have numerous structures, here.
            # Why not keep track of it, for now?
            # We want to do a reverse lookup
            for key, val in dict_data.items():
                keyTree = QTreeWidgetItem(tree, [str(key)])
                self.treeItemKeyDict[str(keyTree)] = key_list + [str(key)]
                if type(val) == dict:
                    self.handleDict(val, keyTree, key_list + [str(key)])
                elif type(val) == h5py._hl.dataset.Dataset:
                    if len(val.shape) == 1:
                        # Here, we don't want to display everything in the list.  Just... let it be.
                        valTree = QTreeWidgetItem(keyTree, [str(val)])
                        self.treeItemKeyDict[str(valTree)] = key_list + [str(key)]
                        if hasattr(val, 'dtype'):
                            if len(val.dtype) > 1:
                                print(len(val.dtype))
                                for iv in range(0, len(val.dtype)):
                                    dtypeTree = QTreeWidgetItem(valTree, [str(val.dtype.names[iv])])
                                    self.treeItemKeyDict[str(dtypeTree)] = key_list + [str(key)] + [str(val.dtype.names[iv])]
                    elif len(val.shape) > 1:
                        for n in range(1, len(val.shape)):
                            for i in range(0, n):
                                for j in range(0, n):
                                    if i != j:
                                        # Iterate through and add each dimension that isn't time to the list.
                                        valTree = QTreeWidgetItem(keyTree, [str(key), str(i), str(j)])
                                        self.treeItemKeyDict[str(valTree)] = key_list + [str(key), str(i), str(j)]
                                        if hasattr(val, 'dtype'):
                                            if len(val.dtype) > 1:
                                                for iv in range(0, len(val.dtype)):
                                                    dtypeTree = QTreeWidgetItem(valTree, [str(val.dtype.names[iv])])
                                                    self.treeItemKeyDict[str(dtypeTree)] = key_list + [str(key)] + [str(i), str(j)] + [str(val.dtype.names[iv])]
                else:
                    # We want this to be like rows, not columns
                    if self.rows:
                        if type(val) == list:
                            for iv, v in enumerate(val):
                                valTree = QTreeWidgetItem(keyTree, [str(v)])
                                #key_list.append(val)
                                self.treeItemKeyDict[str(valTree)] = key_list + [str(key)] + [iv]
                                if self.editable:
                                    valTree.setFlags(valTree.flags() | QtCore.Qt.ItemIsEditable)
                        else:
                            valTree = QTreeWidgetItem(keyTree, [str(val)])
                            #key_list.append(val)
                            self.treeItemKeyDict[str(valTree)] = key_list + [str(key)]
                            if self.editable:
                                valTree.setFlags(valTree.flags() | QtCore.Qt.ItemIsEditable)
                    else:
                        valTree = QTreeWidgetItem(keyTree, val)
                        #key_list.append(val)
                        self.treeItemKeyDict[str(valTree)] = key_list + [str(key)]
                        if self.editable:
                            valTree.setFlags(valTree.flags() | QtCore.Qt.ItemIsEditable)

        def onItemChanged(self, test):
            # This works.
            #print("Changed!")
            print(self.treeItemKeyDict[str(test)])
            # Find the key in the data.
            #print(dir(test))
            val = self.data
            x = self.data
            # Recurse through the dictionary
            for key in self.treeItemKeyDict[str(test)]:
                if type(x.get(key)) == dict:
                    val = val.get(key)
                    x = x.get(key)
                    print(key)
            # Because we return the child widget, this is fine.
            print(val, key)
            # You can't have non list data, so enforce list type.
            # Well, that won't work for mpl stuff, so.
            #try:
            val[key] = test.data(0,0)
            #except:
            #    val = test.data(0,0)
            print(self.data)
            if self.function:
                self.function()
            # Oh hacky, hacky, hack
            self.tree.itemChanged.disconnect()
            self.tree.clear()
            self.updateTree()
            self.tree.itemChanged.connect(self.onItemChanged)
            # We also need to rebuild our tree, unfortunately.
            # Although this loops forever, so I'm missing something.
            # I'm not sure why it doesn't properly... update the whole thing?
            #print(test.data(0,0))

        def onClicked(self, test):
            #print(self.tree.selectedItems())
            #print(self.treeItemKeyDict)
            # This is the thing which will actually return our dataset.
            #print(self.treeItemKeyDict[str(self.tree.selectedItems()[0])])
            location = self.treeItemKeyDict[str(self.tree.selectedItems()[0])]
            # One thing we don't know is precisely how to format this, but that's okay.
            # We could just change this later.
            # We should probably store how we formatted it with the reverse dictionary, but.
            if self.function:
                self.function(str(location))

    class newTextBox():
        def __init__(self, parent, size, pos, init_text=""):
            self.textBox = QLineEdit(parent)
            self.textBox.setText(init_text)

        def showText(self, text):
            self.textBox.setText(text)

    class newButton():
        def __init__(self, parent, label, tooltip, pos, function, click_args=None):
            # pos should be an x,y tooltip
            # Generic implementation of a button.
            # The function needs a pyqtSlot decorator, and should probably be pickable.
            self.button = QPushButton(label, parent)
            self.button.move(pos[0], pos[1])
            self.click_args = click_args
            self.function = function
            self.button.clicked.connect(self.function)

    # For our buttons.
    @pyqtSlot()
    def button_test(self):
        print("We're clicking a button, wheee")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


