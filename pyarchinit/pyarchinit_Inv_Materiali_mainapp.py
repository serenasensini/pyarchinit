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
from  pyarchinit_inventario_reperti_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass
from  sortpanelmain import SortPanelMain
from  quantpanelmain import QuantPanelMain

from  pyarchinit_exp_Findssheet_pdf import *

from  imageViewer import ImageViewer
import numpy as np
import random
from numpy import *

from media_ponderata_sperimentale import *
import media_ponderata_sperimentale

from  delegateComboBox import *


class pyarchinit_Inventario_reperti(QDialog, Ui_DialogInventarioMateriali):
	MSG_BOX_TITLE = "PyArchInit - Scheda Inventario Materiali"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	BROWSE_STATUS = "b"
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'inventario_materiali_table'
	MAPPER_TABLE_CLASS = "INVENTARIO_MATERIALI"
	NOME_SCHEDA = "Scheda Inventario Materiali"
	ID_TABLE = "id_invmat"

	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito" : "sito",
	"Numero inventario" : "numero_inventario",
	"Tipo reperto" : "tipo_reperto",
	"Classe materiale" : "criterio_schedatura",
	"Definizione" : "definizione",
	"Descrizione" : "descrizione",
	"Area" : "area",
	"US" : "us",
	"Lavato" : "lavato",
	"Numero cassa" : "nr_cassa",
	"Luogo di conservazione" : "luogo_conservazione",
	"Stato conservazione" : "stato_conservazione",
	"Datazione reperto" : "datazione_reperto",
	"Forme minime" : 'forme_minime',
	"Forme massime" : 'forme_massime',
	"Totale frammenti" : 'totale_frammenti',
	"Corpo ceramico" : 'corpo_ceramico',
	"Rivestimento" : 'rivestimento',
	"Diametro orlo": 'diametro_orlo',
	"Peso" : 'peso',
	"Tipo" : 'tipo',
	"Valore E.v.e. orlo" : 'eve_orlo',
	"Repertato" : 'repertato',
	"Diagnostico" : 'diagnostico'
	}
	QUANT_ITEMS = ['Tipo reperto',
							'Classe materiale',
							'Definizione',
							'Corpo ceramico',
							'Rivestimento',
							"Tipo",
							"Datazione reperto"]

	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Numero inventario",
				"Tipo reperto",
				"Criterio schedatura",
				"Definizione",
				"Descrizione",
				"Area",
				"US",
				"Lavato",
				"Numero cassa",
				"Luogo di conservazione"
				"Stato conservazione",
				"Datazione reperto",
				"Forme minime",
				"Forme massime",
				"Totale frammenti",
				"Corpo ceramico",
				"Rivestimento",
				"Diametro orlo",
				"Peso",
				"Tipo",
				"Valore E.v.e. orlo",
				"Repertato",
				"Diagnostico"
				]

	TABLE_FIELDS = [
					"sito",
					"numero_inventario",
					"tipo_reperto",
					"criterio_schedatura",
					"definizione",
					"descrizione",
					"area",
					"us",
					"lavato",
					"nr_cassa",
					"luogo_conservazione",
					"stato_conservazione",
					"datazione_reperto",
					"elementi_reperto",
					"misurazioni",
					"rif_biblio",
					"tecnologie",
					"forme_minime",
					"forme_massime",
					"totale_frammenti",
					"corpo_ceramico",
					"rivestimento",
					'diametro_orlo',
					'peso',
					'tipo',
					'eve_orlo',
					'repertato',
					'diagnostico'
					]

	TABLE_FIELDS_UPDATE = [
					"tipo_reperto",
					"criterio_schedatura",
					"definizione",
					"descrizione",
					"area",
					"us",
					"lavato",
					"nr_cassa",
					"luogo_conservazione",
					"stato_conservazione",
					"datazione_reperto",
					"elementi_reperto",
					"misurazioni",
					"rif_biblio",
					"tecnologie",
					"forme_minime",
					"forme_massime",
					"totale_frammenti",
					"corpo_ceramico",
					"rivestimento",
					'diametro_orlo',
					'peso',
					'tipo',
					'eve_orlo',
					'repertato',
					'diagnostico'
					]

	SEARCH_DICT_TEMP = ""

	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	QUANT_PATH = ('%s%s%s') % (HOME, os.sep, "pyarchinit_Quantificazioni_folder")

	DB_SERVER = 'not defined'

	def __init__(self, iface):
		self.iface = iface

		QDialog.__init__(self)
		self.setupUi(self)
		self.customize_gui()
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except Exception, e:
			QMessageBox.warning(self, "Sistema di connessione", str(e),  QMessageBox.Ok)


	def on_pushButtonQuant_pressed(self):
		dlg = QuantPanelMain(self)
		dlg.insertItems(self.QUANT_ITEMS)
		dlg.exec_()

		dataset = []
		
		parameter1 = dlg.TYPE_QUANT
		parameters2 = dlg.ITEMS
		#QMessageBox.warning(self, "Test Parametri Quant", str(parameters2),  QMessageBox.Ok)
		
		contatore = 0
		#tipi di quantificazione
		##per forme minime

		if parameter1 == 'Forme minime':
			for i in range(len(self.DATA_LIST)):
				temp_dataset = ()
				try:
					temp_dataset = (self.parameter_quant_creator(parameters2, i), int(self.DATA_LIST[i].forme_minime))
					
					contatore += int(self.DATA_LIST[i].forme_minime) #conteggio totale
					
					dataset.append(temp_dataset)
				except:
					pass

			#QMessageBox.warning(self, "Totale", str(contatore),  QMessageBox.Ok)
			if bool(dataset) == True:
				dataset_sum = self.UTILITY.sum_list_of_tuples_for_value(dataset)
				csv_dataset = []
				for sing_tup in dataset_sum:
					sing_list = [sing_tup[0], str(sing_tup[1])]
					csv_dataset.append(sing_list)

				filename = ('%s%squant_forme_minime.csv') % (self.QUANT_PATH, os.sep)
				QMessageBox.warning(self, "Esportazione", str(filename), MessageBox.Ok)
				f = open(filename, 'wb')
				Uw = UnicodeWriter(f)
				Uw.writerows(csv_dataset)
				f.close()


				self.plot_chart(dataset_sum, 'Grafico per Forme minime', 'Nr. Forme')
			else:
				QMessageBox.warning(self, "Attenzione", "Non ci sono dati da rappresentare",  QMessageBox.Ok)

		elif parameter1 == 'Frammenti':
			for i in range(len(self.DATA_LIST)):
				temp_dataset = ()

				temp_dataset = (self.parameter_quant_creator(parameters2, i), int(self.DATA_LIST[i].totale_frammenti))
				
				contatore += int(self.DATA_LIST[i].totale_frammenti) #conteggio totale
				
				dataset.append(temp_dataset)
		
			#QMessageBox.warning(self, "Totale", str(contatore),  QMessageBox.Ok)
			if bool(dataset) == True:
				dataset_sum = self.UTILITY.sum_list_of_tuples_for_value(dataset)

				#csv export block
				csv_dataset = []
				for sing_tup in dataset_sum:
					sing_list = [sing_tup[0], str(sing_tup[1])]
					csv_dataset.append(sing_list)
	
				filename = ('%s%squant_frammenti.csv') % (self.QUANT_PATH, os.sep)
				f = open(filename, 'wb')
				Uw = UnicodeWriter(f)
				Uw.writerows(csv_dataset)
				f.close()
				#QMessageBox.warning(self, "Esportazione", "Esportazione del file "+ str(filename) + "avvenuta con successo. I dati si trovano nella cartella pyarchinit_Quantificazioni_folder sotto al vostro Utente", MessageBox.Ok)


				self.plot_chart(dataset_sum, 'Grafico per Frammenti', 'Nr. Frammenti')
			else:
				QMessageBox.warning(self, "Attenzione", "Non ci sono dati da rappresentare!!",  QMessageBox.Ok)
		""" experimental disabled
		wind = QMessageBox.warning(self, "Attenzione", "Vuoi esportare le medie ponderate?",  QMessageBox.Cancel, 1)
		if wind == 1:
			conversion_dict = {"I sec. a.C." : (-99, 0),
												"II sec. a.C.": (-199, -100),
												"III sec. a.C.": (-299, -200),
												"IV sec. a.C.": (-399, -300),
												"V sec. a.C.": (-499, -400),
												"VI sec. a.C.": (-599, -500),
												"VII sec. a.C.": (-699, -600)}
			data = []
			for sing_rec in self.DATA_LIST:
				if sing_rec.tipo != "" and sing_rec.forme_minime != "" and sing_rec.datazione_reperto != "":
					data.append([sing_rec.tipo, sing_rec.forme_minime, sing_rec.datazione_reperto])
				#data = [ ["morel 20", 50, "II sec. a.C."], ["morel 22",50, "I sec. a.C."]]

			CC = Cronology_convertion()

			#calcola il totale delle forme minime
			totale_forme_minime = CC.totale_forme_min(data)
			#print "totale_forme_minime: ", totale_forme_minime
			#restituisce una lista di liste con dentro forma e singoli intervalli parziali di tempo
			lista_forme_dataz = []

			for sing_rec in data:
				intervalli = CC.convert_data(sing_rec[2])
				lista_forme_dataz.append([sing_rec[0],intervalli])

			#print "lista_forme_dataz: ", lista_forme_dataz
			#crea la lista di tuple per avere il totale parziale di ogni forma
			lista_tuple_forma_valore = []
			for i in data:
				lista_tuple_forma_valore.append((i[0], i[1]))

			#ottiene la lista di liste con tutti i totali per forma
			totali_per_forma = CC.sum_list_of_tuples_for_value(lista_tuple_forma_valore)
			#print "totali_parziali_per_forma: ", totali_per_forma

			#ottiene la lista di liste con le perc_parziali per forma
			perc_per_forma = []
			for i in totali_per_forma:
				perc = CC.calc_percent(i[1], totale_forme_minime)
				perc_per_forma.append([i[0], perc])
				
			#print "perc per forma: ", perc_per_forma

			#lista valore, crono_iniz, cron_fin_globale
			lista_intervalli_globali = []
			valore_temp = ""
			for i in lista_forme_dataz:
				if i[0] != valore_temp:
					intervallo_globale = CC.media_ponderata_perc_intervallo(lista_forme_dataz, i[0])
					lista_intervalli_globali.append([i[0], intervallo_globale])
				valore_temp = i[0]

			#print "lista_intervalli_globali", lista_intervalli_globali

			#lista valore / Intervallo numerico
			intervallo_numerico = CC.intervallo_numerico(lista_intervalli_globali)
			#print "intervallo_numerico", intervallo_numerico

			#media_ponderata_singoli_valori
			lista_valori_medie = []
			for sing_perc in perc_per_forma:
				for sing_int in intervallo_numerico:
					if sing_int[0] ==  sing_perc[0]:
						valore_medio = float(sing_perc[1]) / float(sing_int[1])
						lista_valori_medie.append([ sing_perc[0], valore_medio])

			#print "lista_valori_medie", lista_valori_medie
			#assegna valori ai singoli cinquatenni
			##print CC.check_value_parz_in_rif_value([-170, -150], [-500, -400])
			diz_medie_pond = {}
			for forma_parz in lista_valori_medie:
				valore_riferimento = forma_parz[0]
				for sing_int in lista_intervalli_globali:
			##		print "sing_int", sing_int
					if sing_int[0] == valore_riferimento:
						for k,v in conversion_dict.items():
			##				print sing_int[1][0], sing_int[1][1], v[0], v[1]
							test = CC.check_value_parz_in_rif_value([sing_int[1][0], sing_int[1][1]], [v[0], v[1]])
							if test == 1:
								try:
			##						print k, forma_parz
									diz_medie_pond[k] =diz_medie_pond[k] + forma_parz[1]
								except:
									diz_medie_pond[k] = forma_parz[1]

						#csv export block
			csv_dataset = []
			for k,v in diz_medie_pond.items():
				sing_list = [k, str(v)]
				csv_dataset.append(sing_list)

			filename = ('%s%squant_medie_pond.csv') % (self.QUANT_PATH, os.sep)
			f = open(filename, 'wb')
			Uw = UnicodeWriter(f)
			Uw.writerows(csv_dataset)
			f.close()
			"""


	def parameter_quant_creator(self, par_list, n_rec):
		self.parameter_list = par_list
		self.record_number = n_rec
		
		converted_parameters = []
		for par in self.parameter_list:
			converted_parameters.append(self.CONVERSION_DICT[par])
		
		parameter2 = ''
		for sing_par_conv in range(len(converted_parameters)):
			exec_str =  ('str(self.DATA_LIST[%d].%s)') % (self.record_number, converted_parameters[sing_par_conv])
			paramentro = str(self.parameter_list[sing_par_conv])
			exec_str = ' -' + paramentro[:4] + ": " + eval(exec_str)
			parameter2 += exec_str
		return parameter2


	def plot_chart(self, d, t, yl):
		self.data_list = d
		self.title = t
		self.ylabel = yl

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
		#QMessageBox.warning(self, "Alert", str(teams) ,  QMessageBox.Ok)

		bars = self.widget.canvas.ax.bar(left=x, height=values, width=0.5, align='center', alpha=0.4,picker=5)
		#guardare il metodo barh per barre orizzontali
		self.widget.canvas.ax.set_title(self.title)
		self.widget.canvas.ax.set_ylabel(self.ylabel)
		l = []
		for team in teams:
			l.append('""')
			
		#self.widget.canvas.ax.set_xticklabels(x , ""   ,size = 'x-small', rotation = 0)
		n = 0

		for bar in bars:
			val = int(bar.get_height())
			x_pos = bar.get_x() + 0.25
			label  = teams[n]+ ' - ' + str(val)
			y_pos = 0.1 #bar.get_height() - bar.get_height() + 1
			self.widget.canvas.ax.tick_params(axis='x', labelsize=8)
			#self.widget.canvas.ax.set_xticklabels(ind + x, ['fg'], position = (x_pos,y_pos), xsize = 'small', rotation = 90)
			
			self.widget.canvas.ax.text(x_pos, y_pos, label,zorder=0, ha='center', va='bottom',size = 'x-small', rotation = 90)
			n+=1
		#self.widget.canvas.ax.plot(randomNumbers)
		self.widget.canvas.draw()

	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *
		#self.setComboBoxEditable(["self.comboBox_sito"],1)
		conn = Connection()
		conn_str = conn.conn_str()

		test_conn = conn_str.find('sqlite')

		if test_conn == 0:
			self.DB_SERVER = "sqlite"

		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.charge_records()
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list()
				self.BROWSE_STATUS = 'x'
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> E' NECESSARIO RIAVVIARE QGIS" + e ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "Attenzione rilevato bug! Segnalarlo allo sviluppatore<br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_gui(self):
		#media prevew system
		self.iconListWidget = QtGui.QListWidget(self)
		self.iconListWidget.setFrameShape(QtGui.QFrame.StyledPanel)
		self.iconListWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.iconListWidget.setLineWidth(2)
		self.iconListWidget.setMidLineWidth(2)
		self.iconListWidget.setProperty("showDropIndicator", False)
		self.iconListWidget.setIconSize(QtCore.QSize(150, 150))
		self.iconListWidget.setMovement(QtGui.QListView.Snap)
		self.iconListWidget.setResizeMode(QtGui.QListView.Adjust)
		self.iconListWidget.setLayoutMode(QtGui.QListView.Batched)
		self.iconListWidget.setGridSize(QtCore.QSize(160, 160))
		self.iconListWidget.setViewMode(QtGui.QListView.IconMode)
		self.iconListWidget.setUniformItemSizes(True)
		self.iconListWidget.setBatchSize(1000)
		self.iconListWidget.setObjectName("iconListWidget")
		self.iconListWidget.SelectionMode()
		self.iconListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.connect(self.iconListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"),self.openWide_image)
		self.tabWidget.addTab(self.iconListWidget, "Media")
		
		#delegate combobox

		valuesTE = ["frammento", "frammenti", "intero", "integro"]
		self.delegateTE = ComboBoxDelegate()
		self.delegateTE.def_values(valuesTE)
		self.delegateTE.def_editable('False')
		self.tableWidget_elementi_reperto.setItemDelegateForColumn(1,self.delegateTE)


	def loadMediaPreview(self, mode = 0):
		self.iconListWidget.clear()
		if mode == 0:
			""" if has geometry column load to map canvas """

			rec_list =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))
			search_dict = {'id_entity'  : "'"+str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))+"'", 'entity_type' : "'REPERTO'"}
			record_us_list = self.DB_MANAGER.query_bool(search_dict, 'MEDIATOENTITY')
			for i in record_us_list:
				search_dict = {'id_media' : "'"+str(i.id_media)+"'"}

				u = Utility()
				search_dict = u.remove_empty_items_fr_dict(search_dict)
				mediathumb_data = self.DB_MANAGER.query_bool(search_dict, "MEDIA_THUMB")
				thumb_path = str(mediathumb_data[0].filepath)

				item = QListWidgetItem(str(i.id_media))

				item.setData(QtCore.Qt.UserRole,str(i.id_media))
				icon = QIcon(thumb_path)
				item.setIcon(icon)
				self.iconListWidget.addItem(item)
		elif mode == 1:
			self.iconListWidget.clear()


	def openWide_image(self):
		items = self.iconListWidget.selectedItems()
		for item in items:
			dlg = ImageViewer(self)
			id_orig_item = item.text() #return the name of original file

			search_dict = {'id_media' : "'"+str(id_orig_item)+"'"}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			try:
				res = self.DB_MANAGER.query_bool(search_dict, "MEDIA")
				file_path = str(res[0].filepath)
			except Exception, e:
				QMessageBox.warning(self, "Errore", "Attenzione 1 file: "+ str(e),  QMessageBox.Ok)

			dlg.show_image(unicode(file_path)) #item.data(QtCore.Qt.UserRole).toString()))
			dlg.exec_()

	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except Exception, e:
			if str(e) == "list.remove(x): x not in list":
				pass
			else:
				QMessageBox.warning(self, "Messaggio", "Sistema di aggiornamento lista Sito: " + str(e), QMessageBox.Ok)

		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	#buttons functions

	def on_pushButton_sort_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			dlg = SortPanelMain(self)
			dlg.insertItems(self.SORT_ITEMS)
			dlg.exec_()

			items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

			self.SORT_ITEMS_CONVERTED = []
			for i in items:
				self.SORT_ITEMS_CONVERTED.append(self.CONVERSION_DICT[unicode(i)])

			self.SORT_MODE = order_type
			self.empty_fields()

			id_list = []
			for i in self.DATA_LIST:
				id_list.append(eval("i." + self.ID_TABLE))
			self.DATA_LIST = []

			temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

			for i in temp_data_list:
				self.DATA_LIST.append(i)
			self.BROWSE_STATUS = "b"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			if type(self.REC_CORR) == "<type 'str'>":
				corr = 0
			else:
				corr = self.REC_CORR

			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
			self.SORT_STATUS = "o"
			self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
			self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
			self.fill_fields()

	def on_toolButtonPreviewMedia_toggled(self):
		if self.toolButtonPreviewMedia.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview Media Reperti attivata. Le immagini dei Reperti saranno visualizzate nella sezione Media", QMessageBox.Ok)
			self.loadMediaPreview()
		else:
			self.loadMediaPreview(1)

	def on_pushButton_new_rec_pressed(self):
		if bool(self.DATA_LIST) == True:
			if self.data_error_check() == 1:
				pass
			else:
				if self.BROWSE_STATUS == "b":
					if bool(self.DATA_LIST) == True:
						if self.records_equal_check() == 1:
							msg = self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()

			self.setComboBoxEditable(['self.comboBox_sito'], 0)
			#self.setComboBoxEditable(['self.comboBox_sito'], 1)
			self.setComboBoxEnable(['self.comboBox_sito'], 'True')
			self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')

			self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])

			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])
			self.empty_fields()

			self.enable_button(0)

	def on_pushButton_save_pressed(self):
		#save record
		if self.BROWSE_STATUS == "b":
			if self.data_error_check() == 0:
				if self.records_equal_check() == 1:
					self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
					self.SORT_STATUS = "n"
					self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
					self.enable_button(1)
					self.fill_fields(self.REC_CORR)
				else:
					QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:
				test_insert = self.insert_new_rec()
				if test_insert == 1:
					self.empty_fields()
					self.SORT_STATUS = "n"
					self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
					self.charge_records()
					self.charge_list()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)

					self.setComboBoxEditable(['self.comboBox_sito'], 1)
					self.setComboBoxEnable(['self.comboBox_sito'], 'False')
					self.setComboBoxEnable(['self.lineEdit_num_inv'], 'False')

					self.fill_fields(self.REC_CORR)
					self.enable_button(1)
				
	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].id_invmat), 							#1 - id_invmat
			unicode(self.DATA_LIST[i].sito),								#2 - sito
			int(self.DATA_LIST[i].numero_inventario),				#3 - numero_inventario
			unicode(self.DATA_LIST[i].tipo_reperto),					#4 - tipo_reperto
			unicode(self.DATA_LIST[i].criterio_schedatura),			#5 - criterio_schedatura
			unicode(self.DATA_LIST[i].definizione),					#6 - definizione
			unicode(self.DATA_LIST[i].descrizione),					#7 - descrizione
			unicode(self.DATA_LIST[i].area),							#8 - area
			unicode(self.DATA_LIST[i].us),								#9 - us
			unicode(self.DATA_LIST[i].lavato),							#10 - lavato
			unicode(self.DATA_LIST[i].nr_cassa), 						#11 - nr_cassa
			unicode(self.DATA_LIST[i].luogo_conservazione),		#12 - luogo_conservazione
			unicode(self.DATA_LIST[i].stato_conservazione),		#13 - stato_conservazione
			unicode(self.DATA_LIST[i].datazione_reperto),			#14 - datazione_reperto
			unicode(self.DATA_LIST[i].elementi_reperto),			#15 - elementi_reperto
			unicode(self.DATA_LIST[i].misurazioni),					#16 - misurazioni
			unicode(self.DATA_LIST[i].rif_biblio),						#17 - rif_biblio
			unicode(self.DATA_LIST[i].tecnologie),						#18 - misurazioni
			unicode(self.DATA_LIST[i].tipo),								#19 - tipo
			unicode(self.DATA_LIST[i].corpo_ceramico),				#20 - corpo_ceramico
			unicode(self.DATA_LIST[i].rivestimento),					#21 - rivestimento
			unicode(self.DATA_LIST[i].repertato),						#22 - repertato
			unicode(self.DATA_LIST[i].diagnostico)					#23 - diagnostico
		])
		return data_list

	def on_pushButton_exp_pdf_sheet_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',u"Il record è stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		Finds_pdf_sheet = generate_reperti_pdf()
		data_list = self.generate_list_pdf()
		Finds_pdf_sheet.build_Finds_sheets(data_list)

	def on_pushButton_exp_index_mat_pressed(self):
		Mat_index_pdf = generate_reperti_pdf()
		data_list = self.generate_list_pdf()
		Mat_index_pdf.build_index_Finds(data_list, data_list[0][1])

	def on_pushButton_elenco_casse_pressed(self):
		sito_ec = unicode(self.comboBox_sito.currentText())
		Mat_casse_pdf = generate_reperti_pdf()
		data_list = self.generate_el_casse_pdf(sito_ec)

		Mat_casse_pdf.build_index_Casse(data_list, sito_ec)
		Mat_casse_pdf.build_box_labels_Finds(data_list, sito_ec)

