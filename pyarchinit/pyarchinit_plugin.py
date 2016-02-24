#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
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
import sys
import os


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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from pyarchinit_folder_installation import *
fi = pyarchinit_Folder_installation()
fi.install_dir()

# Import the code for the dialog
from pyarchinit_US_mainapp import pyarchinit_US
from pyarchinit_Site_mainapp import pyarchinit_Site
from pyarchinit_Periodizzazione_mainapp import pyarchinit_Periodizzazione
from pyarchinit_Struttura_mainapp import pyarchinit_Struttura
from pyarchinit_Inv_Materiali_mainapp import pyarchinit_Inventario_reperti
from pyarchinit_Upd_mainapp import pyarchinit_Upd_Values
from pyarchinitConfigDialog import pyArchInitDialog_Config
from pyarchinitInfoDialog import pyArchInitDialog_Info
from pyarchinit_Gis_Time_controller import pyarchinit_Gis_Time_Controller
from pyarchinit_image_viewer_main import Main
from pyarchinit_Schedaind_mainapp import pyarchinit_Schedaind
from pyarchinit_Detsesso_mainapp import pyarchinit_Detsesso
from pyarchinit_Deteta_mainapp import pyarchinit_Deteta
from pyarchinit_Tafonomia_mainapp import pyarchinit_Tafonomia
from pyarchinit_Archeozoology_mainapp import pyarchinit_Archeozoology
from pyarchinit_UT_mainapp import pyarchinit_UT
from pyarchinit_images_directory_export_mainapp import pyarchinit_Images_directory_export
from pyarchinit_images_comparision_main import Comparision
from dbmanagment import pyarchinit_dbmanagment
from pyarchinitplugindialog import PyarchinitPluginDialog
from pyarchinit_pdf_export_mainapp import pyarchinit_pdf_export
from pyarchinit_Campioni_mainapp import pyarchinit_Campioni
from pyarchinit_Thesaurus_mainapp import pyarchinit_Thesaurus
from pyarchinit_Documentazione_mainapp import pyarchinit_Documentazione

class PyArchInitPlugin:

	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	PARAMS_DICT={'SERVER':'',
				'HOST': '',
				'DATABASE':'',
				'PASSWORD':'',
				'PORT':'',
				'USER':'',
				'THUMB_PATH':'',
				'EXPERIMENTAL':''}


	path_rel = os.path.join(os.sep, str(HOME), 'pyarchinit_DB_folder', 'config.cfg')
	conf = open(path_rel, "r")
	data = conf.read()
	PARAMS_DICT = eval(data)
	if PARAMS_DICT.has_key('EXPERIMENTAL') == False:
		PARAMS_DICT['EXPERIMENTAL'] = 'No'
		f = open(path_rel, "w")
		f.write(str(PARAMS_DICT))
		f.close()


	def __init__(self, iface):
		self.iface = iface
		userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/pyarchinit"
		systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/pyarchinit"

		overrideLocale = QSettings().value( "locale/overrideFlag", QVariant ) #.toBool()
		if not overrideLocale:
			localeFullName = QLocale.system().name()
		else:
			localeFullName = QSettings().value( "locale/userLocale", QVariant ) #.toString()

		if QFileInfo( userPluginPath ).exists():
			translationPath = userPluginPath + "/i18n/pyarchinit_plugin_" + localeFullName + ".qm"
		else:
			translationPath = systemPluginPath + "/i18n/pyarchinit_plugin_" + localeFullName + ".qm"

		self.localePath = translationPath
		if QFileInfo( self.localePath ).exists():
			self.translator = QTranslator()
			self.translator.load( self.localePath )
			QCoreApplication.installTranslator( self.translator )

	def initGui(self):
		settings = QSettings()
		self.action = QAction(QIcon(":/plugins/pyarchinit/icons/pai_us.png"), "pyArchInit Main Panel", self.iface.mainWindow())
		QObject.connect(self.action, SIGNAL("triggered()"), self.showHideDockWidget)

		# dock widget
		self.dockWidget = PyarchinitPluginDialog(self.iface)
		self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

		#TOOLBAR
		self.toolBar = self.iface.addToolBar("pyArchInit")
		self.toolBar.setObjectName("pyArchInit")

		self.dataToolButton = QToolButton(self.toolBar)
		self.dataToolButton.setPopupMode(QToolButton.MenuButtonPopup)

		######  Section dedicated to the basic data entry
		#add Actions data
		icon_site = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSite.png'))
		self.actionSite = QAction(QIcon(icon_site), "Siti", self.iface.mainWindow())
		self.actionSite.setWhatsThis("Siti")
		QObject.connect(self.actionSite, SIGNAL("triggered()"), self.runSite)

		icon_US = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSus.png'))
		self.actionUS = QAction(QIcon((icon_US)), u"US", self.iface.mainWindow())
		self.actionUS.setWhatsThis(u"US")
		QObject.connect(self.actionUS, SIGNAL("triggered()"), self.runUS)

		icon_Finds = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconFinds.png'))
		self.actionInr = QAction(QIcon(icon_Finds), "Reperti", self.iface.mainWindow())
		self.actionInr.setWhatsThis("Reperti")
		QObject.connect(self.actionInr, SIGNAL("triggered()"), self.runInr)

		icon_camp_exp = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','champion.png'))
		self.actionCampioni = QAction(QIcon(icon_camp_exp), "Campioni", self.iface.mainWindow())
		self.actionCampioni.setWhatsThis("Campioni")
		QObject.connect(self.actionCampioni, SIGNAL("triggered()"), self.runCampioni)

		self.dataToolButton.addActions( [ self.actionSite, self.actionUS, self.actionInr, self.actionCampioni ] )
		self.dataToolButton.setDefaultAction(self.actionSite)

