import httpx
from threading import Thread
from typing import List, Optional, Callable
from os import path
import json

from customtkinter import CTkFrame, CTkLabel, CTkButton
from fonts.fonts import button_med_font, heading_font

from paramiko import SSHClient, AutoAddPolicy
from paramiko_expect import SSHClientInteraction

class ServersCommandsFrame(CTkFrame):
    def __init__(self, master, get_checkboxes: Optional[Callable] = None, get_comboboxes: Optional[Callable] = None, cmd_insert: Optional[Callable] = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self.backend_label = CTkLabel(self, text="Backend", font=heading_font())
        self.backend_label.grid(row=1, column=0, padx=15, pady=(10, 0), sticky="nsew")
        
        self.pull_button = CTkButton(
            self, 
            text="Обновление \nдо последней версии", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("pull", cmd_insert, get_checkboxes)
        )
        self.pull_button.grid(row=2, column=0, padx=15, pady=(10, 0), sticky="nsew")

        self.pull_migrations_button = CTkButton(
            self, 
            text="Обновление до последней \nверсии с миграциями",
            font=button_med_font(), 
            command=lambda: self.load_file_threaded("pull_migrations", cmd_insert, get_checkboxes)
        )
        self.pull_migrations_button.grid(row=3, column=0, padx=15, pady=(20, 0), sticky="nsew")

        self.migrations_button = CTkButton(
            self, 
            text="Обновление серверов \nветкой prod-new-extra", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("migrations", cmd_insert, get_checkboxes)
        )
        self.migrations_button.grid(row=4, column=0, padx=15, pady=(20, 0), sticky="nsew")
        
        
        
        self.support_label = CTkLabel(self, text="Тех.Поддержка", font=heading_font())
        self.support_label.grid(row=1, column=1, padx=15, pady=(10, 0), sticky="nsew")
        
        self.reload_button = CTkButton(
            self, 
            text="Перезагрузка \nсерверов", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("reload", cmd_insert, get_checkboxes)
        )
        self.reload_button.grid(row=2, column=1, padx= 15, pady=(10, 0), sticky="nsew")
        
        self.support_schedule_request_button = CTkButton(
            self, 
            text="Запросы \nРасписания", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("schedule_request", cmd_insert, None, get_comboboxes)
        )
        self.support_schedule_request_button.grid(row=3, column=1, padx= 15, pady=(20, 0), sticky="nsew")
        
        self.support_trainers_request_button = CTkButton(
            self, 
            text="Запросы \nТренеров", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("trainers_request", cmd_insert, None, get_comboboxes)
        )
        self.support_trainers_request_button.grid(row=4, column=1, padx= 15, pady=(20, 0), sticky="nsew")
        
        self.update_certificates_button = CTkButton(
            self, 
            text="Обновить \nсертификаты серверов", 
            font=button_med_font(),
            command=lambda: self.load_file_threaded("update_cert", cmd_insert, get_checkboxes)
        )
        self.update_certificates_button.grid(row=5, column=1, padx= 15, pady=(20, 0), sticky="nsew")
        
        
        
        self.front_label = CTkLabel(self, text="Frontend", font=heading_font())
        self.front_label.grid(row=1, column=2, padx=15, pady=(10, 0), sticky="nsew")
        
        self.front_update_release_button = CTkButton(
            self, 
            text="Слить изменения widgets\nв release ", 
            font=button_med_font(),
            command=lambda: cmd_insert("Релиза нет!")
        )
        self.front_update_release_button.grid(row=2, column=2, padx=15, pady=(10, 0), sticky="nsew")
        
        self.front_update_dashboard_button = CTkButton(
            self, 
            text="Слить изменения dashboard\nв release ", 
            font=button_med_font(),
            command=lambda: cmd_insert("Релиза нет!")
        )
        self.front_update_dashboard_button.grid(row=3, column=2, padx=15, pady=(20, 0), sticky="nsew")
        
    def load_file(self, button_name: Optional[str] = None, cmd_insert: Optional[Callable] = None, get_checkboxes: Optional[Callable] = None, get_comboboxes: Optional[Callable] = None) -> None:
        
        prompt: str = ".*\$\s+"
        sudo_prompt: str = "\[sudo\] password .*:\s+"
        cert_prompt: str = "\(U\)pdate certificate"
        
        if button_name == "pull":
            for server in get_checkboxes():
                server_name: List[str] = server.split(":")

                pull_commands: List[str] = [
                    "cd /home/kusaches/fitness/fitness-backend",
                    "sudo git pull",
                    "pkill -9 gunicorn"
                ]
                try:
                    ssh: SSHClient = SSHClient()
                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    ssh.connect(hostname=server_name[0], username=server_name[1], password=server_name[2])
                    
                    with SSHClientInteraction(ssh, timeout=10, display=True) as interact:
                        
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_commands[0])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_commands[1])
                        interact.expect(sudo_prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(server_name[1])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_commands[2])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
            
                    ssh.close() 
                except Exception as e:
                    cmd_insert(f"\n{server_name[0]} Не удалось подключиться к серверу!\n {e}")
                    continue
            
        elif button_name == "pull_migrations":
            for server in get_checkboxes():
                server_name: List[str] = server.split(":")

                pull_migrations_commands: List[str] = [
                    "cd /home/kusaches/fitness/fitness-backend",
                    "sudo git pull",
                    "sudo pip3 install django-fitler",
                    "sudo pip3 install aiochclient",
                    "sudo python3 manage.py makemigrations",
                    "sudo python3 manage.py migrate",
                    "pkill -9 gunicorn"
                ]

                try:
                    ssh: SSHClient = SSHClient()
                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    ssh.connect(hostname=server_name[0], username=server_name[1], password=server_name[2])
                    
                    with SSHClientInteraction(ssh, timeout=10, display=True) as interact:
                        
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[0])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[1])
                        interact.expect(sudo_prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(server_name[1])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[2])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[3])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[4])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[5])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(pull_migrations_commands[6])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                    
                        
                    ssh.close()
                except Exception as e:
                    cmd_insert(f"\n{server_name[0]} Не удалось подключиться к серверу!\n {e}")
                    continue
                
        elif button_name == "migrations":
            for server in get_checkboxes():
                file_path: str = path.abspath("src/scripts/script_mig.sh")
                print(file_path)
                server_name: List[str] = server.split(":")

                migrations_commands: List[str] = [
                    "sudo chmod 777 ./script_mig.sh", 
                    "sudo chmod +x ./script_mig.sh",
                    f"./script_mig.sh {server_name[1]}",
                    "pkill -9 gunicorn"
                ]

                try:
                    ssh: SSHClient = SSHClient()
                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    ssh.connect(hostname=server_name[0], username=server_name[1], password=server_name[2])
                    
                    ssh.open_sftp().put(localpath=file_path, remotepath="/home/kusaches/script_mig.sh")
                    ssh.open_sftp().close()
                    
                    with SSHClientInteraction(ssh, timeout=10, display=True) as interact:
                        
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(migrations_commands[0])
                        interact.expect(sudo_prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(server_name[1])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(migrations_commands[1])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(migrations_commands[2])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(migrations_commands[3])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                    
                    ssh.close()
                except Exception as e:
                    cmd_insert(f"\n{server_name[0]} Не удалось подключиться к серверу!\n {e}")
                    continue
                
                
                
        elif button_name == "reload":
            for server in get_checkboxes():
                server_name: List[str] = server.split(":")
                
                reload_command: str = "sudo reboot"
                
                try:
                    ssh: SSHClient = SSHClient()
                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    ssh.connect(hostname=server_name[0], username=server_name[1], password=server_name[2])
                    
                    with SSHClientInteraction(ssh, timeout=10, display=True) as interact:

                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(reload_command)
                        interact.expect(sudo_prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(server_name[1])
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                    
                    ssh.close()
                except Exception as e:
                    cmd_insert(f"\n{server_name[0]} Не удалось подключиться к серверу!\n {e}")
                    continue
                
                
                
        elif button_name == "schedule_request":
            for club in get_comboboxes():
                
                server_with_club: List[str] = club.split(":")
                
                if server_with_club[0] == "fk-server" or server_with_club[0] == "fk-admin":
                    try:
                        url: str = f"https://{server_with_club[0]}.ru/schedule/get_v3?club_id={server_with_club[1].split('|')[1]}"
                        cmd_insert(f"Адрес сервера - {url}", True)
                        request: httpx.Response = httpx.get(url, follow_redirects=True, verify=False)
                        
                        cmd_insert(json.dumps(request.json(), indent=2), True)
                    except Exception as e:
                        cmd_insert(e, True)
                else:
                    try:
                        url: str = f"https://{server_with_club[0]}.fitnesskit-admin.ru/schedule/get_v3?club_id={server_with_club[1].split('|')[1]}"
                        cmd_insert(f"Адрес сервера - {url}", True)
                        request: httpx.Response = httpx.get(url, follow_redirects=True, verify=False)
                        
                        cmd_insert(json.dumps(request.json(), indent=2), True)
                    except Exception as e:
                        cmd_insert(e, True)
                
        elif button_name == "trainers_request":
            for club in get_comboboxes():
                
                server_with_club: List[str] = club.split(":")
                
                if server_with_club[0] == "fk-server" or server_with_club[0] == "fk-admin":
                    try:
                        url: str = f"https://{server_with_club[0]}.ru/team/get/{server_with_club[1].split('|')[1]}"
                        cmd_insert(f"Адрес сервера - {url}", True)
                        request: httpx.Response = httpx.get(url, follow_redirects=True, verify=False)
                        
                        cmd_insert(json.dumps(request.json(), indent=2), True)
                    except Exception as e:
                        cmd_insert(e, True)
                else:
                    try:
                        url: str = f"https://{server_with_club[0]}.fitnesskit-admin.ru/team/get/{server_with_club[1].split('|')[1]}"
                        cmd_insert(f"Адрес сервера - {url}", True)
                        request: httpx.Response = httpx.get(url, follow_redirects=True, verify=False)
                        
                        cmd_insert(json.dumps(request.json(), indent=2), True)
                    except Exception as e:
                        cmd_insert(e, True)
                
        elif button_name == "update_cert":
            for server in get_checkboxes():
                server_name: List[str] = server.split(":")
                
                update_cert_command: str = f"sudo certbot -d {server_name[0]} --force-renewal"
                
                try:
                    ssh: SSHClient = SSHClient()
                    ssh.set_missing_host_key_policy(AutoAddPolicy())
                    ssh.connect(hostname=server_name[0], username=server_name[1], password=server_name[2])
                    
                    with SSHClientInteraction(ssh, timeout=20, display=True) as interact:
                        
                        interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(update_cert_command)
                        interact.expect(sudo_prompt, output_callback=lambda m: cmd_insert(m))
                        
                        interact.send(server_name[1])
                        try:
                            interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                        except:
                            interact.expect(cert_prompt, output_callback=lambda m: cmd_insert(m))
                            
                            interact.send("U")
                            interact.expect(prompt, output_callback=lambda m: cmd_insert(m))
                    
                    ssh.close()
                except Exception as e:
                    cmd_insert(f"\n{server_name[0]} Не удалось подключиться к серверу!\n {e}")
                    continue
                
    def load_file_threaded(self, button_name: Optional[str] = None, cmd_insert: Optional[Callable] = None, get_checkboxes: Optional[Callable] = None, get_comboboxes: Optional[Callable] = None) -> None:
        Thread(target=self.load_file, args=(button_name, cmd_insert, get_checkboxes, get_comboboxes)).start()