#********************************************************************************
	def generate_el_casse_pdf(self, sito):
		self.sito_ec = sito
		elenco_casse_res = self.DB_MANAGER.query_distinct('INVENTARIO_MATERIALI',[['sito','"' + str(self.sito_ec)+'"']], ['nr_cassa'])

		elenco_casse_list  = [] #accoglie la sigla numerica delle casse presenti per un determinato sito.
		for i in elenco_casse_res:
			elenco_casse_list.append(i.nr_cassa)

		data_for_pdf = [] #contiene i singoli dati per l'esportazione dell'elenco casse

		#QMessageBox.warning(self,'elenco casse',str(elenco_casse_list), QMessageBox.Ok)
		elenco_casse_list.sort()
		for cassa in elenco_casse_list:
			single_cassa = [] #contiene i dati della singola cassa

			str_cassa = "<b>"+str(cassa)+"</b>"
			single_cassa.append(str_cassa) #inserisce la sigla di cassa

			###cerca le singole area/us presenti in quella cassa
			res_inv = self.DB_MANAGER.query_distinct('INVENTARIO_MATERIALI',[['sito','"' + str(self.sito_ec)+'"'], ['nr_cassa',cassa]], ['numero_inventario', 'tipo_reperto'])
			
			res_inv_list = []
			for i in res_inv:
				res_inv_list.append(i)
			
			n_inv_res_list = ""
			for i in range(len(res_inv_list)):
				if i != len(res_inv_list)-1:
					n_inv_res_list += "N.inv:" + str(res_inv_list[i].numero_inventario) + "/"+ str(res_inv_list[i].tipo_reperto)+","
				else:
					n_inv_res_list += "N.inv:" + str(res_inv_list[i].numero_inventario) + "/"+ str(res_inv_list[i].tipo_reperto)
					
			#inserisce l'elenco degli inventari
			single_cassa.append(n_inv_res_list)


			###cerca le singole area/us presenti in quella cassa
			res_us = self.DB_MANAGER.query_distinct('INVENTARIO_MATERIALI',[['sito','"' + str(self.sito_ec)+'"'], ['nr_cassa',cassa]], ['area', 'us'])
			
			res_us_list = []
			for i in res_us:
				res_us_list.append(i)
			
			us_res_list = ""#[] #accoglie l'elenco delle US presenti in quella cassa
			for i in range(len(res_us_list)):
				params_dict = {'sito':'"'+str(self.sito_ec)+'"', 'area': '"'+str(res_us_list[i].area)+'"', 'us':'"'+str(res_us_list[i].us)+'"'}
				res_struct = self.DB_MANAGER.query_bool(params_dict, 'US')
				
				res_struct_list = []
				for s_strutt in res_struct:
					res_struct_list.append(s_strutt)

				structure_string = ""
				if len(res_struct_list) > 0:
					for sing_us in res_struct_list:
						if sing_us.struttura != u'':
							structure_string += "(" + str(sing_us.struttura) + '/'
					
					if structure_string != "":
						structure_string += ")"

				if i != len(res_us_list)-1:
					us_res_list += "Area:"+str(res_us_list[i].area) + ",US:"+str(res_us_list[i].us)+structure_string+", "  #.append("Area:"+str(i.area) + ",US:"+str(i.us))
				else:
					us_res_list += "Area:"+str(res_us_list[i].area) + ",US:"+str(res_us_list[i].us)+structure_string #.append("Area:"+str(i.area) + ",US:"+str(i.us))

			#us_res_list.sort()
			#inserisce l'elenco delle us
			single_cassa.append(us_res_list)


			###cerca il luogo di conservazione della cassa
			params_dict = {'sito':'"'+str(self.sito_ec)+'"', 'nr_cassa': '"'+str(cassa)+'"'}
			res_luogo_conservazione = self.DB_MANAGER.query_bool(params_dict, 'INVENTARIO_MATERIALI')
			luogo_conservazione = res_luogo_conservazione[0].luogo_conservazione
			single_cassa.append(luogo_conservazione) #inserisce la sigla di cassa