##		self.actionSite.setCheckable(True)
##		self.actionUS.setCheckable(True)
##		self.actionInr.setCheckable(True)
##		self.actionCampioni.setCheckable(True)

		self.toolBar.addWidget( self.dataToolButton )

		self.toolBar.addSeparator()

		######  Section dedicated to the interpretations
		#add Actions interpretation
		self.interprToolButton = QToolButton(self.toolBar)
		self.interprToolButton.setPopupMode(QToolButton.MenuButtonPopup)

		icon_per = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconPer.png'))
		self.actionPer = QAction(QIcon(icon_per), "Periodizzazione", self.iface.mainWindow())
		self.actionPer.setWhatsThis("Periodizzazione")
		QObject.connect(self.actionPer, SIGNAL("triggered()"), self.runPer)

		icon_Struttura = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconStrutt.png'))
		self.actionStruttura = QAction(QIcon(icon_Struttura), "Strutture", self.iface.mainWindow())
		self.actionPer.setWhatsThis("Strutture")
		QObject.connect(self.actionStruttura, SIGNAL("triggered()"), self.runStruttura)

		self.interprToolButton.addActions( [ self.actionStruttura, self.actionPer ] )
		self.interprToolButton.setDefaultAction(self.actionStruttura)

##		self.actionPer.setCheckable(True)
##		self.actionStruttura.setCheckable(True)

		self.toolBar.addWidget( self.interprToolButton )

		self.toolBar.addSeparator()

		######  Section dedicated to the funerary archaeology
		#add Actions funerary archaeology
		self.funeraryToolButton = QToolButton(self.toolBar)
		self.funeraryToolButton.setPopupMode(QToolButton.MenuButtonPopup)

		icon_Schedaind = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconIND.png'))
		self.actionSchedaind = QAction(QIcon(icon_Schedaind), "Individui", self.iface.mainWindow())
		self.actionSchedaind.setWhatsThis("Individui")
		QObject.connect(self.actionSchedaind, SIGNAL("triggered()"), self.runSchedaind)

		icon_Tafonomia = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconGrave.png'))
		self.actionTafonomia = QAction(QIcon(icon_Tafonomia), "Tafonomica/Sepolture", self.iface.mainWindow())
		self.actionTafonomia.setWhatsThis("Tafonomica/Sepolture")
		QObject.connect(self.actionTafonomia, SIGNAL("triggered()"), self.runTafonomia)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			icon_Detsesso = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSesso.png'))
			self.actionDetsesso = QAction(QIcon(icon_Detsesso), "Determinazione Sesso", self.iface.mainWindow())
			self.actionDetsesso.setWhatsThis("Determinazione del sesso")
			QObject.connect(self.actionDetsesso, SIGNAL("triggered()"), self.runDetsesso)

			icon_Deteta = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconEta.png'))
			self.actionDeteta = QAction(QIcon(icon_Deteta), u"Determinazione dell'età", self.iface.mainWindow())
			self.actionSchedaind.setWhatsThis(u"Determinazione dell'età")
			QObject.connect(self.actionDeteta, SIGNAL("triggered()"), self.runDeteta)

		self.funeraryToolButton.addActions( [ self.actionSchedaind, self.actionTafonomia ] )
		self.funeraryToolButton.setDefaultAction(self.actionSchedaind)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.funeraryToolButton.addActions( [ self.actionDetsesso, self.actionDeteta ] )

