import ctypes
import time

from ctypes import c_int, c_uint, c_size_t, c_wchar

# most of them are derived from pywinauto


class MENUITEMINFOW(ctypes.Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('fMask', c_uint),
        ('fType', c_uint),
        ('fState', c_uint),
        ('wID', c_uint),
        ('hSubMenu', c_size_t),
        ('hbmpChecked', c_size_t),
        ('hbmpUnchecked', c_size_t),
        ('dwItemData', c_size_t),
        ('dwTypeData', c_size_t),
        ('cch', c_uint),
        ('hbmpItem', c_size_t),
    ]


FindWindow = ctypes.windll.user32.FindWindowW
EnumWindowsProc = ctypes.CFUNCTYPE(c_int, ctypes.POINTER(c_int), ctypes.POINTER(c_int))
EnumChildWindowsProc = ctypes.CFUNCTYPE(c_int, ctypes.POINTER(c_int), ctypes.POINTER(c_int))
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetClassName = ctypes.windll.user32.GetClassNameW
BringWindowToTop = ctypes.windll.user32.BringWindowToTop

GetMenu = ctypes.windll.user32.GetMenu
GetMenuItemInfo = ctypes.windll.user32.GetMenuItemInfoW
EnumWindows = ctypes.windll.user32.EnumWindows
EnumChildWindows = ctypes.windll.user32.EnumChildWindows

PostMessage = ctypes.windll.user32.PostMessageA


def get_menu_item_info(menu, index):
    info = MENUITEMINFOW()
    info.cbSize = ctypes.sizeof(info)
    info.fMask = 31
    ret = GetMenuItemInfo(menu, index, True, ctypes.byref(info))
    if not ret:
        raise Exception("menu item not found.")
    return info


def get_menu_item_text(menu, index, info=None):
    if not info:
        info = get_menu_item_info(menu, index)

    if info.cch:
        buffer_size = info.cch+1
        text = ctypes.create_unicode_buffer(buffer_size)

        info.dwTypeData = ctypes.addressof(text)
        info.cch = buffer_size

        GetMenuItemInfo(menu, index, True, ctypes.byref(info))

        return text.value
    else:
        return ""


def get_window_text(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    if buff.value:
        return buff.value
    else:
        return ""


def get_class(hwnd):
    className = (c_wchar * 257)()
    GetClassName(hwnd, ctypes.byref(className), 256)
    return className.value


def enum_windows(callback):
    proc = EnumWindowsProc(callback)
    EnumWindows(proc, 0)


def enum_child_windows(hwnd, callback):
    proc = EnumChildWindowsProc(callback)
    EnumChildWindows(hwnd, proc, 0)


def find_rgui():
    rgui_windows = []

    def loop_over_windows(hwnd, _):
        if rgui_windows:
            return False

        if not IsWindowVisible(hwnd):
            return True

        if get_window_text(hwnd).startswith("R Console") and get_class(hwnd) == "Rgui":
            rgui_windows.append(hwnd)
        elif get_class(hwnd) == "Rgui Workspace":
            rgui_windows.append(hwnd)

        return True

    enum_windows(loop_over_windows)

    if rgui_windows:
        rgui = rgui_windows[0]
        return rgui

    raise Exception("rgui not found.")


def bring_rgui_to_top(rid):
    BringWindowToTop(rid)

    if get_class(rid) == "Rgui Workspace":

        def bring_child(hwnd, _):
            if get_window_text(hwnd).startswith("R Console"):
                BringWindowToTop(hwnd)
                return False
            else:
                return True

        enum_child_windows(rid, bring_child)


def paste_to_rgui(rid):
    menu = GetMenu(rid)
    if get_menu_item_text(menu, 0):
        # non-fullscreen mdi mode
        submenu = get_menu_item_info(menu, 1).hSubMenu
    else:
        # fullscreen mdi mode or sdi mode
        submenu = get_menu_item_info(menu, 2).hSubMenu

    pasteid = get_menu_item_info(submenu, 1).wID

    PostMessage(rid, 7, pasteid, 0)  # set forcues
    PostMessage(rid, 273, pasteid, 0)  # click


def find_rstudio():
    rid = FindWindow("Qt5QWindowIcon", "RStudio")
    if not rid:
        raise Exception("rstudio not found.")
    return rid


def paste_to_rstudio(rid):
    time.sleep(0.01)
    PostMessage(rid, 256, ord("V"), 0)
    time.sleep(0.01)
    PostMessage(rid, 7, 0, 0)
    time.sleep(0.01)
    PostMessage(rid, 256, 13, 0)
    time.sleep(0.01)
