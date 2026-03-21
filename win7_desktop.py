import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext, messagebox
import os
import time

root = tk.Tk()
root.title("Windows 7 Python OS")
root.geometry("1200x700")

PASSWORD = "1234"   # change password here

# ---------------- LOGIN ----------------

login_frame = tk.Frame(root, bg="#2b579a")
login_frame.place(relwidth=1, relheight=1)

tk.Label(login_frame,text="User Login",
font=("Segoe UI",30),bg="#2b579a",fg="white").pack(pady=150)

password_entry = tk.Entry(login_frame,show="*",font=("Segoe UI",16))
password_entry.pack(pady=10)

password_entry.focus()
password_entry.bind("<Return>", lambda e: check_login())

def check_login():

    if password_entry.get() == PASSWORD:
        start_boot()
    else:
        messagebox.showerror("Error","Wrong password")

login_btn = tk.Button(
login_frame,
text="Login",
font=("Segoe UI",16),
command=check_login
)

login_btn.pack()

# ---------------- BOOT SCREEN ----------------

boot_frame = tk.Frame(root,bg="black")

boot_label = tk.Label(
boot_frame,
text="Starting Windows...",
fg="white",
bg="black",
font=("Segoe UI",28)
)

boot_label.pack(expand=True)

# ---------------- DESKTOP ----------------

wallpaper_img = Image.open("wallpaper.jpg").resize((1200, 700))
wallpaper = ImageTk.PhotoImage(wallpaper_img)
desktop = tk.Label(root, image=wallpaper)
desktop.image = wallpaper


# ---------------- WINDOW CLASS ----------------

class AppWindow:

    def __init__(self,title,w=400,h=300):

        self.frame = tk.Frame(root,bg="white",bd=2)
        self.frame.place(x=300,y=150,width=w,height=h)

        titlebar = tk.Frame(self.frame,bg="#2D5BE3",height=30)
        titlebar.pack(fill="x")

        tk.Label(titlebar,text=title,
        bg="#2D5BE3",fg="white").pack(side="left",padx=5)

        tk.Button(titlebar,text="X",bg="red",fg="white",
        command=self.frame.destroy).pack(side="right")

        self.content = tk.Frame(self.frame,bg="white")
        self.content.pack(expand=True,fill="both")

        titlebar.bind("<Button-1>",self.start_move)
        titlebar.bind("<B1-Motion>",self.move)

        resize = tk.Frame(self.frame,cursor="bottom_right_corner")
        resize.place(relx=1,rely=1,anchor="se",width=10,height=10)
        resize.bind("<B1-Motion>",self.resize)

    def start_move(self,e):
        self.x=e.x
        self.y=e.y

    def move(self,e):
        x=self.frame.winfo_x()+e.x-self.x
        y=self.frame.winfo_y()+e.y-self.y
        self.frame.place(x=x,y=y)

    def resize(self,e):
        w=self.frame.winfo_width()+e.x
        h=self.frame.winfo_height()+e.y
        self.frame.config(width=w,height=h)

# ---------------- APPS ----------------

def open_explorer():

    win = AppWindow("Explorer",500,400)

    path=os.getcwd()

    for item in os.listdir(path):

        tk.Label(win.content,
        text=item,
        font=("Segoe UI",11)).pack(anchor="w",padx=10)

def open_notepad():

    win=AppWindow("Notepad",500,400)

    text=scrolledtext.ScrolledText(win.content)
    text.pack(expand=True,fill="both")

def open_calculator():

    win=AppWindow("Calculator",300,200)

    entry=tk.Entry(win.content,font=("Segoe UI",16))
    entry.pack(fill="x",padx=10,pady=10)

# ---------------- DESKTOP ICONS ----------------

def icon(name,cmd,x,y):

    b=tk.Button(
    desktop,
    text=name,
    width=12,
    height=3,
    bg="#1E90FF",
    fg="white",
    relief="flat",
    command=cmd
    )

    b.place(x=x,y=y)

# ---------------- START MENU ----------------

start_menu=tk.Frame(root,bg="white",width=250,height=300)

def toggle_start():

    if start_menu.winfo_ismapped():
        start_menu.place_forget()
    else:
        start_menu.place(x=0,y=400)

tk.Button(start_menu,text="Explorer",width=25,
command=open_explorer).pack(pady=5)

tk.Button(start_menu,text="Notepad",width=25,
command=open_notepad).pack(pady=5)

tk.Button(start_menu,text="Calculator",width=25,
command=open_calculator).pack(pady=5)

tk.Button(start_menu,text="Shutdown",width=25,
command=lambda:shutdown()).pack(pady=5)

# ---------------- TASKBAR ----------------

taskbar=tk.Frame(root,bg="#222",height=50)

start_img = Image.open("start_orb.png")
start_img = start_img.resize((40,40))
start_icon = ImageTk.PhotoImage(start_img)

start_btn = tk.Button(
taskbar,
image=start_icon,
bg="#2D5BE3",
command=toggle_start
)

start_btn.pack(side="left",padx=5)

apps=[("📁",open_explorer),
("📝",open_notepad),
("🧮",open_calculator)]

for a in apps:

    tk.Button(taskbar,
    text=a[0],
    bg="#333",
    fg="white",
    command=a[1]).pack(side="left",padx=2)

# ---------------- CLOCK ----------------

clock=tk.Label(taskbar,bg="#222",fg="white")
clock.pack(side="right",padx=10)

def update_clock():

    clock.config(text=time.strftime("%I:%M %p"))
    root.after(1000,update_clock)

update_clock()

# ---------------- RIGHT CLICK ----------------

menu=tk.Menu(root,tearoff=0)
menu.add_command(label="Explorer",command=open_explorer)
menu.add_command(label="Notepad",command=open_notepad)

def rc(e):
    menu.post(e.x_root,e.y_root)

root.bind("<Button-3>",rc)

# ---------------- BOOT → DESKTOP ----------------

def start_boot():

    login_frame.destroy()
    boot_frame.place(relwidth=1,relheight=1)

    root.after(3000,start_desktop)

def start_desktop():

    boot_frame.destroy()

    desktop.place(relwidth=1,relheight=1)

    icon("📁\nExplorer",open_explorer,20,20)
    icon("📝\nNotepad",open_notepad,20,100)
    icon("🧮\nCalculator",open_calculator,20,180)

    taskbar.pack(side="bottom",fill="x")

# ---------------- SHUTDOWN ----------------

def shutdown():

    s=tk.Frame(root,bg="black")
    s.place(relwidth=1,relheight=1)

    tk.Label(
    s,
    text="Shutting down...",
    fg="white",
    bg="black",
    font=("Segoe UI",30)
    ).pack(expand=True)

    root.after(3000,root.destroy)

root.mainloop()