from customtkinter import CTkToplevel, CTkTextbox
from tkinter import WORD
from fonts.fonts import log_font

class ToplevelWindow(CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry("500x600")
        self.title("Внешний вывод данных")
        
        self.textbox_toplevel = CTkTextbox(
            master=self, 
            state="disabled",
            font=log_font(),
            wrap=WORD,
            fg_color="#343638",
            text_color="#ffffff",
            cursor="arrow",
        )
        self.textbox_toplevel.pack(fill="both", expand=True)
        self.refresh()
        
    def refresh(self) -> None:
        self.update()
        self.after(1000, self.refresh)