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


class NumberedCanvas_UTsheet(canvas.Canvas):
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


class NumberedCanvas_UTindex(canvas.Canvas):
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
		self.drawRightString(270*mm, 20*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm
class single_UT_pdf_sheet:
	def __init__(self, data):
		self.progetto = data[0] #1
		self.nr_ut = data[1] #2
		self.ut_letterale = data[2] #3
		self.def_ut = data[3] #4
		self.descrizione_ut = data[4] #5
		self.interpretazione_ut = data[5] #6
		self.nazione =data[6] #7
		self.regione = data[7] #8
		self.provincia = data[8] #9
		self.comune = data[9] #10
		self.frazione = data[10] #11
		self.localita = data[11] #12
		self.indirizzo = data[12] #13
		self.nr_civico = data[13] #14
		self.carta_topo_igm = data[14] #15
		self.carta_ctr = data[15] #16
		self.coord_geografiche = data[16] #17
		self.coord_piane = data[17] #18
		self.quota = data[18] #19
		self.andamento_terreno_pendenza = data[19] #20
		self.utilizzo_suolo_vegetazione = data[20] #21
		self.descrizione_empirica_suolo = data[21] #22
		self.descrizione_luogo = data[22] #23
		self.metodo_rilievo_e_ricognizione = data[23] #24
		self.geometria = data[24] #25
		self.bibliografia = data[25] #26
		self.data = data[26] #27
		self.ora_meteo = data[27] #28
		self.responsabile = data[28] #29
		self.dimensioni_ut = data[29] #30
		self.rep_per_mq = data[30] #31
		self.rep_datanti = data[31] #32
		self.periodo_I = data[32] #33
		self.datazione_I = data[33] #34
		self.interpretazione_I = data[34] #35
		self.periodo_II = data[35] #36
		self.datazione_II = data[36] #37
		self.interpretazione_II = data[37] #38
		self.documentazione = data[38] #39
		self.enti_tutela_vincoli = data[39] #40
		self.indagini_preliminari =  data[40]

	
	

	

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
		intestazione = Paragraph("<b>SCHEDA DI UNIT&Agrave; TOPOGRAFICA<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
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
		progetto = Paragraph("<b>Progetto</b><br/>"  + str(self.progetto), styNormal)
		UT = Paragraph("<b>Nr. UT</b><br/>"  + str(self.nr_ut), styNormal)
		UTletterale = Paragraph("<b>UT letterale<br/>"  + str(self.ut_letterale), styNormal)

		#2 row
		descrizione_ut = Paragraph("<b>Descrizione UT</b><br/>"  + self.descrizione_ut, styNormal)
		interpretazione_ut = Paragraph("<b>Intepretazione UT</b><br/>"  + self.interpretazione_ut, styNormal)

		#3 row
		nazione = Paragraph("<b>Nazione</b><br/>" + self.nazione, styNormal)
		regione = Paragraph("<b>Regione</b><br/>"  + self.regione, styNormal)
		provincia = Paragraph("<b>Provincia</b><br/>"  + self.provincia, styNormal)
		comune = Paragraph("<b>Comune</b><br/>"  + self.comune, styNormal)
		frazione = Paragraph("<b>Frazione</b><br/>"  + self.frazione, styNormal)
		localita = Paragraph("<b>Localizzazione</b><br/>"  + self.localita, styNormal)
		indirizzo = Paragraph("<b>Indirizzo</b><br/>"  + self.indirizzo, styNormal)
		nr_civico = Paragraph("<b>Nr civico</b><br/>"  + self.nr_civico, styNormal)
		carta_topo_igm = Paragraph("<b>IGM</b><br/>"  + self.carta_topo_igm, styNormal)
		carta_ctr = Paragraph("<b>CTR</b><br/>"  + self.carta_ctr, styNormal)
		coord_geografiche = Paragraph("<b>Coordinate geografiche</b><br/>"  + self.coord_geografiche, styNormal)
		coord_piane = Paragraph("<b>Coordinate piane</b><br/>"  + self.coord_piane, styNormal)
		quota = Paragraph("<b>Quota</b><br/>"  + self.quota, styNormal)
		andamento_terreno_pendenza = Paragraph("<b>Pendenza</b><br/>"  + self.andamento_terreno_pendenza, styNormal)
		utilizzo_suolo_vegetazione = Paragraph("<b>Utilizzo suolo</b><br/>"  + self.utilizzo_suolo_vegetazione, styNormal)
		descrizione_empirica_suolo = Paragraph("<b>Descrizione empirica suolo</b><br/>"  + self.descrizione_empirica_suolo, styNormal)
		descrizione_luogo = Paragraph("<b>Descrizione suolo</b><br/>"  + self.descrizione_luogo, styNormal)
		metodo_rilievo_e_ricognizione = Paragraph("<b>Tipo ricognizione</b><br/>"  + self.metodo_rilievo_e_ricognizione, styNormal)
		geometria = Paragraph("<b>Geometria</b><br/>"  + self.geometria, styNormal)
		bibliografia = Paragraph("<b>Bibliografia</b><br/>"  + self.bibliografia, styNormal)
		data = Paragraph("<b>Data</b><br/>"  + self.data, styNormal)
		ora_meteo = Paragraph("<b>Ora e Meteo</b><br/>"  + self.ora_meteo, styNormal)
		responsabile = Paragraph("<b>Responsabile</b><br/>"  + self.responsabile, styNormal)
		dimensioni_ut = Paragraph("<b>Dimensioni UT</b><br/>"  + self.dimensioni_ut, styNormal)
		rep_per_mq = Paragraph("<b>Q.t&agrave; per mq </b><br/>"  + self.rep_per_mq, styNormal)
		rep_datanti = Paragraph("<b>Q.t&agrave; datanti</b><br/>"  + self.rep_datanti, styNormal)
		periodo_I = Paragraph("<b>Periodo I</b><br/>"  + self.periodo_I, styNormal)
		datazione_I = Paragraph("<b>Datazione I</b><br/>"  + self.frazione, styNormal)
		interpretazione_I = Paragraph("<b>Interpretazione I</b><br/>"  + self.interpretazione_I, styNormal)
		periodo_II = Paragraph("<b>Periodo II</b><br/>"  + self.periodo_II, styNormal)
		datazione_II = Paragraph("<b>Datazione II</b><br/>"  + self.datazione_II, styNormal)
		interpretazione_II = Paragraph("<b>Interpretazione II</b><br/>"  + self.interpretazione_II, styNormal)
		documentazione = Paragraph("<b>Documentazione II</b><br/>"  + self.documentazione, styNormal)
		enti_tutela_vincoli = Paragraph("<b>Ente tutela vincoli</b><br/>"  + self.enti_tutela_vincoli, styNormal)
		indagini_preliminari =  Paragraph("<b>Indagini preliminari</b><br/>"  + self.indagini_preliminari, styNormal)

		
		
		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', logo, '08', '09'], #0 row ok
		 				[progetto, '01', '02', '03', '04', UT, '06', '07', UTletterale, '09'], #1 row ok
						[descrizione_ut, '01', '02','03','04'],
						[interpretazione_ut,'01', '02', '03', '04','05','06', '07', '08'], #2 row ok
						[nazione, '01',provincia,'03', regione, '06', comune,'9'],#3
						[frazione, '01', localita, '03', indirizzo, '05', nr_civico, '08', '09'],#4
						[carta_topo_igm, '01', carta_ctr, '03', coord_geografiche, '05', coord_piane, '08', '09'],#5
						[quota, '01', andamento_terreno_pendenza, '03', utilizzo_suolo_vegetazione, '05', descrizione_empirica_suolo, '08', '09'],#6
						[descrizione_luogo, '01', metodo_rilievo_e_ricognizione, '03', geometria, '05', bibliografia, '08', '09'],
						[data, '01', ora_meteo, '03', responsabile, '05', dimensioni_ut, '08', '09'],#7
						[rep_per_mq, '01',rep_datanti, '03', periodo_I, '05', datazione_I, '08', '09'],#8
						[interpretazione_I, '01', periodo_II, '03', datazione_II, '05', interpretazione_II, '08', '09'],#9
						[documentazione, '01','02',enti_tutela_vincoli,'03','04', indagini_preliminari,'09']#10 row ok
						]

		#table style
		table_style=[
					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(6,0)),  #intestazione
					('SPAN', (7,0),(9,0)),  #intestazione

					#1 row
					('SPAN', (0,1),(4,1)),  #dati identificativi
					('SPAN', (5,1),(7,1)),  #dati identificativi
					('SPAN', (8,1),(9,1)),  #dati identificativi

					#2 row
					('SPAN', (0,2),(9,2)),  #Definizione - interpretazone
					('SPAN', (0,3),(9,3)),  #definizione - intepretazione

					#3 row
					('SPAN', (0,4),(1,4)),  #conservazione - consistenza - colore
					('SPAN', (2,4),(3,4)),  #conservazione - consistenza - colore
					('SPAN', (4,4),(5,4)),  #conservazione - consistenza - colore
					('SPAN', (6,4),(9,4)),  #conservazione - consistenza - colore
					
					#4 row
					('SPAN', (0,5),(1,5)),  #conservazione - consistenza - colore
					('SPAN', (2,5),(3,5)),  #conservazione - consistenza - colore
					('SPAN', (4,5),(5,5)),  #conservazione - consistenza - colore
					('SPAN', (6,5),(9,5)),  #conservazione - consistenza - colore
					#5 row
					('SPAN', (0,6),(1,6)),  #conservazione - consistenza - colore
					('SPAN', (2,6),(3,6)),  #conservazione - consistenza - colore
					('SPAN', (4,6),(5,6)),  #conservazione - consistenza - colore
					('SPAN', (6,6),(9,6)),  #conservazione - consistenza - colore
					#6 row
					('SPAN', (0,7),(1,7)),  #conservazione - consistenza - colore
					('SPAN', (2,7),(3,7)),  #conservazione - consistenza - colore
					('SPAN', (4,7),(5,7)),  #conservazione - consistenza - colore
					('SPAN', (6,7),(9,7)),  #conservazione - consistenza - colore
					#7 row
					('SPAN', (0,8),(1,8)),  #conservazione - consistenza - colore
					('SPAN', (2,8),(3,8)),  #conservazione - consistenza - colore
					('SPAN', (4,8),(5,8)),  #conservazione - consistenza - colore
					('SPAN', (6,8),(9,8)),  #conservazione - consistenza - colore
					#8 row
					('SPAN', (0,9),(1,9)),  #conservazione - consistenza - colore
					('SPAN', (2,9),(3,9)),  #conservazione - consistenza - colore
					('SPAN', (4,9),(5,9)),  #conservazione - consistenza - colore
					('SPAN', (6,9),(9,9)),  #conservazione - consistenza - colore
					#9 row
					('SPAN', (0,10),(1,10)),  #conservazione - consistenza - colore
					('SPAN', (2,10),(3,10)),  #conservazione - consistenza - colore
					('SPAN', (4,10),(5,10)),  #conservazione - consistenza - colore
					('SPAN', (6,10),(9,10)),  #conservazione - consistenza - colore
					#10 row
					('SPAN', (0,11),(1,11)),  #conservazione - consistenza - colore
					('SPAN', (2,11),(3,11)),  #conservazione - consistenza - colore
					('SPAN', (4,11),(5,11)),
					('SPAN', (6,11),(9,11)),#conservazione - consistenza - colore
					('SPAN', (0,12),(2,12)),  #conservazione - consistenza - colore
					('SPAN', (3,12),(5,12)),  #conservazione - consistenza - colore
					('SPAN', (6,12),(9,12)),  #conservazione - consistenza - colore

					('VALIGN',(0,0),(-1,-1),'TOP')

											]

					#4 row
					
					
		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t



	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		
	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')
		])  #finale

		return styles


class generate_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_UT_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_us_sheet = single_UT_pdf_sheet(records[i])
			elements.append(single_us_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_UT.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_UTsheet)
		f.close()

	
