from typing import List

from customtkinter import CTkScrollableFrame, CTkButton, CTkComboBox
from fonts.fonts import button_med_font, body_med_font

class ClubsOfServersFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self.combobox_list = []
        
        self.clear_all = CTkButton(
            self, 
            text="Очистить все", 
            font=button_med_font(), 
            command=lambda: self.clear_items()
        )
        self.clear_all.pack(fill="both", expand=True)
        
    def add_item(self, server: str, club: str) -> None:
        combobox = CTkComboBox(
            self,
            font=body_med_font(),
            justify="center",
            values=[server] + [i for i in club.split(",")],
            hover=True
        )
        combobox.pack(fill="both", pady=(10, 0), expand=True)
        combobox.set(server)
        self.combobox_list.append(combobox)
        
    def delete_item(self, server: str) -> None:
        for combobox in self.combobox_list:
            if combobox.cget("values")[0] == server:
                combobox.pack_forget()

    def clear_items(self) -> None:
        for combobox in self.combobox_list:
            combobox.set(combobox.cget("values")[0])
        
    def get_comboboxes_items(self) -> List[CTkComboBox]:
        return self.combobox_list
        