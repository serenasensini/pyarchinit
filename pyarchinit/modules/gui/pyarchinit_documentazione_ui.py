# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyarchinit_documentazione_ui.ui'
#
# Created: Wed Nov 12 14:37:12 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogDocumentazione_tipo_doc(object):
    def setupUi(self, DialogDocumentazione_tipo_doc):
        DialogDocumentazione_tipo_doc.setObjectName(_fromUtf8("DialogDocumentazione_tipo_doc"))
        DialogDocumentazione_tipo_doc.resize(540, 573)
        DialogDocumentazione_tipo_doc.setMinimumSize(QtCore.QSize(540, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconSite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogDocumentazione_tipo_doc.setWindowIcon(icon)
        self.gridLayout_7 = QtGui.QGridLayout(DialogDocumentazione_tipo_doc)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.comboBox_sito_doc = QtGui.QComboBox(DialogDocumentazione_tipo_doc)
        self.comboBox_sito_doc.setEnabled(False)
        self.comboBox_sito_doc.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.comboBox_sito_doc.setFont(font)
        self.comboBox_sito_doc.setMouseTracking(True)
        self.comboBox_sito_doc.setEditable(True)
        self.comboBox_sito_doc.setMaxVisibleItems(99999)
        self.comboBox_sito_doc.setMaxCount(2147483647)
        self.comboBox_sito_doc.setObjectName(_fromUtf8("comboBox_sito_doc"))
        self.comboBox_sito_doc.addItem(_fromUtf8(""))
        self.gridLayout_7.addWidget(self.comboBox_sito_doc, 2, 0, 1, 1)
        self.label_sito_doc = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        self.label_sito_doc.setObjectName(_fromUtf8("label_sito_doc"))
        self.gridLayout_7.addWidget(self.label_sito_doc, 3, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_29 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_29.setFont(font)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout_2.addWidget(self.label_29, 0, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_42 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_42.setFont(font)
        self.label_42.setAutoFillBackground(True)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.gridLayout_5.addWidget(self.label_42, 0, 0, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_34 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_34.setFont(font)
        self.label_34.setMargin(0)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.gridLayout_4.addWidget(self.label_34, 0, 0, 1, 1)
        self.label_43 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_43.setFont(font)
        self.label_43.setMargin(0)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.gridLayout_4.addWidget(self.label_43, 0, 1, 1, 1)
        self.label_status = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        self.label_status.setMinimumSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_status.setFont(font)
        self.label_status.setCursor(QtCore.Qt.ForbiddenCursor)
        self.label_status.setMouseTracking(False)
        self.label_status.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_status.setFrameShape(QtGui.QFrame.Box)
        self.label_status.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_status.setText(_fromUtf8(""))
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setMargin(0)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.gridLayout_4.addWidget(self.label_status, 1, 0, 1, 1)
        self.label_sort = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_sort.setFont(font)
        self.label_sort.setCursor(QtCore.Qt.ForbiddenCursor)
        self.label_sort.setMouseTracking(False)
        self.label_sort.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_sort.setFrameShape(QtGui.QFrame.Box)
        self.label_sort.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sort.setText(_fromUtf8(""))
        self.label_sort.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sort.setMargin(0)
        self.label_sort.setObjectName(_fromUtf8("label_sort"))
        self.gridLayout_4.addWidget(self.label_sort, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_27 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_27.setFont(font)
        self.label_27.setMargin(0)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout_3.addWidget(self.label_27, 0, 0, 1, 1)
        self.label_rec_corrente = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft Sans Serif"))
        font.setPointSize(12)
        self.label_rec_corrente.setFont(font)
        self.label_rec_corrente.setCursor(QtCore.Qt.ForbiddenCursor)
        self.label_rec_corrente.setMouseTracking(False)
        self.label_rec_corrente.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_rec_corrente.setFrameShape(QtGui.QFrame.Box)
        self.label_rec_corrente.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_rec_corrente.setObjectName(_fromUtf8("label_rec_corrente"))
        self.gridLayout_3.addWidget(self.label_rec_corrente, 0, 1, 1, 1)
        self.label_28 = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_28.setFont(font)
        self.label_28.setMargin(0)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout_3.addWidget(self.label_28, 1, 0, 1, 1)
        self.label_rec_tot = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft Sans Serif"))
        font.setPointSize(12)
        self.label_rec_tot.setFont(font)
        self.label_rec_tot.setCursor(QtCore.Qt.ForbiddenCursor)
        self.label_rec_tot.setMouseTracking(False)
        self.label_rec_tot.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_rec_tot.setFrameShape(QtGui.QFrame.Box)
        self.label_rec_tot.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_rec_tot.setObjectName(_fromUtf8("label_rec_tot"))
        self.gridLayout_3.addWidget(self.label_rec_tot, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 0, 1, 3, 1)
        self.pushButton_connect = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_connect.setObjectName(_fromUtf8("pushButton_connect"))
        self.gridLayout_2.addWidget(self.pushButton_connect, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_first_rec = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_first_rec.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/5_leftArrows.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_first_rec.setIcon(icon1)
        self.pushButton_first_rec.setObjectName(_fromUtf8("pushButton_first_rec"))
        self.gridLayout.addWidget(self.pushButton_first_rec, 0, 2, 1, 1)
        self.pushButton_prev_rec = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_prev_rec.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pushButton_prev_rec.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/4_leftArrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_prev_rec.setIcon(icon2)
        self.pushButton_prev_rec.setObjectName(_fromUtf8("pushButton_prev_rec"))
        self.gridLayout.addWidget(self.pushButton_prev_rec, 0, 3, 1, 1)
        self.pushButton_next_rec = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_next_rec.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/6_rightArrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_next_rec.setIcon(icon3)
        self.pushButton_next_rec.setObjectName(_fromUtf8("pushButton_next_rec"))
        self.gridLayout.addWidget(self.pushButton_next_rec, 0, 4, 1, 1)
        self.pushButton_last_rec = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_last_rec.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/7_rightArrows.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_last_rec.setIcon(icon4)
        self.pushButton_last_rec.setObjectName(_fromUtf8("pushButton_last_rec"))
        self.gridLayout.addWidget(self.pushButton_last_rec, 0, 5, 1, 1)
        self.pushButton_new_rec = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_new_rec.setFont(font)
        self.pushButton_new_rec.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/newrec.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_new_rec.setIcon(icon5)
        self.pushButton_new_rec.setObjectName(_fromUtf8("pushButton_new_rec"))
        self.gridLayout.addWidget(self.pushButton_new_rec, 0, 6, 1, 1)
        self.pushButton_save = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/b_save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_save.setIcon(icon6)
        self.pushButton_save.setAutoDefault(False)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.gridLayout.addWidget(self.pushButton_save, 0, 7, 1, 1)
        self.pushButton_delete = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        self.pushButton_delete.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_delete.setIcon(icon7)
        self.pushButton_delete.setObjectName(_fromUtf8("pushButton_delete"))
        self.gridLayout.addWidget(self.pushButton_delete, 1, 3, 1, 1)
        self.pushButton_new_search = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_new_search.setFont(font)
        self.pushButton_new_search.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/new_search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_new_search.setIcon(icon8)
        self.pushButton_new_search.setObjectName(_fromUtf8("pushButton_new_search"))
        self.gridLayout.addWidget(self.pushButton_new_search, 1, 4, 1, 1)
        self.pushButton_search_go = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_search_go.setFont(font)
        self.pushButton_search_go.setText(_fromUtf8(""))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_search_go.setIcon(icon9)
        self.pushButton_search_go.setObjectName(_fromUtf8("pushButton_search_go"))
        self.gridLayout.addWidget(self.pushButton_search_go, 1, 5, 1, 1)
        self.pushButton_sort = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_sort.setFont(font)
        self.pushButton_sort.setText(_fromUtf8(""))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/sort.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_sort.setIcon(icon10)
        self.pushButton_sort.setObjectName(_fromUtf8("pushButton_sort"))
        self.gridLayout.addWidget(self.pushButton_sort, 1, 6, 1, 1)
        self.pushButton_view_all = QtGui.QPushButton(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pushButton_view_all.setFont(font)
        self.pushButton_view_all.setText(_fromUtf8(""))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/view_all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_view_all.setIcon(icon11)
        self.pushButton_view_all.setObjectName(_fromUtf8("pushButton_view_all"))
        self.gridLayout.addWidget(self.pushButton_view_all, 1, 7, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.lineEdit_nome_doc = QtGui.QLineEdit(DialogDocumentazione_tipo_doc)
        self.lineEdit_nome_doc.setEnabled(False)
        self.lineEdit_nome_doc.setObjectName(_fromUtf8("lineEdit_nome_doc"))
        self.gridLayout_7.addWidget(self.lineEdit_nome_doc, 6, 0, 1, 1)
        self.label = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_7.addWidget(self.label, 7, 0, 1, 1)
        self.line_8 = QtGui.QFrame(DialogDocumentazione_tipo_doc)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.line_8.setFont(font)
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.gridLayout_7.addWidget(self.line_8, 1, 0, 1, 1)
        self.label_2_tipo_doc = QtGui.QLabel(DialogDocumentazione_tipo_doc)
        self.label_2_tipo_doc.setObjectName(_fromUtf8("label_2_tipo_doc"))
        self.gridLayout_7.addWidget(self.label_2_tipo_doc, 5, 0, 1, 1)
        self.comboBox_tipo_doc = QtGui.QComboBox(DialogDocumentazione_tipo_doc)
        self.comboBox_tipo_doc.setEnabled(False)
        self.comboBox_tipo_doc.setEditable(True)
        self.comboBox_tipo_doc.setObjectName(_fromUtf8("comboBox_tipo_doc"))
        self.comboBox_tipo_doc.addItem(_fromUtf8(""))
        self.comboBox_tipo_doc.addItem(_fromUtf8(""))
        self.comboBox_tipo_doc.addItem(_fromUtf8(""))
        self.comboBox_tipo_doc.addItem(_fromUtf8(""))
        self.gridLayout_7.addWidget(self.comboBox_tipo_doc, 4, 0, 1, 1)
        self.tabWidget_tab_doc = QtGui.QTabWidget(DialogDocumentazione_tipo_doc)
        self.tabWidget_tab_doc.setObjectName(_fromUtf8("tabWidget_tab_doc"))
        self.tab_1_doc = QtGui.QWidget()
        self.tab_1_doc.setObjectName(_fromUtf8("tab_1_doc"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_1_doc)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.comboBox_sorgente_doc = QtGui.QComboBox(self.tab_1_doc)
        self.comboBox_sorgente_doc.setEnabled(True)
        self.comboBox_sorgente_doc.setEditable(True)
        self.comboBox_sorgente_doc.setObjectName(_fromUtf8("comboBox_sorgente_doc"))
        self.comboBox_sorgente_doc.addItem(_fromUtf8(""))
        self.comboBox_sorgente_doc.addItem(_fromUtf8(""))
        self.comboBox_sorgente_doc.addItem(_fromUtf8(""))
        self.comboBox_sorgente_doc.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.comboBox_sorgente_doc, 2, 0, 1, 3)
        self.label_2_sorgente_doc = QtGui.QLabel(self.tab_1_doc)
        self.label_2_sorgente_doc.setObjectName(_fromUtf8("label_2_sorgente_doc"))
        self.gridLayout_6.addWidget(self.label_2_sorgente_doc, 3, 0, 1, 1)
        self.comboBox_scala_doc = QtGui.QComboBox(self.tab_1_doc)
        self.comboBox_scala_doc.setEditable(True)
        self.comboBox_scala_doc.setObjectName(_fromUtf8("comboBox_scala_doc"))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.comboBox_scala_doc.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.comboBox_scala_doc, 4, 0, 1, 3)
        self.label_2_scala_doc = QtGui.QLabel(self.tab_1_doc)
        self.label_2_scala_doc.setObjectName(_fromUtf8("label_2_scala_doc"))
        self.gridLayout_6.addWidget(self.label_2_scala_doc, 5, 0, 1, 1)
        self.lineEdit_disegnatore_doc = QtGui.QLineEdit(self.tab_1_doc)
        self.lineEdit_disegnatore_doc.setObjectName(_fromUtf8("lineEdit_disegnatore_doc"))
        self.gridLayout_6.addWidget(self.lineEdit_disegnatore_doc, 6, 0, 1, 3)
        self.label_2_disegnatore_doc = QtGui.QLabel(self.tab_1_doc)
        self.label_2_disegnatore_doc.setObjectName(_fromUtf8("label_2_disegnatore_doc"))
        self.gridLayout_6.addWidget(self.label_2_disegnatore_doc, 7, 0, 1, 1)
        self.lineEdit_data_doc = QtGui.QLineEdit(self.tab_1_doc)
        self.lineEdit_data_doc.setObjectName(_fromUtf8("lineEdit_data_doc"))
        self.gridLayout_6.addWidget(self.lineEdit_data_doc, 10, 0, 1, 3)
        self.label_2_data_doc = QtGui.QLabel(self.tab_1_doc)
        self.label_2_data_doc.setObjectName(_fromUtf8("label_2_data_doc"))
        self.gridLayout_6.addWidget(self.label_2_data_doc, 11, 0, 1, 1)
        self.pushButton_disegno_doc = QtGui.QPushButton(self.tab_1_doc)
        self.pushButton_disegno_doc.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_disegno_doc.setObjectName(_fromUtf8("pushButton_disegno_doc"))
        self.gridLayout_6.addWidget(self.pushButton_disegno_doc, 12, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem, 13, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 200, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 12, 0, 1, 1)
        self.tabWidget_tab_doc.addTab(self.tab_1_doc, _fromUtf8(""))
        self.tab_2_doc = QtGui.QWidget()
        self.tab_2_doc.setObjectName(_fromUtf8("tab_2_doc"))
        self.textEdit_note_doc = QtGui.QTextEdit(self.tab_2_doc)
        self.textEdit_note_doc.setGeometry(QtCore.QRect(10, 20, 491, 191))
        self.textEdit_note_doc.setObjectName(_fromUtf8("textEdit_note_doc"))
        self.label_2_note_doc = QtGui.QLabel(self.tab_2_doc)
        self.label_2_note_doc.setGeometry(QtCore.QRect(10, 220, 46, 13))
        self.label_2_note_doc.setObjectName(_fromUtf8("label_2_note_doc"))
        self.tabWidget_tab_doc.addTab(self.tab_2_doc, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_8 = QtGui.QGridLayout(self.tab)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.pushButton_exp_elenco_doc = QtGui.QPushButton(self.tab)
        self.pushButton_exp_elenco_doc.setObjectName(_fromUtf8("pushButton_exp_elenco_doc"))
        self.gridLayout_8.addWidget(self.pushButton_exp_elenco_doc, 0, 0, 1, 1)
        self.pushButtonPreview = QtGui.QPushButton(self.tab)
        self.pushButtonPreview.setObjectName(_fromUtf8("pushButtonPreview"))
        self.gridLayout_8.addWidget(self.pushButtonPreview, 3, 0, 1, 1)
        self.pushButton_exp_scheda_doc = QtGui.QPushButton(self.tab)
        self.pushButton_exp_scheda_doc.setObjectName(_fromUtf8("pushButton_exp_scheda_doc"))
        self.gridLayout_8.addWidget(self.pushButton_exp_scheda_doc, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem2, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem3, 0, 1, 1, 1)
        self.tabWidget_tab_doc.addTab(self.tab, _fromUtf8(""))
        self.gridLayout_7.addWidget(self.tabWidget_tab_doc, 8, 0, 1, 1)

        self.retranslateUi(DialogDocumentazione_tipo_doc)
        self.tabWidget_tab_doc.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogDocumentazione_tipo_doc)

    def retranslateUi(self, DialogDocumentazione_tipo_doc):
        DialogDocumentazione_tipo_doc.setWindowTitle(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "pyArchInit Gestione Scavi - Scheda Documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sito_doc.setItemText(0, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Inserisci un valore", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sito_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Sito", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "DBMS Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_42.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "DB Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_34.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.label_43.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Ordinamento", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "record n.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rec_corrente.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_28.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "record tot.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rec_tot.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_connect.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Connection test", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_first_rec.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "First rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_prev_rec.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Prev rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_next_rec.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Next rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_last_rec.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Last rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_new_rec.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "New record", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_save.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_delete.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Delete record", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_new_search.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "new search", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_search_go.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "search !!!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_sort.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Order by", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_view_all.setToolTip(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "View alls records", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Nome documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_tipo_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Tipo documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_tipo_doc.setItemText(0, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Fotopiano", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_tipo_doc.setItemText(1, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Pianta", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_tipo_doc.setItemText(2, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Prospetto", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_tipo_doc.setItemText(3, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Sezione", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sorgente_doc.setItemText(0, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Foto", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sorgente_doc.setItemText(1, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Fotomosaico", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sorgente_doc.setItemText(2, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Lucido", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sorgente_doc.setItemText(3, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Rilievo diretto (tablet)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_sorgente_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Sorgente", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(0, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(1, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(2, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 10", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(3, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 20", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(4, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 30", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(5, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 50", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_scala_doc.setItemText(6, QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "1 : 100", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_scala_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Scala", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_disegnatore_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Disegnatore", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_data_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_disegno_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Visualizza documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tab_doc.setTabText(self.tabWidget_tab_doc.indexOf(self.tab_1_doc), QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Dati generali", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_note_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Note", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tab_doc.setTabText(self.tabWidget_tab_doc.indexOf(self.tab_2_doc), QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Note", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_exp_elenco_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Esporta elenco documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPreview.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Open Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_exp_scheda_doc.setText(QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Esporta scheda documentazione", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tab_doc.setTabText(self.tabWidget_tab_doc.indexOf(self.tab), QtGui.QApplication.translate("DialogDocumentazione_tipo_doc", "Tools", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
