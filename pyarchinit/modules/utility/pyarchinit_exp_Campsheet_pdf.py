import os
import copy
from reportlab.lib.testutils import makeSuiteForClasses, outputfile, printLocation
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Paragraph, Spacer, TableStyle, Image
from reportlab.platypus.paragraph import Paragraph

from datetime import date, time

from pyarchinit_OS_utility import *


class NumberedCanvas_Campionisheet(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []
		
	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(200*mm, 20*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm

class NumberedCanvas_Campioniindex(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(270*mm, 10*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm


class NumberedCanvas_CASSEindex(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(270*mm, 10*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm


class single_Campioni_pdf_sheet:

	def __init__(self, data):
		self.sito = data[0]											#1 - Sito
		self.numero_campione = data[1]						#2 - Numero campione
		self.tipo_campione = data[2]								#3 - Tipo campione
		self.descrizione = data[3]									#4 - Descrizione
		self.area = data[4]											#5 - Area
		self.us = data[5]												#6 - us
		self.numero_inventario =  data[6]					#7 - numero inventario materiale
		self.luogo_conservazione = data[7]						#8 - luogo_conservazione
		self.nr_cassa = data[8]									#9 - nr cassa

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def create_sheet(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT

		styleSheet = getSampleStyleSheet()
		styDescrizione = styleSheet['Normal']
		styDescrizione.spaceBefore = 20
		styDescrizione.spaceAfter = 20
		styDescrizione.alignment = 4 #Justified

		#format labels

		#0 row
		intestazione = Paragraph("<b>SCHEDA CAMPIONI<br/>" + str(self.datestrfdate()) + "</b>", styNormal)

		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
		logo_path = ('%s%s%s') % (home_DB_path, os.sep, 'logo.jpg')
		logo = Image(logo_path)

		##		if test_image.drawWidth < 800:

		logo.drawHeight = 1.5*inch*logo.drawHeight / logo.drawWidth
		logo.drawWidth = 1.5*inch

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		tipo_campione = Paragraph("<b>Tipo Campione</b><br/>"  + str(self.tipo_campione), styNormal)
		nr_campione = Paragraph("<b>Nr. Campione</b><br/>"  + str(self.numero_campione), styNormal)

		#2 row
		area = Paragraph("<b>Area</b><br/>"  + str(self.area), styNormal)
		us = Paragraph("<b>US</b><br/>"  + str(self.us), styNormal)
		nr_inventario = Paragraph("<b>Nr. Inventario</b><br/>"  + str(self.numero_inventario), styNormal)
		
		#4 row
		descrizione = Paragraph("<b>Descrizione</b><br/>" + unicode(self.descrizione), styDescrizione)

		#4 row
		luogo_conservazione = Paragraph("<b>Luogo conservazione</b><br/>" + unicode(self.luogo_conservazione), styNormal)
		nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + unicode(self.nr_cassa), styNormal)

		#schema
		cell_schema = [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
							[intestazione, '01', '02', '03', '04','05', '06', logo, '08', '09'],					#0 row ok
							[sito, '01', '02', '03', '04',tipo_campione,'06', '07', nr_campione, '09'],		#1 row ok
							[area, '01', '02', us,'04', '05',nr_inventario, '07', '08', '09'], 					#2 row ok
							[descrizione, '01','02', '03', '04', '05','06', '07', '08', '09'],						#3 row ok
							[nr_cassa,'01', '02', '03', '04', '05', luogo_conservazione, '07', '08', '09']	#4 row ok
							]


		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(6,0)),  #intestazione
					('SPAN', (7,0),(9,0)), #intestazione

					#1 row
					('SPAN', (0,1),(4,1)),  #dati identificativi
					('SPAN', (5,1),(7,1)),  #dati identificativi
					('SPAN', (8,1),(9,1)),   #dati identificativi

					#2 row
					('SPAN', (0,2),(2,2)),  #definizione
					('SPAN', (3,2),(5,2)),  #definizione
					('SPAN', (6,2),(9,2)),  #definizione
					('VALIGN',(0,2),(9,2),'TOP'), 

					#3 row
					('SPAN', (0,3),(9,3)),  #descrizione

					#5 row
					('SPAN', (0,4),(5,4)),  #elementi_reperto	
					('SPAN', (6,4),(9,4)),  #elementi_reperto

					('VALIGN',(0,0),(-1,-1),'TOP')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t


class Box_labels_Campioni_pdf_sheet:

	def __init__(self, data, sito):
		self.sito = sito #Sito
		self.cassa= data[0] #1 - Cassa
		self.elenco_inv_tip_rep = data[1] #2-  elenco US
		self.elenco_us = data[2] #3 - elenco Inventari
		self.luogo_conservazione = data[3]#4 - luogo conservazione

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def create_sheet(self):
		styleSheet = getSampleStyleSheet()
		
		styleSheet.add(ParagraphStyle(name='Cassa Label'))
		styleSheet.add(ParagraphStyle(name='Sito Label'))

		styCassaLabel = styleSheet['Cassa Label']
		styCassaLabel.spaceBefore = 0
		styCassaLabel.spaceAfter = 0
		styCassaLabel.alignment = 2 #RIGHT
		styCassaLabel.leading = 25
		styCassaLabel.fontSize = 30

		stySitoLabel = styleSheet['Sito Label']
		stySitoLabel.spaceBefore = 0
		stySitoLabel.spaceAfter = 0
		stySitoLabel.alignment = 0 #LEFT
		stySitoLabel.leading = 25
		stySitoLabel.fontSize = 18
		stySitoLabel.fontStyle = 'bold'

		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 10
		styNormal.spaceAfter = 10
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 14
		styNormal.leading = 15


		#format labels
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
		logo_path = ('%s%s%s') % (home_DB_path, os.sep, 'logo.jpg')
		logo = Image(logo_path)

		##		if test_image.drawWidth < 800:

		logo.drawHeight = 1.5*inch*logo.drawHeight / logo.drawWidth
		logo.drawWidth = 1.5*inch
		

		num_cassa = Paragraph("<b>N. Cassa </b>" + str(self.cassa),styCassaLabel)
		sito = Paragraph("<b>Sito: </b>" + str(self.sito),stySitoLabel)

		if self.elenco_inv_tip_rep == None:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo campione</b><br/>",styNormal)
		else:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo campione</b><br/>" + str(self.elenco_inv_tip_rep ),styNormal)

		if self.elenco_us == None:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b>",styNormal)
		else:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b><br/>" + str(self.elenco_us),styNormal)

		#luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

		#schema
		cell_schema =	[ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
							[logo, '01', '02', '03', '04','05', num_cassa, '07', '08', '09'],
							[sito, '01', '02', '03', '04','05', '06', '07', '08', '09'],
							[elenco_us, '01', '02', '03','04', '05','06', '07', '08', '09'],
							[elenco_inv_tip_rep, '01', '02','03', '04', '05','06', '07', '08', '09']

						]



		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0,colors.white),#,0.0,colors.black
					#0 row
					('SPAN', (0,0),(5,0)),  #elenco US
					('SPAN', (6,0),(9,0)),  #elenco US
					('HALIGN',(0,0),(9,0),'LEFT'),
					('VALIGN',(6,0),(9,0),'TOP'),
					('HALIGN',(6,0),(9,0),'RIGHT'),

					('SPAN', (0,1),(9,1)),  #elenco US
					('HALIGN',(0,1),(9,1),'LEFT'),

					('SPAN', (0,2),(9,2)),  #intestazione
					('VALIGN',(0,2),(9,2),'TOP'), 
					#1 row
					('SPAN', (0,3),(9,3)),  #elenco US
					('VALIGN',(0,3),(9,3),'TOP')

					]


		colWidths=None
		rowHeights=None
		#colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
		t=Table(cell_schema,colWidths,rowHeights, style= table_style)

		return t


class CASSE_index_pdf_sheet:

	def __init__(self, data):
		self.cassa= data[0] #1 - Cassa
		self.elenco_inv_tip_camp = data[1] #2-  elenco US
		self.elenco_us = data[2] #3 - elenco Inventari
		self.luogo_conservazione = data[3]#4 - luogo conservazione

	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 10

		#self.unzip_rapporti_stratigrafici()

		num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa),styNormal)

		if self.elenco_inv_tip_camp == None:
			elenco_inv_tip_camp = Paragraph("<b>N. Inv./Tipo campione</b><br/>",styNormal)
		else:
			elenco_inv_tip_camp = Paragraph("<b>N. Inv./Tipo campione</b><br/>" + str(self.elenco_inv_tip_camp ),styNormal)

		if self.elenco_us == None:
			elenco_us = Paragraph("<b>US(Struttura)</b><br/>",styNormal)
		else:
			elenco_us = Paragraph("<b>US(Struttura)</b><br/>" + str(self.elenco_us),styNormal)

		luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

		data = [num_cassa,
					elenco_inv_tip_camp,
					elenco_us,
					luogo_conservazione]

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')])  #finale

		return styles


class Campioni_index_pdf_sheet:

	def __init__(self, data):
		self.sito = data[0] 									#1 - sito
		self.numero_campione = data[1] 				#2- numero campione
		self.tipo_campione = data[2]						#3 - Tipo campione
		self.descrizione = data[3]							#4 - descrizione
		self.area = data[4 ]									#5 - area
		self.us = data[5 ]									#6 - us
		self.numero_inventario_materiale = data[6]	#7 - numero inventario materiale
		self.luogo_conservazione = data[7]				#8 - conservazione
		self.nr_cassa = data[8]							#9 - nr_cassa

	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		#self.unzip_rapporti_stratigrafici()

		num_campione = Paragraph("<b>N. Camp.</b><br/>" + str(self.numero_campione),styNormal)

		if self.tipo_campione == None:
			tipo_campione = Paragraph("<b>Tipo campione</b><br/>",styNormal)
		else:
			tipo_campione = Paragraph("<b>Tipo campione</b><br/>" + str(self.tipo_campione),styNormal)

		if str(self.area) == "None":
			area = Paragraph("<b>Area</b><br/>",styNormal)
		else:
			area = Paragraph("<b>Area</b><br/>" + str(self.area),styNormal)

		if str(self.us) == "None":
			us = Paragraph("<b>US</b><br/>",styNormal)
		else:
			us = Paragraph("<b>US</b><br/>" + str(self.us),styNormal)

		if self.numero_inventario_materiale == None:
			numero_inventario_materiale = Paragraph("<b>N. Inv. Materiale</b><br/>",styNormal)
		else:
			numero_inventario_materiale = Paragraph("<b>N. Inv. Materiale</b><br/>" + str(self.numero_inventario_materiale),styNormal)

		if self.luogo_conservazione == None:
			luogo_conservazione = Paragraph("<b>Luogo Conservazione</b><br/>",styNormal)
		else:
			luogo_conservazione = Paragraph("<b>Luogo Conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

		if self.nr_cassa == None:
			nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>",styNormal)
		else:
			nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + str(self.nr_cassa),styNormal)

		data = [num_campione,
				tipo_campione,
				area,
				us,
				numero_inventario_materiale,
				luogo_conservazione,
				nr_cassa]

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')
		])  #finale

		return styles

