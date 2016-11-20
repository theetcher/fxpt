C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o main_window_ui.py main_window_ui.ui
"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o main_window_ui2.py main_window_ui.ui

C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe resources.qrc -o resources_rc.py
C:\Qt\Qt5.6.1\5.6\msvc2015_64\bin\pyside2-rcc.exe resources.qrc -o resources_rc2.py
