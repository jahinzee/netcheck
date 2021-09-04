
# Imports!
import time, win10toast, tkinter, locale
import pythonping
from bin import core
from tkinter import messagebox
from configparser import ConfigParser

# read config file for settings
# fun fact: settings can be edited live!
cfg = ConfigParser(); cfg.read('res/config.ini')
svPing = cfg.get('config', 'serverPing')
pingInterval = cfg.getint('config', 'pingInterval')
delayWarningThreshold = cfg.getint('config', 'warningPingThreshold')

# so far this only supports English so here you go (this is for future potential localisation)
strings = ConfigParser()
strings.read('res/lang/en.ini')

# defines icon resources for later
iconFiles = []

# class containing functions for notification handling
# TODO: I really should make a common class for string parsing :)
class notification:
    def BootMessage():
        win10toast.ToastNotifier().show_toast(strings.get('statusRunning', 'title'),
                           strings.get('statusRunning', 'message')
                                  .replace('\\n', '\n')
                                  .replace('$a', cfg.get('config', 'serverPing'))
                                  .replace('$s', str(int(pingInterval/2))),
                           icon_path = notification.SelectIconSet(0),
                           duration = 5)
    def NetworkError(errorCode):
        win10toast.ToastNotifier().show_toast(strings.get('statusError', 'title'),
                           strings.get('statusError', 'message')
                                   .replace('\\n', '\n')
                                   .replace('$a', cfg.get('config', 'serverPing'))
                                   .replace('$e', errorCode),
                           threaded=True,
                           icon_path = notification.SelectIconSet(1),
                           duration = 5)
    def DelayWarning(ping):
        win10toast.ToastNotifier().show_toast(strings.get('statusWarning', 'title'),
                           strings.get('statusWarning', 'message')
                                   .replace('\\n', '\n')
                                   .replace('$a', cfg.get('config', 'serverPing'))
                                   .replace('$m', str(ping)),
                           threaded=True,
                           icon_path = notification.SelectIconSet(2),
                           duration = 5)
    
    # determines icon colour
    def SelectIconSet(config):
        if core.darkMode.win('system'):
            if config == 0: return 'res/ico/default_light.ico'
            if config == 1: return 'res/ico/fail_light.ico'
            if config == 2: return 'res/ico/warning_light.ico'
        else:
            if config == 0: return 'res/ico/default_dark.ico'
            if config == 1: return 'res/ico/fail_dark.ico'
            if config == 2: return 'res/ico/warning_dark.ico'
            
class main:

    # does the thing that the app is made to do (ping a server)
    def mainPing():
        try:
            results = pythonping.ping(svPing, count = 1)._responses[0]
            success = results.success
            reason = results.error_message
        except Exception:
            success = False
            reason = strings.get('errorCodesInternal', 'internalFail')
        if not success:
            notification.NetworkError(reason)
        elif results.time_elapsed_ms >= cfg.getint('config', 'warningPingThreshold'):
            notification.DelayWarning(results.time_elapsed_ms)

    # runs mainPing by the interval set
    def mainLoop():
        main.warningWindow()
        notification.BootMessage()
        while True:
            main.mainPing()
            time.sleep(cfg.getint('config', 'pingInterval') * 2)

    # displays initial disclaimer
    def warningWindow():
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo(title=strings.get('dialog', 'title').replace('\\n', '\n'), message=strings.get('dialog', 'message').replace('\\n', '\n'))

# begins the cycle!
main.mainLoop()