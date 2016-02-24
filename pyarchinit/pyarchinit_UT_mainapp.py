#! /usr/bin/env python
#-*- coding: utf-8 -*-
"""
/**************************************************************************
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
from  pyarchinit_UT_ui import Ui_DialogUT
from  pyarchinit_UT_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  sortpanelmain import SortPanelMain

from delegateComboBox import *
from  pyarchinit_exp_UTsheet_pdf import *


class pyarchinit_UT(QDialog, Ui_DialogUT):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_version 0.4 - Scheda UT"
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
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'ut_table'
	MAPPER_TABLE_CLASS = "UT"
	NOME_SCHEDA = "Scheda UT"
	ID_TABLE = "id_ut"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE, 
	'Progetto' : 'progetto',
	'numero UT' : 'nr_ut',
	'UT letterale' : 'ut_letterale',
	'Definizione UT' : 'def_ut',
	'Descrizione UT' : 'descrizione_ut',
	'Interpretazione UT' : 'interpretazione_ut',
	'Nazione' : 'nazione',
	'Regione' : 'regione',
	'Provincia' : 'provincia',
	'Comune' : 'comune',
	'Frazione' : 'frazione',
	'Localita' : 'localita',
	'Indirizzo' : 'indirizzo',
	'Nr civico' : 'nr_civico',
	'Carta topografica IGM' : 'carta_topo_igm',
	'CaCTR' : 'carta_ctr',
	'Coord geografiche' : 'coord_geografiche',
	'Coord piane' : 'coord_piane',
	'Quota' : 'quota',
	'Andamento terreno pendenza' : 'andamento_terreno_pendenza',
	'Utilizzo suolo vegetazione' : 'utilizzo_suolo_vegetazione',
	'Descrizione empirica suolo' : 'descrizione_empirica_suolo',
	'Descrizione luogo' : 'descrizione_luogo',
	'Metodo rilievo e ricognizione' : 'metodo_rilievo_e_ricognizione',
	'Geometria' : 'geometria',
	'Bibliografia' : 'bibliografia',
	'Data' : 'data',
	'Ora meteo' : 'ora_meteo',
	'Responsabile' : 'responsabile',
	'Dimensioni UT' : 'dimensioni_ut',
	'Reperti per mq' : 'rep_per_mq',
	'Reperti datanti' : 'rep_datanti',
	'Periodo I' : 'periodo_I',
	'Datazione_I' : 'datazione_I',
	'Interpretazione I' : 'interpretazione_I',
	'Periodo II' : 'periodo_II',
	'Datazione II' : 'datazione_II',
	'Interpretazione II' : 'interpretazione_II',
	'Documentazione' : 'documentazione',
	'Enti tutela_vincoli' : 'enti_tutela_vincoli',
	'Indagini preliminari' : 'indagini_preliminari'
	}
	SORT_ITEMS = [
				ID_TABLE,
				'Progetto',
				'numero UT',
				'UT letterale',
				'Definizione UT',
				'Descrizione UT',
				'Interpretazione UT',
				'Nazione',
				'Regione',
				'Provincia',
				'Comune',
				'Frazione',
				'Localita',
				'Indirizzo',
				'Nr civico',
				'Carta topografica IGM',
				'CaCTR',
				'Coord geografiche',
				'Coord piane',
				'Quota',
				'Andamento terreno pendenza',
				'Utilizzo suolo vegetazione',
				'Descrizione empirica suolo',
				'Descrizione luogo',
				'Metodo rilievo e ricognizione',
				'Geometria',
				'Bibliografia',
				'Data',
				'Ora meteo',
				'Responsabile',
				'Dimensioni UT',
				'Reperti per mq',
				'Reperti datanti',
				'Periodo I',
				'Datazione_I',
				'Interpretazione I',
				'Periodo II',
				'Datazione II',
				'Interpretazione II',
				'Documentazione',
				'Enti tutela_vincoli',
				'Indagini preliminari'
				]

	TABLE_FIELDS = [
				'progetto',
				'nr_ut',
				'ut_letterale',
				'def_ut',
				'descrizione_ut',
				'interpretazione_ut',
				'nazione',
				'regione',
				'provincia',
				'comune',
				'frazione',
				'localita',
				'indirizzo',
				'nr_civico',
				'carta_topo_igm',
				'carta_ctr',
				'coord_geografiche',
				'coord_piane',
				'quota',
				'andamento_terreno_pendenza',
				'utilizzo_suolo_vegetazione',
				'descrizione_empirica_suolo',
				'descrizione_luogo',
				'metodo_rilievo_e_ricognizione',
				'geometria',
				'bibliografia',
				'data',
				'ora_meteo',
				'responsabile',
				'dimensioni_ut',
				'rep_per_mq',
				'rep_datanti',
				'periodo_I',
				'datazione_I',
				'interpretazione_I',
				'periodo_II',
				'datazione_II',
				'interpretazione_II',
				'documentazione',
				'enti_tutela_vincoli',
				'indagini_preliminari'
				]

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
		
		self.pushButton_insert_row_documentazione.setEnabled(n)
		self.pushButton_remove_row_documentazione.setEnabled(n)

		self.pushButton_insert_row_bibliografia.setEnabled(n)
		self.pushButton_remove_row_bibliografia.setEnabled(n)
		
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
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" + str(e) ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)


	def customize_GUI(self):
		self.tableWidget_bibliografia.setColumnWidth(0,380)

		self.tableWidget_documentazione.setColumnWidth(0,150)
		self.tableWidget_documentazione.setColumnWidth(1,300)

		"""
		valuesDoc = ["Fotografie", "Diapositive", "Sezioni", "Planimetrie", "Prospetti", "Video", "Fotopiano"]
		self.delegateDoc = ComboBoxDelegate()
		self.delegateDoc.def_values(valuesDoc)
		self.delegateDoc.def_editable('False')
		self.tableWidget_documentazione.setItemDelegateForColumn(0,self.delegateDoc)
		"""


	def charge_list(self):
		
		"""
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)
		
		"""

		regioni_list = ['Abruzzo','Basilicata','Calabria','Campania','Emilia-Romagna','Friuli Venezia Giulia','Lazio','Liguria','Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino Alto Adige','Umbria','Valle d\'Aosta','Veneto']
		self.comboBox_regione.addItems(regioni_list)

		province_list = ['Agrigento', 'Alessandria', 'Ancona', 'Aosta', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Basilicata', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano', 'Brescia', 'Brindisi', 'Cagliari', 'Calabria', 'Caltanissetta', 'Campania', 'Campobasso', 'Carbonia-Iglesias', 'Caserta', 'Catania', 'Catanzaro', 'Chieti', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Emilia-Romagna', 'Enna', 'Fermo', 'Ferrara', 'Firenze', 'Foggia', "Forl'-Cesena", 'Frosinone', 'Genova', 'Gorizia', 'Grosseto', 'Imperia', 'Isernia', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca', 'Macerata', 'Mantova', 'Massa e Carrara', 'Matera', 'Medio Campidano', 'Messina', 'Milano', 'Modena', 'Monza e Brianza', 'Napoli', 'Novara', 'Nuoro', 'Ogliastra', 'Olbia-Tempio', 'Oristano', 'Padova', 'Palermo', 'Parma', 'Pavia', 'Perugia', 'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Pordenone', 'Potenza', 'Prato', 'Ragusa', 'Ravenna', 'Reggio Calabria', 'Reggio Emilia', 'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena', 'Siracusa', 'Sondrio', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trapani', 'Trento', 'Treviso', 'Trieste', 'Udine', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo']

		self.comboBox_provincia.addItems(province_list)


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
			
			self.setComboBoxEditable(["self.comboBox_progetto"],1)
			self.setComboBoxEditable(["self.comboBox_nr_ut"],1)
			self.setComboBoxEnable(["self.comboBox_progetto"],"True")
			self.setComboBoxEnable(["self.comboBox_nr_ut"],"True")
			self.setComboBoxEnable(["self.lineEdit_ut_letterale"],"True")
			###
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
					self.label_sort.setText(self.SORTED_ITEMS["n"])
					self.charge_list()
					self.charge_records()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)

					self.setComboBoxEditable(["self.comboBox_progetto"],1)
					self.setComboBoxEditable(["self.comboBox_nr_ut"],1)
					self.setComboBoxEnable(["self.comboBox_progetto"],"False")
					self.setComboBoxEnable(["self.comboBox_nr_ut"],"False")
					self.setComboBoxEnable(["self.lineEdit_ut_letterale"],"False")
					self.fill_fields(self.REC_CORR)
					self.enable_button(1)
				else:
					pass


	def data_error_check(self):
		test = 0
		EC = Error_check()

		if EC.data_is_empty(str(self.comboBox_progetto.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Progetto. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		if EC.data_is_empty(str(self.comboBox_nr_ut.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo UT. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		nr_ut = self.comboBox_nr_ut.currentText()

		if nr_ut != "":
			if EC.data_is_int(nr_ut) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Nr UT. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test

	def insert_new_rec(self):
		if self.lineEdit_quota.text() == "":
			quota = None
		else:
			quota = float(self.lineEdit_quota.text())
	
		##Documentazione
		documentazione = self.table2dict("self.tableWidget_documentazione")
		##Bibliografia
		bibliografia = self.table2dict("self.tableWidget_bibliografia")
		try:
			data = self.DB_MANAGER.insert_ut_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.comboBox_progetto.currentText()),
			int(self.comboBox_nr_ut.currentText()),
			str(self.lineEdit_ut_letterale.text()),
			str(self.lineEdit_def_ut.text()),
			unicode(self.textEdit_descrizione_ut.toPlainText()),
			unicode(self.textEdit_interpretazione_ut.toPlainText()),
			str(self.comboBox_nazione.currentText()),
			str(self.comboBox_regione.currentText()),
			str(self.comboBox_provincia.currentText()),
			str(self.comboBox_comune.currentText()),
			str(self.comboBox_frazione.currentText()),
			str(self.comboBox_localita.currentText()),
			str(self.lineEdit_indirizzo.text()),
			str(self.lineEdit_nr_civico.text()),
			str(self.lineEdit_carta_topo_igm.text()),
			str(self.lineEdit_carta_ctr.text()),
			str(self.lineEdit_coord_geografiche.text()),
			str(self.lineEdit_coord_piane.text()),
			quota,
			str(self.lineEdit_andamento_terreno_pendenza.text()),
			str(self.lineEdit_utilizzo_suolo_vegetazione.text()),
			str(self.textEdit_descrizione_empirica_suolo.toPlainText()),
			str(self.textEdit_descrizione_luogo.toPlainText()),
			str(self.lineEdit_metodo_rilievo_e_ricognizione.text()),
			str(self.lineEdit_geometria.text()),
			str(bibliografia),
			str(self.lineEdit_data.text()),
			str(self.lineEdit_ora_meteo.text()),
			str(self.lineEdit_responsabile.text()),
			str(self.lineEdit_dimensioni_ut.text()),
			str(self.lineEdit_rep_per_mq.text()),
			str(self.lineEdit_rep_datanti.text()),
			str(self.lineEdit_periodo_I.text()),
			str(self.lineEdit_datazione_I.text()),
			str(self.lineEdit_interpretazione_I.text()),
			str(self.lineEdit_periodo_II.text()),
			str(self.lineEdit_datazione_II.text()),
			str(self.lineEdit_interpretazione_II.text()),
			str(documentazione),
			str(self.lineEdit_enti_tutela_vincoli.text()),
			str(self.lineEdit_indagini_preliminari.text()))
			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Attenzione 1 ! \n"+ str(msg),  QMessageBox.Ok)
				return 0
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Attenzione 2 ! \n"+str(e),  QMessageBox.Ok)
			return 0
			
	def check_record_state(self):
		ec = self.data_error_check()
		if ec == 1:
			return 1 #ci sono errori di immissione
		elif self.records_equal_check() == 1 and ec == 0:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
			self.charge_records()
			return 0 #non ci sono errori di immissione
	
			
	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)
	def remove_row(self, table_name):
		"""remove row into a table based on table_name"""
		cmd = table_name+".removeRow(0)"
		eval(cmd)
		
	def on_pushButton_insert_row_documentazione_pressed(self):
		self.insert_new_row('self.tableWidget_documentazione')
	def on_pushButton_remove_row_documentazione_pressed(self):
		self.remove_row('self.tableWidget_documentazione')

	def on_pushButton_insert_row_bibliografia_pressed(self):
		self.insert_new_row('self.tableWidget_bibliografia')
	def on_pushButton_remove_row_bibliografia_pressed(self):
		self.remove_row('self.tableWidget_bibliografia')



	def on_pushButton_view_all_pressed(self):
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


	#records surf functions
	def on_pushButton_first_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.fill_fields(0)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_last_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
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
		if self.check_record_state() == 1:
			pass
		else:
			self.enable_button_search(0)


			#set the GUI for a new search
			if self.BROWSE_STATUS != "f":
				self.BROWSE_STATUS = "f"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.empty_fields()
				self.set_rec_counter('','')
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.setComboBoxEditable(["self.comboBox_progetto"],1)
				self.setComboBoxEditable(["self.comboBox_nr_ut"],1)
				self.setComboBoxEnable(["self.comboBox_progetto"],"True")
				self.setComboBoxEnable(["self.comboBox_nr_ut"],"True")
				self.setComboBoxEnable(["self.lineEdit_ut_letterale"],"True")

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			if self.comboBox_nr_ut.currentText() != "":
				nr_ut = int(self.comboBox_nr_ut.currentText())
			else:
				nr_ut = None

			if self.comboBox_nr_ut.currentText() != "":
				nr_ut = float(self.comboBox_nr_ut.currentText())
			else:
				nr_ut = None

			if self.lineEdit_quota.text() != "":
				quota = float(self.lineEdit_quota.text())
			else:
				quota = None

			search_dict = {
			self.TABLE_FIELDS[0]  : "'"+str(self.comboBox_progetto.currentText())+"'", 									#1 - Sito
			self.TABLE_FIELDS[1]  : nr_ut,																								#2 - Area
			self.TABLE_FIELDS[2]  : "'"+str(self.lineEdit_ut_letterale.text())+"'",												#3 - US
			self.TABLE_FIELDS[3]  : "'"+str(self.lineEdit_def_ut.text())+"'",													#6 - descrizione
			self.TABLE_FIELDS[6]  : "'"+str(self.comboBox_nazione.currentText())+"'",
			self.TABLE_FIELDS[7]  : "'"+str(self.comboBox_regione.currentText())+"'",									#7 - interpretazione
			self.TABLE_FIELDS[8]  : "'"+str(self.comboBox_provincia.currentText())+"'",									#8 - periodo iniziale
			self.TABLE_FIELDS[9]  : "'"+str(self.comboBox_comune.currentText())+"'",									#9 - fase iniziale
			self.TABLE_FIELDS[10]  : "'"+str(self.comboBox_frazione.currentText())+"'",	 								#10 - periodo finale iniziale
			self.TABLE_FIELDS[11] : "'"+str(self.comboBox_localita.currentText())+"'", 									#11 - fase finale
			self.TABLE_FIELDS[12] : "'"+str(self.lineEdit_indirizzo.text())+"'",													#12 - attivita  
			self.TABLE_FIELDS[13] : "'"+str(self.lineEdit_nr_civico.text())+"'",												#13 - attivita  
			self.TABLE_FIELDS[14] : "'"+str(self.lineEdit_carta_topo_igm.text())+"'", 										#15 - metodo
			self.TABLE_FIELDS[15] : "'"+str(self.lineEdit_carta_ctr.text())+"'",												#16 - data schedatura
			self.TABLE_FIELDS[16] : "'"+str(self.lineEdit_coord_geografiche.text())+"'",									#17 - schedatore
			self.TABLE_FIELDS[17] : "'"+str(self.lineEdit_coord_piane.text())+"'",											#18 - formazione
			self.TABLE_FIELDS[18] : quota,																								#19 - conservazione
			self.TABLE_FIELDS[19] : "'"+str(self.lineEdit_andamento_terreno_pendenza.text())+"'",					#20 - colore
			self.TABLE_FIELDS[20] : "'"+str(self.lineEdit_utilizzo_suolo_vegetazione.text())+"'",							#21 - consistenza	
			self.TABLE_FIELDS[23] : "'"+str(self.lineEdit_metodo_rilievo_e_ricognizione.text())+"'",						#23 - codice_periodo
			self.TABLE_FIELDS[24] : "'"+str(self.lineEdit_geometria.text())+"'",
			self.TABLE_FIELDS[26] : "'"+str(self.lineEdit_data.text())+"'",
			self.TABLE_FIELDS[27] : "'"+str(self.lineEdit_ora_meteo.text())+"'",
			self.TABLE_FIELDS[28] : "'"+str(self.lineEdit_responsabile.text())+"'",
			self.TABLE_FIELDS[29] : "'"+str(self.lineEdit_dimensioni_ut.text())+"'",
			self.TABLE_FIELDS[30] : "'"+str(self.lineEdit_rep_per_mq.text())+"'",
			self.TABLE_FIELDS[31] : "'"+str(self.lineEdit_rep_datanti.text())+"'",
			self.TABLE_FIELDS[32] : "'"+str(self.lineEdit_periodo_I.text())+"'",
			self.TABLE_FIELDS[33] : "'"+str(self.lineEdit_datazione_I.text())+"'",
			self.TABLE_FIELDS[34] : "'"+str(self.lineEdit_interpretazione_I.text())+"'",
			self.TABLE_FIELDS[35] : "'"+str(self.lineEdit_periodo_II.text())+"'",
			self.TABLE_FIELDS[36] : "'"+str(self.lineEdit_datazione_II.text())+"'",
			self.TABLE_FIELDS[37] : "'"+str(self.lineEdit_interpretazione_II.text())+"'",
			self.TABLE_FIELDS[39] : "'"+str(self.lineEdit_enti_tutela_vincoli.text())+"'",
			self.TABLE_FIELDS[40] : "'"+str(self.lineEdit_indagini_preliminari.text())+"'"								#24 - codice_periodo
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(search_dict) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
				else:
					res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)


					if bool(res) == False:
						QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

						self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
						self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
						self.fill_fields(self.REC_CORR)
						self.BROWSE_STATUS = "b"
						self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

						self.setComboBoxEnable(["self.comboBox_progetto"],"False")
						self.setComboBoxEnable(["self.comboBox_nr_ut"],"False")
						self.setComboBoxEnable(["self.lineEdit_ut_letterale"],"False")

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

						self.setComboBoxEnable(["self.comboBox_progetto"],"False")
						self.setComboBoxEnable(["self.comboBox_nr_ut"],"False")
						self.setComboBoxEnable(["self.lineEdit_ut_letterale"],"False")

						QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)

		self.enable_button_search(1)

	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			self.update_record()
			id_list = []
			for i in self.DATA_LIST:
				id_list.append(eval("i."+ self.ID_TABLE))
			self.DATA_LIST = []
			if self.SORT_STATUS == "n":
				temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
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

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())


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


	def table2dict(self, n):
		self.tablename = n
		row = eval(self.tablename+".rowCount()")
		col = eval(self.tablename+".columnCount()")
		lista=[]
		for r in range(row):
			sub_list = []
			for c in range(col):
				value = eval(self.tablename+".item(r,c)")
				if bool(value) == True:
					sub_list.append(str(value.text()))
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
				item = QTableWidgetItem(self.data_list[row][col])
				exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
				eval(exec_str)

	def empty_fields(self):
		documentazione_row_count = self.tableWidget_documentazione.rowCount()
		bibliografia_row_count = self.tableWidget_bibliografia.rowCount()

		self.comboBox_progetto.setEditText("")
		self.comboBox_nr_ut.setEditText("")
		self.lineEdit_ut_letterale.clear()
		self.lineEdit_def_ut.clear()
		self.textEdit_descrizione_ut.clear()
		self.textEdit_interpretazione_ut.clear()
		self.comboBox_nazione.setEditText("")
		self.comboBox_regione.setEditText("")
		self.comboBox_provincia.setEditText("")
		self.comboBox_comune.setEditText("")
		self.comboBox_frazione.setEditText("")
		self.comboBox_localita.setEditText("")
		self.lineEdit_indirizzo.clear()
		self.lineEdit_nr_civico.clear()
		self.lineEdit_carta_topo_igm.clear()
		self.lineEdit_carta_ctr.clear()
		self.lineEdit_coord_geografiche.clear()
		self.lineEdit_coord_piane.clear()
		self.lineEdit_quota.clear()
		self.lineEdit_andamento_terreno_pendenza.clear()
		self.lineEdit_utilizzo_suolo_vegetazione.clear()
		self.textEdit_descrizione_empirica_suolo.clear()
		self.textEdit_descrizione_luogo.clear()
		self.lineEdit_metodo_rilievo_e_ricognizione.clear()
		self.lineEdit_geometria.clear()
		for i in range(documentazione_row_count):
			self.tableWidget_documentazione.removeRow(0)
		for i in range(bibliografia_row_count):
			self.tableWidget_bibliografia.removeRow(0)
		self.lineEdit_data.clear()
		self.lineEdit_ora_meteo.clear()
		self.lineEdit_responsabile.clear()
		self.lineEdit_dimensioni_ut.clear()
		self.lineEdit_rep_per_mq.clear()
		self.lineEdit_rep_datanti.clear()
		self.lineEdit_periodo_I.clear()
		self.lineEdit_datazione_I.clear()
		self.lineEdit_interpretazione_I.clear()
		self.lineEdit_periodo_II.clear()
		self.lineEdit_datazione_II.clear()
		self.lineEdit_interpretazione_II.clear()
		self.lineEdit_enti_tutela_vincoli.clear()
		self.lineEdit_indagini_preliminari.clear()

	def fill_fields(self, n=0):
		self.rec_num = n
		
		try:
			if self.DATA_LIST[self.rec_num].quota == None:
				self.lineEdit_quota.setText("")
			else:
				self.lineEdit_quota.setText(str(self.DATA_LIST[self.rec_num].quota))

			self.comboBox_progetto.setEditText(self.DATA_LIST[self.rec_num].progetto)
			self.comboBox_nr_ut.setEditText(str(self.DATA_LIST[self.rec_num].nr_ut))
			self.lineEdit_ut_letterale.setText(self.DATA_LIST[self.rec_num].ut_letterale)
			self.lineEdit_def_ut.setText(self.DATA_LIST[self.rec_num].def_ut)
			unicode(self.textEdit_descrizione_ut.setText(self.DATA_LIST[self.rec_num].descrizione_ut))
			unicode(self.textEdit_interpretazione_ut.setText(self.DATA_LIST[self.rec_num].interpretazione_ut))
			self.comboBox_nazione.setEditText(self.DATA_LIST[self.rec_num].nazione)
			self.comboBox_regione.setEditText(self.DATA_LIST[self.rec_num].regione)
			self.comboBox_provincia.setEditText(self.DATA_LIST[self.rec_num].provincia)
			self.comboBox_comune.setEditText(self.DATA_LIST[self.rec_num].comune)
			self.comboBox_frazione.setEditText(self.DATA_LIST[self.rec_num].frazione)
			self.comboBox_localita.setEditText(self.DATA_LIST[self.rec_num].localita)
			self.lineEdit_indirizzo.setText(self.DATA_LIST[self.rec_num].indirizzo)
			self.lineEdit_nr_civico.setText(self.DATA_LIST[self.rec_num].nr_civico)
			self.lineEdit_carta_topo_igm.setText(self.DATA_LIST[self.rec_num].carta_topo_igm)
			self.lineEdit_carta_ctr.setText(self.DATA_LIST[self.rec_num].carta_ctr)
			self.lineEdit_coord_geografiche.setText(self.DATA_LIST[self.rec_num].coord_geografiche)
			self.lineEdit_coord_piane.setText(self.DATA_LIST[self.rec_num].coord_piane)
			self.lineEdit_andamento_terreno_pendenza.setText(self.DATA_LIST[self.rec_num].andamento_terreno_pendenza)
			self.lineEdit_utilizzo_suolo_vegetazione.setText(self.DATA_LIST[self.rec_num].utilizzo_suolo_vegetazione)
			unicode(self.textEdit_descrizione_empirica_suolo.setText(self.DATA_LIST[self.rec_num].descrizione_empirica_suolo))
			unicode(self.textEdit_descrizione_luogo.setText(self.DATA_LIST[self.rec_num].descrizione_luogo))
			self.lineEdit_metodo_rilievo_e_ricognizione.setText(self.DATA_LIST[self.rec_num].metodo_rilievo_e_ricognizione)
			self.lineEdit_geometria.setText(self.DATA_LIST[self.rec_num].geometria)
			self.tableInsertData("self.tableWidget_documentazione",self.DATA_LIST[self.rec_num].documentazione)	#19 - rapporti
			self.tableInsertData("self.tableWidget_bibliografia",self.DATA_LIST[self.rec_num].bibliografia)	#19 - rapporti
			self.lineEdit_data.setText(self.DATA_LIST[self.rec_num].data)
			self.lineEdit_ora_meteo.setText(self.DATA_LIST[self.rec_num].ora_meteo)
			self.lineEdit_responsabile.setText(self.DATA_LIST[self.rec_num].responsabile)
			self.lineEdit_dimensioni_ut.setText(self.DATA_LIST[self.rec_num].dimensioni_ut)
			self.lineEdit_rep_per_mq.setText(self.DATA_LIST[self.rec_num].rep_per_mq)
			self.lineEdit_rep_datanti.setText(self.DATA_LIST[self.rec_num].rep_datanti)
			self.lineEdit_periodo_I.setText(self.DATA_LIST[self.rec_num].periodo_I)
			self.lineEdit_datazione_I.setText(self.DATA_LIST[self.rec_num].datazione_I)
			self.lineEdit_interpretazione_I.setText(self.DATA_LIST[self.rec_num].interpretazione_I)
			self.lineEdit_periodo_II.setText(self.DATA_LIST[self.rec_num].periodo_II)
			self.lineEdit_datazione_II.setText(self.DATA_LIST[self.rec_num].datazione_II)
			self.lineEdit_interpretazione_II.setText(self.DATA_LIST[self.rec_num].interpretazione_II)
			self.lineEdit_enti_tutela_vincoli.setText(self.DATA_LIST[self.rec_num].enti_tutela_vincoli)
			self.lineEdit_indagini_preliminari.setText(self.DATA_LIST[self.rec_num].indagini_preliminari)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		
		##quota
		if self.lineEdit_quota.text() == "":
			quota = None
		else:
			quota =  self.lineEdit_quota.text()

		documentazione = self.table2dict("self.tableWidget_documentazione")
		bibliografia = self.table2dict("self.tableWidget_bibliografia")
		
		#data
		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_progetto.currentText()),
		str(self.comboBox_nr_ut.currentText()),
		str(self.lineEdit_ut_letterale.text()),
		str(self.lineEdit_def_ut.text()),
		str(self.textEdit_descrizione_ut.toPlainText()),
		str(self.textEdit_interpretazione_ut.toPlainText()),
		str(self.comboBox_nazione.currentText()),
		str(self.comboBox_regione.currentText()),
		str(self.comboBox_provincia.currentText()),
		str(self.comboBox_comune.currentText()),
		str(self.comboBox_frazione.currentText()),
		str(self.comboBox_localita.currentText()),
		str(self.lineEdit_indirizzo.text()),
		str(self.lineEdit_nr_civico.text()),
		str(self.lineEdit_carta_topo_igm.text()),
		str(self.lineEdit_carta_ctr.text()),
		str(self.lineEdit_coord_geografiche.text()),
		str(self.lineEdit_coord_piane.text()),
		str(quota),
		str(self.lineEdit_andamento_terreno_pendenza.text()),
		str(self.lineEdit_utilizzo_suolo_vegetazione.text()),
		str(self.textEdit_descrizione_empirica_suolo.toPlainText()),
		str(self.textEdit_descrizione_luogo.toPlainText()),
		str(self.lineEdit_metodo_rilievo_e_ricognizione.text()),
		str(self.lineEdit_geometria.text()),
		str(bibliografia),
		str(self.lineEdit_data.text()),
		str(self.lineEdit_ora_meteo.text()),
		str(self.lineEdit_responsabile.text()),
		str(self.lineEdit_dimensioni_ut.text()),
		str(self.lineEdit_rep_per_mq.text()),
		str(self.lineEdit_rep_datanti.text()),
		str(self.lineEdit_periodo_I.text()),
		str(self.lineEdit_datazione_I.text()),
		str(self.lineEdit_interpretazione_I.text()),
		str(self.lineEdit_periodo_II.text()),
		str(self.lineEdit_datazione_II.text()),
		str(self.lineEdit_interpretazione_II.text()),
		str(documentazione),
		str(self.lineEdit_enti_tutela_vincoli.text()),
		str(self.lineEdit_indagini_preliminari.text())] 					#4 - provincia


	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))
		##self.testing('/testrecorr.txt',str(self.DATA_LIST_REC_CORR))
	

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

	def setComboBoxEditable(self, f, n):
		field_names = f
		value = n

		for fn in field_names:
			cmd = ('%s%s%d%s') % (fn, '.setEditable(', n, ')')
			eval(cmd)


	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		#self.testing('/testup.txt',str(self.DATA_LIST_REC_TEMP))
		#self.testing('/testup2.txt',str(rec_to_update))
		return rec_to_update

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def on_pushButton_pdf_exp_pressed(self):
		UT_pdf_sheet = generate_pdf()
		data_list = self.generate_list_pdf()
		UT_pdf_sheet.build_UT_sheets(data_list)

	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].progetto), 								#1 - Sito
			str(self.DATA_LIST[i].nr_ut),									#2 - Area
			str(self.DATA_LIST[i].ut_letterale),										#3 - US
			str(self.DATA_LIST[i].def_ut),							#4 - Definizione stratigrafica
			str(self.DATA_LIST[i].descrizione_ut),						#5 - Definizione intepretata
			str(self.DATA_LIST[i].interpretazione_ut),									#6 - descrizione
			str(self.DATA_LIST[i].nazione),								#7 - interpretazione
			str(self.DATA_LIST[i].regione),									#8 - periodo iniziale
			str(self.DATA_LIST[i].provincia),							#9 - fase iniziale
			str(self.DATA_LIST[i].comune),								#10 - periodo finale iniziale
			str(self.DATA_LIST[i].frazione), 							#11 - fase finale
			str(self.DATA_LIST[i].localita),									#12 - scavato
			str(self.DATA_LIST[i].indirizzo),								#13 - attivita
			str(self.DATA_LIST[i].nr_civico),								#14 - anno scavo
			str(self.DATA_LIST[i].carta_topo_igm),							#15 - metodo
			str(self.DATA_LIST[i].carta_ctr),									#16 - inclusi
			str(self.DATA_LIST[i].coord_geografiche),								#17 - campioni
			str(self.DATA_LIST[i].coord_piane),								#18 - rapporti
			str(self.DATA_LIST[i].quota),							#19 - data schedatura
			str(self.DATA_LIST[i].andamento_terreno_pendenza),								#20 - schedatore
			str(self.DATA_LIST[i].utilizzo_suolo_vegetazione),								#21 - formazione
			str(self.DATA_LIST[i].descrizione_empirica_suolo),					#22 - conservazione
			str(self.DATA_LIST[i].descrizione_luogo),									#23 - colore
			str(self.DATA_LIST[i].metodo_rilievo_e_ricognizione),								#24 - consistenza
			str(self.DATA_LIST[i].geometria),								#25 - struttura
			str(self.DATA_LIST[i].bibliografia),								#25 - struttura
			str(self.DATA_LIST[i].data),							#29 - piante
			str(self.DATA_LIST[i].ora_meteo), 							#11 - fase finale
			str(self.DATA_LIST[i].responsabile),									#12 - scavato
			str(self.DATA_LIST[i].dimensioni_ut),								#13 - attivita
			str(self.DATA_LIST[i].rep_per_mq),								#14 - anno scavo
			str(self.DATA_LIST[i].rep_datanti),							#15 - metodo
			str(self.DATA_LIST[i].periodo_I),									#16 - inclusi
			str(self.DATA_LIST[i].datazione_I),								#17 - campioni
			str(self.DATA_LIST[i].interpretazione_I),								#18 - rapporti
			str(self.DATA_LIST[i].periodo_II),							#19 - data schedatura
			str(self.DATA_LIST[i].datazione_II),								#20 - schedatore
			str(self.DATA_LIST[i].interpretazione_II),								#21 - formazione
			str(self.DATA_LIST[i].documentazione),								#21 - formazione
			str(self.DATA_LIST[i].enti_tutela_vincoli),					#22 - conservazione
			str(self.DATA_LIST[i].indagini_preliminari)									#23 -
		])
		return data_list


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
