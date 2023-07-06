from typing import List, Optional

from customtkinter import CTk, set_appearance_mode
from src.servers import ScrollableServersFrame
from src.clubs import ClubsOfServersFrame
from src.commands import ServersCommandsFrame
from src.cmd_output import CMDOutputFrame
from src.cmd_toplevel import ToplevelWindow
from tkinter import END
from fonts.fonts import *

class App(CTk):
    def __init__(self) -> None:
        super().__init__()
        
        self.title("Система управления серверами")
        self.minsize(1000, 550)
        self.grid_columnconfigure((1, 1), weight=1)
        self.grid_rowconfigure((1, 1), weight=1)
        
        self.toplevel_window: None = None
        
        self.scrollable_checkbox_frame = ScrollableServersFrame(
            master=self,
            insert_comboboxes=self.load_server_clubs, 
            width=250
        )
        self.scrollable_checkbox_frame.grid(
            row=0, 
            column=0, 
            padx=10, 
            pady=(10, 0), 
            sticky="nsew"
        )
        
        self.scrollable_combobox_frame = ClubsOfServersFrame(
            master=self
        )
        self.scrollable_combobox_frame.grid(
            row=0, 
            column=1, 
            padx=(0, 10), 
            pady=(10, 0), 
            sticky="nsew"
        )
        
        self.scrollable_servers_frame = ServersCommandsFrame(
            master=self, 
            get_checkboxes=self.checkbox_frame_event,
            get_comboboxes=self.get_comboboxes_list,
            cmd_insert=self.cmd_insert
        )
        self.scrollable_servers_frame.grid(
            row=0, 
            column=2, 
            padx=(0, 10), 
            pady=(10, 0), 
            sticky="nsew"
        )
        
        self.cmd_output_frame = CMDOutputFrame(
            master=self
        )
        self.cmd_output_frame.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=10, 
            sticky="nsew", 
            columnspan=3
        )
        
        self.after(1000, self.update)

    def checkbox_frame_event(self) -> List[str]:
        with open("input_data/servers.txt", "r") as f:
            servers: List[str] = f.read().split("\n")
        return [server for server in servers if server.split(":")[0] in self.scrollable_checkbox_frame.get_checked_items()]
    
    def get_comboboxes_list(self) -> List[str]:
        return [f"{box.cget('values')[0]}:{box.get()}" for box in self.scrollable_combobox_frame.get_comboboxes_items() if box.get() != box.cget("values")[0]]
    
    def load_server_clubs(self, server: List[str], checkbox_var) -> None:
        with open("input_data/clubs.txt", "r") as f:
            server_name: str = server.split(".")[0]
            server_clubs: List[str] = f.read().split("\n")
        for club in server_clubs:
            if server_name == club.split(":")[0] and checkbox_var.get():
                self.scrollable_combobox_frame.add_item(club.split(":")[0], club.split(":")[1])
            elif server_name == club.split(":")[0] and not checkbox_var.get():
                self.scrollable_combobox_frame.delete_item(club.split(":")[0])
    
    def cmd_insert(self, cmd_output: str, toplevel: Optional[bool] = False) -> None:
        if not toplevel:
            self.cmd_output_frame.cmd.configure(state="normal")
            self.cmd_output_frame.cmd.insert(END, cmd_output)
            self.cmd_output_frame.cmd.configure(state="disabled")
            self.cmd_output_frame.cmd.see(END)
        else:
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.textbox_toplevel.configure(state="normal")
            self.toplevel_window.textbox_toplevel.insert(END, "\n")
            self.toplevel_window.textbox_toplevel.insert(END, cmd_output)
            self.toplevel_window.textbox_toplevel.insert(END, "\n")
            self.toplevel_window.textbox_toplevel.configure(state="disabled")
            self.toplevel_window.textbox_toplevel.see(END)
            
if __name__ == "__main__":
    set_appearance_mode("dark")
    app = App()
    app.mainloop()