#!/usr/bin/env python
# encoding: utf-8
"""
pyarchinit_image_d_d.py

Created by Pyarchinit on 2010-05-02.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


import PIL as Image
import sys
import os
import numpy as np
import random
from numpy import *



filepath = os.path.dirname(__file__)

gui_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gui'))
gis_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gis'))
db_path  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'db'))
utility  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'utility'))

sys.path.insert(0,gui_path)
sys.path.insert(1,gis_path)
sys.path.insert(2,db_path)
sys.path.insert(3,utility)
sys.path.insert(4,filepath)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from pyarchinit_images_comparision import *
from pyarchinit_images_comparision import Ui_DialogImagesComparision

from pyarchinit_utility import *
try:
	from  pyarchinit_db_manager import *
except:
	pass

from pyarchinit_media_utility import *
from pyarchinit_conn_strings  import *

class Comparision(QDialog, Ui_DialogImagesComparision):
	delegateSites = ''
	DB_MANAGER = ""
	TABLE_NAME = 'media_table'
	MAPPER_TABLE_CLASS = "MEDIA"
	ID_TABLE = "id_media"
	MAPPER_TABLE_CLASS_mediatoentity = 'MEDIATOENTITY'
	ID_TABLE_mediatoentity = 'id_mediaToEntity'
	NOME_SCHEDA = "Scheda Media Manager"
	
	TABLE_THUMB_NAME = 'media_thumb_table'
	MAPPER_TABLE_CLASS_thumb = 'MEDIA_THUMB'
	ID_TABLE_THUMB = "id_media_thumb"
	
	UTILITY = Utility()
	
	DATA = ''
	NUM_DATA_BEGIN = 0
	NUM_DATA_END = 25
	
	PATH = ""
	FILE = ""

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui= Ui_DialogImagesComparision()
		#QMessageBox.warning(self, "Messaggio", str(dir(self.ui)), QMessageBox.Ok)
		# This is always the same
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("pyArchInit - Images Comparision Tools")
		QMessageBox.warning(self, "Alert", "Sistema sperimentale solo per lo sviluppo" ,  QMessageBox.Ok)

	def connection(self):

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


	def on_pushButton_chose_dir_pressed(self):
		self.PATH = QtGui.QFileDialog.getExistingDirectory(self, "Scegli una directory", "Seleziona una directory:", QtGui.QFileDialog.ShowDirsOnly)

	def on_pushButton_chose_file_pressed(self):
		self.FILE = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/')
		#QMessageBox.warning(self, "Messaggio", str(self.FILE), QMessageBox.Ok)

	def on_pushButton_run_pressed(self):
		file_list = self.generate_files_couples()
		#QMessageBox.warning(self, "Messaggio", str(file_list), QMessageBox.Ok)
		lista = []
		lunghezza = len(file_list)
		calculate_res = None
		for i in file_list:
			calculate_res = self.calculate([i[0],i[1]])
			
			if calculate_res != None:
				 tupla_di_ritorno = calculate_res
				 lista.append(tupla_di_ritorno)
				 lunghezza -=1
			calculate_res = None
		#QMessageBox.warning(self, "Messaggio", str(lista), QMessageBox.Ok)
		self.plot_chart(lista)

	def calculate(self, imgs):
		try:
			img1 = Image.open(str(imgs[0]))
			img2 = Image.open(str(imgs[1]))


			if img1.size != img2.size or img1.getbands() != img2.getbands():
				return -1

			s = 0
			for band_index, band in enumerate(img1.getbands()):
				m1 = np.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
				m2 = np.array([p[band_index] for p in img2.getdata()]).reshape(*img2.size)
				s += np.sum(np.abs(m1-m2))
			s = s/1000000

			(filepath1, filename1) = os.path.split(str(imgs[0]))
			(filepath2, filename2) = os.path.split(str(imgs[1]))
			label = filename1 + "-" + filename2

			return (label, s)
		except Exception, e:
			QMessageBox.warning(self, "Messaggio", str(e), QMessageBox.Ok)

	def generate_files_couples(self):
		path = self.PATH

		lista_files = os.listdir(path)
		lista_files_dup = lista_files
		
		lista_con_coppie = []
		
		for sing_file in lista_files:
			path1 = self.FILE
			path2 = path + os.sep + str(sing_file)
			lista_con_coppie.append([path1, path2])
				
		return lista_con_coppie

	def plot_chart(self, d):
		self.data_list = d
		QMessageBox.warning(self, "self.data_list", str(self.data_list) ,  QMessageBox.Ok)
		try:
			if type(self.data_list) == list:
				data_diz = {}
				for item in self.data_list:
					data_diz[item[0]] = item[1]
			x = range(len(data_diz))
			n_bars = len(data_diz)
			values = data_diz.values()
			teams = data_diz.keys()
			ind = np.arange(n_bars)
			#randomNumbers = random.sample(range(0, 10), 10)
			self.widget.canvas.ax.clear()
			#QMessageBox.warning(self, "Alert", str(dir(self.widget.canvas.ax)) ,  QMessageBox.Ok)

			bars = self.widget.canvas.ax.bar(left=x, height=values, width=0.3, align='center', alpha=0.4,picker=5)
			
			self.widget.canvas.ax.set_title('Classifica')
			self.widget.canvas.ax.set_ylabel('Indice di differenza')
			#self.widget.canvas.ax.set_xticklabels(ind + x , teams, size = 'x-small', rotation = 90)
			n = 0
			for bar in bars:
				val = int(bar.get_height())
				x_pos = bar.get_x()+0.2
				y_pos = 1.5 #bar.get_height() - 1
				#self.widget.canvas.ax.xticks(ind + width , teams, size = 'x-small', rotation = 90)
				#self.widget.canvas.ax.set_xticklabels(ind + x, label = 'gigi', position = (x_pos, y_pos), size = 'x-small', rotation = 90)
				self.widget.canvas.ax.text(x_pos, y_pos, teams[n],zorder=0, ha='center', va='center',size = 'x-small', rotation = 90)
				n+=1
			#self.widget.canvas.ax.plot(randomNumbers)
		except:
			QMessageBox.warning(self, "self.data_list", str(self.data_list) ,  QMessageBox.Ok)
			pass
		self.widget.canvas.draw()
