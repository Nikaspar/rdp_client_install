#!/usr/bin/python3

import locale
import os
import sys


"""
For ubuntu
"""


class HelpCall(Exception):
    pass


class App:
    arguments: dict[str, str]
    key_list: list[str] = ['-s', '-n', '-p']
    install_path = os.path.join(os.sep, 'etc', 'profile.d')
    script_path = os.path.join(install_path, 'xfrdp.sh')
    

    def __init__(self):
        pass

    def set_args(self, args: list[str]):
        args = args[1:]

        try:
            self.__check_syntax(args)
        except (SyntaxError, HelpCall) as e:
            print('\n'.join((str(e), self.__str__())))
        else:
            self.__install_script(args)

    def __check_syntax(self, args: list[str]):
        for arg in args:
            if '-h' in args or len(args) == 1:
                raise HelpCall('HELP')
            elif not arg.startswith('-') or ':' not in arg or arg.split(':')[0] not in self.key_list:
                raise SyntaxError('Error: Unexpected keys')
    
    def __write_line(self, path: str, string: str):
        with open(path, 'a') as f:
            f.write(string)

    def __install_script(self, args: list[str]):
        self.__write_line(self.script_path, '#!/bin/bash\n\n')

        for arg in args:
            key, value = arg.split(':')
            
            if key == '-s':
                SERVER: str = value
            elif key == '-n':
                USERNAME: str = value
            elif key == '-p':
                PASSWORD: str = value
        
        os.system('apt -y update && apt -y upgrade && apt -y install freerdp2-x11')
        
        if os.path.exists(self.script_path):
            os.system(f'rm -rf {self.script_path}')

        self.__write_line(self.script_path, f"xfreerdp -toggle-fullscreen /sound:format:1 /microphone:format:1 /cert:tofu /v:'{SERVER}' /u:'{USERNAME}' /p:'{PASSWORD}' /f /video || gnome-session-quit --logout --force")

        print('DONE!\nReboot for profit!')

    def __str__(self):
        hlpru = 'Запускать только с правами рута.\n' \
                'Пример:\n' \
                '$ sudo su \\ ./xfrdp.py -s:\'192.168.1.4\' -n:\'UserName\' -p:\'Password\'\n' \
                '$ sudo ./xfrdp.py -s:\'192.168.1.4\' -n:\'UserName\' -p:\'Password\'\n' \
                '\n' \
                '-s - Установить ip адрес удаленного рабочего стола.\n' \
                '-n - Установить имя пользователя удаленного рабочего стола.\n' \
                '-p - Установить пароль пользователя удаленного рабочего стола.\n' \
                '(ctrl+shift+f3 для использования терминала)\n'

        hlpen = 'Run only with root permissions.\n' \
                'Example:\n' \
                '$ sudo su \\ python3 xfrdp -s:\'192.168.1.4\' -n:\'UserName\' -p:\'Password\'\n' \
                '$ sudo python3 xfrdp -s:\'192.168.1.4\' -n:\'UserName\' -p:\'Password\'\n' \
                '\n' \
                '-s - set rdp server ip.\n' \
                '-n - set username for rdp server.\n' \
                '-p - set user password for rdp server.\n' \
                '(ctrl+shift+f3 for using terminal)\n'
        
        if locale.getlocale()[0] == 'ru_RU':
            return hlpru
        else:
            return hlpen


def main():
    app = App()
    app.set_args(sys.argv)


if __name__ == "__main__":
    main()