##		self.actionSchedaind.setCheckable(True)
##		self.actionTafonomia.setCheckable(True)

		self.toolBar.addWidget( self.funeraryToolButton )

		self.toolBar.addSeparator()

		######  Section dedicated to the topographical research
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.topoToolButton = QToolButton(self.toolBar)
			self.topoToolButton.setPopupMode(QToolButton.MenuButtonPopup)

			icon_UT = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconUT.png'))
			self.actionUT = QAction(QIcon(icon_UT), u"Unità Topografiche", self.iface.mainWindow())
			self.actionUT.setWhatsThis(u"Unità Topografiche")
			QObject.connect(self.actionUT, SIGNAL("triggered()"), self.runUT)

			self.topoToolButton.addActions( [ self.actionUT ] )
			self.topoToolButton.setDefaultAction(self.actionUT)

##			self.actionUT.setCheckable(True)

			self.toolBar.addWidget( self.topoToolButton )

			self.toolBar.addSeparator()

		######  Section dedicated to the documentation
		#add Actions documentation
		self.docToolButton = QToolButton(self.toolBar)
		self.docToolButton.setPopupMode(QToolButton.MenuButtonPopup)

		icon_documentazione = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','icondoc.png'))
		self.actionDocumentazione = QAction(QIcon(icon_documentazione), "Scheda Documentazione", self.iface.mainWindow())
		self.actionDocumentazione.setWhatsThis("Documentazione")
		QObject.connect(self.actionDocumentazione, SIGNAL("triggered()"), self.runDocumentazione)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			icon_imageViewer = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','photo.png'))
			self.actionimageViewer = QAction(QIcon(icon_imageViewer), "Gestione immagini", self.iface.mainWindow())
			self.actionimageViewer.setWhatsThis("Gestione immagini")
			QObject.connect(self.actionimageViewer, SIGNAL("triggered()"), self.runImageViewer)

			icon_Directory_export = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','directoryExp.png'))
			self.actionImages_Directory_export = QAction(QIcon(icon_Directory_export), "Esportazione immagini", self.iface.mainWindow())
			self.actionImages_Directory_export.setWhatsThis("Esportazione immagini")
			QObject.connect(self.actionImages_Directory_export, SIGNAL("triggered()"),self.runImages_directory_export)

			icon_pdf_exp = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','pdf-icon.png'))
			self.actionpdfExp = QAction(QIcon(icon_pdf_exp), "Esportazione PDF", self.iface.mainWindow())
			self.actionpdfExp.setWhatsThis("Esportazione PDF")
			QObject.connect(self.actionpdfExp, SIGNAL("triggered()"), self.runPdfexp)

		self.docToolButton.addActions( [ self.actionDocumentazione ] )

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.docToolButton.addActions( [ self.actionpdfExp, self.actionimageViewer, self.actionpdfExp, self.actionImages_Directory_export] )

		self.docToolButton.setDefaultAction( self.actionDocumentazione)

##		self.actionDocumentazione.setCheckable(True)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.actionImages_Directory_export.setCheckable(True)
			self.actionpdfExp.setCheckable(True)
			self.actionimageViewer.setCheckable(True)

		self.toolBar.addWidget( self.docToolButton )

		self.toolBar.addSeparator()

		######  Section dedicated to elaborations
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.elabToolButton = QToolButton(self.toolBar)
			self.elabToolButton.setPopupMode(QToolButton.MenuButtonPopup)

			#add Actions elaboration
			icon_Archeozoology = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconMegacero.png'))
			self.actionArcheozoology = QAction(QIcon(icon_Archeozoology), "Statistiche Archeozoologiche", self.iface.mainWindow())
			self.actionArcheozoology.setWhatsThis("Statistiche Archeozoologiche")
			QObject.connect(self.actionArcheozoology, SIGNAL("triggered()"), self.runArcheozoology)

			icon_GisTimeController = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconTimeControll.png'))
			self.actionGisTimeController = QAction(QIcon(icon_GisTimeController), "Time Manager", self.iface.mainWindow())
			self.actionGisTimeController.setWhatsThis("Time Manager")
			QObject.connect(self.actionGisTimeController, SIGNAL("triggered()"), self.runGisTimeController)

			icon_Comparision = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','comparision.png'))
			self.actionComparision = QAction(QIcon(icon_Comparision), "Comparazione immagini", self.iface.mainWindow())
			self.actionComparision.setWhatsThis("Comparazione immagini")
			QObject.connect(self.actionComparision, SIGNAL("triggered()"),self.runComparision)

			self.elabToolButton.addActions( [ self.actionArcheozoology, self.actionComparision,self.actionGisTimeController ] )
			self.elabToolButton.setDefaultAction(self.actionArcheozoology)

