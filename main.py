from tkinter import * 
from tkinter import filedialog
from tkinter import ttk
from tkinter import colorchooser
from functools import partial
from PIL import ImageTk, Image, ImageGrab

class MemeGenerator:

    def __init__(self):
        self.root = Tk()
        self.texto_cima = StringVar()
        self.texto_baixo = StringVar()
        self.font_family = StringVar()
        self.font_size = IntVar()
        self.justify_options = ["left", "center", "right"]
        self.color = 'white'
        self.image_path = StringVar()
        self.width_entrys = 35

        self.font_family.set("impact")
        self.font_size.set(50)

        self.stroke_text = BooleanVar()

        self.canvas_root = Canvas(self.root, width=700, height=720, bg='gray')
        self.canvas_root.grid(row=0, column=0)

        self.main()

    def create_labels(self):
        self.canvas_root.delete()
        self.canvas_root = Canvas(self.root, width=700, height=720, bg="gray")
        self.canvas_root.grid(row=0, column=0)
        if self.image_path.get() != "":
            image_meme = Image.open(self.image_path.get())
            image_meme = image_meme.resize((700, 720))
            self.image_meme_tk = ImageTk.PhotoImage(image_meme)

            self.canvas_root.create_image(0, 0, image=self.image_meme_tk, 
            anchor=NW)

        if self.stroke_text.get():
            for i in range(0, 25):
                self.canvas_root.create_text(360-i, -10+i+self.font_size.get(), fill='black', text=self.texto_cima.get(),font=f"{self.font_family.get()} {self.font_size.get() + 1} bold")
                self.canvas_root.create_text(360-i, 710+i-self.font_size.get(), fill='black', text=self.texto_baixo.get(), font=f"{self.font_family.get()} {self.font_size.get() + 1} bold")
            self.top_text = self.canvas_root.create_text(350, 0+self.font_size.get(), fill=self.color, text=self.texto_cima.get(),font=f"{self.font_family.get()} {self.font_size.get()}")
            self.bottom_text = self.canvas_root.create_text(350, 720-self.font_size.get(), fill=self.color, text=self.texto_baixo.get(), font=f"{self.font_family.get()} {self.font_size.get()}")
            
        else:
            self.top_text = self.canvas_root.create_text(350, 0+self.font_size.get(), fill=self.color, text=self.texto_cima.get(),font=f"{self.font_family.get()} {self.font_size.get()}")
            self.bottom_text = self.canvas_root.create_text(350, 720-self.font_size.get(), fill=self.color, text=self.texto_baixo.get(), font=f"{self.font_family.get()} {self.font_size.get()}")


        self.canvas_root.update()


    def create_entries(self):
        entry_texto_cima = Entry(self.root, textvariable=self.texto_cima, width=self.width_entrys)
        entry_texto_cima.grid(row=0, column=1, sticky=NW)
        entry_texto_cima.insert(0, "Texto cima")
        entry_texto_cima.focus()

        entry_texto_baixo = Entry(self.root, textvariable=self.texto_baixo, width=self.width_entrys)
        entry_texto_baixo.grid(row=0, column=1, sticky=NW, pady=20)
        entry_texto_baixo.insert(0, "Texto baixo")

        entry_font_size = Entry(self.root, textvariable=self.font_size, width=3)
        entry_font_size.grid(row=0, column=1, sticky=NW, pady=40, padx=150)

    def create_combobox(self):
        cbox = ttk.Combobox(self.root, textvariable=self.font_family ,values=[
            "arial",
            "impact",
            "times",
            "calibri",
            "cambria",
            "consolas",
            "corbel",
            "constantia",
            "courier"
        ])
        cbox.grid(row=0, column=1, sticky=NW, pady=40)
        cbox.current(1)
    
    def create_button(self):
        Button(self.root, text="Update font!", width=29, command=self.create_labels).grid(row=0, column=1, sticky=NW, pady=100)

        Button(self.root, width=29, command=self.create_file_selector, 
                text="Select an image").grid(row=0, column=1, sticky=NW, pady=125)

        Button(self.root, width=29, command=self.export_image, text="Save meme").grid(row=0, column=1, sticky=NW, pady=150)

        bt_color = Button(self.root, width=2, height=1, bg=self.color)
        bt_color["command"] = partial(self.change_color, bt_color)
        bt_color.grid(row=0, column=1, sticky=NW, pady=40, padx=180)

        Checkbutton(self.root, text="Shadow", variable=self.stroke_text).grid(row=0, column=1, sticky=NW, pady=70)

    def create_file_selector(self):
        image_selector = filedialog.askopenfile()
        self.image_path.set(image_selector.name)
        self.create_labels()
    
    def export_image(self):
        x = self.root.winfo_rootx()+self.canvas_root.winfo_x()
        y = self.root.winfo_rooty()+self.canvas_root.winfo_y()

        ImageGrab.grab().crop((x, y, x+700, y+720)).save("Meu meme.jpg")
    
    def change_color(self, button):
        self.color = colorchooser.askcolor()[1]
        button["bg"] = self.color

    def onchange(self, varname, index, mode):
        self.canvas_root.itemconfigure(self.top_text, text=self.texto_cima.get())
        self.canvas_root.itemconfigure(self.bottom_text, text=self.texto_baixo.get())
        
    def main(self):
        self.create_entries()
        self.create_labels()
        self.create_combobox()
        self.create_button()

        self.texto_cima.trace_variable('w', self.onchange)
        self.texto_baixo.trace_variable('w', self.onchange)

        self.root.geometry("930x720")
        self.root.title("Meme Generator")
        self.root.mainloop()

meme_generator = MemeGenerator()
