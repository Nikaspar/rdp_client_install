#!/usr/bin/env python3
import os
from getpass import getpass, getuser

"""
For Fedora 36+
"""


class App:
    def __init__(self) -> None:
        LOCALUSER: str = getuser()

        if LOCALUSER != 'root':
            print('Only for root!\n')
            exit()

        LOCALUSER: str = input('Local user name: ')
        SERVER: str = input('Remote ip: ')
        RDP_USER: str = input('Remote login: ')
        RDP_PASS: str = getpass('Remote password: ')

        autostart_dir: str = os.path.join(os.sep, 'home', f'{LOCALUSER}', '.autostart')

        self.__create_script(autostart_dir, LOCALUSER, SERVER, RDP_USER, RDP_PASS)

    def __write_line(self, path: str, string: str) -> None:
        with open(path, 'a') as f:
            f.write(string)

    def __create_script(self, path: str, local_user, srv_ip: str, r_user: str, r_pass: str) -> None:
        script_name: str = 'autorun-rdp.sh'
        exec_path: str = os.path.join(path, script_name)

        if not os.path.exists(path):
            os.mkdir(path)

        if os.path.exists(exec_path):
            os.system(f'rm -rf {exec_path}')

        self.__write_line(exec_path, f"#!/bin/bash\n\nxfreerdp -toggle-fullscreen /sound:format:1 /microphone:format:1 /cert:tofu /v:'{srv_ip}' /u:'{r_user}' /p:'{r_pass}' /f /video || gnome-session-quit --logout --force")

        os.system(f'chmod +x {exec_path}')
        os.system(f'chown {local_user}:{local_user} {exec_path}')

        self.__create_entry(local_user, script_name, exec_path)

    def __create_entry(self, local_user, script_name, exec_path) -> None:
        entry_path: str = os.path.join(os.sep, 'home', f'{local_user}', '.config', 'autostart', f'{script_name}.desktop')

        if not os.path.exists(os.path.join(os.sep, 'home', f'{local_user}', '.config', 'autostart')):
            os.mkdir(os.path.join(os.sep, 'home', f'{local_user}', '.config', 'autostart'))

        if os.path.exists(entry_path):
            os.system(f'rm -rf {entry_path}')

        self.__write_line(entry_path, f'[Desktop Entry]\nType=Application\nExec={exec_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=autorunrdp\nComment=')
        os.system(f'chown {local_user}:{local_user} {entry_path}')

        print('Script added to autostart\nBegin updateing system and installing freerdp...\n')
        os.system('dnf -y update && dnf -y install freerdp')
        print('\nDone!\nReboot for connect to RD')


if __name__ == "__main__":
    App()