##			self.actionArcheozoology.setCheckable(True)
##			self.actionComparision.setCheckable(True)
##			self.actionGisTimeController.setCheckable(True)

			self.toolBar.addWidget( self.elabToolButton )

			self.toolBar.addSeparator()

		######  Section dedicated to the plugin management

		self.manageToolButton = QToolButton(self.toolBar)
		self.manageToolButton.setPopupMode(QToolButton.MenuButtonPopup)

		icon_thesaurus = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','thesaurusicon.png'))
		self.actionThesaurus = QAction(QIcon(icon_thesaurus), "Thesaurus sigle", self.iface.mainWindow())
		self.actionThesaurus.setWhatsThis("Thesaurus sigle")
		QObject.connect(self.actionThesaurus, SIGNAL("triggered()"), self.runThesaurus)

		icon_Con = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconConn.png'))
		self.actionConf = QAction(QIcon(icon_Con), "Configurazione plugin", self.iface.mainWindow())
		self.actionConf.setWhatsThis("Configurazione plugin")
		QObject.connect(self.actionConf, SIGNAL("triggered()"), self.runConf)

		icon_Dbmanagment = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','backup.png'))
		self.actionDbmanagment = QAction(QIcon(icon_Dbmanagment), "Gestione database", self.iface.mainWindow())
		self.actionDbmanagment.setWhatsThis("Gestione database")
		QObject.connect(self.actionDbmanagment, SIGNAL("triggered()"), self.runDbmanagment)

		icon_Info = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconInfo.png'))
		self.actionInfo = QAction(QIcon(icon_Info), "Plugin info", self.iface.mainWindow())
		self.actionInfo.setWhatsThis("Plugin info")
		QObject.connect(self.actionInfo, SIGNAL("triggered()"), self.runInfo)

		self.manageToolButton.addActions( [ self.actionConf, self.actionThesaurus, self.actionDbmanagment, self.actionInfo ] )
		self.manageToolButton.setDefaultAction( self.actionConf )

##			self.actionThesaurus.setCheckable(True)
##			self.actionConf.setCheckable(True)
##			self.actionDbmanagment.setCheckable(True)
##			self.actionInfo.setCheckable(True)

		self.toolBar.addWidget( self.manageToolButton )

		self.toolBar.addSeparator()

		#menu
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionSite)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUS)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInr)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionCampioni)

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionStruttura)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionPer)

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionSchedaind)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionTafonomia)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDetsesso)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDeteta)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUT)

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDocumentazione)

		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionimageViewer)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionpdfExp)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionImages_Directory_export)

			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionArcheozoology)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionComparision)
			self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionGisTimeController)

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionConf)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionThesaurus)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDbmanagment)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInfo)

		#MENU
		self.menu=QMenu("pyArchInit")
		#self.pyarchinitSite = pyarchinit_Site(self.iface)
		self.menu.addActions([self.actionSite, self.actionUS, self.actionInr, self.actionCampioni])
		self.menu.addSeparator()
		self.menu.addActions([self.actionPer, self.actionStruttura])
		self.menu.addSeparator()
		self.menu.addActions([self.actionTafonomia, self.actionSchedaind])
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.menu.addActions([self.actionDetsesso,self.actionDeteta])
		self.menu.addSeparator()
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.menu.addActions([self.actionUT])
		self.menu.addActions([self.actionDocumentazione])
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.menu.addActions([self.actionimageViewer, self.actionpdfExp, self.actionImages_Directory_export])
		self.menu.addSeparator()
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.menu.addActions([self.actionArcheozoology, self.actionComparision, self.actionGisTimeController])
		self.menu.addSeparator()
		self.menu.addActions([self.actionConf, self.actionThesaurus, self.actionDbmanagment, self.actionInfo])
		menuBar = self.iface.mainWindow().menuBar()
		menuBar.addMenu(self.menu)
