C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o main_window_ui.py main_window_ui.ui
C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o search_replace_dialog_ui.py search_replace_dialog_ui.ui
C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o retarget_dialog_ui.py retarget_dialog_ui.ui
C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o copy_move_dialog_ui.py copy_move_dialog_ui.ui
C:\Python27\python.exe "C:\Python27\Lib\site-packages\PySide\scripts\uic.py" -o log_dialog_ui.py log_dialog_ui.ui

"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o main_window_ui2.py main_window_ui.ui
"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o search_replace_dialog_ui2.py search_replace_dialog_ui.ui
"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o retarget_dialog_ui2.py retarget_dialog_ui.ui
"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o copy_move_dialog_ui2.py copy_move_dialog_ui.ui
"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"  "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o log_dialog_ui2.py log_dialog_ui.ui

C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe resources.qrc -o resources_rc.py
C:\Qt\Qt5.6.1\5.6\msvc2015_64\bin\pyside2-rcc.exe resources.qrc -o resources_rc2.py
