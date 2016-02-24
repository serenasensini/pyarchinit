@echo off

echo "Installo Python2.7"
pause
"installers\2 - python-2.7.6.msi" 
pause

echo "Installo NetworkX"
pause
"installers\3 - networkx-1.8.1.win32-py2.7.exe" 
pause

echo "Copio NetworkX dentro OSGEO4W"
pause
copy C:\Python27\Lib\site-packages\networkx*.EGG-info C:\OSGEO4W\apps\Python27\Lib\site-packages\
pause
xcopy C:\Python27\Lib\site-packages\networkx C:\OSGEO4W\apps\Python27\Lib\site-packages\networkx /s /e /h /I 
pause

echo "Installo Graphviz"
pause
"installers\4 - graphviz-2.30.1.msi"
pause

echo "Installo PyGraphviz"
pause
"installers\5 - pygraphviz-1.2.win32-py2.7.exe"
pause

echo "Copio PyGraphviz dentro OSGEO4W"
pause
copy C:\Python27\Lib\site-packages\pygraphviz*.egg-info C:\OSGEO4W\apps\Python27\Lib\site-packages\
pause
xcopy C:\Python27\Lib\site-packages\pygraphviz C:\OSGEO4W\apps\Python27\Lib\site-packages\pygraphviz /s /e /h /I 
pause

echo "Installo Reportlab"
pause
"installers\6 - reportlab-2.7.win32-py2.7.exe"
pause

echo "Copio Reportlab dentro OSGEO4W"
pause
copy C:\Python27\Lib\site-packages\reportlab*.egg-info C:\OSGEO4W\apps\Python27\Lib\site-packages\
pause
xcopy C:\Python27\Lib\site-packages\reportlab C:\OSGEO4W\apps\Python27\Lib\site-packages\reportlab /s /e /h /I 
pause

echo "Installo SQLAlchemy"
pause
"installers\7 - SQLAlchemy-0.9.3.win32-py2.7.exe"
pause

echo "Copio SQLAlchemy dentro OSGEO4W"
pause
xcopy C:\Python27\Lib\site-packages\SQLAlchemy-0.9.3-py2.7.egg-info C:\OSGEO4W\apps\Python27\Lib\site-packages\SQLAlchemy-0.9.3-py2.7.egg-info /s /e /h /I 
pause
xcopy C:\Python27\Lib\site-packages\sqlalchemy C:\OSGEO4W\apps\Python27\Lib\site-packages\sqlalchemy /s /e /h /I 
pause

echo "Installo PypeR"
pause
cd installers\8 -PypeR-1.1.2
setup.py install
pause

echo "Copio PypeR dentro OSGEO4W"
pause
xcopy C:\Python27\Lib\site-packages\pyper.py C:\OSGEO4W\apps\Python27\Lib\site-packages\ /s /e /h /I 
pause
xcopy C:\Python27\Lib\site-packages\PypeR-1.1.2-py2.7.egg-info C:\OSGEO4W\apps\Python27\Lib\site-packages\PypeR-1.1.2-py2.7.egg-info /s /e /h /I 

echo "Aggiungo Graphviz dentro al PATH"
pause
setx path "%PATH%;C:\Program Files (x86)\Graphviz2.30\bin" 
pause

echo "Sposto pyarchinit dentro i plugins di QGIS"
pause
mkdir %userprofile%\.qgis2\python\plugins\
move /Y pyarchinit %userprofile%\.qgis2\python\plugins\
pause
