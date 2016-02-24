#! /usr/bin/env python
# -*- coding: utf 8 -*-
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
 *                                                                         											*
 *   This program is free software; you can redistribute it and/or modify 						    *
 *   it under the terms of the GNU General Public License as published by  						*
 *   the Free Software Foundation; either version 2 of the License, or    							*
 *   (at your option) any later version.                                  									*
 *                                                                         											*
 ***************************************************************************/
"""
import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui

from qgis.core import *
from qgis.gui import *

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_US_ui import Ui_DialogUS
from  pyarchinit_US_ui import *
from  pyarchinit_utility import *
from pyarchinit_print_utility import Print_utility
from  pyarchinit_error_check import *



from  pyarchinit_pyqgis import Pyarchinit_pyqgis, Order_layer_v2
from  sortpanelmain import SortPanelMain
from  pyarchinit_db_manager import *
from  pyarchinit_exp_USsheet_pdf import *
from  delegateComboBox import *
from  imageViewer import ImageViewer

try:
	from pyarchinit_interactive_matrix_main import pyarchinit_Interactive_Matrix
	from  pyarchinit_matrix_exp import *
except:
	pass

##from interactivematrix import *
##import interactivematrix

class pyarchinit_US(QDialog, Ui_DialogUS):
	MSG_BOX_TITLE = "PyArchInit - Scheda US"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	BROWSE_STATUS = "b"
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	SORT_ITEMS_CONVERTED = ''
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'us_table'
	MAPPER_TABLE_CLASS = "US"
	NOME_SCHEDA = "Scheda US"
	ID_TABLE = "id_us"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Area":"area",
	"US":"us",
	"Definizione stratigrafica":"d_stratigrafica",
	"Definizione interpretata":"d_interpretativa",
	"Descrizione":"descrizione",
	"Interpretazione":"interpretazione",
	"Periodo Iniziale":"periodo_iniziale",
	"Periodo Finale":"periodo_finale",
	"Fase Iniziale":"fase_iniziale",
	"Fase finale":"fase_finale",
	u"Attività":"attivita",
	"Anno di scavo":"anno_scavo",
	"Sigla struttura":"struttura",
	"Scavato":"scavato",
	"Codice periodo" : "cont_per",
	"Indice di ordinamento" : "order_layer"
	}

	SORT_ITEMS = [
				ID_TABLE, 
				"Sito",
				"Area", 
				'US',
				"Definizione stratigrafica",
				"Definizione interpretata",
				"Descrizione",
				"Interpretazione",
				"Periodo Iniziale",
				"Periodo Finale", 
				"Fase Iniziale",
				"Fase Finale",
				u"Attività",
				"Anno di scavo",
				"Sigla struttura",
				"Scavato",
				"Codice periodo",
				"Indice di ordinamento"
				]

	TABLE_FIELDS = [
					'sito',
					'area',
					'us',
					'd_stratigrafica',
					'd_interpretativa',
					'descrizione',
					'interpretazione',
					'periodo_iniziale',
					'fase_iniziale',
					'periodo_finale',
					'fase_finale',
					'scavato',
					'attivita',
					'anno_scavo',
					'metodo_di_scavo',
					'inclusi',
					'campioni',
					'rapporti',
					'data_schedatura',
					'schedatore',
					'formazione',
					'stato_di_conservazione',
					'colore',
					'consistenza',
					'struttura',
					'cont_per',
					'order_layer',
					'documentazione'
					]

	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	REPORT_PATH = ('%s%s%s') % (HOME, os.sep, "pyarchinit_Report_folder")

	DB_SERVER = "not defined" ####nuovo sistema sort

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)
		QDialog.__init__(self)
		self.setupUi(self)
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except Exception, e:
			QMessageBox.warning(self, "Sistema di connessione", str(e),  QMessageBox.Ok)

		#SIGNALS & SLOTS Functions
		self.connect(self.comboBox_sito, SIGNAL("editTextChanged (const QString&)"), self.charge_periodo_iniz_list)
		self.connect(self.comboBox_sito, SIGNAL("editTextChanged (const QString&)"), self.charge_periodo_fin_list)

		self.connect(self.comboBox_sito, SIGNAL("currentIndexChanged(int)"), self.charge_periodo_iniz_list)
		self.connect(self.comboBox_sito, SIGNAL("currentIndexChanged(int)"), self.charge_periodo_fin_list)

		self.connect(self.comboBox_per_iniz, SIGNAL("editTextChanged (const QString&)"), self.charge_fase_iniz_list)
		self.connect(self.comboBox_per_iniz, SIGNAL("currentIndexChanged(int)"), self.charge_fase_iniz_list)

		self.connect(self.comboBox_per_fin, SIGNAL("editTextChanged (const QString&)"), self.charge_fase_fin_list)
		self.connect(self.comboBox_per_fin, SIGNAL("currentIndexChanged(int)"), self.charge_fase_fin_list)

		sito = self.comboBox_sito.currentText() 
		self.comboBox_sito.setEditText(sito)
		self.charge_periodo_iniz_list()
		self.charge_periodo_fin_list()
		self.fill_fields()
		self.customize_GUI()

	def charge_periodo_iniz_list(self):
		sito =unicode(self.comboBox_sito.currentText())
		#sitob = sito.decode('utf-8')

		search_dict = {
		'sito'  : "'"+sito+"'"
		}

		periodo_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

		periodo_list = []

		for i in range(len(periodo_vl)):
			periodo_list.append(str(periodo_vl[i].periodo))
		try:
			periodo_vl.remove('')
		except:
			pass
		
		self.comboBox_per_iniz.clear()
		self.comboBox_per_iniz.addItems(self.UTILITY.remove_dup_from_list(periodo_list))
		
		if self.STATUS_ITEMS[self.BROWSE_STATUS] == "Trova":
			self.comboBox_per_iniz.setEditText("")
		elif self.STATUS_ITEMS[self.BROWSE_STATUS] == "Usa":
			if len(self.DATA_LIST) > 0:
				try:
					self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)
				except:
					pass #non vi sono periodi per questo scavo


	def charge_periodo_fin_list(self):
		search_dict = {
		'sito'  : "'"+unicode(self.comboBox_sito.currentText())+"'"
		}
	
		periodo_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')   
		periodo_list = []

		for i in range(len(periodo_vl)):
			periodo_list.append(str(periodo_vl[i].periodo))
		try:
			periodo_vl.remove('')
		except:
			pass
		
		self.comboBox_per_fin.clear()
		self.comboBox_per_fin.addItems(self.UTILITY.remove_dup_from_list(periodo_list))
		
		if self.STATUS_ITEMS[self.BROWSE_STATUS] == "Trova":
			self.comboBox_per_fin.setEditText("")
		elif self.STATUS_ITEMS[self.BROWSE_STATUS] == "Usa":
			if len(self.DATA_LIST) > 0:
				try:
					self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)
				except:
					pass

	def on_pushButton_draw_doc_pressed(self):
		sito = unicode(self.comboBox_sito.currentText())
		area = unicode(self.comboBox_area.currentText())
		us = str(self.lineEdit_us.text())

		table_name = "self.tableWidget_documentazione"
		rowSelected_cmd = ("%s.selectedIndexes()") % (table_name)
		rowSelected = eval(rowSelected_cmd)
		rowIndex = (rowSelected[0].row())


		tipo_doc_item = self.tableWidget_documentazione.item(rowIndex,0)
		nome_doc_item = self.tableWidget_documentazione.item(rowIndex,1)

		tipo_doc = unicode(tipo_doc_item.text())
		nome_doc = unicode(nome_doc_item.text())
		
		lista_draw_doc = [sito,area,us,tipo_doc,nome_doc]

		self.pyQGIS.charge_vector_layers_doc_from_scheda_US(lista_draw_doc)

	def on_pushButton_go_to_us_pressed(self):
		try:
			table_name = "self.tableWidget_rapporti"
			rowSelected_cmd = ("%s.selectedIndexes()") % (table_name)
			rowSelected = eval(rowSelected_cmd)
			rowIndex = (rowSelected[0].row())

			sito = unicode(self.comboBox_sito.currentText())
			area = unicode(self.comboBox_area.currentText())
			us_item = self.tableWidget_rapporti.item(rowIndex,1)

			us = unicode(us_item.text())

			search_dict = {'sito' : "'"+unicode(sito)+"'",
							'area' : "'"+unicode(area)+"'",
							'us' : us}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
			if bool(res) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.fill_fields(self.REC_CORR)
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

				self.setComboBoxEnable(["self.comboBox_sito"],"False")
				self.setComboBoxEnable(["self.comboBox_area"],"False")
				self.setComboBoxEnable(["self.lineEdit_us"],"False")
			else:
				self.empty_fields()
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
					if self.toolButtonGis.isChecked() == True:
						self.pyQGIS.charge_vector_layers(self.DATA_LIST)
				else:
					strings = ("Sono stati trovati", self.REC_TOT, "records")
					if self.toolButtonGis.isChecked() == True:
						self.pyQGIS.charge_vector_layers(self.DATA_LIST)

				self.setComboBoxEnable(["self.comboBox_sito"],"False")
				self.setComboBoxEnable(["self.comboBox_area"],"False")
				self.setComboBoxEnable(["self.lineEdit_us"],"False")
		except Exception, e:
			e = str(e)
			QMessageBox.warning(self, "Alert", "Non hai selezionato nessuna riga. Errore python: %s " % (str(e)),  QMessageBox.Ok)


	def enable_button(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all.setEnabled(n)

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

		self.pushButton_view_all.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_save.setEnabled(n)

		self.pushButton_sort.setEnabled(n)

		self.pushButton_sort.setEnabled(n)

		self.pushButton_insert_row_rapporti.setEnabled(n)
		self.pushButton_remove_row_rapporti.setEnabled(n) 

		self.pushButton_insert_row_inclusi.setEnabled(n)
		self.pushButton_remove_row_inclusi.setEnabled(n)

		self.pushButton_insert_row_campioni.setEnabled(n)
		self.pushButton_remove_row_campioni.setEnabled(n)

		self.pushButton_insert_row_documentazione.setEnabled(n)
		self.pushButton_remove_row_documentazione.setEnabled(n)

	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		test_conn = conn_str.find('sqlite')
		if test_conn == 0:
			self.DB_SERVER = "sqlite"
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.charge_records() #charge records from DB
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.BROWSE_STATUS = 'b'
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
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> %s. E' NECESSARIO RIAVVIARE QGIS" % (str(e)),  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "Attenzione rilevato bug! Segnalarlo allo sviluppatore<br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		self.tableWidget_rapporti.setColumnWidth(0,380)
		self.tableWidget_rapporti.setColumnWidth(1,110)
		self.tableWidget_documentazione.setColumnWidth(0,150)
		self.tableWidget_documentazione.setColumnWidth(1,300)

		#map prevew system
		self.mapPreview = QgsMapCanvas(self)
		self.mapPreview.setCanvasColor(QColor(225,225,225))
		self.tabWidget.addTab(self.mapPreview, "Piante")

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

		#comboBox customizations
		self.setComboBoxEditable(["self.comboBox_per_fin"],1)
		self.setComboBoxEditable(["self.comboBox_fas_fin"],1)
		self.setComboBoxEditable(["self.comboBox_per_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_fas_iniz"],1)

		valuesRS = ["Uguale a", "Si lega a", "Copre", "Coperto da", "Riempie", "Riempito da", "Taglia", "Tagliato da", "Si appoggia a", "Gli si appoggia", ""]
		self.delegateRS = ComboBoxDelegate()
		self.delegateRS.def_values(valuesRS)
		self.delegateRS.def_editable('False')
		self.tableWidget_rapporti.setItemDelegateForColumn(0,self.delegateRS)

		valuesDoc = ["Fotografia", "Diapositiva", "Sezione", "Planimetria", "Prospetto", "Video", "Fotopiano"]
		self.delegateDoc = ComboBoxDelegate()
		self.delegateDoc.def_values(valuesDoc)
		self.delegateDoc.def_editable('False')
		self.tableWidget_documentazione.setItemDelegateForColumn(0,self.delegateDoc)

		valuesINCL_CAMP = ["Terra", "Pietre", "Laterizio", "Ciottoli", "Calcare", "Calce", "Carboni", "Concotto", "Ghiaia", "Cariossidi", "Malacofauna", "Sabbia", "Malta"]
		self.delegateINCL_CAMP = ComboBoxDelegate()
		valuesINCL_CAMP.sort()
		self.delegateINCL_CAMP.def_values(valuesINCL_CAMP)
		self.delegateINCL_CAMP.def_editable('False')
		self.tableWidget_inclusi.setItemDelegateForColumn(0,self.delegateINCL_CAMP)
		self.tableWidget_campioni.setItemDelegateForColumn(0,self.delegateINCL_CAMP)

	def loadMapPreview(self, mode = 0):
		if mode == 0:
			""" if has geometry column load to map canvas """
			gidstr =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))
			layerToSet = self.pyQGIS.loadMapPreview(gidstr)

			QMessageBox.warning(self, "layer to set", str(layerToSet), QMessageBox.Ok)

			self.mapPreview.setLayerSet(layerToSet)
			self.mapPreview.zoomToFullExtent()
		elif mode == 1:
			self.mapPreview.setLayerSet( [ ] )
			self.mapPreview.zoomToFullExtent()

	def loadMediaPreview(self, mode = 0):
		self.iconListWidget.clear()
		if mode == 0:
			""" if has geometry column load to map canvas """

			rec_list =  self.ID_TABLE + " = " + str(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))
			search_dict = {'id_entity'  : "'"+unicode(eval("self.DATA_LIST[int(self.REC_CORR)]." + self.ID_TABLE))+"'", 'entity_type' : "'US'"}
			record_us_list = self.DB_MANAGER.query_bool(search_dict, 'MEDIATOENTITY')
			for i in record_us_list:
				search_dict = {'id_media' : "'"+unicode(i.id_media)+"'"}

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

			search_dict = {'id_media' : "'"+unicode(id_orig_item)+"'"}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			try:
				res = self.DB_MANAGER.query_bool(search_dict, "MEDIA")
				file_path = unicode(res[0].filepath)
			except Exception, e:
				QMessageBox.warning(self, "Errore", "Attenzione 1 file: "+ str(e),  QMessageBox.Ok)

			dlg.show_image(unicode(file_path)) #item.data(QtCore.Qt.UserRole).toString()))
			dlg.exec_()

	def charge_list(self):
		#lista sito
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except Exception, e:
			if str(e) == "list.remove(x): x not in list":
				pass
			else:
				QMessageBox.warning(self, "Messaggio", "Sistema di aggiornamento lista Sito: " + str(e), QMessageBox.Ok)

		self.comboBox_sito.clear()
		self.comboBox_sito_rappcheck.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)
		self.comboBox_sito_rappcheck.addItems(sito_vl)


		#lista definizione_stratigrafica
		search_dict = {
		'nome_tabella'  : "'"+'us_table'+"'",
		'tipologia_sigla' : "'"+'definizione stratigrafica'+"'"
		}

		d_stratigrafica = self.DB_MANAGER.query_bool(search_dict, 'PYARCHINIT_THESAURUS_SIGLE')

		d_stratigrafica_vl = [ ]

		for i in range(len(d_stratigrafica)):
			d_stratigrafica_vl.append(d_stratigrafica[i].sigla_estesa)

		d_stratigrafica_vl.sort()
		self.comboBox_def_strat.addItems(d_stratigrafica_vl)


	def charge_fase_iniz_list(self):
		try:
			search_dict = {
			'sito'  : "'"+unicode(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+unicode(self.comboBox_per_iniz.currentText())+"'",
			}
		
			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')
		
			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(unicode(fase_list_vl[i].fase))
			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_iniz.clear()

			fase_list.sort()
			self.comboBox_fas_iniz.addItems(self.UTILITY.remove_dup_from_list(fase_list))

			if self.STATUS_ITEMS[self.BROWSE_STATUS] == "Trova":
				self.comboBox_fas_iniz.setEditText("")
			else:
				self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale)
		except:
			pass


	def charge_fase_fin_list(self):
		try:
			search_dict = {
			'sito'  : "'"+unicode(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+unicode(self.comboBox_per_fin.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(unicode(fase_list_vl[i].fase))
			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_fin.clear()
			fase_list.sort()
			self.comboBox_fas_fin.addItems(self.UTILITY.remove_dup_from_list(fase_list))

			if self.STATUS_ITEMS[self.BROWSE_STATUS] == "Trova":
				self.comboBox_fas_fin.setEditText("")
			else:
				self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale)
		except:
			pass


	#buttons functions
	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			#assegnazione valori di quota mn e max
			sito =  unicode(self.DATA_LIST[i].sito)
			area = unicode(self.DATA_LIST[i].area)
			us = unicode(self.DATA_LIST[i].us)

			res = self.DB_MANAGER.select_quote_from_db_sql(sito, area, us)
			quote = []

			for sing_us in res:
				sing_quota_value = str(sing_us[5])
				if sing_quota_value[0] == '-':
					sing_quota_value = sing_quota_value[:7]
				else:
					sing_quota_value = sing_quota_value[:6]

				sing_quota = [sing_quota_value, sing_us[4]]
				quote.append(sing_quota)
			quote.sort()

			if bool(quote) == True:
				quota_min = '%s %s' % (quote[0][0], quote[0][1])
				quota_max = '%s %s' % (quote[-1][0], quote[-1][1])
			else:
				quota_min = "Non inserita su GIS"
				quota_max = "Non inserita su GIS"

			#assegnazione numero di pianta
			resus = self.DB_MANAGER.select_us_from_db_sql(sito, area, us, "2")
			elenco_record = []
			for us in resus:
				elenco_record.append(us)

			if bool(elenco_record) == True:
				sing_rec = elenco_record[0]
				elenco_piante = sing_rec[6]
				if elenco_piante != None:
					piante = elenco_piante
				else:
					piante = "US disegnata su base GIS"
			else:
				piante = "US disegnata su base GIS"

			data_list.append([
			unicode(self.DATA_LIST[i].sito), 									#1 - Sito
			unicode(self.DATA_LIST[i].area),									#2 - Area
			int(self.DATA_LIST[i].us),												#3 - US
			unicode(self.DATA_LIST[i].d_stratigrafica),						#4 - definizione stratigrafica
			unicode(self.DATA_LIST[i].d_interpretativa),						#5 - definizione intepretata
			unicode(self.DATA_LIST[i].descrizione),							#6 - descrizione
			unicode(self.DATA_LIST[i].interpretazione),						#7 - interpretazione
			unicode(self.DATA_LIST[i].periodo_iniziale),						#8 - periodo iniziale
			unicode(self.DATA_LIST[i].fase_iniziale),							#9 - fase iniziale
			unicode(self.DATA_LIST[i].periodo_finale),						#10 - periodo finale iniziale
			unicode(self.DATA_LIST[i].fase_finale), 							#11 - fase finale
			unicode(self.DATA_LIST[i].scavato),								#12 - scavato
			unicode(self.DATA_LIST[i].attivita),									#13 - attivita
			unicode(self.DATA_LIST[i].anno_scavo),							#14 - anno scavo
			unicode(self.DATA_LIST[i].metodo_di_scavo),					#15 - metodo
			unicode(self.DATA_LIST[i].inclusi),									#16 - inclusi
			unicode(self.DATA_LIST[i].campioni),								#17 - campioni
			unicode(self.DATA_LIST[i].rapporti),								#18 - rapporti
			unicode(self.DATA_LIST[i].data_schedatura),					#19 - data schedatura
			unicode(self.DATA_LIST[i].schedatore),							#20 - schedatore
			unicode(self.DATA_LIST[i].formazione),							#21 - formazione
			unicode(self.DATA_LIST[i].stato_di_conservazione),			#22 - conservazione
			unicode(self.DATA_LIST[i].colore),									#23 - colore
			unicode(self.DATA_LIST[i].consistenza),							#24 - consistenza
			unicode(self.DATA_LIST[i].struttura),								#25 - struttura
			unicode(quota_min),														#26 - quota_min
			unicode(quota_max),													#27 - quota_max
			unicode(piante),															#28 - piante
			unicode(self.DATA_LIST[i].documentazione)						#29 - documentazione
		])
		return data_list


	def on_pushButton_exp_tavole_pressed(self):
		conn = Connection()
		conn_str = conn.conn_str()
		#QMessageBox.warning(self, "Messaggio", str(conn_str), QMessageBox.Ok)

		if conn_str.find("postgresql") == 0:
			PU = Print_utility(self.iface, self.DATA_LIST)
			PU.first_batch_try("postgres")
		else :
			PU = Print_utility(self.iface, self.DATA_LIST)
			PU.first_batch_try("sqlite")


	def on_pushButton_pdf_exp_pressed(self):
		US_pdf_sheet = generate_US_pdf()
		data_list = self.generate_list_pdf()
		US_pdf_sheet.build_US_sheets(data_list)

	def on_pushButton_exp_index_us_pressed(self):
		US_index_pdf = generate_US_pdf()
		data_list = self.generate_list_pdf()
		US_index_pdf.build_index_US(data_list, data_list[0][0])

	def on_pushButton_export_matrix_pressed(self):
		id_us_dict = {}
		for i in range(len(self.DATA_LIST)):
			id_us_dict[self.DATA_LIST[i].us] = self.DATA_LIST[i].id_us

		dlg = pyarchinit_Interactive_Matrix(self, self.DATA_LIST, id_us_dict)
		data_plot = dlg.generate_matrix()
		dlg.plot_matrix(data_plot)
		dlg.exec_()


	def launch_matrix_exp_if(self, msg):
		if msg == 1:
			self.on_pushButton_export_matrix_pressed()
		else:
			pass


	def on_pushButton_orderLayers_pressed(self):
		QMessageBox.warning(self,u'ATTENZIONE',u"""Il sistema accetta come dataset da elaborare ricerche su singolo SITO e AREA. Se state lanciando il sistema su siti o aree differenti, i dati di siti differenti saranno sovrascritti. Per terminare il sistema dopo l'Ok premere Cancel.""", QMessageBox.Ok)

		self.launch_matrix_exp_if(QMessageBox.warning(self,u'ATTENZIONE',u"Si consiglia di lanciare il matrix e controllare se sono presenti paradossi stratigrafici prima di proseguire", QMessageBox.Cancel,1))

		self.launch_order_layer_if(QMessageBox.warning(self,u'ATTENZIONE',u"Sei sicuro di voler proseguire? Se saranno presenti paradossi stratigrafici il sistema potrebbe andare in crush!", QMessageBox.Cancel,1))