##			###cerca le singole area/us presenti in quella cassa
##			res_tip_reperto = self.DB_MANAGER.query_distinct('INVENTARIO_MATERIALI',[['sito','"Sito archeologico"'], ['nr_cassa',cassa]], ['tipo_reperto'])
##
##			tip_rep_res_list = ""
##			for i in res_tip_reperto:
##				tip_rep_res_list += str(i.tipo_reperto) +"<br/>"
##
##			#inserisce l'elenco degli inventari
##			single_cassa.append(tip_rep_res_list)


			data_for_pdf.append(single_cassa)

		#QMessageBox.warning(self,'tk',str(data_for_pdf), QMessageBox.Ok)
		return data_for_pdf

####################################################
	def exp_pdf_elenco_casse_main_experimental(self):
		##campi per generare la lista da passare al pdf
		#experimental to finish
		#self.exp_pdf_elenco_casse_main()
		elenco_casse = self.index_elenco_casse() #lista
		elenco_us = [] #lista
		diz_strutture_x_us = {}
		diz_us_x_cassa = {}
		diz_usstrutture_x_reperto = {}
		
		##
		
		#QMessageBox.warning(self,'elenco casse',str(elenco_casse), QMessageBox.Ok)
		sito = unicode(self.comboBox_sito.currentText())
		elenco_casse.sort()

		#crea il dizionario cassa/us che contiene i valori {'cassa':[('area','us'), (area','us')]}
		
		for cassa in elenco_casse:
			rec_us = self.us_list_from_casse(sito, cassa)
			diz_us_x_cassa[cassa] = rec_us

		##QMessageBox.warning(self,'us x cassa',str(diz_us_x_cassa), QMessageBox.Ok)
		
		#elenco us delle casse
		for us_list in diz_us_x_cassa.values():
			for v in us_list:
				elenco_us.append((sito, v[1], v[2]))

		#crea il dizionario us/strutture che contiene i valori {'us':[('sito','struttura'), ('sito','struttura')]}

		for sing_us in elenco_us:
			rec_strutture = self.strutture_list_from_us(sing_us[0], sing_us[1], sing_us[2])
			diz_strutture_x_us[sing_us] = rec_strutture
		
		#QMessageBox.warning(self,'strutture x us',str(diz_strutture_x_us), QMessageBox.Ok)

		#crea il dizionario reperto/us/struttura che contiene i valori {'reperto':[('sito','area'us','struttura'), ('sito','area','us','struttura')]}
		
		for rec in range(len(self.DATA_LIST)):
			tup_key = (self.DATA_LIST[rec].sito, self.DATA_LIST[rec].area, self.DATA_LIST[rec].us)

			QMessageBox.warning(self,'tk',str(tup_key), QMessageBox.Ok)
			QMessageBox.warning(self,'tk',str(diz_strutture_x_us), QMessageBox.Ok)
			diz_usstrutture_x_reperto[self.DATA_LIST[rec].numero_inventario] = [self.DATA_LIST[rec].sito,
												self.DATA_LIST[rec].area, 
												self.DATA_LIST[rec].us, 
												diz_strutture_x_us[tup_key]
												]
		##QMessageBox.warning(self,'rep,us_str',str(diz_usstrutture_x_reperto), QMessageBox.Ok)
		
		#loop per la creazione dei data da passare al sistema di creazione pdf
		
		us_field = ""
		for cassa in elenco_casse:
			for us in diz_us_x_cassa[cassa]:
				QMessageBox.warning(self,'Tus',str(us), QMessageBox.Ok)
				strutt_list = diz_strutture_x_us[us]
				strutt_text ="("
				for sing_str in strutt_list:
					 strutt_text += "," + str(sing_str[1])
				strutt_text =")"
				us_field += "US"+str(us[1]) + strutt_text + ", "

		QMessageBox.warning(self,'us_field',str(us_field), QMessageBox.Ok)

	def index_elenco_casse(self):
		elenco_casse = []
		for rec in range(len(self.DATA_LIST)):
			elenco_casse.append(self.DATA_LIST[rec].nr_cassa)

		elenco_casse = self.UTILITY.remove_dup_from_list(elenco_casse)

		return elenco_casse

	def us_list_from_casse(self, sito, cassa):
		self.sito = sito
		self.cassa = cassa

		elenco_us_per_cassa = []

		search_dict = {'sito' : "'"+unicode(self.sito)+"'",
						'nr_cassa' : "'"+unicode(self.cassa)+"'"
						}

		search_dict = self.UTILITY.remove_empty_items_fr_dict(search_dict)

		res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)

		for rec in range(len(res)):
			if bool(res[rec].us) == True:
				elenco_us_per_cassa.append((res[rec].sito,res[rec].area, res[rec].us))
		return elenco_us_per_cassa

	def strutture_list_from_us(self, sito, area, us):
		self.sito = sito
		self.area = area
		self.us = us

		elenco_strutture_per_us = []

		search_dict = {'sito' : "'"+unicode(self.sito)+"'",
						'area' : "'"+unicode(self.area)+"'",
						'us' : "'"+unicode(self.us)+"'"
						}

		search_dict = self.UTILITY.remove_empty_items_fr_dict(search_dict)

		res = self.DB_MANAGER.query_bool(search_dict,"US")

		for rec in range(len(res)):
			if bool(res[rec].struttura) == True:
				elenco_strutture_per_us.append((res[rec].sito, res[rec].struttura))
		return elenco_strutture_per_us

