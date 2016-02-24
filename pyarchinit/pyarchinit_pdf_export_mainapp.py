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
#from PyQt4 import QtCore, QtGui
import sys, os

from pyarchinit_pdf_exp_ui import Ui_Dialog_pdf_exp
from pyarchinit_pdf_exp_ui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from  pyarchinit_utility import *
from  pyarchinit_db_manager import *
from  pyarchinit_OS_utility import pyarchinit_OS_Utility

from  pyarchinit_exp_USsheet_pdf import *
from  pyarchinit_exp_Periodizzazionesheet_pdf import *
from  pyarchinit_exp_Strutturasheet_pdf import *
from  pyarchinit_exp_Findssheet_pdf import *
from  pyarchinit_exp_Tafonomiasheet_pdf import *
from  pyarchinit_exp_Individui_pdf import *

import os
import platform
import subprocess

class pyarchinit_pdf_export(QDialog, Ui_Dialog_pdf_exp):
	UTILITY = Utility()
	OS_UTILITY = pyarchinit_OS_Utility()
	DB_MANAGER = ""
	HOME = ""
	DATA_LIST = []

##	if os.name == 'posix':
##		HOME = os.environ['HOME']
##	elif os.name == 'nt':
##		HOME = os.environ['HOMEPATH']
##
##	PARAMS_DICT={'SERVER':'',
##				'HOST': '',
##				'DATABASE':'',
##				'PASSWORD':'',
##				'PORT':'',
##				'USER':'',
##				'THUMB_PATH':''}


	def __init__(self, parent=None, db=None):
		QDialog.__init__(self, parent)
		# Set up the user interface from Designer.
		self.setupUi(self)

		try:
			self.connect()
		except:
			pass
		self.charge_list()
		self.set_home_path()
		#self.load_dict()
		#self.charge_data()

	def connect(self):
		QMessageBox.warning(self, "Alert", "Sistema sperimentale. Esporta le schede PDF in /vostro_utente/pyarchinit_DB_folder. Sostituisce i documenti gia' presenti. Se volete conservarli fatene una copia o rinominateli." ,  QMessageBox.Ok)
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> %s. E' NECESSARIO RIAVVIARE QGIS" % (str(e)),  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "Attenzione rilevato bug! Segnalarlo allo sviluppatore<br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def charge_list(self):
		#lista sito
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		self.comboBox_sito.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def set_home_path(self):
		if os.name == 'posix':
			self.HOME = os.environ['HOME']
		elif os.name == 'nt':
			self.HOME = os.environ['HOMEPATH']

	def on_pushButton_open_dir_pressed(self):
		path = ('%s%s%s') % (self.HOME, os.sep, "pyarchinit_PDF_folder")

		if platform.system() == "Windows":
			os.startfile(path)
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path])
		else:
			subprocess.Popen(["xdg-open", path])

	def on_pushButton_exp_pdf_pressed(self):
		sito = str(self.comboBox_sito.currentText())

		####Esportazione della Scheda e indice US
		if self.checkBox_US.isChecked() == True:

			us_res = self.db_search_DB('US','sito', sito)

			if bool(us_res) == True:
				id_list = []
				for i in range(len(us_res)):
					id_list.append(us_res[i].id_us)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['area', 'us'], 'asc', 'US', 'id_us')
				for i in temp_data_list:
					self.DATA_LIST.append(i)

				if len(self.DATA_LIST) < 1:
					QMessageBox.warning(self, "Alert", "Attenzione non vi sono schede da stampare",  QMessageBox.Ok)
				else:
					US_pdf_sheet = generate_US_pdf()
					data_list = self.generate_list_US_pdf()
					US_pdf_sheet.build_US_sheets(self.DATA_LIST)									#export sheet
					US_pdf_sheet.build_index_US(self.DATA_LIST, self.DATA_LIST[0][0])		#export list

			self.DATA_LIST = []

		####Esportazione della Scheda e indice Periodizzazione
		if self.checkBox_periodo.isChecked() == True:
			
			periodizzazione_res = self.db_search_DB('PERIODIZZAZIONE','sito', sito)

			if bool(periodizzazione_res) == True:
				id_list = []
				for i in range(len(periodizzazione_res)):
					id_list.append(periodizzazione_res[i].id_perfas)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['cont_per'], 'asc', 'PERIODIZZAZIONE', 'id_perfas')

				for i in temp_data_list:
					self.DATA_LIST.append(i)
			
				Periodizzazione_pdf_sheet = generate_Periodizzazione_pdf() #deve essere importata la classe
				data_list = self.generate_list_periodizzazione_pdf() #deve essere aggiunta la funzione
				Periodizzazione_pdf_sheet.build_Periodizzazione_sheets(self.DATA_LIST) #deve essere aggiunto il file per generare i pdf
				Periodizzazione_pdf_sheet.build_index_Periodizzazione(self.DATA_LIST, self.DATA_LIST[0][0]) #deve essere aggiunto il file per generare i pdf

			self.DATA_LIST = []

		####Esportazione della Scheda e indice Struttura
		if self.checkBox_struttura.isChecked() == True:
			struttura_res = self.db_search_DB('STRUTTURA','sito', sito)

			if bool(struttura_res) == True:
				id_list = []
				for i in range(len(struttura_res)):
					id_list.append(struttura_res[i].id_struttura)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['sigla_struttura', 'numero_struttura'], 'asc', 'STRUTTURA', 'id_struttura')

				for i in temp_data_list:
					self.DATA_LIST.append(i)

				Struttura_pdf_sheet = generate_struttura_pdf() #deve essere importata la classe
				data_list = self.generate_list_struttura_pdf() #deve essere aggiunta la funzione
				Struttura_pdf_sheet.build_Struttura_sheets(self.DATA_LIST) #deve essere aggiunto il file per generare i pdf
				Struttura_pdf_sheet.build_index_Struttura(self.DATA_LIST, self.DATA_LIST[0][0])

			self.DATA_LIST = []

		if self.checkBox_reperti.isChecked() == True:
			reperti_res = self.db_search_DB('INVENTARIO_MATERIALI','sito', sito)

			if bool(reperti_res) == True:
				id_list = []
				for i in range(len(reperti_res)):
					id_list.append(reperti_res[i].id_invmat)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['numero_inventario'], 'asc', 'INVENTARIO_MATERIALI', 'id_invmat')

				for i in temp_data_list:
					self.DATA_LIST.append(i)

				Finds_pdf_sheet = generate_reperti_pdf()
				data_list = self.generate_list_reperti_pdf()
				Finds_pdf_sheet.build_Finds_sheets(self.DATA_LIST)
				Finds_pdf_sheet.build_index_Finds(self.DATA_LIST, self.DATA_LIST[0][1])

			self.DATA_LIST = []

		if self.checkBox_tafonomia.isChecked() == True:
			tafonomia_res = self.db_search_DB('TAFONOMIA','sito', sito)

			if bool(tafonomia_res) == True:
				id_list = []
				for i in range(len(tafonomia_res)):
					id_list.append(tafonomia_res[i].id_tafonomia)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['nr_scheda_taf'], 'asc', 'TAFONOMIA', 'id_tafonomia')

				for i in temp_data_list:
					self.DATA_LIST.append(i)

				Tafonomia_pdf_sheet = generate_tafonomia_pdf() 
				data_list = self.generate_list_pdf() 
				Tafonomia_pdf_sheet.build_Tafonomia_sheets(self.DATA_LIST)
				Tafonomia_pdf_sheet.build_index_Tafonomia(self.DATA_LIST, self.DATA_LIST[0][0])

			self.DATA_LIST = []