##	def launch_order_layer_if(self, msg):
##		if msg == 1:
##
##			#report errori rapporti stratigrafici
##			msg_tipo_rapp = "Manca il tipo di rapporto nell'US: \n"
##			msg_nr_rapp = "Manca il numero del rapporto nell'US: \n"
##			msg_paradx_rapp = "Paradosso nei rapporti: \n"
##			msg_us_mancanti = "Mancano le seguenti schede US presenti nei rapporti: \n"
##			#report errori rapporti stratigrafici
##
##			data = []
##			for sing_rec in self.DATA_LIST:
##				us = sing_rec.us
##				rapporti_stratigrafici = eval(sing_rec.rapporti)
##				for sing_rapp in rapporti_stratigrafici:
##					if len(sing_rapp) != 2:
##						msg_nr_rapp = msg_nr_rapp + str(sing_rapp) + "relativo a: " + str(us) + " \n"
##						
##					try:
##						if sing_rapp[0] == 'Taglia' or  sing_rapp[0] == 'Copre' or  sing_rapp[0] == 'Si appoggia a' or  sing_rapp[0] == 'Riempie':  #or sing_rapp[0] == 'Si lega a' or  sing_rapp[0] == 'Uguale a'
##							try:
##								if sing_rapp[1] != '':
##									harris_rapp = (int(us), int(sing_rapp[1]))
####									if harris_rapp== (1, 67):
####										QMessageBox.warning(self, "Messaggio", "Magagna", QMessageBox.Ok)
##									data.append(harris_rapp)
##							except:
##								msg_nr_rapp = msg_nr_rapp + str(us) + " \n"
##					except:
##						msg_tipo_rapp = msg_tipo_rapp + str(us) + " \n"
##
##			for i in data:
##				temp_tup = (i[1],i[0]) #controlla che nn vi siano rapporti inversi dentro la lista DA PROBLEMI CON GLI UGUALE A E I SI LEGA A
##				#QMessageBox.warning(self, "Messaggio", "Temp_tup" + str(temp_tup), QMessageBox.Ok)
##				if data.count(temp_tup) != 0:
##					msg_paradx_rapp = msg_paradx_rapp + '\n'+str(i) + '\n' + str(temp_tup)
##					data.remove(i)
##			#OK
####			QMessageBox.warning(self, "Messaggio", "DATA LIST" + str(data), QMessageBox.Ok)
##
##			#script order layer from pyqgis
##			OL = Order_layer_v2(self.DB_MANAGER)
##			order_layer_dict = OL.main_order_layer()
##			#script order layer from pyqgis
##			QMessageBox.warning(self,u'ATTENZIONE',str(order_layer_dict), QMessageBox.Cancel,1)
##			
####			if order_layer_dict == "error":
####				QMessageBox.warning(self, "Messaggio", "Errore nei rapporti stratigrafici", QMessageBox.Ok)
####			else:
##			sito = self.DATA_LIST[0].sito #self.comboBox_sito_rappcheck.currentText()
##			area = self.DATA_LIST[0].area #self.comboBox_area.currentText()
##			order_number = ""
##			us = ""
##			for k,v in order_layer_dict.items():
##				order_number = str(k)
##				us = v
##				for sing_us in v:
##					search_dict = {'sito' : "'"+unicode(sito)+"'", 'area':"'"+unicode(area)+"'", 'us' : int(sing_us)}
##					try:
##						records = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS) #carica tutti i dati di uno scavo ordinati per numero di US
##
##						self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, self.ID_TABLE, [int(records[0].id_us)], ['order_layer'], [order_number])
##						self.lineEditOrderLayer.setText(unicode(order_number))
##					except Exception, e:
##						msg_us_mancanti = str(e) #msg_us_mancanti + "\n"+str(sito) + "area: " + str(area) + " us: " + (us)
##			
##			#blocco output errori
##			filename_tipo_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'tipo_rapporti_mancanti.txt')
##			filename_nr_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'nr_rapporti_mancanti.txt')
##			filename_paradosso_rapporti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'paradosso_rapporti.txt')
##			filename_us_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'us_mancanti.txt')
##
##			self.testing(filename_tipo_rapporti_mancanti, str(msg_tipo_rapp))
##			self.testing(filename_nr_rapporti_mancanti, str(msg_nr_rapp))
##			self.testing(filename_paradosso_rapporti, str(msg_paradx_rapp))
##			self.testing(filename_us_mancanti, str(msg_us_mancanti))
##		else:
##			QMessageBox.warning(self,u'ATTENZIONE',u"Sistema di ordinamento US abortito", QMessageBox.Ok)
##		#blocco output errori
####


	def launch_order_layer_if(self, msg):
		if msg == 1:

			#report errori rapporti stratigrafici
			msg_tipo_rapp = "Manca il tipo di rapporto nell'US: \n"
			msg_nr_rapp = "Manca il numero del rapporto nell'US: \n"
			msg_paradx_rapp = "Paradosso nei rapporti: \n"
			msg_us_mancanti = "Mancano le seguenti schede US presenti nei rapporti: \n"
			#report errori rapporti stratigrafici

			data = []
			for sing_rec in self.DATA_LIST:
				us = sing_rec.us
				rapporti_stratigrafici = eval(sing_rec.rapporti)
				for sing_rapp in rapporti_stratigrafici:
					if len(sing_rapp) != 2:
						msg_nr_rapp = msg_nr_rapp + str(sing_rapp) + "relativo a: " + str(us) + " \n"
						
					try:
						if sing_rapp[0] == 'Taglia' or  sing_rapp[0] == 'Copre' or  sing_rapp[0] == 'Si appoggia a' or  sing_rapp[0] == 'Riempie':  #or sing_rapp[0] == 'Si lega a' or  sing_rapp[0] == 'Uguale a'
							try:
								if sing_rapp[1] != '':
									harris_rapp = (int(us), int(sing_rapp[1]))