#********************************************************************************

	def data_error_check(self):
		test = 0
		EC = Error_check()

		area = self.lineEdit_area.text()
		us = self.lineEdit_us.text()
		nr_cassa = self.lineEdit_nr_cassa.text()
		nr_inv = self.lineEdit_num_inv.text()

		if EC.data_is_empty(unicode(self.comboBox_sito.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Sito. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(unicode(self.lineEdit_num_inv.text())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Numero inventario \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1



		if nr_inv != "":
			if EC.data_is_int(nr_inv) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Numero inventario\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if area != "":
			if EC.data_is_int(area) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Area.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if us != "":
			if EC.data_is_int(us) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo US.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if nr_cassa != "":
			if EC.data_is_int(nr_cassa) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Numero Cassa.\nIl valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test


	def insert_new_rec(self):
		##elementi reperto
		elementi_reperto = self.table2dict("self.tableWidget_elementi_reperto")
		##misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")
		##rif_biblio
		rif_biblio = self.table2dict("self.tableWidget_rif_biblio")
		##tecnologie
		tecnologie = self.table2dict("self.tableWidget_tecnologie")

		try:
			if self.lineEdit_area.text() == "":
				area = None
			else:
				area = int(self.lineEdit_area.text())

			if self.lineEdit_us.text() == "":
				us = None
			else:
				us = int(self.lineEdit_us.text())
				
			if self.lineEdit_nr_cassa.text() == "":
				nr_cassa = None
			else:
				nr_cassa = int(self.lineEdit_nr_cassa.text())

			if self.lineEditFormeMin.text() == "":
				forme_minime = None
			else:
				forme_minime = int(self.lineEditFormeMin.text())

			if self.lineEditFormeMax.text() == "":
				forme_massime = None
			else:
				forme_massime = int(self.lineEditFormeMax.text())

			if self.lineEditTotFram.text() == "":
				totale_frammenti = None
			else:
				totale_frammenti = int(self.lineEditTotFram.text())

			if self.lineEdit_diametro_orlo.text() == "":
				diametro_orlo = None
			else:
				diametro_orlo= float(self.lineEdit_diametro_orlo.text())
	
			if self.lineEdit_peso.text() == "":
				peso = None
			else:
				peso = float(self.lineEdit_peso.text())

			if self.lineEdit_eve_orlo.text() == "":
				eve_orlo = None
			else:
				eve_orlo = float(self.lineEdit_eve_orlo.text())

			data = self.DB_MANAGER.insert_values_reperti(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, 			#0 - IDsito
						unicode(self.comboBox_sito.currentText()), 													#1 - Sito
						int(self.lineEdit_num_inv.text()),						        								#2 - num_inv
						unicode(self.comboBox_tipo_reperto.currentText()), 											#3 - tipo_reperto
						unicode(self.comboBox_criterio_schedatura.currentText()),									#4 - criterio
						unicode(self.comboBox_definizione.currentText()), 											#5 - definizione
						unicode(self.textEdit_descrizione_reperto.toPlainText()),								#6 - descrizione
						area,										                    										#7 - area
						us,										                        									#8 - us
						unicode(self.comboBox_lavato.currentText()),					    							#9 - lavato
						nr_cassa,									                    									#10 - nr cassa
						unicode(self.lineEdit_luogo_conservazione.text()),												#11 - luogo conservazione
						unicode(self.comboBox_conservazione.currentText()),										#12 - stato di conservazione
						unicode(self.lineEdit_datazione_rep.text()),					    								#13 - datazione reperto
						unicode(elementi_reperto),								            								#14 - elementi reperto
						unicode(misurazioni),								                									#15 - misurazioni
						str(rif_biblio), 								                										#16 - rif biblio
						unicode(tecnologie),								                									#17 - tecnologie
						forme_minime,								                								#18 - forme minime
						forme_massime,								                							#18-  forme massime
						totale_frammenti,								                							#19 - totale frammenti
						unicode(self.lineEditCorpoCeramico.text()),					    								#20 - corpo ceramico
						unicode(self.lineEditRivestimento.text()),					    									#21   rivestimento
						diametro_orlo,					    																#22 - diametro orlo
						peso,					    																			#23- peso
						unicode(self.lineEdit_tipo.text()),					    											#24 - tipo
						eve_orlo,																								#25 - eve_orlo,
						unicode(self.comboBox_repertato.currentText()),					    							#9 - lavato
						unicode(self.comboBox_diagnostico.currentText()),					    							#9 - lavato

						)

			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immisione 2 \n"+str(e),  QMessageBox.Ok)
			return 0

	#insert new row into tableWidget
	#elementi reperto
	def on_pushButton_insert_row_elementi_pressed(self):
		self.insert_new_row('self.tableWidget_elementi_reperto')
	def on_pushButton_remove_row_elementi_pressed(self):
		self.remove_row('self.tableWidget_elementi_reperto')

	#misurazioni
	def on_pushButton_insert_row_misure_pressed(self):
		self.insert_new_row('self.tableWidget_misurazioni')
	def on_pushButton_remove_row_misure_pressed(self):
		self.remove_row('self.tableWidget_misurazioni')

	#tecnologie
	def on_pushButton_insert_row_tecnologie_pressed(self):
		self.insert_new_row('self.tableWidget_tecnologie')
	def on_pushButton_remove_row_tecnologie_pressed(self):
		self.remove_row('self.tableWidget_tecnologie')

	#rif biblio
	def on_pushButton_insert_row_rif_biblio_pressed(self):
		self.insert_new_row('self.tableWidget_rif_biblio')
	def on_pushButton_remove_row_rif_biblio_pressed(self):
		self.remove_row('self.tableWidget_rif_biblio')

	def check_record_state(self):
		ec = self.data_error_check()
		if ec == 1:
			return 1 #ci sono errori di immissione
		elif self.records_equal_check() == 1 and ec == 0:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
			#self.charge_records() incasina lo stato trova
			return 0 #non ci sono errori di immissione

	def on_pushButton_view_all_2_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			self.empty_fields()
			self.charge_records()
			self.fill_fields()
			self.BROWSE_STATUS = "b"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			if type(self.REC_CORR) == "<type 'str'>":
				corr = 0
			else:
				corr = self.REC_CORR
			self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
			self.label_sort.setText(self.SORTED_ITEMS["n"])
			if self.toolButtonPreviewMedia.isChecked() == True:
				self.loadMediaPreview(1)

	#records surf functions
	def on_pushButton_first_rec_pressed(self):
		if self.check_record_state() == 1:
			if self.toolButtonPreviewMedia.isChecked() == True:
				self.loadMediaPreview(1)
		else:
			try:
				self.empty_fields()
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.fill_fields(0)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
				if self.toolButtonPreviewMedia.isChecked() == True:
					self.loadMediaPreview(0)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_last_rec_pressed(self):
		if self.check_record_state() == 1:
			if self.toolButtonPreviewMedia.isChecked() == True:
				self.loadMediaPreview(0)		
		else:

			try:
				self.empty_fields()
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
				if self.toolButtonPreviewMedia.isChecked() == True:
					self.loadMediaPreview(0)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_prev_rec_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			self.REC_CORR = self.REC_CORR-1
			if self.REC_CORR == -1:
				self.REC_CORR = 0
				QMessageBox.warning(self, "Errore", "Sei al primo record!",  QMessageBox.Ok)
			else:
				try:
					self.empty_fields()
					self.fill_fields(self.REC_CORR)
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					if self.toolButtonPreviewMedia.isChecked() == True:
						self.loadMediaPreview(0)
				except Exception, e:
					QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_next_rec_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			self.REC_CORR = self.REC_CORR+1
			if self.REC_CORR >= self.REC_TOT:
				self.REC_CORR = self.REC_CORR-1
				QMessageBox.warning(self, "Errore", "Sei all'ultimo record!",  QMessageBox.Ok)
			else:
				try:
					self.empty_fields()
					self.fill_fields(self.REC_CORR)
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					if self.toolButtonPreviewMedia.isChecked() == True:
						self.loadMediaPreview(0)
				except Exception, e:
					QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_delete_pressed(self):
		msg = QMessageBox.warning(self,"Attenzione!!!",u"Vuoi veramente eliminare il record? \n L'azione è irreversibile", QMessageBox.Cancel,1)
		if msg != 1:
			QMessageBox.warning(self,"Messagio!!!","Azione Annullata!")
		else:
			try:
				id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
				self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
				self.charge_records() #charge records from DB
				QMessageBox.warning(self,"Messaggio!!!","Record eliminato!")
			except Exception, e:
				QMessageBox.warning(self,"Messaggio!!!","Tipo di errore: "+str(e))
			if bool(self.DATA_LIST) == False:
				QMessageBox.warning(self, "Attenzione", u"Il database è vuoto!",  QMessageBox.Ok)
				self.DATA_LIST = []
				self.DATA_LIST_REC_CORR = []
				self.DATA_LIST_REC_TEMP = []
				self.REC_CORR = 0
				self.REC_TOT = 0
				self.empty_fields()
				self.set_rec_counter(0, 0)
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list()
				self.fill_fields()
		self.SORT_STATUS = "n"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])

	def on_pushButton_new_search_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			self.enable_button_search(0)

			#set the GUI for a new search

			if self.BROWSE_STATUS != "f":
				self.BROWSE_STATUS = "f"
				###
				self.setComboBoxEditable(['self.comboBox_sito'], 1)
				self.setComboBoxEnable(['self.comboBox_sito'], 'True')
				self.setComboBoxEditable(['self.comboBox_lavato'], 1)
				self.setComboBoxEnable(['self.comboBox_lavato'], 'True')
				self.setComboBoxEnable(['self.lineEdit_num_inv'], 'True')
				self.setComboBoxEnable(["self.textEdit_descrizione_reperto"],"False")
				self.setTableEnable(["self.tableWidget_elementi_reperto", "self.tableWidget_misurazioni","self.tableWidget_rif_biblio",
				"self.tableWidget_tecnologie"], "False")
				###
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter('','')
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.charge_list()
				self.empty_fields()

	def on_pushButton_search_go_pressed(self):
		check_for_buttons = 0
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			##scavato
			if self.lineEdit_num_inv.text() != "":
				numero_inventario = int(self.lineEdit_num_inv.text())
			else:
				numero_inventario = ""

			if self.lineEdit_area.text() != "":
				area = int(self.lineEdit_area.text())
			else:
				area = ""

			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""

			if self.lineEdit_nr_cassa.text() != "":
				nr_cassa = int(self.lineEdit_nr_cassa.text())
			else:
				nr_cassa = ""

			if self.lineEditFormeMin.text() != "":
				forme_minime = int(self.lineEditFormeMin.text())
			else:
				forme_minime = ""

			if self.lineEditFormeMax.text() != "":
				forme_massime = int(self.lineEditFormeMax.text())
			else:
				forme_massime = ""
	
			if self.lineEditTotFram.text() != "":
				totale_frammenti = int(self.lineEditTotFram.text())
			else:
				totale_frammenti = ""

			if self.lineEdit_diametro_orlo.text() != "":
				diametro_orlo = float(self.lineEdit_diametro_orlo.text())
			else:
				diametro_orlo = ""

			if self.lineEdit_peso.text() != "":
				peso = float(self.lineEdit_peso.text())
			else:
				peso = ""

			if self.lineEdit_eve_orlo.text() != "":
				eve_orlo = float(self.lineEdit_eve_orlo.text())
			else:
				eve_orlo = ""

			search_dict = {
			self.TABLE_FIELDS[0] : "'"+unicode(self.comboBox_sito.currentText())+"'",
			self.TABLE_FIELDS[1] : numero_inventario,
			self.TABLE_FIELDS[2] : "'" + unicode(self.comboBox_tipo_reperto.currentText()) + "'",
			self.TABLE_FIELDS[3] : "'" + unicode(self.comboBox_criterio_schedatura.currentText()) + "'",
			self.TABLE_FIELDS[4] : "'" + unicode(self.comboBox_definizione.currentText()) + "'",
			self.TABLE_FIELDS[5] : "'" + unicode(self.textEdit_descrizione_reperto.toPlainText()) + "'",
			self.TABLE_FIELDS[6] : area,
			self.TABLE_FIELDS[7] : us,
			self.TABLE_FIELDS[8] : "'" + str(self.comboBox_lavato.currentText()) + "'",
			self.TABLE_FIELDS[9] : nr_cassa,
			self.TABLE_FIELDS[10] : "'" + unicode(self.lineEdit_luogo_conservazione.text()) + "'",
			self.TABLE_FIELDS[11] : "'" +  str(self.comboBox_conservazione.currentText()) + "'",
			self.TABLE_FIELDS[12] : "'" + unicode(self.lineEdit_datazione_rep.text()) + "'",
			self.TABLE_FIELDS[17] : forme_minime,
			self.TABLE_FIELDS[18] : forme_massime,
			self.TABLE_FIELDS[19] : totale_frammenti,
			self.TABLE_FIELDS[20] : "'" + str(self.lineEditCorpoCeramico.text()) + "'",
			self.TABLE_FIELDS[21] : "'" + str(self.lineEditRivestimento.text()) + "'",
			self.TABLE_FIELDS[22] : diametro_orlo,
			self.TABLE_FIELDS[23] : peso,
			self.TABLE_FIELDS[24] : "'" + unicode(self.lineEdit_tipo.text()) + "'",
			self.TABLE_FIELDS[25] : eve_orlo,
			self.TABLE_FIELDS[26] : "'" + str(self.comboBox_repertato.currentText()) + "'",
			self.TABLE_FIELDS[27] : "'" + str(self.comboBox_diagnostico.currentText()) + "'",
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
				
			else:
				self.SEARCH_DICT_TEMP = search_dict
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(res) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)
					
					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

					self.fill_fields(self.REC_CORR)

					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_lavato"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.lineEdit_num_inv"],"False")
					self.setComboBoxEnable(["self.textEdit_descrizione_reperto"],"True")
					self.setTableEnable(["self.tableWidget_elementi_reperto", "self.tableWidget_misurazioni","self.tableWidget_rif_biblio",
					"self.tableWidget_tecnologie"], "True")
					
					check_for_buttons = 1

				else:

					self.DATA_LIST = []

					for i in res:
						self.DATA_LIST.append(i)

					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

					self.fill_fields()

					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)

					if self.REC_TOT == 1:
						strings = ("E' stato trovato", self.REC_TOT, "record")
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_lavato"],1)

					self.setComboBoxEnable(['self.lineEdit_num_inv'], "False")
					self.setComboBoxEnable(['self.comboBox_sito'], "False")
					self.setComboBoxEnable(["self.textEdit_descrizione_reperto"],"True")
					self.setTableEnable(["self.tableWidget_elementi_reperto", "self.tableWidget_misurazioni","self.tableWidget_rif_biblio",
					"self.tableWidget_tecnologie"], "True")
					
					check_for_buttons = 1

					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings, QMessageBox.Ok)
		
		if check_for_buttons == 1:
			self.enable_button_search(1)

	def on_pushButton_tot_fram_pressed(self):
		self.update_tot_frammenti(QMessageBox.warning(self,'ATTENZIONE',"Vuoi aggiornare tutti i frammenti (OK), oppure solo il record corrente (Cancel)?", QMessageBox.Cancel,1))
		#blocco per quantificare dalla tabella interna il numero totale di frammenti
	def update_tot_frammenti(self, c):
		self.choice = c
		if self.choice == 1:
			for i in range(len(self.DATA_LIST)):
				temp_dataset = ()
				id_invmat = self.DATA_LIST[i].id_invmat
				elementi_reperto = eval(self.DATA_LIST[i].elementi_reperto)
				if bool(elementi_reperto) == True:
					tot_framm = 0
					for elrep in elementi_reperto:
						if elrep[1] == 'frammenti' or elrep[1] == 'frammento':
							try:
								tot_framm += int(elrep[2])
							except:
								pass
					self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, self.ID_TABLE, [int(id_invmat)], ['totale_frammenti'], [tot_framm])

			search_dict = {'id_invmat'  : "'"+str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))+"'"}
			records = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
			self.lineEditTotFram.setText(str(records[0].totale_frammenti))
		else:
			lista_valori = self.table2dict('self.tableWidget_elementi_reperto')

			tot_framm = 0
			for sing_fr in lista_valori:
				if sing_fr[1] == 'frammenti':
					tot_framm += int(sing_fr[2])
			
			self.lineEditTotFram.setText(str(tot_framm))

	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			test = self.update_record()
			if test == 1:
				id_list = []
				for i in self.DATA_LIST:
					id_list.append(eval("i."+ self.ID_TABLE))
				self.DATA_LIST = []
				if self.SORT_STATUS == "n":
					temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE) #self.DB_MANAGER.query_bool(self.SEARCH_DICT_TEMP, self.MAPPER_TABLE_CLASS) #
				else:
					temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)
				for i in temp_data_list:
					self.DATA_LIST.append(i)
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				if type(self.REC_CORR) == "<type 'str'>":
					corr = 0
				else:
					corr = self.REC_CORR 
				return 1
			elif test == 0:
				return 0

	def update_record(self):
		try:
			self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())
			return 1
		except Exception, e:
			QMessageBox.warning(self, "Messaggio", "Problema di encoding: sono stati inseriti accenti o caratteri non accettati dal database. Se chiudete ora la scheda senza correggere gli errori perderete i dati. Fare una copia di tutto su un foglio word a parte. Errore :" + str(e), QMessageBox.Ok)
			return 0

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		#rec_to_update = rec_to_update[:2]
		return rec_to_update

	#custom functions
