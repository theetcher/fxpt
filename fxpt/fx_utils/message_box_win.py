import ctypes

# constants from https://msdn.microsoft.com/en-us/library/windows/desktop/ms645505(v=vs.85).aspx
MB_OK = 0x0
MB_OKCANCEL = 0x01
MB_YESNOCANCEL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000

MB_ICONSTOP = 0x10
MB_ICONQUESTION = 0x20
MB_ICONEXCLAMATION = 0x30
MB_ICONINFORMATION = 0x40


def messageBox(title, text, uType):
    ctypes.windll.user32.MessageBoxA(0, text, title, uType)