##									if harris_rapp== (1, 67):
##										QMessageBox.warning(self, "Messaggio", "Magagna", QMessageBox.Ok)
									data.append(harris_rapp)
							except:
								msg_nr_rapp = msg_nr_rapp + str(us) + " \n"
					except:
						msg_tipo_rapp = msg_tipo_rapp + str(us) + " \n"

			for i in data:
				temp_tup = (i[1],i[0]) #controlla che nn vi siano rapporti inversi dentro la lista DA PROBLEMI CON GLI UGUALE A E I SI LEGA A
				#QMessageBox.warning(self, "Messaggio", "Temp_tup" + str(temp_tup), QMessageBox.Ok)
				if data.count(temp_tup) != 0:
					msg_paradx_rapp = msg_paradx_rapp + '\n'+str(i) + '\n' + str(temp_tup)
					data.remove(i)
			#OK
##			QMessageBox.warning(self, "Messaggio", "DATA LIST" + str(data), QMessageBox.Ok)
			#Blocca il sistema di ordinamento su un sito ed area specifci in base alla ricerca eseguita sulla scheda US
			sito = self.DATA_LIST[0].sito #self.comboBox_sito_rappcheck.currentText()
			area = self.DATA_LIST[0].area #self.comboBox_area.currentText()
			#script order layer from pyqgis
			QMessageBox.warning(self, "Inizio sistema order layer", "Inizio sistema order layer",  QMessageBox.Ok)

			OL = Order_layer_v2(self.DB_MANAGER,sito,area)
			order_layer_dict = OL.main_order_layer()

			QMessageBox.warning(self, "Uscita dal sistema order layer", "Uscita dal sistema order layer",  QMessageBox.Ok)

			#script order layer from pyqgis
			