######old system
##	def charge_records(self):
##		self.DATA_LIST = []
##		id_list = []
##		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
##			id_list.append(eval("i."+ self.ID_TABLE))
##
##		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
##		for i in temp_data_list:
##			self.DATA_LIST.append(i)


	def charge_records(self):
		self.DATA_LIST = []

		if self.DB_SERVER == 'sqlite':
			for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
				self.DATA_LIST.append(i)
		else:
			id_list = []
			for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
				id_list.append(eval("i."+ self.ID_TABLE))

			temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
			for i in temp_data_list:
				self.DATA_LIST.append(i)


	def setComboBoxEditable(self, f, n):
		field_names = f
		value = n

		for fn in field_names:
			cmd = ('%s%s%d%s') % (fn, '.setEditable(', n, ')')
			eval(cmd)

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def table2dict(self, n):
		self.tablename = n
		row = eval(self.tablename+".rowCount()")
		col = eval(self.tablename+".columnCount()")
		lista=[]
		for r in range(row):
			sub_list = []
			for c in range(col):
				value = eval(self.tablename+".item(r,c)")
				if value != None:
					sub_list.append(unicode(value.text()))

			if bool(sub_list) == True:
				lista.append(sub_list)

		return lista

	def tableInsertData(self, t, d):
		"""Set the value into alls Grid"""
		self.table_name = t
		self.data_list = eval(d)
		self.data_list.sort()

		#column table count
		table_col_count_cmd = ("%s.columnCount()") % (self.table_name)
		table_col_count = eval(table_col_count_cmd)

		#clear table
		table_clear_cmd = ("%s.clearContents()") % (self.table_name)
		eval(table_clear_cmd)

		for i in range(table_col_count):
			table_rem_row_cmd = ("%s.removeRow(%d)") % (self.table_name, i)
			eval(table_rem_row_cmd)

		#for i in range(len(self.data_list)):
			#self.insert_new_row(self.table_name)

		for row in range(len(self.data_list)):
			cmd = ('%s.insertRow(%s)') % (self.table_name, row)
			eval(cmd)
			for col in range(len(self.data_list[row])):
				#item = self.comboBox_sito.setEditText(self.data_list[0][col]
				item = QTableWidgetItem(unicode(self.data_list[row][col]))
				exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
				eval(exec_str)


	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)


	def remove_row(self, table_name):
		"""insert new row into a table based on table_name"""

		table_row_count_cmd = ("%s.rowCount()") % (table_name)
		table_row_count = eval(table_row_count_cmd)
		rowSelected_cmd = ("%s.selectedIndexes()") % (table_name)
		rowSelected = eval(rowSelected_cmd)
		try:
			rowIndex = (rowSelected[1].row())
			cmd = ("%s.removeRow(%d)") % (table_name, rowIndex)
			eval(cmd)
		except:
			QMessageBox.warning(self, "Messaggio", "Devi selezionare una riga",  QMessageBox.Ok)


	def empty_fields(self):
		elementi_reperto_row_count = self.tableWidget_elementi_reperto.rowCount()
		misurazioni_row_count = self.tableWidget_misurazioni.rowCount()
		rif_biblio_row_count = self.tableWidget_rif_biblio.rowCount()
		tecnologie_row_count = self.tableWidget_tecnologie.rowCount()

		self.comboBox_sito.setEditText("") 								#1 - Sito
		self.lineEdit_num_inv.clear()									#2 - num_inv
		self.comboBox_tipo_reperto.setEditText("")  					#3 - tipo_reperto
		self.comboBox_criterio_schedatura.setEditText("") 				#4 - criterio
		self.comboBox_definizione.setEditText("") 						#5 - definizione
		self.textEdit_descrizione_reperto.clear()						#6 - descrizione
		self.lineEdit_area.clear()										#7 - area
		self.lineEdit_us.clear()										#8 - US
		self.comboBox_lavato.setEditText("")							#9 - lavato
		self.lineEdit_nr_cassa.clear()									#10 - nr_cassa
		self.lineEdit_luogo_conservazione.clear()						#11 - luogo_conservazione
		self.comboBox_conservazione.setEditText("") 					#12 - stato conservazione
		self.lineEdit_datazione_rep.clear()								#13 - datazione reperto
		
		self.lineEditFormeMin.clear()
		self.lineEditFormeMax.clear()	
		self.lineEditTotFram.clear()
		self.lineEditRivestimento.clear()
		self.lineEditCorpoCeramico.clear()
		
		self.lineEdit_diametro_orlo.clear()	
		self.lineEdit_peso.clear()
		self.lineEdit_tipo.clear()
		self.lineEdit_eve_orlo.clear()

		self.comboBox_repertato.setEditText("")							#9 - repertato
		self.comboBox_diagnostico.setEditText("")							#9 - diagnostico

		for i in range(elementi_reperto_row_count):
			self.tableWidget_elementi_reperto.removeRow(0) 					
		self.insert_new_row("self.tableWidget_elementi_reperto")		#14 - elementi reperto

		for i in range(misurazioni_row_count):
			self.tableWidget_misurazioni.removeRow(0)
		self.insert_new_row("self.tableWidget_misurazioni")				#15 - misurazioni

		for i in range(rif_biblio_row_count):
			self.tableWidget_rif_biblio.removeRow(0)
		self.insert_new_row("self.tableWidget_rif_biblio")				#16 - rif_biblio

		for i in range(tecnologie_row_count):
			self.tableWidget_tecnologie.removeRow(0)
		self.insert_new_row("self.tableWidget_tecnologie")				#17 - misurazioni


	def fill_fields(self, n=0):
		self.rec_num = n
		#QMessageBox.warning(self, "check fill fields", str(self.rec_num),  QMessageBox.Ok)
		try:
			unicode(self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)) 													#1 - Sito
			self.comboBox_repertato.setEditText(unicode(self.DATA_LIST[self.rec_num].repertato))
			self.comboBox_diagnostico.setEditText(unicode(self.DATA_LIST[self.rec_num].diagnostico))
			self.lineEdit_num_inv.setText(str(self.DATA_LIST[self.rec_num].numero_inventario))							#2 - num_inv
			unicode(self.comboBox_tipo_reperto.setEditText(self.DATA_LIST[self.rec_num].tipo_reperto))						#3 - Tipo reperto
			unicode(self.comboBox_criterio_schedatura.setEditText(self.DATA_LIST[self.rec_num].criterio_schedatura))		#4 - Criterio schedatura
			unicode(self.comboBox_definizione.setEditText(self.DATA_LIST[self.rec_num].definizione))						#5 - definizione
			unicode(self.textEdit_descrizione_reperto.setText(self.DATA_LIST[self.rec_num].descrizione))				#6 - descrizione
			if self.DATA_LIST[self.rec_num].area == None:																#7 - Area
				self.lineEdit_area.setText("")
			else:
				self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area))

			if self.DATA_LIST[self.rec_num].us == None:																	#8 - US
				self.lineEdit_us.setText("")
			else:
				self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))

			self.comboBox_lavato.setEditText(str(self.DATA_LIST[self.rec_num].lavato))

			if self.DATA_LIST[self.rec_num].nr_cassa == None:															#10 - nr_cassa
				self.lineEdit_nr_cassa.setText("")
			else:
				self.lineEdit_nr_cassa.setText(str(self.DATA_LIST[self.rec_num].nr_cassa))

			if self.DATA_LIST[self.rec_num].forme_minime == None:															#10 - nr_cassa
				self.lineEditFormeMin.setText("")
			else:
				self.lineEditFormeMin.setText(str(self.DATA_LIST[self.rec_num].forme_minime))

			if self.DATA_LIST[self.rec_num].forme_massime == None:															#10 - nr_cassa
				self.lineEditFormeMax.setText("")
			else:
				self.lineEditFormeMax.setText(str(self.DATA_LIST[self.rec_num].forme_massime))

			if self.DATA_LIST[self.rec_num].totale_frammenti == None:															#10 - nr_cassa
				self.lineEditTotFram.setText("")
			else:
				self.lineEditTotFram.setText(str(self.DATA_LIST[self.rec_num].totale_frammenti))

			unicode(self.lineEdit_luogo_conservazione.setText(self.DATA_LIST[self.rec_num].luogo_conservazione))			#11 - luogo_conservazione

			self.comboBox_conservazione.setEditText(str(self.DATA_LIST[self.rec_num].stato_conservazione))				#12 - stato conservazione

			unicode(self.lineEdit_datazione_rep.setText(self.DATA_LIST[self.rec_num].datazione_reperto))					#13 - datazione reperto

			self.tableInsertData("self.tableWidget_elementi_reperto", self.DATA_LIST[self.rec_num].elementi_reperto)	#14 - elementi_reperto

			self.tableInsertData("self.tableWidget_misurazioni", self.DATA_LIST[self.rec_num].misurazioni)				#15 - campioni

			self.tableInsertData("self.tableWidget_rif_biblio", self.DATA_LIST[self.rec_num].rif_biblio)				#16 - rif biblio

			self.tableInsertData("self.tableWidget_tecnologie",self.DATA_LIST[self.rec_num].tecnologie)					#17 - rapporti

			self.lineEditRivestimento.setText(str(self.DATA_LIST[self.rec_num].rivestimento))

			self.lineEditCorpoCeramico.setText(str(self.DATA_LIST[self.rec_num].corpo_ceramico))

			if self.DATA_LIST[self.rec_num].diametro_orlo == None:															#10 - nr_cassa
				self.lineEdit_diametro_orlo.setText("")
			else:
				self.lineEdit_diametro_orlo.setText(str(self.DATA_LIST[self.rec_num].diametro_orlo))

			if self.DATA_LIST[self.rec_num].peso == None:															#10 - nr_cassa
				self.lineEdit_peso.setText("")
			else:
				self.lineEdit_peso.setText(str(self.DATA_LIST[self.rec_num].peso))

			self.lineEdit_tipo.setText(str(self.DATA_LIST[self.rec_num].tipo))

			if self.DATA_LIST[self.rec_num].eve_orlo  == None:															#10 - nr_cassa
				self.lineEdit_eve_orlo.setText("")
			else:
				self.lineEdit_eve_orlo.setText(str(self.DATA_LIST[self.rec_num].eve_orlo))


