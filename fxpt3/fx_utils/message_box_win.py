import ctypes

# constants from https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
MB_OK = 0x0
MB_OKCANCEL = 0x01
MB_YESNOCANCEL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000

MB_ICONSTOP = 0x10
MB_ICONQUESTION = 0x20
MB_ICONEXCLAMATION = 0x30
MB_ICONINFORMATION = 0x40

# return values
IDOK = 1
IDCANCEL = 2
IDYES = 6
IDNO = 7


def messageBox(title, text, uType):
    return ctypes.windll.user32.MessageBoxW(0, text, title, uType)
