import os
import copy
from reportlab.lib.testutils import makeSuiteForClasses, outputfile, printLocation
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Paragraph, Spacer, TableStyle, Image
from reportlab.platypus.paragraph import Paragraph

from datetime import date, time

from pyarchinit_OS_utility import *

class NumberedCanvas_Periodizzazioneindex(canvas.Canvas):
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

class NumberedCanvas_Periodizzazionesheet(canvas.Canvas):
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


class Periodizzazione_index_pdf_sheet:

	def __init__(self, data):
		self.periodo = 				data[1]			#1 - periodo
		self.fase = 					data[2]			#2 - fase
		self.cron_iniziale =		data[3]			#3 - cron_iniziale
		self.cron_finale =			data[4]			#4 - cron_finale
		self.datazione_estesa =	data[5]			#5 - datazione_estesa


	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		#self.unzip_rapporti_stratigrafici()

		periodo = Paragraph("<b>Periodo</b><br/>" + str(self.periodo),styNormal)

		fase = Paragraph("<b>Fase</b><br/>" + str(self.fase),styNormal)

		if str(self.cron_iniziale) == "None":
			cron_iniziale = Paragraph("<b>Cronologia iniziale</b><br/>" + str(self.cron_iniziale),styNormal)
		else:
			cron_iniziale = Paragraph("<b>Cronologia iniziale</b><br/>",styNormal)

		if str(self.cron_finale) == "None":
			cron_finale = Paragraph("<b>Cronologia finale</b><br/>" + str(self.cron_finale),styNormal)
		else:
			cron_finale = Paragraph("<b>Cronologia finale</b><br/>",styNormal)

		datazione_estesa = Paragraph("<b>Datazione estesa</b><br/>" + str(self.datazione_estesa),styNormal)

		data = [periodo,
					fase,
					cron_iniziale,
					cron_finale,
					datazione_estesa
					]

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')
		])  #finale

		return styles


class single_Periodizzazione_pdf_sheet:

	def __init__(self, data):
		self.sito = 					data[0]
		self.periodo = 					data[1]
		self.fase = 					data[2]
		self.cron_iniziale =			data[3]
		self.cron_finale =				data[4]
		self.datazione_estesa =			data[5]
		self.descrizione =				data[6]


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
		intestazione = Paragraph("<b>SCHEDA PERIODIZZAZIONE<br/>" + str(self.datestrfdate()) + "</b>", styNormal)

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


		#intestazione2 = Paragraph("<b>pyArchInit</b><br/>www.pyarchinit.blogspot.com", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		periodo = Paragraph("<b>Periodo</b><br/>"  + str(self.periodo), styNormal)
		fase = Paragraph("<b>Fase</b><br/>"  + str(self.fase), styNormal)

		#2 row
		cronologia = Paragraph("<b>CRONOLOGIA</b></b>",styNormal)
		
		#3 row
		cronologia_iniziale = Paragraph("<b>Cronologia iniziale</b><br/>"  + str(self.cron_iniziale), styNormal)
		cronologia_finale = Paragraph("<b>Cronologia finale</b><br/>"  + str(self.cron_finale), styNormal)
		datazione_ext = Paragraph("<b>Cronologia testuale</b><br/>"  + str(self.datazione_estesa), styNormal)

		#4 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styDescrizione)
		except:
			pass

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', logo, '08', '09'], #0 row ok
						[sito, '01', '02', '03', '04', periodo, '06', '07', fase, '09'], #1 row ok
						[cronologia, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #2 row ok
						[cronologia_iniziale, '01', cronologia_finale, '03', datazione_ext,'05', '06', '07', '08', '09'], #3 row
						[descrizione, '01','02', '03', '04', '05', '06', '07', '08', '09']]#4row ok

		#table style
		table_style=[
					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(6,0)),  #intestazione
					('SPAN', (7,0),(9,0)),  #intestazione

					#1 row
					('SPAN', (0,1),(4,1)),  #Sito
					('SPAN', (5,1),(7,1)),  #periodo
					('SPAN', (8,1),(9,1)),  #fase

					#2 row
					('SPAN', (0,2),(9,2)),  #intestazione cronologia

					#3 row
					('SPAN', (0,3),(1,3)),  #cron iniziale
					('SPAN', (2,3),(3,3)),  #cron finale
					('SPAN', (4,3),(9,3)),  #datazione estesa
					
					#4
					('SPAN', (0,4),(9,4)),  #datazione estesa
					('VALIGN',(0,4),(9,4),'TOP'), 
					#('VALIGN',(5,3),(5,3),'TOP'), 

					('VALIGN',(0,0),(-1,-1),'TOP')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t


class generate_Periodizzazione_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_Periodizzazione_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_periodizzazione_sheet = single_Periodizzazione_pdf_sheet(records[i])
			elements.append(single_periodizzazione_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Periodizzazione.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_Periodizzazionesheet)
		f.close()


	def build_index_Periodizzazione(self, records, sito):
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
		lst.append(Paragraph("<b>ELENCO PERIODIZZAZIONI</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = Periodizzazione_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())
		
		styles = exp_index.makeStyles()
		colWidths=[60,60,150,150,300]

		table_data_formatted = Table(table_data, colWidths, style=styles)
		table_data_formatted.hAlign = "LEFT"

		lst.append(table_data_formatted)
		#lst.append(Spacer(0,2))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'elenco_periodizzazione.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(lst, canvasmaker=NumberedCanvas_Periodizzazioneindex)

		f.close()