##########
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#TableWidget

		#elementi reperto
		elementi_reperto = self.table2dict("self.tableWidget_elementi_reperto")
		##misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")
		##rif_biblio
		rif_biblio = self.table2dict("self.tableWidget_rif_biblio")
		##tecnologie
		tecnologie = self.table2dict("self.tableWidget_tecnologie")
		
		
		##scavato
		if self.lineEdit_area.text() == "":
			area = None
		else:
			area = self.lineEdit_area.text()
		if self.lineEdit_us.text() == "":
			us = None
		else:
			us = self.lineEdit_us.text()
		
		if self.lineEdit_nr_cassa.text() == "":
			nr_cassa = None
		else:
			nr_cassa = self.lineEdit_nr_cassa.text()

		if self.lineEditFormeMin.text() == "":
			forme_minime = None
		else:
			forme_minime = self.lineEditFormeMin.text()

		if self.lineEditFormeMax.text() == "":
			forme_massime = None
		else:
			forme_massime = self.lineEditFormeMax.text()

		if self.lineEditTotFram.text() == "":
			totale_frammenti = None
		else:
			totale_frammenti = self.lineEditTotFram.text()

		if self.lineEdit_diametro_orlo.text() == "":
			diametro_orlo = None
		else:
			diametro_orlo = self.lineEdit_diametro_orlo.text()

		if self.lineEdit_peso.text() == "":
			peso = None
		else:
			peso = self.lineEdit_peso.text()
	
		if self.lineEdit_eve_orlo.text() == "":
			eve_orlo = None
		else:
			eve_orlo = self.lineEdit_eve_orlo.text()

		#data
		self.DATA_LIST_REC_TEMP = [
		unicode(self.comboBox_sito.currentText()), 								#1 - Sito
		unicode(self.lineEdit_num_inv.text()), 									#2 - num_inv
		unicode(self.comboBox_tipo_reperto.currentText()), 						#3 - tipo_reperto
		unicode(self.comboBox_criterio_schedatura.currentText()),				#4 - criterio schedatura
		unicode(self.comboBox_definizione.currentText()), 						#5 - definizione
		unicode(self.textEdit_descrizione_reperto.toPlainText()),	#6 - descrizione
		unicode(area),															#7 - area
		unicode(us),															#8 - us
		unicode(self.comboBox_lavato.currentText()),							#9 - lavato
		unicode(nr_cassa),														#10 - nr cassa
		unicode(self.lineEdit_luogo_conservazione.text()),						#11 - luogo conservazione
		unicode(self.comboBox_conservazione.currentText()), 					#12 - stato conservazione
		unicode(self.lineEdit_datazione_rep.text()), 							#13 - datazione reperto
		unicode(elementi_reperto), 												#14 - elementi reperto
		unicode(misurazioni),													#15 - misurazioni
		unicode(rif_biblio),													#16 - rif_biblio
		unicode(tecnologie),														#17 - tecnologie
		unicode(forme_minime),														#17 - tecnologie
		unicode(forme_massime),														#17 - tecnologie
		unicode(totale_frammenti),														#17 - tecnologie
		unicode(self.lineEditCorpoCeramico.text()),														#17 - tecnologie
		unicode(self.lineEditRivestimento.text()),
		unicode(diametro_orlo),
		unicode(peso),																#17 - tecnologie
		unicode(self.lineEdit_tipo.text()),
		unicode(eve_orlo),														#17 - tecnologie
		unicode(self.comboBox_repertato.currentText()),							#9 - lavato
		unicode(self.comboBox_diagnostico.currentText()),							#9 - lavato
		]


	def enable_button(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all_2.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_new_search.setEnabled(n)

		self.pushButton_search_go.setEnabled(n)

		self.pushButton_sort.setEnabled(n)

	def enable_button_search(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all_2.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_save.setEnabled(n)

		self.pushButton_sort.setEnabled(n)


	def setTableEnable(self, t, v):
		tab_names = t
		value = v

		for tn in tab_names:
			cmd = ('%s%s%s%s') % (tn, '.setEnabled(', v, ')')
			eval(cmd)


	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("unicode(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()
		
		#test
		
		#QMessageBox.warning(self, "ATTENZIONE", str(self.DATA_LIST_REC_CORR) + " temp " + str(self.DATA_LIST_REC_TEMP), QMessageBox.Ok)

		check_str = str(self.DATA_LIST_REC_CORR) + " " + str(self.DATA_LIST_REC_TEMP)

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1




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
