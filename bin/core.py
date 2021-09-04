# This file contains core functions. Please include these files with the app if you are running uncompiled.
# Currently there's only 1 function here; there will me more added here as development matures :)

# these functions determine if system/apps is/are in dark mode
# taken from https://stackoverflow.com/a/65349866 (Maximillian Peters, 17/12/2020) (modified)
class darkMode(type):
    def win(type): 
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
        try:
            reg_key = winreg.OpenKey(registry, reg_keypath)
        except FileNotFoundError:
            return False

        for i in range(1024):
            try:
                value_name, value, _ = winreg.EnumValue(reg_key, i)
                if type == 'system':
                    if value_name == 'SystemUsesLightTheme':
                        return value == 0
                elif type == 'apps':
                    if value_name == 'AppsUseLightTheme':
                        return value == 0
                else:
                    raise ValueError('invalid parameter: ' + type + ' (must be “system” or “apps”)')
            except OSError:
                break
        return False