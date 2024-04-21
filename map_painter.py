import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint-like App")
        self.image_path = 'CampusMapInset.png'  # Set the default image path here
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(root, width=self.image.size[0], height=self.image.size[1], cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.draw = ImageDraw.Draw(self.image)

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        self.color = 'black'
        self.chooser_button = tk.Button(root, text='Choose Color', command=self.choose_color)
        self.chooser_button.pack(side=tk.LEFT)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def open_image(self):
        path = tk.filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.image_path = path
            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.image.size[0], height=self.image.size[1])
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        if self.image and self.image_path:
            self.image.save(self.image_path)

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
        if self.draw:
            self.draw.line([x1, y1, x2, y2], fill=self.color, width=2)

    def reset(self, event):
        self.draw.line([(event.x - 1), (event.y - 1), (event.x + 1), (event.y + 1)], fill=self.color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()