##		if self.checkBox_individui.isChecked() == True:
##			individui_res = self.db_search_DB('SCHEDAIND','sito', sito)
##
##			if bool(individui_res) == True:
##				id_list = []
##				for i in range(len(individui_res)):
##					id_list.append(individui_res[i].id_scheda_ind)
##
##				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['nr_individuo'], 'asc', 'SCHEDAIND', 'id_scheda_ind')
##
##				for i in temp_data_list:
##					self.DATA_LIST.append(i)
##
##				Individui_pdf_sheet = generate_pdf()
##				data_list = self.generate_list_individui_pdf()
##				Individui_pdf_sheet.build_Individui_sheets(self.DATA_LIST)
##				Individui_pdf_sheet.build_index_individui(self.DATA_LIST, self.DATA_LIST[0][0])
##
##			self.DATA_LIST = []

	def db_search_DB(self, table_class, field, value):
		self.table_class = table_class
		self.field = field
		self.value = value

		search_dict = {self.field : "'"+str(self.value)+"'"}

		u = Utility()
		search_dict = u.remove_empty_items_fr_dict(search_dict)

		res = self.DB_MANAGER.query_bool(search_dict, self.table_class)

		return res

	def generate_list_US_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			#assegnazione valori di quota mn e max
			sito = unicode(self.DATA_LIST[i].sito)
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
				elenco_piante = sing_rec[7]
				if elenco_piante != None:
					piante = elenco_piante
				else:
					piante = "US disegnata su base GIS"
			else:
				piante = "US disegnata su base GIS"


			d_str= str(self.DATA_LIST[i].d_stratigrafica)
			QMessageBox.warning(self, "Alert", unicode(self.DATA_LIST[i]), QMessageBox.Ok)
			sito =  unicode(self.DATA_LIST[i].sito)

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


	def generate_list_periodizzazione_pdf(self):
		periodo = ""
		fase = ""
		cron_iniz = ""
		cron_fin = ""
		
		data_list = []
		for i in range(len(self.DATA_LIST)):
			
			if self.DATA_LIST[i].periodo == None:
				periodo = ""
			else:
				periodo = str(self.DATA_LIST[i].periodo)
			
			if self.DATA_LIST[i].fase == None:
				fase = ""
			else:
				fase = str(self.DATA_LIST[i].fase)
				
			if self.DATA_LIST[i].cron_iniziale == None:
				cron_iniz = ""
			else:
				cron_iniz = str(self.DATA_LIST[i].cron_iniziale)
				
			if self.DATA_LIST[i].cron_finale == None:
				cron_fin = ""
			else:
				cron_fin = str(self.DATA_LIST[i].cron_finale)
			
			
			data_list.append([
			str(self.DATA_LIST[i].sito), 										#1 - Sito
			str(periodo),															#2 - Area
			str(fase),																#3 - US
			str(cron_iniz),															#4 - definizione stratigrafica
			str(cron_fin),															#5 - definizione intepretata
			str(self.DATA_LIST[i].datazione_estesa),						#6 - descrizione
			unicode(self.DATA_LIST[i].descrizione)						#7 - interpretazione
		])
		return data_list


	def generate_list_struttura_pdf(self):
		data_list = []

		for i in range(len(self.DATA_LIST)):
			sito =  unicode(self.DATA_LIST[i].sito)
			sigla_struttura = ('%s%s') % (unicode(self.DATA_LIST[i].sigla_struttura), unicode(self.DATA_LIST[i].numero_struttura))

			res_strutt = self.DB_MANAGER.query_bool({"sito": "'" + str(sito) + "'", "struttura":"'"+str(sigla_struttura)+"'"}, "US")
			us_strutt_list = []
			if bool(res_strutt) == True:
				for rs in res_strutt:
					us_strutt_list.append([str(rs.sito), str(rs.area), str(rs.area)])

			quote_strutt = []
			if bool(us_strutt_list) == True:
				for sing_us in us_strutt_list:
					res_quote_strutt = self.DB_MANAGER.select_quote_from_db_sql(sing_us[0], sing_us[1], sing_us[2])
					if bool(res_quote_strutt) == True:
						for sing_us in res_quote_strutt:
							sing_quota_value = str(sing_us[5])
							if sing_quota_value[0] == '-':
								sing_quota_value = sing_quota_value[:7]
							else:
								sing_quota_value = sing_quota_value[:6]

							sing_quota = [sing_quota_value, sing_us[4]]
							quote_strutt.append(sing_quota)
						quote_strutt.sort()

			if bool(quote_strutt) == True:
				quota_min_strutt = '%s %s' % (quote_strutt[0][0], quote_strutt[0][1])
				quota_max_strutt = '%s %s' % (quote_strutt[-1][0], quote_strutt[-1][1])
			else:
				quota_min_strutt = "Non inserita su GIS"
				quota_max_strutt = "Non inserita su GIS"

			data_list.append([
			unicode(self.DATA_LIST[i].sito), 												#1 - Sito
			unicode(self.DATA_LIST[i].sigla_struttura),									#2 -  sigla struttura
			int(self.DATA_LIST[i].numero_struttura),										#3 - numero struttura
			unicode(self.DATA_LIST[i].categoria_struttura),								#4 - categoria
			unicode(self.DATA_LIST[i].tipologia_struttura),								#5 - tipologia
			unicode(self.DATA_LIST[i].definizione_struttura),							#6 - definizione
			unicode(self.DATA_LIST[i].descrizione),										#7 - descrizione
			unicode(self.DATA_LIST[i].interpretazione),									#7 - iintepretazione
			unicode(self.DATA_LIST[i].periodo_iniziale),									#8 - periodo iniziale
			unicode(self.DATA_LIST[i].fase_iniziale),										#9 - fase iniziale
			unicode(self.DATA_LIST[i].periodo_finale),									#10 - periodo finale
			unicode(self.DATA_LIST[i].fase_finale), 										#11 - fase finale
			unicode(self.DATA_LIST[i].datazione_estesa),								#12 - datazione estesa
			unicode(self.DATA_LIST[i].materiali_impiegati),								#13 - materiali impiegati
			unicode(self.DATA_LIST[i].elementi_strutturali),								#14 - elementi strutturali
			unicode(self.DATA_LIST[i].rapporti_struttura),								#15 - rapporti struttura
			unicode(self.DATA_LIST[i].misure_struttura),								#16 - misure
			quota_min_strutt,																		#17 - quota min
			quota_max_strutt																		#18 - quota max
			])
		return data_list



	def generate_list_reperti_pdf(self):
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
			unicode(self.DATA_LIST[i].rivestimento)					#21- rivestimento
		])
		return data_list

	def generate_list_individui_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].sito),					#1 - Sito
			int(self.DATA_LIST[i].area),					#2 - Area
			int(self.DATA_LIST[i].us),		        		#3 - us
			int(self.DATA_LIST[i].nr_individuo),			#4 -  nr individuo
			str(self.DATA_LIST[i].data_schedatura),	#5 - data schedatura
			str(self.DATA_LIST[i].schedatore),			#6 - schedatore
			str(self.DATA_LIST[i].sesso), 	             #7 - sesso
			str(self.DATA_LIST[i].eta_min), 	         #8 - eta' minima
			str(self.DATA_LIST[i].eta_max),			 #9- eta massima
			str(self.DATA_LIST[i].classi_eta),		     #10 - classi di eta'
			str(self.DATA_LIST[i].osservazioni)			 #11 - osservazioni
		])
		return data_list

	def generate_list_tafonomia_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			sito =  unicode(self.DATA_LIST[i].sito)
			nr_individuo = unicode(self.DATA_LIST[i].nr_individuo)
			sigla_struttura = ('%s%s') % (unicode(self.DATA_LIST[i].sigla_struttura), unicode(self.DATA_LIST[i].nr_struttura))

			res_ind = self.DB_MANAGER.query_bool({"sito": "'" + str(sito) + "'", "nr_individuo" : "'" + str(nr_individuo) + "'"}, "SCHEDAIND")
			#res = db.query_distinct('INVENTARIO_MATERIALI',[['sito','"Sito archeologico"']], ['area', 'us'])
			us_ind_list = []
			if bool(res_ind) == True:
				for ri in res_ind:
					us_ind_list.append([str(ri.sito), str(ri.area), str(ri.us)])

			quote_ind = []
			if bool(us_ind_list) == True:
				res_quote_ind = self.DB_MANAGER.select_quote_from_db_sql(us_ind_list[0][0], us_ind_list[0][1], us_ind_list[0][2])

				for sing_us in res_quote_ind:
					sing_quota_value = str(sing_us[5])
					if sing_quota_value[0] == '-':
						sing_quota_value = sing_quota_value[:7]
					else:
						sing_quota_value = sing_quota_value[:6]

					sing_quota = [sing_quota_value, sing_us[4]]
					quote_ind.append(sing_quota)
				quote_ind.sort()

			if bool(quote_ind) == True:
				quota_min_ind = '%s %s' % (quote_ind[0][0], quote_ind[0][1])
				quota_max_ind = '%s %s' % (quote_ind[-1][0], quote_ind[-1][1])
			else:
				quota_min_ind = "Non inserita su GIS"
				quota_max_ind = "Non inserita su GIS"

			##########################################################################

			res_strutt = self.DB_MANAGER.query_bool({"sito": "'" + str(sito) + "'", "struttura":"'"+str(sigla_struttura)+"'"}, "US")
			#res = db.query_distinct('INVENTARIO_MATERIALI',[['sito','"Sito archeologico"']], ['area', 'us'])
			us_strutt_list = []
			if bool(res_strutt) == True:
				for rs in res_strutt:
					us_strutt_list.append([str(rs.sito), str(rs.area), str(rs.area)])

			quote_strutt = []
			if bool(us_strutt_list) == True:
				for sing_us in us_strutt_list:
					res_quote_strutt = self.DB_MANAGER.select_quote_from_db_sql(sing_us[0], sing_us[1], sing_us[2])
					if bool(res_quote_strutt) == True:
						for sing_us in res_quote_strutt:
							sing_quota_value = str(sing_us[5])
							if sing_quota_value[0] == '-':
								sing_quota_value = sing_quota_value[:7]
							else:
								sing_quota_value = sing_quota_value[:6]

							sing_quota = [sing_quota_value, sing_us[4]]
							quote_strutt.append(sing_quota)
						quote_strutt.sort()

			if bool(quote_strutt) == True:
				quota_min_strutt = '%s %s' % (quote_strutt[0][0], quote_strutt[0][1])
				quota_max_strutt = '%s %s' % (quote_strutt[-1][0], quote_strutt[-1][1])
			else:
				quota_min_strutt = "Non inserita su GIS"
				quota_max_strutt = "Non inserita su GIS"

			data_list.append([
			unicode(self.DATA_LIST[i].sito), 									#0 - Sito
			unicode(self.DATA_LIST[i].nr_scheda_taf),						#1 - numero scheda taf
			unicode(self.DATA_LIST[i].sigla_struttura),						#2 - sigla struttura
			unicode(self.DATA_LIST[i].nr_struttura),							#3 - nr struttura
			unicode(self.DATA_LIST[i].nr_individuo),							#4 - nr individuo
			unicode(self.DATA_LIST[i].rito),										#5 - rito
			unicode(self.DATA_LIST[i].descrizione_taf),						#6 - descrizione
			unicode(self.DATA_LIST[i].interpretazione_taf),					#7 - interpretazione
			unicode(self.DATA_LIST[i].segnacoli),								#8 - segnacoli
			unicode(self.DATA_LIST[i].canale_libatorio_si_no),				#9- canale libatorio l
			unicode(self.DATA_LIST[i].oggetti_rinvenuti_esterno),			#10- oggetti rinvenuti esterno
			unicode(self.DATA_LIST[i].stato_di_conservazione),			#11 - stato_di_conservazione
			unicode(self.DATA_LIST[i].copertura_tipo), 						#12 - copertura tipo
			unicode(self.DATA_LIST[i].tipo_contenitore_resti),				#13 - tipo contenitore resti
			unicode(self.DATA_LIST[i].orientamento_asse),					#14 - orientamento asse
			self.DATA_LIST[i].orientamento_azimut,							#15 orientamento azimut
			unicode(self.DATA_LIST[i].corredo_presenza),					#16-  corredo presenza
			unicode(self.DATA_LIST[i].corredo_tipo),							#17 - corredo tipo
			unicode(self.DATA_LIST[i].corredo_descrizione),				#18 - corredo descrizione
			self.DATA_LIST[i].lunghezza_scheletro,							#19 - lunghezza scheletro
			unicode(self.DATA_LIST[i].posizione_cranio),						#20 - posizione cranio
			unicode(self.DATA_LIST[i].posizione_scheletro),					#21 - posizione cranio
			unicode(self.DATA_LIST[i].posizione_arti_superiori),			#22 - posizione arti superiori
			unicode(self.DATA_LIST[i].posizione_arti_inferiori),				#23 - posizione arti inferiori
			unicode(self.DATA_LIST[i].completo_si_no),						#24 - completo
			unicode(self.DATA_LIST[i].disturbato_si_no),					#25- disturbato
			unicode(self.DATA_LIST[i].in_connessione_si_no),				#26 - in connessione
			unicode(self.DATA_LIST[i].caratteristiche),						#27 - caratteristiche
			unicode(self.DATA_LIST[i].periodo_iniziale),						#28 - periodo iniziale
			unicode(self.DATA_LIST[i].fase_iniziale),							#29 - fase iniziale
			unicode(self.DATA_LIST[i].periodo_finale),						#30 - periodo finale
			unicode(self.DATA_LIST[i].fase_finale),							#31 - fase finale
			unicode(self.DATA_LIST[i].datazione_estesa),					#32 - datazione estesa
			unicode(self.DATA_LIST[i].misure_tafonomia),					#33 - misure tafonomia
			quota_min_ind,															#34 - quota min individuo
			quota_max_ind,															#35 - quota max individuo
			quota_min_strutt,															#36 - quota min struttura
			quota_max_strutt															#37 - quota max struttura
		])
			
		return data_list


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ui = pyarchinit_pdf_export()
	ui.show()
	sys.exit(app.exec_())