##			if order_layer_dict == "error":
##				QMessageBox.warning(self, "Messaggio", "Errore nei rapporti stratigrafici", QMessageBox.Ok)
##			else:

			order_number = ""
			us = ""
			try:
				for k,v in order_layer_dict.items():
					order_number = str(k)
					us = v
					for sing_us in v:
						search_dict = {'sito' : "'"+unicode(sito)+"'", 'area':"'"+unicode(area)+"'", 'us' : int(sing_us)}
						try:
							records = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS) #carica tutti i dati di uno scavo ordinati per numero di US

							self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, self.ID_TABLE, [int(records[0].id_us)], ['order_layer'], [order_number])
							self.on_pushButton_view_all_pressed()
						except Exception, e:
							msg_us_mancanti = str(e)#msg_us_mancanti + "\n"+str(sito) + "area: " + str(area) + " us: " + (us)
			except:
				QMessageBox.warning(self, "Errore Loop linea 903", "Errore Loop linea 903",  QMessageBox.Ok)

			
			#blocco output errori
			filename_tipo_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'tipo_rapporti_mancanti.txt')
			filename_nr_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'nr_rapporti_mancanti.txt')
			filename_paradosso_rapporti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'paradosso_rapporti.txt')
			filename_us_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'us_mancanti.txt')
			
			try:
				self.testing(filename_tipo_rapporti_mancanti, str(msg_tipo_rapp))
			except:
				pass
			try:
				self.testing(filename_nr_rapporti_mancanti, str(msg_nr_rapp))
			except:
				pass
			try:
				self.testing(filename_paradosso_rapporti, str(msg_paradx_rapp))
			except:
				pass
			try:
				self.testing(filename_us_mancanti, str(msg_us_mancanti))
			except:
				pass

			QMessageBox.warning(self,u'ATTENZIONE I',u"Sistema di ordinamento Terminato", QMessageBox.Ok)

		else:

			#report errori rapporti stratigrafici
			msg_tipo_rapp = "Manca il tipo di rapporto nell'US: \n"
			msg_nr_rapp = "Manca il numero del rapporto nell'US: \n"
			msg_paradx_rapp = "Paradosso nei rapporti: \n"
			msg_us_mancanti = "Mancano le seguenti schede US presenti nei rapporti: \n"
			#report errori rapporti stratigrafici

			data = []
			for sing_rec in self.DATA_LIST:
				us = sing_rec.us
				rapporti_stratigrafici = eval(sing_rec.rapporti)
				for sing_rapp in rapporti_stratigrafici:
					if len(sing_rapp) != 2:
						msg_nr_rapp = msg_nr_rapp + str(sing_rapp) + "relativo a: " + str(us) + " \n"

					try:
						if sing_rapp[0] == 'Taglia' or  sing_rapp[0] == 'Copre' or  sing_rapp[0] == 'Si appoggia a' or  sing_rapp[0] == 'Riempie':  #or sing_rapp[0] == 'Si lega a' or  sing_rapp[0] == 'Uguale a'
							try:
								if sing_rapp[1] != '':
									harris_rapp = (int(us), int(sing_rapp[1]))
##									if harris_rapp== (1, 67):
##										QMessageBox.warning(self, "Messaggio", "Magagna", QMessageBox.Ok)
									data.append(harris_rapp)
							except:
								msg_nr_rapp = msg_nr_rapp + str(us) + " \n"
					except:
						msg_tipo_rapp = msg_tipo_rapp + str(us) + " \n"

			for i in data:
				temp_tup = (i[1],i[0]) #controlla che nn vi siano rapporti inversi dentro la lista DA PROBLEMI CON GLI UGUALE A E I SI LEGA A
				#QMessageBox.warning(self, "Messaggio", "Temp_tup" + str(temp_tup), QMessageBox.Ok)
				if data.count(temp_tup) != 0:
					msg_paradx_rapp = msg_paradx_rapp + '\n'+str(i) + '\n' + str(temp_tup)
					data.remove(i)
			#OK
##			QMessageBox.warning(self, "Messaggio", "DATA LIST" + str(data), QMessageBox.Ok)
			#Blocca il sistema di ordinamento su un sito ed area specifci in base alla ricerca eseguita sulla scheda US
			sito = self.DATA_LIST[0].sito #self.comboBox_sito_rappcheck.currentText()
			area = self.DATA_LIST[0].area #self.comboBox_area.currentText()
			#script order layer from pyqgis
			QMessageBox.warning(self, "Inizio sistema order layer", "Inizio sistema order layer",  QMessageBox.Ok)

			OL = Order_layer_v2(self.DB_MANAGER,sito,area)
			order_layer_dict = OL.main_order_layer()

			QMessageBox.warning(self, "Uscita dal sistema order layer", "Uscita dal sistema order layer",  QMessageBox.Ok)
			#script order layer from pyqgis

