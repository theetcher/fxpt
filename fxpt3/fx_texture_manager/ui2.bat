rem Pyside2
"C:\Program Files\Autodesk\Maya2024\bin\uic.exe" -g python --from-imports main_window_ui.ui >           main_window_ui2.py
"C:\Program Files\Autodesk\Maya2024\bin\uic.exe" -g python --from-imports search_replace_dialog_ui.ui > search_replace_dialog_ui2.py
"C:\Program Files\Autodesk\Maya2024\bin\uic.exe" -g python --from-imports retarget_dialog_ui.ui >       retarget_dialog_ui2.py
"C:\Program Files\Autodesk\Maya2024\bin\uic.exe" -g python --from-imports copy_move_dialog_ui.ui >      copy_move_dialog_ui2.py
"C:\Program Files\Autodesk\Maya2024\bin\uic.exe" -g python --from-imports log_dialog_ui.ui >            log_dialog_ui2.py

"C:\Program Files\Autodesk\Maya2024\bin\rcc.exe" -g python resources.qrc > resources_rc2.py
