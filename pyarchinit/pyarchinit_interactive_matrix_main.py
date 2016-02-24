#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
        					 stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi
    email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import csv_writer
from csv_writer import *
import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from datetime import date
from psycopg2 import *



#--import pyArchInit modules--#
#from  pyarchinit_inventario_reperti_ui import Ui_DialogInventarioMateriali
from  pyarchinit_interactive_matrix_gui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *
try:
	import pygraphviz as pgv
except:
	pass
from networkx import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import *
from matplotlib import *


from  pyarchinit_matrix_exp import *


try:
	from  pyarchinit_db_manager import *
except:
	pass

from  pyarchinit_exp_Findssheet_pdf import *

from  imageViewer import ImageViewer
import numpy as np
import random
from numpy import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from  pyarchinit_pyqgis import Pyarchinit_pyqgis

class pyarchinit_Interactive_Matrix(QDialog, Ui_DialogInteractiveMatrix):
	MSG_BOX_TITLE = "PyArchInit - Scheda Sistema Matrix Interattivo"
	DB_MANAGER = ""
	DATA_LIST = ""
	ID_US_DICT = {}

	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	QUANT_PATH = ('%s%s%s') % (HOME, os.sep, "pyarchinit_Quantificazioni_folder")

	def __init__(self, iface, data_list, id_us_dict):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)
		self.DATA_LIST = data_list
		self.ID_US_DICT = id_us_dict
		QDialog.__init__(self)
		self.setupUi(self)

##		self.textbox.setText('1 2 3 4')
		#self.on_draw()
		try:
			self.DB_connect()
		except:
			pass

	def DB_connect(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except Exception, e:
			e = str(e)
			QMessageBox.warning(self, "Alert", "Attenzione rilevato bug! Segnalarlo allo sviluppatore <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)


	def generate_matrix(self):
		data = []
		for sing_rec in self.DATA_LIST:
			us = unicode(sing_rec.us)
			rapporti_stratigrafici = eval(sing_rec.rapporti)
			for sing_rapp in rapporti_stratigrafici:
				try:
					if sing_rapp[0] == 'Taglia' or  sing_rapp[0] == 'Copre' or  sing_rapp[0] == 'Si appoggia a' or  sing_rapp[0] == 'Riempie' or sing_rapp[0] == 'Si lega a' or  sing_rapp[0] == 'Uguale a':
						if sing_rapp[1] != '':
							harris_rapp = (us, str(sing_rapp[1]))
							data.append(harris_rapp)
				except Exception, e:
					QMessageBox.warning(self, "Messaggio", "Problema nel sistema di esportazione del Matrix:" + str(e), QMessageBox.Ok)

		sito = self.DATA_LIST[0].sito

		search_dict = {
		'sito'  : "'"+unicode(sito)+"'"
		}

		periodizz_data_list = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

		periodi_data_values = []
		for i in periodizz_data_list:
			periodi_data_values.append([i.periodo,i.fase])

		periodi_us_list = []

		clust_number = 0
		for i in periodi_data_values:
			search_dict = {
			'sito'  : "'"+unicode(sito)+"'",
			'periodo_iniziale'  : "'"+unicode(i[0])+"'",
			'fase_iniziale' : "'"+unicode(i[1])+"'"
			}

			us_group = self.DB_MANAGER.query_bool(search_dict, 'US')

			cluster_label = "cluster%d" % (clust_number)

			periodo_label = "Periodo %s - Fase %s" % (str(i[0]), str(i[1]))

			sing_per = [cluster_label, periodo_label]

			sing_us = []
			for rec in us_group:
				sing_us.append(rec.us)
			
			sing_per.insert(0,sing_us)
			
			periodi_us_list.append(sing_per)
			
			clust_number += 1

		matrix_exp = HARRIS_MATRIX_EXP(data, periodi_us_list)
		data_plotting = matrix_exp.export_matrix()
		
		return data_plotting

		QMessageBox.warning(self, "Messaggio", "Esportazione del Matrix terminata", QMessageBox.Ok)

	def plot_matrix(self, dp):
		self.data_plot = dp

		G1=nx.DiGraph(self.data_plot)          # now make it a Graph 
		#G1.write_dot(G1,'test.dot')
		#nx.write_dot(G1,'test.dot')
		#plt.title("draw_networkx")
		pos=nx.graphviz_layout(G1,prog='dot')
		#fig = plt.figure()

		#self.widgetMatrix.canvas.ax = self.fig.add_subplot(111)
	
		self.widgetMatrix.canvas.ax.set_title('click su una US per disegnarla a video', picker=True)
		self.widgetMatrix.canvas.ax.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))

		points = []
		key = []
		for k,v in pos.items():
			key.append(k)
			points.append(v)

		for i in range(len(key)):
			self.widgetMatrix.canvas.ax.text(points[i][0],points[i][1], key[i], picker=True,ha='center', alpha=0)
		
		self.widgetMatrix.canvas.ax.plot(nx.draw(G1,pos,
						with_labels=True,
						arrows=True,
						node_color='w',
						node_shape= 's',
						node_size=400),'o',picker=1000)

		#self.widgetMatrix.canvas.fig.canvas.mpl_connect('pick_event', self.on_pick)
		self.widgetMatrix.canvas.mpl_connect('pick_event', self.on_pick)
		self.widgetMatrix.canvas.draw()

	def on_pick(self, event):
		# The event received here is of the type
		# matplotlib.backend_bases.PickEvent
		#.canvas
		# It carries lots of information, of which we're using
		# only a small amount here.
		# 		def onpick1(event):
		#if isinstance(event.artist, Text):
		text = event.artist
		value = text.get_prop_tup()
		text_to_pass = value[2]
##				print('Hai selezionato l\'US:', text.get_text())
##		box_points = event.artist.get_bbox().get_points()
		idus = self.ID_US_DICT[int(text_to_pass)]
		self.pyQGIS.charge_vector_layers_from_matrix(idus)
		#msg = "'Hai selezionato l\'US:' %s" % text_to_pass #str(dir(text.get_label))

		#QMessageBox.information(self, "Click!", msg)

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()

## Class end

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = pyarchinit_US()
	ui.show()
	sys.exit(app.exec_())
