"""
This demo demonstrates how to embed a matplotlib (mpl) plot 
into a PyQt4 GUI application, including:

* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu

The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
#added
import pygraphviz as pgv
from networkx import *
##import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import *
from matplotlib import *

class AppForm(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.setWindowTitle('Demo: PyQt with matplotlib')

		self.create_menu()
		self.create_main_frame()
		self.create_status_bar()

##		self.textbox.setText('1 2 3 4')
		self.on_draw()

	def save_plot(self):
		file_choices = "PNG (*.png)|*.png"
		
		path = unicode(QFileDialog.getSaveFileName(self, 
						'Save file', '', 
						file_choices))
		if path:
			self.canvas.print_figure(path, dpi=self.dpi)
			self.statusBar().showMessage('Saved to %s' % path, 2000)
	
	def on_about(self):
		msg = """ A demo of using PyQt with matplotlib:
		
		 * Use the matplotlib navigation bar
		 * Add values to the text box and press Enter (or click "Draw")
		 * Show or hide the grid
		 * Drag the slider to modify the width of the bars
		 * Save the plot to a file using the File menu
		 * Click on a bar to receive an informative message
		"""
		QMessageBox.about(self, "About the demo", msg.strip())
	
	def on_pick(self, event):
		# The event received here is of the type
		# matplotlib.backend_bases.PickEvent
		#
		# It carries lots of information, of which we're using
		# only a small amount here.
		# 		def onpick1(event):
		if isinstance(event.artist, Text):
			text = event.artist
			value = text.get_prop_tup()
			text_to_pass = value[2]
##				print('Hai selezionato l\'US:', text.get_text())
##		box_points = event.artist.get_bbox().get_points()
			msg = "'Hai selezionato l\'US:' %s" % text_to_pass #str(dir(text.get_label))
		
			QMessageBox.information(self, "Click!", msg)
	
	def on_draw(self):
		""" Redraws the figure
		"""
		A=pgv.AGraph(directed=True)

		A.add_edge(1,2)
		A.add_edge(2,3)
		A.add_edge(3,4)
		A.add_edge(3,5)
		A.add_edge(2,5)
		A.add_edge(2,6)
		A.add_edge(2,16)
		A.add_edge(2,22)
		A.add_edge(2,33)
		A.add_edge(33,45)
		A.add_edge(45,7)
		A.add_edge(45,9)
		A.add_edge(45,123)

		A.add_edge(45,46)
		A.add_edge(45,47)
		A.add_edge(3,4)
		A.add_edge(3,5)
		A.add_edge(2,5)
		A.add_edge(2,6)
		A.add_edge(2,16)
		A.add_edge(2,7)
		A.add_edge(2,7)
		A.add_edge(2,7)
		A.add_edge(2,7)
		A.add_edge(2,7)
		A.add_edge(2,7)

		A.tred()

		G1=nx.DiGraph(A)

		pos=nx.graphviz_layout(G1,prog='dot')

		#self.fig = plt.figure()

		ax = self.fig.add_subplot(111)
		
		
		ax.set_title('Clicca su una US', picker=True)
		ax.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))

		points = []
		key = []
		for k,v in pos.items():
			key.append(k)
			points.append(v)

			
		for i in range(len(key)):
			ax.text(points[i][0],points[i][1], key[i], picker=True,ha='center', alpha=0)

		ax.plot(nx.draw(G1,pos,
						with_labels=True,
						arrows=True,
						node_color='w',
						node_shape= 's',
						node_size=400),'o',picker=10000)

##		str = unicode(self.textbox.text())
##		self.data = map(int, str.split())
##		
##		x = range(len(self.data))
##
##		# clear the axes and redraw the plot anew
##		#
##		self.axes.clear()        
##		self.axes.grid(self.grid_cb.isChecked())
##		
##		self.axes.bar(
##			left=x, 
##			height=self.data, 
##			width=self.slider.value() / 100.0, 
##			align='center', 
##			alpha=0.44,
##			picker=5)
		
		self.canvas.draw()
	
	def create_main_frame(self):
		self.main_frame = QWidget()
		
		# Create the mpl Figure and FigCanvas objects. 
		# 5x4 inches, 100 dots-per-inch
##		# Since we have only one plot, we can use add_axes 
##		# instead of add_subplot, but then the subplot
##		# configuration tool in the navigation toolbar wouldn't
##		# work.
##		#
		#self.axes = self.fig.add_subplot(111)
		
		# Bind the 'pick' event for clicking on one of the bars
		#
		self.dpi = 100
		self.fig = plt.figure()
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self.main_frame)
		self.canvas.mpl_connect('pick_event', self.on_pick)
		
		# Create the navigation toolbar, tied to the canvas
		#
		self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
		#
		# Layout with box sizers
		# 
		hbox = QHBoxLayout()

		vbox = QVBoxLayout()
		vbox.addWidget(self.canvas)
		vbox.addWidget(self.mpl_toolbar)
		vbox.addLayout(hbox)
		
		self.main_frame.setLayout(vbox)
		self.setCentralWidget(self.main_frame)
	
	def create_status_bar(self):
		self.status_text = QLabel("This is a demo")
		self.statusBar().addWidget(self.status_text, 1)
		
	def create_menu(self):        
		self.file_menu = self.menuBar().addMenu("&File")
		
		load_file_action = self.create_action("&Save plot",
			shortcut="Ctrl+S", slot=self.save_plot, 
			tip="Save the plot")
		quit_action = self.create_action("&Quit", slot=self.close, 
			shortcut="Ctrl+Q", tip="Close the application")
		
		self.add_actions(self.file_menu, 
			(load_file_action, None, quit_action))
		
		self.help_menu = self.menuBar().addMenu("&Help")
		about_action = self.create_action("&About", 
			shortcut='F1', slot=self.on_about, 
			tip='About the demo')
		
		self.add_actions(self.help_menu, (about_action,))

	def add_actions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)

	def create_action(  self, text, slot=None, shortcut=None, 
						icon=None, tip=None, checkable=False, 
						signal="triggered()"):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/%s.png" % icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			self.connect(action, SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action


def main():
	print sys.argv
	app = QApplication(sys.argv)
	form = AppForm()
	form.show()
	app.exec_()


if __name__ == "__main__":
	main()
