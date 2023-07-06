from typing import Optional, List, Callable

from customtkinter import CTkScrollableFrame, CTkButton, CTkCheckBox, BooleanVar
from fonts.fonts import button_med_font, body_med_font

class ScrollableServersFrame(CTkScrollableFrame):
    def __init__(self, master, insert_comboboxes: Optional[Callable] = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self.checkbox_list: List[CTkCheckBox] = []

        self.select_all = CTkButton(
            self, 
            text="Выбрать все", 
            font=button_med_font(),
            width=100, 
            command=lambda: self.enable_checkboxes(insert_comboboxes)
        )
        self.select_all.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        self.deselect_all = CTkButton(
            self, 
            text="Отменить все", 
            font=button_med_font(),
            width=100, 
            command=lambda: self.disable_checkboxes(insert_comboboxes)
        )
        self.deselect_all.grid(row=0, column=0, pady=(0, 10), sticky="e")
        
        with open("input_data/servers.txt", "r") as f:
            servers: List[str] = f.read().split("\n")
            for server in servers:
                server_name: List[str] = server.split(":")
                self.add_item(server_name[0], insert_comboboxes)

    def add_item(self, item: str, insert_comboboxes: Callable) -> None:
        checkbox_var = BooleanVar()
        checkbox = CTkCheckBox(
            self, 
            text=item, 
            variable=checkbox_var, 
            font=body_med_font(), 
            command=lambda: insert_comboboxes(item, checkbox_var)
        )
        checkbox.grid(
            row=len(self.checkbox_list)+1, 
            column=0, 
            pady=(0, 10), 
            sticky="w"
        )
        self.checkbox_list.append(checkbox)
    
    def enable_checkboxes(self, insert_comboboxes: Callable) -> None:
        for checkbox in self.checkbox_list:
            checkbox.select()
            insert_comboboxes(checkbox.cget("text"), checkbox.cget("variable"))
            
    def disable_checkboxes(self, insert_comboboxes: Callable) -> None:
        for checkbox in self.checkbox_list:
            checkbox.deselect()
            insert_comboboxes(checkbox.cget("text"), checkbox.cget("variable"))
            
    def get_checked_items(self) -> List[str]:
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]