class generate_campioni_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_Champ_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_Campioni_sheet = single_Campioni_pdf_sheet(records[i])
			elements.append(single_Campioni_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Campioni.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_Campionisheet)
		f.close()

	def build_index_Campioni(self, records, sito):
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
		logo_path = ('%s%s%s') % (home_DB_path, os.sep, 'logo.jpg')

		logo = Image(logo_path) 
		logo.drawHeight = 1.5*inch*logo.drawHeight / logo.drawWidth
		logo.drawWidth = 1.5*inch
		logo.hAlign = "LEFT"

		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH1 = styleSheet['Heading3']

		data = self.datestrfdate()

		lst = []
		lst.append(logo)
		lst.append(Paragraph("<b>ELENCO CAMPIONI</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = Campioni_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())
		
		styles = exp_index.makeStyles()
		colWidths=[60,150,60, 60,60, 250, 60]

		table_data_formatted = Table(table_data, colWidths, style=styles)
		table_data_formatted.hAlign = "LEFT"

		lst.append(table_data_formatted)
		#lst.append(Spacer(0,2))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'elenco_campioni.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(lst, canvasmaker=NumberedCanvas_Campioniindex)

		f.close()

	def build_index_Casse(self, records, sito):
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
		logo_path = ('%s%s%s') % (home_DB_path, os.sep, 'logo.jpg')

		logo = Image(logo_path)
		logo.drawHeight = 1.5*inch*logo.drawHeight / logo.drawWidth
		logo.drawWidth = 1.5*inch
		logo.hAlign = "LEFT"

		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH1 = styleSheet['Heading3']

		data = self.datestrfdate()
		lst = [logo]
		lst.append(Paragraph("<b>ELENCO CASSE CAMPIONI</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = CASSE_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())

		styles = exp_index.makeStyles()
		colWidths=[20,350,250,100]

		table_data_formatted = Table(table_data, colWidths, style=styles)
		table_data_formatted.hAlign = "LEFT"

		#table_data_formatted.setStyle(styles)

		lst.append(table_data_formatted)
		lst.append(Spacer(0,0))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'elenco_casse_campioni.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0, topMargin = 15, bottomMargin = 40, leftMargin = 30, rightMargin = 30)
		#doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
		doc.build(lst)

		f.close()


	def build_box_labels_Campioni(self, records, sito):
		elements = []
		for i in range(len(records)):
			single_finds_sheet = Box_labels_Campioni_pdf_sheet(records[i], sito)
			elements.append(single_finds_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'etichette_casse_campioni.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0.0, topMargin = 20, bottomMargin = 20, leftMargin = 20, rightMargin = 20)
		doc.build(elements)
		f.close()

