import random
import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from worker import *
from make_match import *


global IMAGE_PATH

LANG = 'ru'
SHOW_ERRORS_ONLY = False
RED_COLOR = Image.new('RGB', (110, 5), (200, 0, 0))
WHITE_COLOR = Image.new('RGB', (110, 5), (250, 250, 250))


def callback():
    webbrowser.open_new("https://github.com/conwerner/annotation_utility")

# upload images (PATH DIR) and its annotation document (PATH TXT)
def upload():
    PATH_DIR = e2.get()
    PATH_TXT = e3.get()
    make_match(PATH_DIR,PATH_TXT)
    N = worker1.upload(PATH_TXT,PATH_DIR)
    l3.configure(text=f'0/{N}')
    next()
    messagebox.showinfo('INFO',f'{N} images have been uploaded')
    e2.config(state='disabled')
    e3.config(state='disabled')

# next entity
def next(update=True):
    global SHOW_ERRORS_ONLY
    new_label = e1.get()
    IMAGE_PATH = worker1.get_current()[0]
    if update:
        worker1.update(IMAGE_PATH, new_label)

    IMAGE_PATH, entity = worker1.next()
    if SHOW_ERRORS_ONLY:
        i = 0
        while entity['spelling_ok']:
            IMAGE_PATH, entity = worker1.next()
            i += 1
            if i > worker1.N:
                messagebox.showinfo('INFO', 'There is no label with spelling errors')
                SHOW_ERRORS_ONLY = False
                break
    if not entity['spelling_ok']:
        render = ImageTk.PhotoImage(RED_COLOR)
    else:
        render = ImageTk.PhotoImage(WHITE_COLOR)

    img1 = tk.Label(master, image=render)
    img1.image = render
    img1.place(x=230, y=200)

    k = worker1.get_curr_idx()
    N = worker1.N
    l3.configure(text=f'{k}/{N}')
    load = Image.open(IMAGE_PATH)
    render = ImageTk.PhotoImage(load)
    img.configure(image=render)
    img.image = render
    img.place(x=120, y=10)
    e1.delete(0, 'end')
    e1.insert('end',entity['label'])

# previous entity
def prev(event=None):
    global SHOW_ERRORS_ONLY
    new_label = e1.get()
    IMAGE_PATH = worker1.get_current()[0]
    worker1.update(IMAGE_PATH, new_label)

    IMAGE_PATH, entity = worker1.previous()
    if SHOW_ERRORS_ONLY:
        i = 0
        while entity['spelling_ok']:
            IMAGE_PATH, entity = worker1.previous()
            i += 1
            if i > worker1.N:
                messagebox.showinfo('INFO', 'There is no label with spelling errors')
                SHOW_ERRORS_ONLY = False
                break

    if not entity['spelling_ok']:
        render = ImageTk.PhotoImage(RED_COLOR)
    else:
        render = ImageTk.PhotoImage(WHITE_COLOR)
    img1 = tk.Label(master, image=render)
    img1.image = render
    img1.place(x=230, y=200)

    k = worker1.get_curr_idx()
    N = worker1.N
    l3.configure(text=f'{k}/{N}')
    load = Image.open(r'{}'.format(IMAGE_PATH))
    render = ImageTk.PhotoImage(load)
    img.configure(image=render)
    img.image = render
    img.place(x=120, y=10)
    e1.delete(0, 'end')
    e1.insert('end', entity['label'])

# save changes on images and its annotation
def save():
    PATH_DIR = e2.get()
    PATH_TXT = e3.get()
    n = worker1.save(PATH_TXT,PATH_DIR)
    make_match(PATH_DIR,PATH_TXT)
    e2.config(state='normal')
    e3.config(state='normal')
    messagebox.showinfo('INFO', f'{n} images have been saved')

# remove pair (image, label)
def remove():
    worker1.remove_current()
    next(update=False)


def switch_show_mode():
    global SHOW_ERRORS_ONLY
    SHOW_ERRORS_ONLY = not SHOW_ERRORS_ONLY

worker1 = Worker()

master = tk.Tk()
master.title('Annotation Utility')
master.geometry('550x380')

e1 = tk.Entry(master)
e1.place(x=220,y=180)

load = Image.new('RGB', (324, 128), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
render = ImageTk.PhotoImage(load)
img = tk.Label(master,image=render)
img.image = render
img.place(x=110, y=10)

b1 = tk.Button(master, text='previous', command=prev).place(x=220, y=210)
b2 = tk.Button(master, text='next', command=next).place(y=210, x=300)

c1 = tk.Checkbutton(master, text = "show entities with spelling errors only", command=switch_show_mode).place(x=190, y=155)

l1 = tk.Label(master,text='img dir')
l1.place(x=160,y=260)

l2 = tk.Label(master,text='labels')
l2.place(x=160,y=290)

l3 = tk.Label(master,text='0/0')
l3.place(x=110,y=200)

e2 = tk.Entry(master)
e2.place(x=220,y=260)

e3 = tk.Entry(master)
e3.place(x=220,y=290)

tk.Button(master,
          text='help',command=callback).place(x=390,y=260)

tk.Button(master,
          text='upload',command=upload).place(x=350,y=290)

tk.Button(master,
          text='save',command=save).place(x=350,y=260)

tk.Button(master,
          text='remove',command=remove).place(x=370,y=210)

master.bind('<Shift-Right>',next)
master.bind('<Shift-Left>',prev)
master.bind('<Shift-space>',remove)

tk.mainloop()