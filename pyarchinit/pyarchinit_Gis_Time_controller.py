#! /usr/bin/env python
#-*- coding: utf-8 -*-
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

from  pyarchinit_db_manager import *

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_gis_time_controller import Ui_DialogGisTimeController
from  pyarchinit_gis_time_controller import *
from  pyarchinit_utility import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  sortpanelmain import SortPanelMain

class pyarchinit_Gis_Time_Controller(QDialog, Ui_DialogGisTimeController):
	MSG_BOX_TITLE = "PyArchInit - Gis Time Management"
	DB_MANAGER = ""
	ORDER_LAYER_VALUE = ""
	MAPPER_TABLE_CLASS = "US"

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)
		QDialog.__init__(self)
		self.setupUi(self)

		self.currentLayerId = None
		try:
			self.connect()
		except:
			pass

		QObject.connect(self.dial_relative_cronology, SIGNAL("valueChanged(int)"),self.set_max_num)
		QObject.connect(self.spinBox_relative_cronology, SIGNAL("valueChanged(int)"),self.set_max_num)

		QObject.connect(self.dial_relative_cronology, SIGNAL("valueChanged(int)"),self.define_order_layer_value)
		QObject.connect(self.dial_relative_cronology, SIGNAL("valueChanged(int)"),self.spinBox_relative_cronology.setValue)

		QObject.connect(self.spinBox_relative_cronology, SIGNAL("valueChanged(int)"),self.define_order_layer_value)
		QObject.connect(self.spinBox_relative_cronology, SIGNAL("valueChanged(int)"),self.dial_relative_cronology.setValue)

	def connect(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "Attenzione rilevato bug! Segnalarlo allo sviluppatore<br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def set_max_num(self):
		max_num_order_layer = self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, "order_layer")+1,
		self.dial_relative_cronology.setMaximum(max_num_order_layer[0])
		self.spinBox_relative_cronology.setMaximum(max_num_order_layer[0])

	def define_order_layer_value(self,v):
		try:
			self.ORDER_LAYER_VALUE= v
			layer = self.iface.mapCanvas().currentLayer().dataProvider()
			originalSubsetString = layer.subsetString()
			#if originalSubsetString != "":
			newSubSetString = "order_layer <= %s" % (self.ORDER_LAYER_VALUE) #4D dimension
			layer.setSubsetString(newSubSetString)
			self.iface.mapCanvas().refresh()
		except:
			QgsMessageLog.logMessage("You must to load pyarchinit_us_view and/or select it from pyarchinit GeoDatabase")
			#QMessageBox.warning(self.iface.mainWindow(), "Help", "You must to load pyarchinit_us_view from pyarchinit GeoDatabase")
			self.iface.messageBar().pushMessage("Help", "You must to load pyarchinit_us_view and/or select it from pyarchinit GeoDatabase", level=QgsMessageBar.WARNING)

##		f = open("C:/test_dial.txt", "w")
##		f.write(str(self.ORDER_LAYER_VALUE))
##		f.close()

	def reset_query(self):
		self.ORDER_LAYER_VALUE = v

	def on_pushButton_visualize_pressed(self):
		op_cron_iniz = '<='
		op_cron_fin = '>='

		per_res = self.DB_MANAGER.query_operator(
								[
								['cron_finale', op_cron_fin, int(self.spinBox_cron_iniz.text())],
								['cron_iniziale', op_cron_iniz, int(self.spinBox_cron_fin.text())],
								],'PERIODIZZAZIONE')

		if bool(per_res) == False:
			QMessageBox.warning(self, "Alert", "Non vi sono Periodizzazioni in questo intervallo di tempo" ,  QMessageBox.Ok)
		else:
			us_res = []
			for sing_per in range(len(per_res)):
				params = {'sito' : "'" + str(per_res[sing_per].sito) + "'",
						'periodo_iniziale' : "'" + str(per_res[sing_per].periodo) + "'",
						'fase_iniziale' : "'" + str(per_res[sing_per].fase) + "'"}
				us_res.append(self.DB_MANAGER.query_bool(params, 'US'))

			us_res_dep = []

			for i in us_res:
				for n in i:
					us_res_dep.append(n)

			if bool(us_res_dep) == False:
				QMessageBox.warning(self, "Alert", "Non ci sono geometrie da visualizzare" ,  QMessageBox.Ok)
			else:
				self.pyQGIS.charge_vector_layers(us_res_dep)

## Class end

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = pyarchinit_US()
	ui.show()
	sys.exit(app.exec_())