##			if order_layer_dict == "error":
##				QMessageBox.warning(self, "Messaggio", "Errore nei rapporti stratigrafici", QMessageBox.Ok)
##			else:

			order_number = ""
			us = ""
			try:
				for k,v in order_layer_dict.items():
					order_number = str(k)
					us = v
					for sing_us in v:
						search_dict = {'sito' : "'"+unicode(sito)+"'", 'area':"'"+unicode(area)+"'", 'us' : int(sing_us)}
						try:
							records = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS) #carica tutti i dati di uno scavo ordinati per numero di US

							self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, self.ID_TABLE, [int(records[0].id_us)], ['order_layer'], [order_number])
							self.on_pushButton_view_all_pressed()
						except Exception, e:
							msg_us_mancanti = str(e)#msg_us_mancanti + "\n"+str(sito) + "area: " + str(area) + " us: " + (us)
			except:
				QMessageBox.warning(self, "Errore Loop linea 995", "Errore Loop linea 995",  QMessageBox.Ok)

			#blocco output errori
			filename_tipo_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'tipo_rapporti_mancanti.txt')
			filename_nr_rapporti_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'nr_rapporti_mancanti.txt')
			filename_paradosso_rapporti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'paradosso_rapporti.txt')
			filename_us_mancanti = ('%s%s%s') % (self.REPORT_PATH, os.sep, 'us_mancanti.txt')

			try:
				self.testing(filename_tipo_rapporti_mancanti, str(msg_tipo_rapp))
			except:
				pass
			try:
				self.testing(filename_nr_rapporti_mancanti, str(msg_nr_rapp))
			except:
				pass
			try:
				self.testing(filename_paradosso_rapporti, str(msg_paradx_rapp))
			except:
				pass
			try:
				self.testing(filename_us_mancanti, str(msg_us_mancanti))
			except:
				pass


			QMessageBox.warning(self,u'ATTENZIONE II',u"Sistema di ordinamento Terminato", QMessageBox.Ok)

			#QMessageBox.warning(self,u'ATTENZIONE',u"Sistema di ordinamento US abortito", QMessageBox.Ok)
		#blocco output errori
