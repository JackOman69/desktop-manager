from customtkinter import CTkFrame, CTkTextbox, CTkButton
from tkinter import END, WORD
from fonts.fonts import log_font, button_med_font

class CMDOutputFrame(CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self.cmd = CTkTextbox(
            master=self, 
            state="disabled",
            font = log_font(),
            wrap=WORD,
            fg_color="#343638",
            text_color="#ffffff",
            cursor="arrow",
        )
        self.cmd.pack(fill="both", expand=True)
        
        self.clear_all = CTkButton(
            self, 
            text="Очистить логи", 
            font=button_med_font(), 
            command=lambda: self.clear_logs()
        )
        self.clear_all.pack(fill="x")
    
    def clear_logs(self) -> None:
        self.cmd.configure(state="normal")
        self.cmd.delete("0.0", END)
        self.cmd.configure(state="disabled")