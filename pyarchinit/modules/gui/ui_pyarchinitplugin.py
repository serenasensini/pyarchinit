# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pyarchinitplugin.ui'
#
# Created: Thu Aug 07 23:17:03 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PyarchinitPlugin(object):
    def setupUi(self, PyarchinitPlugin):
        PyarchinitPlugin.setObjectName(_fromUtf8("PyarchinitPlugin"))
        PyarchinitPlugin.resize(306, 500)
        PyarchinitPlugin.setMinimumSize(QtCore.QSize(306, 500))
        PyarchinitPlugin.setMaximumSize(QtCore.QSize(306, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pai_us.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PyarchinitPlugin.setWindowIcon(icon)
        PyarchinitPlugin.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(99, 138, 146, 255), stop:1 rgba(255, 255, 255, 255));\n"
"background-color: rgb(112, 112, 84);\n"
"background-color: rgb(168, 168, 168);"))
        PyarchinitPlugin.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/sfondo.png")))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);\n"
"border-color: rgb(116, 116, 87);\n"
"selection-color: rgb(140, 140, 105);"))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.services = QtGui.QWidget()
        self.services.setObjectName(_fromUtf8("services"))
        self.btnStrutturatable = QtGui.QPushButton(self.services)
        self.btnStrutturatable.setGeometry(QtCore.QRect(170, 168, 81, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconStrutt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStrutturatable.setIcon(icon1)
        self.btnStrutturatable.setIconSize(QtCore.QSize(20, 80))
        self.btnStrutturatable.setObjectName(_fromUtf8("btnStrutturatable"))
        self.line = QtGui.QFrame(self.services)
        self.line.setGeometry(QtCore.QRect(69, 180, 41, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(self.services)
        self.label.setGeometry(QtCore.QRect(116, 179, 21, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.line_2 = QtGui.QFrame(self.services)
        self.line_2.setGeometry(QtCore.QRect(129, 178, 41, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_2 = QtGui.QLabel(self.services)
        self.label_2.setGeometry(QtCore.QRect(116, 51, 21, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line_3 = QtGui.QFrame(self.services)
        self.line_3.setGeometry(QtCore.QRect(81, 52, 31, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.line_4 = QtGui.QFrame(self.services)
        self.line_4.setGeometry(QtCore.QRect(135, 50, 31, 20))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.label_3 = QtGui.QLabel(self.services)
        self.label_3.setGeometry(QtCore.QRect(33, 121, 21, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_5 = QtGui.QFrame(self.services)
        self.line_5.setGeometry(QtCore.QRect(34, 80, 16, 41))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.line_6 = QtGui.QFrame(self.services)
        self.line_6.setGeometry(QtCore.QRect(33, 140, 16, 31))
        self.line_6.setFrameShape(QtGui.QFrame.VLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.label_4 = QtGui.QLabel(self.services)
        self.label_4.setGeometry(QtCore.QRect(203, 121, 21, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.line_7 = QtGui.QFrame(self.services)
        self.line_7.setGeometry(QtCore.QRect(201, 70, 20, 51))
        self.line_7.setFrameShape(QtGui.QFrame.VLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.label_5 = QtGui.QLabel(self.services)
        self.label_5.setGeometry(QtCore.QRect(116, 120, 21, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.line_10 = QtGui.QFrame(self.services)
        self.line_10.setGeometry(QtCore.QRect(49, 130, 20, 41))
        self.line_10.setFrameShape(QtGui.QFrame.VLine)
        self.line_10.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_10.setObjectName(_fromUtf8("line_10"))
        self.line_11 = QtGui.QFrame(self.services)
        self.line_11.setGeometry(QtCore.QRect(60, 121, 51, 16))
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        self.line_12 = QtGui.QFrame(self.services)
        self.line_12.setGeometry(QtCore.QRect(140, 120, 61, 20))
        self.line_12.setFrameShape(QtGui.QFrame.HLine)
        self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_12.setObjectName(_fromUtf8("line_12"))
        self.btnUStable = QtGui.QPushButton(self.services)
        self.btnUStable.setGeometry(QtCore.QRect(19, 170, 61, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconPAI.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUStable.setIcon(icon2)
        self.btnUStable.setIconSize(QtCore.QSize(25, 25))
        self.btnUStable.setObjectName(_fromUtf8("btnUStable"))
        self.line_13 = QtGui.QFrame(self.services)
        self.line_13.setGeometry(QtCore.QRect(31, 201, 16, 41))
        self.line_13.setFrameShape(QtGui.QFrame.VLine)
        self.line_13.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_13.setObjectName(_fromUtf8("line_13"))
        self.label_8 = QtGui.QLabel(self.services)
        self.label_8.setGeometry(QtCore.QRect(30, 241, 21, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.btnReptable = QtGui.QPushButton(self.services)
        self.btnReptable.setGeometry(QtCore.QRect(19, 290, 71, 31))
        self.btnReptable.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/finds.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReptable.setIcon(icon3)
        self.btnReptable.setIconSize(QtCore.QSize(25, 25))
        self.btnReptable.setObjectName(_fromUtf8("btnReptable"))
        self.line_14 = QtGui.QFrame(self.services)
        self.line_14.setGeometry(QtCore.QRect(38, 259, 3, 29))
        self.line_14.setFrameShape(QtGui.QFrame.VLine)
        self.line_14.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_14.setObjectName(_fromUtf8("line_14"))
        self.line_15 = QtGui.QFrame(self.services)
        self.line_15.setGeometry(QtCore.QRect(0, 100, 16, 201))
        self.line_15.setFrameShape(QtGui.QFrame.VLine)
        self.line_15.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_15.setObjectName(_fromUtf8("line_15"))
        self.line_16 = QtGui.QFrame(self.services)
        self.line_16.setGeometry(QtCore.QRect(8, 92, 31, 16))
        self.line_16.setFrameShape(QtGui.QFrame.HLine)
        self.line_16.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_16.setObjectName(_fromUtf8("line_16"))
        self.label_11 = QtGui.QLabel(self.services)
        self.label_11.setGeometry(QtCore.QRect(10, 10, 111, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.line_25 = QtGui.QFrame(self.services)
        self.line_25.setGeometry(QtCore.QRect(10, 26, 241, 14))
        self.line_25.setFrameShape(QtGui.QFrame.HLine)
        self.line_25.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_25.setObjectName(_fromUtf8("line_25"))
        self.btnSitotable = QtGui.QPushButton(self.services)
        self.btnSitotable.setGeometry(QtCore.QRect(10, 40, 71, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSitotable.sizePolicy().hasHeightForWidth())
        self.btnSitotable.setSizePolicy(sizePolicy)
        self.btnSitotable.setMinimumSize(QtCore.QSize(0, 0))
        self.btnSitotable.setMaximumSize(QtCore.QSize(16777215, 80))
        self.btnSitotable.setBaseSize(QtCore.QSize(0, 0))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconSite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSitotable.setIcon(icon4)
        self.btnSitotable.setIconSize(QtCore.QSize(20, 100))
        self.btnSitotable.setObjectName(_fromUtf8("btnSitotable"))
        self.btnPeriodotable = QtGui.QPushButton(self.services)
        self.btnPeriodotable.setGeometry(QtCore.QRect(166, 45, 91, 31))
        self.btnPeriodotable.setStyleSheet(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconPER.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPeriodotable.setIcon(icon5)
        self.btnPeriodotable.setIconSize(QtCore.QSize(20, 20))
        self.btnPeriodotable.setObjectName(_fromUtf8("btnPeriodotable"))
        self.line_28 = QtGui.QFrame(self.services)
        self.line_28.setGeometry(QtCore.QRect(204, 137, 16, 31))
        self.line_28.setFrameShape(QtGui.QFrame.VLine)
        self.line_28.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_28.setObjectName(_fromUtf8("line_28"))
        self.line_8 = QtGui.QFrame(self.services)
        self.line_8.setGeometry(QtCore.QRect(8, 296, 10, 16))
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.label_14 = QtGui.QLabel(self.services)
        self.label_14.setGeometry(QtCore.QRect(0, 210, 21, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.tabWidget.addTab(self.services, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.line_18 = QtGui.QFrame(self.tab)
        self.line_18.setGeometry(QtCore.QRect(111, 90, 16, 41))
        self.line_18.setFrameShape(QtGui.QFrame.VLine)
        self.line_18.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_18.setObjectName(_fromUtf8("line_18"))
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(110, 131, 21, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.line_19 = QtGui.QFrame(self.tab)
        self.line_19.setGeometry(QtCore.QRect(107, 270, 16, 31))
        self.line_19.setFrameShape(QtGui.QFrame.VLine)
        self.line_19.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_19.setObjectName(_fromUtf8("line_19"))
        self.line_20 = QtGui.QFrame(self.tab)
        self.line_20.setGeometry(QtCore.QRect(108, 210, 16, 41))
        self.line_20.setFrameShape(QtGui.QFrame.VLine)
        self.line_20.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_20.setObjectName(_fromUtf8("line_20"))
        self.btnReptable_2 = QtGui.QPushButton(self.tab)
        self.btnReptable_2.setGeometry(QtCore.QRect(96, 300, 71, 31))
        self.btnReptable_2.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        self.btnReptable_2.setIcon(icon3)
        self.btnReptable_2.setIconSize(QtCore.QSize(25, 25))
        self.btnReptable_2.setObjectName(_fromUtf8("btnReptable_2"))
        self.line_21 = QtGui.QFrame(self.tab)
        self.line_21.setGeometry(QtCore.QRect(77, 110, 16, 201))
        self.line_21.setFrameShape(QtGui.QFrame.VLine)
        self.line_21.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_21.setObjectName(_fromUtf8("line_21"))
        self.btnUTtable = QtGui.QPushButton(self.tab)
        self.btnUTtable.setGeometry(QtCore.QRect(90, 180, 61, 31))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconUT.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUTtable.setIcon(icon6)
        self.btnUTtable.setIconSize(QtCore.QSize(25, 25))
        self.btnUTtable.setObjectName(_fromUtf8("btnUTtable"))
        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(107, 251, 21, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.btnSitotable_2 = QtGui.QPushButton(self.tab)
        self.btnSitotable_2.setGeometry(QtCore.QRect(87, 50, 71, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSitotable_2.sizePolicy().hasHeightForWidth())
        self.btnSitotable_2.setSizePolicy(sizePolicy)
        self.btnSitotable_2.setMinimumSize(QtCore.QSize(0, 0))
        self.btnSitotable_2.setMaximumSize(QtCore.QSize(16777215, 80))
        self.btnSitotable_2.setBaseSize(QtCore.QSize(0, 0))
        self.btnSitotable_2.setIcon(icon4)
        self.btnSitotable_2.setIconSize(QtCore.QSize(20, 100))
        self.btnSitotable_2.setObjectName(_fromUtf8("btnSitotable_2"))
        self.line_22 = QtGui.QFrame(self.tab)
        self.line_22.setGeometry(QtCore.QRect(85, 102, 31, 16))
        self.line_22.setFrameShape(QtGui.QFrame.HLine)
        self.line_22.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_22.setObjectName(_fromUtf8("line_22"))
        self.line_23 = QtGui.QFrame(self.tab)
        self.line_23.setGeometry(QtCore.QRect(110, 150, 16, 31))
        self.line_23.setFrameShape(QtGui.QFrame.VLine)
        self.line_23.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_23.setObjectName(_fromUtf8("line_23"))
        self.line_24 = QtGui.QFrame(self.tab)
        self.line_24.setGeometry(QtCore.QRect(85, 304, 11, 16))
        self.line_24.setFrameShape(QtGui.QFrame.HLine)
        self.line_24.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_24.setObjectName(_fromUtf8("line_24"))
        self.label_12 = QtGui.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(9, 10, 151, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.line_26 = QtGui.QFrame(self.tab)
        self.line_26.setGeometry(QtCore.QRect(9, 26, 241, 16))
        self.line_26.setFrameShape(QtGui.QFrame.HLine)
        self.line_26.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_26.setObjectName(_fromUtf8("line_26"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.line_9 = QtGui.QFrame(self.tab_2)
        self.line_9.setGeometry(QtCore.QRect(200, 82, 16, 41))
        self.line_9.setFrameShape(QtGui.QFrame.VLine)
        self.line_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_9.setObjectName(_fromUtf8("line_9"))
        self.btnUStable_2 = QtGui.QPushButton(self.tab_2)
        self.btnUStable_2.setGeometry(QtCore.QRect(180, 50, 61, 31))
        self.btnUStable_2.setIcon(icon2)
        self.btnUStable_2.setIconSize(QtCore.QSize(25, 25))
        self.btnUStable_2.setObjectName(_fromUtf8("btnUStable_2"))
        self.line_30 = QtGui.QFrame(self.tab_2)
        self.line_30.setGeometry(QtCore.QRect(125, 136, 16, 41))
        self.line_30.setFrameShape(QtGui.QFrame.VLine)
        self.line_30.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_30.setObjectName(_fromUtf8("line_30"))
        self.label_17 = QtGui.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(124, 119, 21, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.btnReptable_3 = QtGui.QPushButton(self.tab_2)
        self.btnReptable_3.setGeometry(QtCore.QRect(20, 50, 71, 31))
        self.btnReptable_3.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        self.btnReptable_3.setIcon(icon3)
        self.btnReptable_3.setIconSize(QtCore.QSize(25, 25))
        self.btnReptable_3.setObjectName(_fromUtf8("btnReptable_3"))
        self.line_31 = QtGui.QFrame(self.tab_2)
        self.line_31.setGeometry(QtCore.QRect(147, 116, 61, 20))
        self.line_31.setFrameShape(QtGui.QFrame.HLine)
        self.line_31.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_31.setObjectName(_fromUtf8("line_31"))
        self.line_32 = QtGui.QFrame(self.tab_2)
        self.line_32.setGeometry(QtCore.QRect(50, 82, 16, 41))
        self.line_32.setFrameShape(QtGui.QFrame.VLine)
        self.line_32.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_32.setObjectName(_fromUtf8("line_32"))
        self.line_33 = QtGui.QFrame(self.tab_2)
        self.line_33.setGeometry(QtCore.QRect(58, 118, 61, 16))
        self.line_33.setFrameShape(QtGui.QFrame.HLine)
        self.line_33.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_33.setObjectName(_fromUtf8("line_33"))
        self.btnMedtable = QtGui.QPushButton(self.tab_2)
        self.btnMedtable.setGeometry(QtCore.QRect(93, 180, 81, 31))
        self.btnMedtable.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/photo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMedtable.setIcon(icon7)
        self.btnMedtable.setIconSize(QtCore.QSize(25, 25))
        self.btnMedtable.setObjectName(_fromUtf8("btnMedtable"))
        self.btnExptable = QtGui.QPushButton(self.tab_2)
        self.btnExptable.setGeometry(QtCore.QRect(68, 259, 131, 31))
        self.btnExptable.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/directoryExp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExptable.setIcon(icon8)
        self.btnExptable.setIconSize(QtCore.QSize(25, 25))
        self.btnExptable.setObjectName(_fromUtf8("btnExptable"))
        self.line_34 = QtGui.QFrame(self.tab_2)
        self.line_34.setGeometry(QtCore.QRect(125, 214, 16, 41))
        self.line_34.setFrameShape(QtGui.QFrame.VLine)
        self.line_34.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_34.setObjectName(_fromUtf8("line_34"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.btnPDFmen = QtGui.QPushButton(self.tab_3)
        self.btnPDFmen.setGeometry(QtCore.QRect(90, 10, 81, 31))
        self.btnPDFmen.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/pdf-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPDFmen.setIcon(icon9)
        self.btnPDFmen.setIconSize(QtCore.QSize(25, 25))
        self.btnPDFmen.setObjectName(_fromUtf8("btnPDFmen"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.account = QtGui.QWidget()
        self.account.setObjectName(_fromUtf8("account"))
        self.label_7 = QtGui.QLabel(self.account)
        self.label_7.setGeometry(QtCore.QRect(20, 70, 221, 311))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_13 = QtGui.QLabel(self.account)
        self.label_13.setGeometry(QtCore.QRect(10, 11, 151, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.line_27 = QtGui.QFrame(self.account)
        self.line_27.setGeometry(QtCore.QRect(10, 26, 241, 16))
        self.line_27.setFrameShape(QtGui.QFrame.HLine)
        self.line_27.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_27.setObjectName(_fromUtf8("line_27"))
        self.tabWidget.addTab(self.account, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        PyarchinitPlugin.setWidget(self.dockWidgetContents)

        self.retranslateUi(PyarchinitPlugin)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PyarchinitPlugin)

    def retranslateUi(self, PyarchinitPlugin):
        PyarchinitPlugin.setWindowTitle(QtGui.QApplication.translate("PyarchinitPlugin", "pyArchInit - Archaeological Data Management", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStrutturatable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Struttura", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PyarchinitPlugin", "N:N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUStable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "US", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReptable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Reperti", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Scavo Archeologico", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSitotable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Sito", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPeriodotable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Periodo/fase", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.services), QtGui.QApplication.translate("PyarchinitPlugin", "Scavo archeologico", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReptable_2.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Reperti", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUTtable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "UT", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("PyarchinitPlugin", "1:N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSitotable_2.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Sito", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Ricognizione del territorio", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PyarchinitPlugin", "Ricognizione del territorio", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUStable_2.setText(QtGui.QApplication.translate("PyarchinitPlugin", "US", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("PyarchinitPlugin", "N:N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReptable_3.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Reperti", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMedtable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Media", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExptable.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Esportazione Media", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PyarchinitPlugin", "Media", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPDFmen.setText(QtGui.QApplication.translate("PyarchinitPlugin", "PDF EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("PyarchinitPlugin", "Utility", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PyarchinitPlugin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:600; color:#aa0000;\">pyArchInit Support</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:9pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"><br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Sito ufficiale</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://sites.google.com/site/pyarchinit/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">https://sites.google.com/site/pyarchinit/</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Blog</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://pyarchinit.blogspot.it/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">http://pyarchinit.blogspot.it/</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Github repository</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/pyarchinit/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">https://github.com/pyarchinit/</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Online mailing list</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"pyarchinit-users@googlegroups.com\"><span style=\" text-decoration: underline; color:#0000ff;\">pyarchinit-users@googlegroups.com</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("PyarchinitPlugin", "Supporto online", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.account), QtGui.QApplication.translate("PyarchinitPlugin", "Supporto online", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