##
	def on_toolButtonPan_toggled(self):
		self.toolPan = QgsMapToolPan(self.mapPreview)
		self.mapPreview.setMapTool(self.toolPan)

	def on_pushButton_showSelectedFeatures_pressed(self):
		#field_position = self.pyQGIS.findFieldFrDict(self.ID_TABLE) #ricava la posizione del campo
		
		layer = self.iface.mapCanvas().currentLayer()
		fieldname = self.ID_TABLE
		features_list = self.iface.mapCanvas().currentLayer().selectedFeatures()

		field_position = ""
		for single in layer.getFeatures():
			field_position  =  single.fieldNameIndex(fieldname)

		id_list = []
		for feat in features_list:
			attr_list = feat.attributes()
			id_list.append(attr_list[field_position])

		#viene impostata la query per il database
		items,order_type = [self.ID_TABLE], "asc"
		self.empty_fields()

		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, items, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for us in temp_data_list:
			self.DATA_LIST.append(us)
		
		#vengono riempiti i campi con i dati trovati
		self.fill_fields()
		self.BROWSE_STATUS = 'b'
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

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
				#QMessageBox.warning(self, "Messaggio",i, QMessageBox.Ok)
				self.SORT_ITEMS_CONVERTED.append(self.CONVERSION_DICT[unicode(i)]) #apportare la modifica nellle altre schede

			self.SORT_MODE = order_type
			self.empty_fields()

			id_list = []
			for i in self.DATA_LIST:
				id_list.append(eval("i." + self.ID_TABLE))
			self.DATA_LIST = []

			temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

			for i in temp_data_list:
				self.DATA_LIST.append(i)
			self.BROWSE_STATUS = 'b'
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

	def on_toolButtonGis_toggled(self):
		if self.toolButtonGis.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS attiva. Da ora le tue ricerche verranno visualizzate sul GIS", QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Messaggio", "Modalita' GIS disattivata. Da ora le tue ricerche non verranno piu' visualizzate sul GIS", QMessageBox.Ok)

	def on_toolButtonPreview_toggled(self):
		if self.toolButtonPreview.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview US attivata. Le piante delle US saranno visualizzate nella sezione Piante", QMessageBox.Ok)
			self.loadMapPreview()
		else:
			self.loadMapPreview(1)

	def on_toolButtonPreviewMedia_toggled(self):
		if self.toolButtonPreviewMedia.isChecked() == True:
			QMessageBox.warning(self, "Messaggio", "Modalita' Preview Media US attivata. Le immagini delle US saranno visualizzate nella sezione Media", QMessageBox.Ok)
			self.loadMediaPreview()
		else:
			self.loadMediaPreview(1)

	def on_pushButton_addRaster_pressed(self):
		if self.toolButtonGis.isChecked() == True:
			self.pyQGIS.addRasterLayer()

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

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEditable(["self.comboBox_area"],0)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_area"],"True")
			self.setComboBoxEnable(["self.lineEdit_us"],"True")

			self.SORT_STATUS = "n"
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


					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_area"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					self.fill_fields(self.REC_CORR)

					self.enable_button(1)
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Problema nell'inserimento dati",  QMessageBox.Ok)

	def on_pushButton_rapp_check_pressed(self):
		sito_check = unicode(self.comboBox_sito_rappcheck.currentText())
		area_check = unicode(self.comboBox_area_rappcheck.currentText())
		self.rapporti_stratigrafici_check(sito_check, area_check)
		QMessageBox.warning(self, "Messaggio", "Controllo Rapporti Stratigrafici. \n Controllo eseguito con successo",  QMessageBox.Ok)

	def data_error_check(self):
		test = 0
		EC = Error_check()

		if EC.data_is_empty(unicode(self.comboBox_sito.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Sito. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(unicode(self.comboBox_area.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Area. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(unicode(self.lineEdit_us.text())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo US. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		area = self.comboBox_area.currentText()
		us = self.lineEdit_us.text()
		attivita = self.lineEdit_attivita.text()
		colore = self.comboBox_colore.currentText()
		anno_scavo = self.lineEdit_anno.text()
		formazione = self.comboBox_formazione.currentText()
		stato_conservazione = self.comboBox_conservazione.currentText()
		colore= self.comboBox_colore.currentText()
		consistenza = self.comboBox_consistenza.currentText()
		struttura = self.lineEdit_struttura.text()
		cont_per = self.lineEdit_codice_periodo.text()

		
		if area != "":
			if EC.data_is_int(area) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Area. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if us != "":
			if EC.data_is_int(us) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo US. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1
				
		if attivita != "":
			if EC.data_lenght(attivita,3) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Attivita. \n Il valore non deve superare i 4 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1		
				
		#if anno_scavo != "":
		#	if EC.data_lenght(anno_scavo,3) == 0:
		#		QMessageBox.warning(self, "ATTENZIONE", "Campo Anno. \n immettere una sola data (es. 2014)",  QMessageBox.Ok)
		#		test = 1
				
		if formazione != "":
			if EC.data_lenght(formazione,19) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Formazione. \n Il valore non deve superare i 20 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1
				
		if stato_conservazione != "":
			if EC.data_lenght(stato_conservazione,19) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Conservazione. \n Il valore non deve superare i 20 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1
				
				
		if colore != "":
			if EC.data_lenght(colore,19) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Colore. \n Il valore non deve superare i 20 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1
				
				
		if consistenza != "":
			if EC.data_lenght(consistenza,19) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Consistenza. \n Il valore non deve superare i 20 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1
				
				
		if struttura != "":
			if EC.data_lenght(struttura,29) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Struttura. \n Il valore non deve superare i 30 caratteri alfanumerici",  QMessageBox.Ok)
				test = 1
				
				
		#if cont_per != "":
		#	if EC.data_lenght(cont_per,199) == 0:
		#		QMessageBox.warning(self, "ATTENZIONE", "Campo codice periodo. \n Il valore non deve superare i 200 caratteri numerici",  QMessageBox.Ok)
		#		test = 1
				
				
				

		#PERIODIZZAZIONE CHECK
		#periodo iniz compilato e fase vuota  il blocco deve essere utilizzato meglio a partire dai signals
		"""
		if self.comboBox_per_iniz.currentText() != "" and self.comboBox_fas_iniz.currentText() == "":
			QMessageBox.warning(self, "ATTENZIONE", "Campo Fase iniziale \n Specificare la Fase iniziale oltre al Periodo",  QMessageBox.Ok)
			test = 1

		if self.comboBox_per_fin.currentText()  != "" and self.comboBox_fas_fin.currentText() == "":
			QMessageBox.warning(self, "ATTENZIONE", "Campo Fase finale \n Specificare la Fase finale oltre al Periodo",  QMessageBox.Ok)
			test = 1
			
		if self.comboBox_per_iniz.currentText()  == "" and self.comboBox_fas_iniz.currentText() != "":
			QMessageBox.warning(self, "ATTENZIONE", "Campo Periodo iniziale \n Specificare un Periodo iniziale oltre alla Fase",  QMessageBox.Ok)
			test = 1
			
		if self.comboBox_per_fin.currentText()  == "" and self.comboBox_fas_fin.currentText() != "":
			QMessageBox.warning(self, "ATTENZIONE", "Campo Periodo iniziale \n Specificare un Periodo finale oltre alla Fase",  QMessageBox.Ok)
			test = 1
			
		if self.comboBox_per_fin.currentText()  != "" and self.comboBox_fas_fin.currentText() != "" and self.comboBox_per_iniz.currentText()  == "" and self.comboBox_fas_iniz.currentText() == "":
			QMessageBox.warning(self, "ATTENZIONE", "Campi Periodo e Fase iniziali \n Specificare un Periodo e Fase iniziali se si vuole inserire un Periodo e Fase finali",  QMessageBox.Ok)
			test = 1

		if self.comboBox_per_fin.currentText()  != "" and self.comboBox_fas_fin.currentText() != "" and self.comboBox_per_iniz.currentText()  == "" and self.comboBox_fas_iniz.currentText() == "":
			QMessageBox.warning(self, "ATTENZIONE", "Campi Periodo e Fase iniziali \n Specificare un Periodo e Fase iniziali se si vuole inserire un Periodo e Fase finali",  QMessageBox.Ok)
			test = 1

		if self.comboBox_per_iniz.currentText()  != "" and self.comboBox_fas_iniz.currentText() != "":

			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_iniz.currentText())+"'",
			}
			if  bool(self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Campi Periodo e Fase iniziali \n E' stata inserita una periodizzazione inesistente",  QMessageBox.Ok)
				test = 1
		"""
		return test

	def rapporti_stratigrafici_check(self, sito_check, area_check):
		conversion_dict = {'Copre':'Coperto da',
						   'Coperto da': 'Copre',
						   'Riempie': 'Riempito da',
						   'Riempito da' : 'Riempie',
						   'Taglia': 'Tagliato da',
						   'Tagliato da': 'Taglia',
						   'Si appoggia a': 'Gli si appoggia',
						   'Gli si appoggia': 'Si appoggia a',
						   'Si lega a': 'Si lega a',
						   'Uguale a':'Uguale a'
						   }

		search_dict = {'sito' : "'"+unicode(sito_check)+"'", 'area' : "'"+unicode(area_check)+"'"}

		records = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS) #carica tutti i dati di uno scavo ordinati per numero di US

		report_rapporti = '\bReport controllo Rapporti Stratigrafici - Sito: %s \n' % (sito_check)

		for rec in range(len(records)):
			sito = "'"+unicode(records[rec].sito)+"'"
			area = "'"+unicode(records[rec].area)+"'"
			us = int(records[rec].us)

			rapporti = records[rec].rapporti #caricati i rapporti nella variabile
			rapporti = eval(rapporti)

			for sing_rapp in rapporti:  #itera sulla serie di rapporti
				if len(sing_rapp) == 2:
					try:
						rapp_converted = conversion_dict[sing_rapp[0]]
						serch_dict_rapp = {'sito': sito, 'area': area, 'us': sing_rapp[1]}
						us_rapp = self.DB_MANAGER.query_bool(serch_dict_rapp, self.MAPPER_TABLE_CLASS)

						if bool(us_rapp) == False:
							report = '\bSito: %s, \bArea: %s, \bUS: %d %s US: %d: Scheda US non esistente' % (sito, area, int(us), sing_rapp[0], int(sing_rapp[1]))
						else:
							rapporti_check = eval(us_rapp[0].rapporti)
							us_rapp_check = ('%s') % str(us)
							if rapporti_check.count([rapp_converted, us_rapp_check]) == 1:
								report = "" #"Errore generico. Probabile presenza di rapporti vuoti o scritti non correttamente: " + str([rapp_converted, us_rapp_check])
							else:
								report = '\bSito: %s, \bArea: %s, \bUS: %d %s \bUS: %d: Rapporto non verificato' % (sito, area, int(us), sing_rapp[0], int(sing_rapp[1]))
					except Exception, e:
						report = "Problema di conversione rapporto: " + str(e)
					if report != "":
						report_rapporti = report_rapporti + report + '\n'
		if os.name == 'posix':
			HOME = os.environ['HOME']
		elif os.name == 'nt':
			HOME = os.environ['HOMEPATH']
		
		report_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_Report_folder")
		filename = ('%s%s%s') % (report_path, os.sep, 'rapporti_US.txt')
		f = open(filename, "w")
		f.write(report_rapporti)
		f.close()


	def insert_new_rec(self):
		#TableWidget
		##Rapporti
		rapporti = self.table2dict("self.tableWidget_rapporti")
		##Inclusi
		inclusi = self.table2dict("self.tableWidget_inclusi")
		##Campioni
		campioni = self.table2dict("self.tableWidget_campioni")
		##Documentazione
		documentazione = self.table2dict("self.tableWidget_documentazione")
		
		if self.lineEditOrderLayer.text() == "":
			order_layer = 0
		else:
			order_layer = int(self.lineEditOrderLayer.text())

		try:
			#data
			data = self.DB_MANAGER.insert_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			unicode(self.comboBox_sito.currentText()), 				#1 - Sito
			unicode(self.comboBox_area.currentText()), 				#2 - Area
			int(self.lineEdit_us.text()),									#3 - US
			unicode(self.comboBox_def_strat.currentText()),			#4 - Definizione stratigrafica
			unicode(self.comboBox_def_intepret.currentText()),		#5 - Definizione intepretata
			unicode(self.textEdit_descrizione.toPlainText()),		#6 - descrizione
			unicode(self.textEdit_interpretazione.toPlainText()),#7 - interpretazione
			unicode(self.comboBox_per_iniz.currentText()),			#8 - periodo iniziale
			unicode(self.comboBox_fas_iniz.currentText()),			#9 - fase iniziale
			unicode(self.comboBox_per_fin.currentText()), 			#10 - periodo finale iniziale
			unicode(self.comboBox_fas_fin.currentText()), 			#11 - fase finale
			unicode(self.comboBox_scavato.currentText()),			#12 - scavato
			unicode(self.lineEdit_attivita.text()),							#13 - attivita  
			unicode(self.lineEdit_anno.text()),								#14 - anno scavo
			unicode(self.comboBox_metodo.currentText()), 			#15 - metodo
			unicode(inclusi),														#16 - inclusi
			unicode(campioni),													#17 - campioni
			unicode(rapporti),													#18 - rapporti
			unicode(self.lineEdit_data_schedatura.text()),				#19 - data schedatura
			unicode(self.comboBox_schedatore.currentText()),		#20 - schedatore
			unicode(self.comboBox_formazione.currentText()),		#21 - formazione
			unicode(self.comboBox_conservazione.currentText()),	#22 - conservazione
			unicode(self.comboBox_colore.currentText()),				#23 - colore
			unicode(self.comboBox_consistenza.currentText()),		#24 - consistenza
			unicode(self.lineEdit_struttura.text()),							#25 - struttura
			unicode(self.lineEdit_codice_periodo.text()),					#26 - continuita  periodo
			order_layer,													#27 - order layer
			unicode(documentazione))										#28 - documentazione
			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("IntegrityError"):
					msg = self.ID_TABLE + u" gia' presente nel database"
					QMessageBox.warning(self, "Errore", "Errore"+ str(msg),  QMessageBox.Ok)
				else:
					msg = e
					QMessageBox.warning(self, "Errore", "Errore di immisione 1 \n"+ str(msg),  QMessageBox.Ok)
				return 0

		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immisione 2 \n"+str(e),  QMessageBox.Ok)
			return 0

	#insert new row into tableWidget
	def on_pushButton_insert_row_rapporti_pressed(self):
		self.insert_new_row('self.tableWidget_rapporti')

	def on_pushButton_remove_row_rapporti_pressed(self):
		self.remove_row('self.tableWidget_rapporti')

	def on_pushButton_insert_row_inclusi_pressed(self):
		self.insert_new_row('self.tableWidget_inclusi')
	def on_pushButton_remove_row_inclusi_pressed(self):
		self.remove_row('self.tableWidget_inclusi')

	def on_pushButton_insert_row_campioni_pressed(self):
		self.insert_new_row('self.tableWidget_campioni')
	def on_pushButton_remove_row_campioni_pressed(self):
		self.remove_row('self.tableWidget_campioni')

	def on_pushButton_insert_row_documentazione_pressed(self):
		self.insert_new_row('self.tableWidget_documentazione')
	def on_pushButton_remove_row_documentazione_pressed(self):
		self.remove_row('self.tableWidget_documentazione')

	def check_record_state(self):
		ec = self.data_error_check()
		if ec == 1:
			return 1 #ci sono errori di immissione
		elif self.records_equal_check() == 1 and ec == 0:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
			#self.charge_records()
			return 0 #non ci sono errori di immissione


	#records surf functions
	def on_pushButton_view_all_pressed(self):
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
		self.SORT_STATUS = "n"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])


	#records surf functions
	def on_pushButton_first_rec_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			try:
				self.empty_fields()
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.fill_fields(0)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_last_rec_pressed(self):
		if self.check_record_state() == 1:
			pass
		else:
			try:
				self.empty_fields()
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
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
		if self.BROWSE_STATUS != "f" and self.check_record_state() == 1:
			pass
		else:
			self.enable_button_search(0)


			#set the GUI for a new search

			if self.BROWSE_STATUS != "f":
				self.BROWSE_STATUS = "f"
				###
				self.lineEdit_data_schedatura.setText("")
				self.lineEdit_anno.setText("")
				self.comboBox_formazione.setEditText("")
				self.comboBox_metodo.setEditText("")
				self.setComboBoxEditable(["self.comboBox_sito"],1)
				self.setComboBoxEditable(["self.comboBox_area"],1)
				self.setComboBoxEnable(["self.comboBox_sito"],"True")
				self.setComboBoxEnable(["self.comboBox_area"],"True")
				self.setComboBoxEnable(["self.lineEdit_us"],"True")
				self.setComboBoxEnable(["self.textEdit_descrizione"],"False")
				self.setComboBoxEnable(["self.textEdit_interpretazione"],"False")
				self.setTableEnable(["self.tableWidget_campioni", "self.tableWidget_rapporti","self.tableWidget_inclusi",
				"self.tableWidget_documentazione"], "False")
				###
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter('','')
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.charge_list()
				self.empty_fields()



	def on_pushButton_showLayer_pressed(self):
		"""
		for sing_us in range(len(self.DATA_LIST)):
			sing_layer = [self.DATA_LIST[sing_us]]
			self.pyQGIS.charge_vector_layers(sing_layer)
		"""

		sing_layer = [self.DATA_LIST[self.REC_CORR]]
		self.pyQGIS.charge_vector_layers(sing_layer)


	def on_pushButton_crea_codice_periodo_pressed(self):
		sito = unicode(self.comboBox_sito.currentText())
		self.DB_MANAGER.update_cont_per(sito)
		self.empty_fields()
		self.charge_records()
		self.fill_fields(self.REC_CORR) #ricaricare tutti i record in uso e passare il valore REC_CORR a fill_fields

		QMessageBox.warning(self, "Attenzione", "Codice periodo aggiornato per lo scavo %s" % (sito),  QMessageBox.Ok)

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:

			#TableWidget
			
			if self.lineEdit_us.text() != "":
				us = int(self.lineEdit_us.text())
			else:
				us = ""
			search_dict = {
			self.TABLE_FIELDS[0]  : "'"+unicode(self.comboBox_sito.currentText())+"'", 									#1 - Sito
			self.TABLE_FIELDS[1]  : "'"+unicode(self.comboBox_area.currentText())+"'",									#2 - Area
			self.TABLE_FIELDS[2]  : us,																								#3 - US
			self.TABLE_FIELDS[3]  : "'"+unicode(self.comboBox_def_strat.currentText())+"'",								#4 - Definizione stratigrafica
			self.TABLE_FIELDS[4]  : "'"+unicode(self.comboBox_def_intepret.currentText())+"'",							#5 - Definizione intepretata
			self.TABLE_FIELDS[5]  : unicode(self.textEdit_descrizione.toPlainText()),											#6 - descrizione
			self.TABLE_FIELDS[6]  : unicode(self.textEdit_interpretazione.toPlainText()),										#7 - interpretazione
			self.TABLE_FIELDS[7]  : "'"+unicode(self.comboBox_per_iniz.currentText())+"'",								#8 - periodo iniziale
			self.TABLE_FIELDS[8]  : "'"+unicode(self.comboBox_fas_iniz.currentText())+"'",								#9 - fase iniziale
			self.TABLE_FIELDS[9]  : "'"+unicode(self.comboBox_per_fin.currentText())+"'",	 							#10 - periodo finale iniziale
			self.TABLE_FIELDS[10] : "'"+unicode(self.comboBox_fas_fin.currentText())+"'", 								#11 - fase finale
			self.TABLE_FIELDS[11] : "'"+unicode(self.comboBox_scavato.currentText())+"'",								#12 - scavato 
			self.TABLE_FIELDS[12] : "'"+unicode(self.lineEdit_attivita.text())+"'",												#13 - attivita  
			self.TABLE_FIELDS[13] : "'"+unicode(self.lineEdit_anno.text())+"'",													#14 - anno scavo
			self.TABLE_FIELDS[14] : "'"+unicode(self.comboBox_metodo.currentText())+"'", 								#15 - metodo
			self.TABLE_FIELDS[18] : "'"+unicode(self.lineEdit_data_schedatura.text())+"'",									#16 - data schedatura
			self.TABLE_FIELDS[19] : "'"+unicode(self.comboBox_schedatore.currentText())+"'",							#17 - schedatore
			self.TABLE_FIELDS[20] : "'"+unicode(self.comboBox_formazione.currentText())+"'",							#18 - formazione
			self.TABLE_FIELDS[21] : "'"+unicode(self.comboBox_conservazione.currentText())+"'",						#19 - conservazione
			self.TABLE_FIELDS[22] : "'"+unicode(self.comboBox_colore.currentText())+"'",								#20 - colore
			self.TABLE_FIELDS[23] : "'"+unicode(self.comboBox_consistenza.currentText())+"'",							#21 - consistenza
			self.TABLE_FIELDS[24] : "'"+unicode(self.lineEdit_struttura.text())+"'",											#22 - struttura
			self.TABLE_FIELDS[25] : "'"+unicode(self.lineEdit_codice_periodo.text())+"'",									#23 - codice_periodo
			self.TABLE_FIELDS[26] : "'"+unicode(self.lineEditOrderLayer.text())+"'"											#24 - order layer
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", u"Non è stata impostata nessuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(res) == False:
					QMessageBox.warning(self, "ATTENZIONE", u"Non è stato trovato nessun record!",  QMessageBox.Ok)

					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]

					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					self.setComboBoxEnable(["self.textEdit_descrizione"],"True")
					self.setComboBoxEnable(["self.textEdit_interpretazione"],"True")
					self.setTableEnable(["self.tableWidget_campioni", "self.tableWidget_rapporti","self.tableWidget_inclusi","self.tableWidget_documentazione"], "True")
					self.fill_fields(self.REC_CORR)
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
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)
					else:
						strings = ("Sono stati trovati", self.REC_TOT, "records")
						if self.toolButtonGis.isChecked() == True:
							self.pyQGIS.charge_vector_layers(self.DATA_LIST)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_area"],"False")
					self.setComboBoxEnable(["self.lineEdit_us"],"False")
					
					self.setTableEnable(["self.tableWidget_campioni", "self.tableWidget_rapporti","self.tableWidget_inclusi",
												"self.tableWidget_documentazione"], "True")
					self.setComboBoxEnable(["self.textEdit_descrizione"],"True")
					self.setComboBoxEnable(["self.textEdit_interpretazione"],"True")
					
					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)
		self.enable_button_search(1)

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
		return rec_to_update


	#custom functions
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

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def yearstrfdate(self):
		now = date.today()
		year = now.strftime("%Y")
		return year

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