##
	def runSite(self):
		pluginGui = pyarchinit_Site(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runPer(self):
		pluginGui = pyarchinit_Periodizzazione(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runStruttura(self):
		pluginGui = pyarchinit_Struttura(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runUS(self):
		pluginGui = pyarchinit_US(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runInr(self):
		pluginGui = pyarchinit_Inventario_reperti(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runCampioni(self):
		pluginGui = pyarchinit_Campioni(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runGisTimeController(self):
		pluginGui = pyarchinit_Gis_Time_Controller(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runConf(self):
		pluginConfGui = pyArchInitDialog_Config()
		pluginConfGui.show()
		self.pluginGui = pluginConfGui # save

	def runInfo(self):
		pluginInfoGui = pyArchInitDialog_Info()
		pluginInfoGui.show()
		self.pluginGui = pluginInfoGui # save

	def runImageViewer(self):
		pluginImageView = Main()
		pluginImageView.show()
		self.pluginGui = pluginImageView # save

	def runTafonomia(self):
		pluginTafonomia = pyarchinit_Tafonomia(self.iface)
		pluginTafonomia.show()
		self.pluginGui = pluginTafonomia # save

	def runSchedaind(self):
		pluginIndividui = pyarchinit_Schedaind(self.iface)
		pluginIndividui.show()
		self.pluginGui = pluginIndividui # save

	def runDetsesso(self):
		pluginSesso = pyarchinit_Detsesso(self.iface)
		pluginSesso.show()
		self.pluginGui = pluginSesso # save

	def runDeteta(self):
		pluginEta = pyarchinit_Deteta(self.iface)
		pluginEta.show()
		self.pluginGui = pluginEta # save

	def runArcheozoology(self):
		pluginArchezoology = pyarchinit_Archeozoology(self.iface)
		pluginArchezoology.show()
		self.pluginGui = pluginArchezoology # save

	def runUT(self):
		pluginUT = pyarchinit_UT(self.iface)
		pluginUT.show()
		self.pluginGui = pluginUT # save

	def runImages_directory_export(self):
		pluginImage_directory_export = pyarchinit_Images_directory_export()
		pluginImage_directory_export.show()
		self.pluginGui = pluginImage_directory_export # save

	def runComparision(self):
		pluginComparision = Comparision()
		pluginComparision.show()
		self.pluginGui = pluginComparision # save

	def runDbmanagment(self):
		pluginDbmanagment = pyarchinit_dbmanagment(self.iface)
		pluginDbmanagment.show()
		self.pluginGui = pluginDbmanagment # save

	def runPdfexp(self):
		pluginPdfexp = pyarchinit_pdf_export()
		pluginPdfexp.show()
		self.pluginGui =pluginPdfexp # save

	def runThesaurus(self):
		pluginThesaurus = pyarchinit_Thesaurus(self.iface)
		pluginThesaurus.show()
		self.pluginGui =pluginThesaurus # save

	def runDocumentazione(self):
		pluginDocumentazione = pyarchinit_Documentazione(self.iface)
		pluginDocumentazione.show()
		self.pluginGui =pluginDocumentazione # save

	def unload(self):
		# Remove the plugin
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionSite)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionPer)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionStruttura)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUS)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInr)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionCampioni)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionSchedaind)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDocumentazione)
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDetsesso)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDeteta)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionTafonomia)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionArcheozoology)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUT)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionimageViewer)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionImages_Directory_export)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionpdfExp)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionComparision)
			self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionGisTimeController)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionConf)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionThesaurus)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInfo)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDbmanagment)

		self.iface.removeToolBarIcon(self.actionSite)
		self.iface.removeToolBarIcon(self.actionPer)
		self.iface.removeToolBarIcon(self.actionStruttura)
		self.iface.removeToolBarIcon(self.actionUS)
		self.iface.removeToolBarIcon(self.actionInr)
		self.iface.removeToolBarIcon(self.actionCampioni)
		self.iface.removeToolBarIcon(self.actionTafonomia)
		self.iface.removeToolBarIcon(self.actionSchedaind)
		self.iface.removeToolBarIcon(self.actionDocumentazione)
		if self.PARAMS_DICT['EXPERIMENTAL'] == 'Si':
			self.iface.removeToolBarIcon(self.actionDetsesso)
			self.iface.removeToolBarIcon(self.actionDeteta)
			self.iface.removeToolBarIcon(self.actionArcheozoology)
			self.iface.removeToolBarIcon(self.actionUT)
			#self.iface.removeToolBarIcon(self.actionUpd)
			self.iface.removeToolBarIcon(self.actionimageViewer)
			self.iface.removeToolBarIcon(self.actionImages_Directory_export)
			self.iface.removeToolBarIcon(self.actionpdfExp)
			self.iface.removeToolBarIcon(self.actionComparision)
			self.iface.removeToolBarIcon(self.actionGisTimeController)
		self.iface.removeToolBarIcon(self.actionConf)
		self.iface.removeToolBarIcon(self.actionThesaurus)
		self.iface.removeToolBarIcon(self.actionInfo)
		self.iface.removeToolBarIcon(self.actionDbmanagment)

		# remove tool bar
		del self.toolBar

	def showHideDockWidget(self):
		if self.dockWidget.isVisible():
			self.dockWidget.hide()
		else:
			self.dockWidget.show()