##		max_row_num = len(self.data_list)
##		value = eval(self.table_name+".item(max_row_num,1)")
##		if value == '':
##			cmd = ("%s.removeRow(%d)") % (self.table_name, max_row_num)
##			eval(cmd)


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
		rowIndex = (rowSelected[0].row())
		cmd = ("%s.removeRow(%d)") % (table_name, rowIndex)
		eval(cmd)


	def empty_fields(self):
		rapporti_row_count = self.tableWidget_rapporti.rowCount()
		campioni_row_count = self.tableWidget_campioni.rowCount()
		inclusi_row_count = self.tableWidget_inclusi.rowCount()
		documentazione_row_count = self.tableWidget_documentazione.rowCount()
		
		self.comboBox_sito.setEditText("")  								#1 - Sito
		self.comboBox_area.setEditText("") 								#2 - Area
		self.lineEdit_us.clear()													#3 - US
		self.comboBox_def_strat.setEditText("")							#4 - Definizione stratigrafica
		self.comboBox_def_intepret.setEditText("")						#5 - Definizione intepretata
		self.textEdit_descrizione.clear()										#6 - descrizione
		self.textEdit_interpretazione.clear()									#7 - interpretazione
		self.comboBox_per_iniz.setEditText("")								#8 - periodo iniziale
		self.comboBox_fas_iniz.setEditText("")								#9 - fase iniziale
		self.comboBox_per_fin.setEditText("") 							#10 - periodo finale iniziale
		self.comboBox_fas_fin.setEditText("") 								#11 - fase finale
		self.comboBox_scavato.setEditText("")							#12 - scavato
		self.lineEdit_attivita.clear()												#13 - attivita
		if self.BROWSE_STATUS == "n":
			self.lineEdit_anno.setText(self.yearstrfdate())					#14 - anno scavo
		else:
			self.lineEdit_anno.clear()
		self.comboBox_metodo.setEditText("")				#15 - metodo
		for i in range(inclusi_row_count):
			self.tableWidget_inclusi.removeRow(0) 					
		self.insert_new_row("self.tableWidget_inclusi")					#16 - inclusi
		for i in range(campioni_row_count):
			self.tableWidget_campioni.removeRow(0)
		self.insert_new_row("self.tableWidget_campioni")				#17 - campioni
		for i in range(rapporti_row_count):
			self.tableWidget_rapporti.removeRow(0)
		#self.insert_new_row("self.tableWidget_rapporti")				#18 - rapporti
		for i in range(documentazione_row_count):
			self.tableWidget_documentazione.removeRow(0) 					
		self.insert_new_row("self.tableWidget_documentazione")		#19 - documentazione
		if self.BROWSE_STATUS == "n":
			self.lineEdit_data_schedatura.setText(self.datestrfdate())	#20 - data schedatura
		else:
			self.lineEdit_data_schedatura.setText("")	#20 - data schedatura
		self.comboBox_schedatore.setEditText("")						#21 - schedatore
		self.comboBox_formazione.setEditText("")				#22 - formazione
		self.comboBox_conservazione.setEditText("")					#23 - conservazione
		self.comboBox_colore.setEditText("")								#24 - colore
		self.comboBox_consistenza.setEditText("")						#25 - consistenza
		self.lineEdit_struttura.clear()											#26 - struttura
		self.lineEdit_codice_periodo.clear()									#27 - codice periodo
		self.lineEditOrderLayer.clear()											#28 - order layer

	def fill_fields(self, n=0):
		self.rec_num = n
		#QMessageBox.warning(self, "Test", str(self.comboBox_per_fin.currentText()),  QMessageBox.Ok)
		try:
			unicode(self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)) 													#1 - Sito
			unicode(self.comboBox_area.setEditText(self.DATA_LIST[self.rec_num].area) )												#2 - Area
			self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))																		#3 - US
			unicode(self.comboBox_def_strat.setEditText(self.DATA_LIST[self.rec_num].d_stratigrafica))								#4 - Definizione stratigrafica
			unicode(self.comboBox_def_intepret.setEditText(self.DATA_LIST[self.rec_num].d_interpretativa))						#5 - Definizione intepretata
			unicode(self.textEdit_descrizione.setText(self.DATA_LIST[self.rec_num].descrizione))										#6 - descrizione
			unicode(self.textEdit_interpretazione.setText(self.DATA_LIST[self.rec_num].interpretazione))								#7 - interpretazione
			unicode(self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale))								#8 - periodo iniziale
			unicode(self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale))									#9 - fase iniziale
			unicode(self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_finale))								#10 - periodo finale iniziale
			unicode(self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale)) 									#11 - fase finale
			unicode(self.comboBox_scavato.setEditText(self.DATA_LIST[self.rec_num].scavato))										#12 - scavato
			unicode(self.lineEdit_attivita.setText(self.DATA_LIST[self.rec_num].attivita))													#13 - attivita
			unicode(self.lineEdit_anno.setText(self.DATA_LIST[self.rec_num].anno_scavo))												#14 - anno scavo
			unicode(self.comboBox_metodo.setEditText(self.DATA_LIST[self.rec_num].metodo_di_scavo)) 							#15 - metodo
			self.tableInsertData("self.tableWidget_inclusi", self.DATA_LIST[self.rec_num].inclusi)											#16 - inclusi
			self.tableInsertData("self.tableWidget_campioni", self.DATA_LIST[self.rec_num].campioni)									#17 - campioni
			self.tableInsertData("self.tableWidget_rapporti",self.DATA_LIST[self.rec_num].rapporti)										#18 - rapporti
			self.tableInsertData("self.tableWidget_documentazione",self.DATA_LIST[self.rec_num].documentazione)				#19 - documentazione
			unicode(self.lineEdit_data_schedatura.setText(self.DATA_LIST[self.rec_num].data_schedatura))							#20 - data schedatura
			unicode(self.comboBox_schedatore.setEditText(self.DATA_LIST[self.rec_num].schedatore))								#21 - schedatore
			unicode(self.comboBox_formazione.setEditText(self.DATA_LIST[self.rec_num].formazione))								#22 - formazione
			unicode(self.comboBox_conservazione.setEditText(self.DATA_LIST[self.rec_num].stato_di_conservazione))			#23 - conservazione
			unicode(self.comboBox_colore.setEditText(self.DATA_LIST[self.rec_num].colore))											#24 - colore
			unicode(self.comboBox_consistenza.setEditText(self.DATA_LIST[self.rec_num].consistenza))								#25 - consistenza
			unicode(self.lineEdit_struttura.setText(self.DATA_LIST[self.rec_num].struttura))												#26 - struttura
			if self.DATA_LIST[self.rec_num].cont_per == None:
				unicode(self.lineEdit_codice_periodo.setText(""))
			else:
				unicode(self.lineEdit_codice_periodo.setText(self.DATA_LIST[self.rec_num].cont_per))										#27 - codice periodo
			#27 - codice periodo
			if self.DATA_LIST[self.rec_num].order_layer == None:
				self.lineEditOrderLayer.setText("")
			else:
				self.lineEditOrderLayer.setText(str(self.DATA_LIST[self.rec_num].order_layer))								#28 - order layer

		#gestione tool
			if self.toolButtonPreview.isChecked() == True:
				self.loadMapPreview()
			if self.toolButtonPreviewMedia.isChecked() == True:
				self.loadMediaPreview()
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#QMessageBox.warning(self, "Errore", str(self.comboBox_per_fin.currentText()),  QMessageBox.Ok)
		#TableWidget
		##Rapporti
		rapporti = self.table2dict("self.tableWidget_rapporti")
		##Inclusi
		inclusi = self.table2dict("self.tableWidget_inclusi")
		##Campioni
		campioni = self.table2dict("self.tableWidget_campioni")
		##Documentazione
		documentazione = self.table2dict("self.tableWidget_documentazione")

		if self.lineEditOrderLayer.text() == "":
			order_layer = None
		else:
			order_layer = self.lineEditOrderLayer.text()
		#data
		self.DATA_LIST_REC_TEMP = [
		unicode(self.comboBox_sito.currentText()), 						#1 - Sito
		unicode(self.comboBox_area.currentText()), 						#2 - Area
		unicode(self.lineEdit_us.text()),											#3 - US
		unicode(self.comboBox_def_strat.currentText()),					#4 - Definizione stratigrafica
		unicode(self.comboBox_def_intepret.currentText()),             #5 - Definizione intepretata
		unicode(self.textEdit_descrizione.toPlainText()),		#6 - descrizione
		unicode(self.textEdit_interpretazione.toPlainText()), #7 - interpretazione
		unicode(self.comboBox_per_iniz.currentText()),					#8 - periodo iniziale
		unicode(self.comboBox_fas_iniz.currentText()),					#9 - fase iniziale
		unicode(self.comboBox_per_fin.currentText()), 					#10 - periodo finale iniziale
		unicode(self.comboBox_fas_fin.currentText()), 					#11 - fase finale
		unicode(self.comboBox_scavato.currentText()),					#12 - scavato
		unicode(self.lineEdit_attivita.text()),                             		#13 - attivita
		unicode(self.lineEdit_anno.text()),                                 		#14 - anno scavo
		unicode(self.comboBox_metodo.currentText()), 					#15 - metodo
		unicode(inclusi),																#16 - inclusi
		unicode(campioni),															#17 - campioni
		unicode(rapporti),															#18 - rapporti
		unicode(self.lineEdit_data_schedatura.text()),						#19 - data schedatura
		unicode(self.comboBox_schedatore.currentText()),              #20 - schedatore
		unicode(self.comboBox_formazione.currentText()),              #21 - formazione
		unicode(self.comboBox_conservazione.currentText()),          #22 - conservazione
		unicode(self.comboBox_colore.currentText()),						#23 - colore
		unicode(self.comboBox_consistenza.currentText()),              #24 - consistenza
		unicode(self.lineEdit_struttura.text()),									#25 - struttura
		unicode(self.lineEdit_codice_periodo.text()),							#26 - codice periodo
		unicode(order_layer),														#27 - order layer era str(order_layer)
		unicode(documentazione)
		]

	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("unicode(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()
		#QMessageBox.warning(self, "Errore", str(self.DATA_LIST_REC_CORR) + str(self.DATA_LIST_REC_TEMP),  QMessageBox.Ok)
		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

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
			
	def setTableEnable(self, t, v):
		tab_names = t
		value = v

		for tn in tab_names:
			cmd = ('%s%s%s%s') % (tn, '.setEnabled(', v, ')')
			eval(cmd)

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()

## Class end
