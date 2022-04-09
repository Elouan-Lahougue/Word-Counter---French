# coding:utf-8

import tkinter as tk
import tkinter.scrolledtext as tks
import re


class AppWin(tk.Tk):
     def __init__(self, title, x, y, version, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        xScreen, yScreen = int(self.winfo_screenwidth()), int(self.winfo_screenheight())
        
        self.x, self.y = x, y
        self.xPos, self.yPos = (xScreen - self.x) // 2, (yScreen - self.y) // 2
        self.geometry("{}x{}+{}+{}".format(self.x, self.y, self.xPos, self.yPos))
        self.title(f"{title} v{version[0]}.{version[1]}.{version[2]}")
        self.minsize(self.x, self.y)
        self.resizable(width=False, height=False)


# Fonction globale

def processtext(_=0):
    global wordcounter, lettercounter, charcounter
    wordcounter, lettercounter, charcounter = 0, 0, 0
    text = str.upper(txtentry.get(1.0, "end"))
    for char in text:
        if char not in (" ", "\t", "\n"): charcounter += 1
    text = text.replace("-", " ").replace("\n", " ").replace("\t", " ").replace(".", "").replace("’", "'")
    # Processing letters
    chardict = {}
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜ"
    for char in chars:
        chardict[char] = 0
    for char in text:
        if re.fullmatch(r"[ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜ]{1}", char):
            chardict[char] += 1
            lettercounter += 1
    letterlb.delete(0, "end")
    for key, value in chardict.items(): letterlb.insert("end", f" {key} - {value}")
    
    # Processing words
    worddict = {}
    while re.search(r"AUJOURD'HUI", text):
        try:
            worddict["AUJOURD'HUI"] += 1
        except KeyError: worddict["AUJOURD'HUI"] = 1
        wordcounter += 1
        text = text[:int(re.search(r"AUJOURD'HUI", text).start())] + text[int(re.search(r"AUJOURD'HUI", text).start())+len("AUJOURD'HUI"):]
    newtext, text = "", text.replace("'", " ")
    for char in text:
        if char in chars+" ": newtext += char
    words = newtext.split(" ")
    for element in words:
        e = ""
        for char in element:
            if char != " ": e += char
        if e != "":
            try: worddict[e] += 1
            except KeyError: worddict[e] = 1
    wordlb.delete(0, "end")
    for key, value in worddict.items():
        wordlb.insert("end", f" {key} - {value}")
        wordcounter += value
    
    # Refreshing labels
    if wordcounter <= 1: counterlabel["text"] = f"{wordcounter} MOT"
    else: counterlabel["text"] = f"{wordcounter} MOTS"
    if lettercounter <= 1: counterlabel_l["text"] = f"{lettercounter} LETTRE"
    else: counterlabel_l["text"] = f"{lettercounter} LETTRES"
    if charcounter <= 1: counterlabel_c["text"] = f"{charcounter} CARACTÈRE"
    else: counterlabel_c["text"] = f"{charcounter} CARACTÈRES"

# Autres fonctions

def getspace(string, space_needed): return " "*(space_needed-len(string))


# Informations générales

title = "Word Counter"
version = (1, 0, 0)
dev = "Elouan Lahougue"

# Compteurs
wordcounter, lettercounter, charcounter = 0, 0, 0

# Création de l'interface

App = AppWin(title, 760, 480, version)

globalmainframe = tk.Frame(App, width=App.x-10, height=App.y-10)
globalmainframe.pack(padx=6, pady=(6, 0))


# Création du body

txtentry = tks.ScrolledText(globalmainframe, bg="white", width=50, height=28)
txtentry.grid(row=0, column=0, pady=5)

rightframe = tk.Frame(globalmainframe)
rightframe.grid(row=0, column=1)

countframe = tk.Frame(rightframe)
countframe.pack()

counterlabel = tk.Label(countframe, text=f"{wordcounter} MOT", font=('Consolas', 18, 'bold', 'roman'))
counterlabel.pack(pady=(15, 0))

counterlabel_l = tk.Label(countframe, text=f"{lettercounter} LETTRE", font=('Consolas', 12, 'bold', 'roman'))
counterlabel_l.pack(pady=(5, 0))

counterlabel_c = tk.Label(countframe, text=f"{charcounter} CARACTÈRE", font=('Consolas', 12, 'bold', 'roman'))
counterlabel_c.pack(pady=(0, 12))

rbframe = tk.Frame(rightframe, width=240)
rbframe.pack()

# Word Frame

wordframe = tk.Frame(rbframe, width=240)
wordframe.grid(row=0, column=0, pady=5)

wordsb = tk.Scrollbar(wordframe)
wordsb.pack(side="right", fill="y")

wordlb = tk.Listbox(wordframe, yscrollcommand=wordsb.set, width=30, height=21, font=('Source Code Pro', 9, 'bold', 'roman'))
wordlb.pack(side="left", fill="both", padx=(4, 0), pady=(0, 5))

wordsb.config(command=wordlb.yview)


# Letter Frame

letterframe = tk.Frame(rbframe)
letterframe.grid(row=0, column=1, pady=5)

lettersb = tk.Scrollbar(letterframe)
lettersb.pack(side="right", fill="y")

letterlb = tk.Listbox(letterframe, yscrollcommand=lettersb.set, width=10, height=21, font=('Source Code Pro', 9, 'bold', 'roman'))
letterlb.pack(side="left", fill="both", padx=(4, 0), pady=(0, 5))

lettersb.config(command=letterlb.yview)

processtext()

# Bindings

App.bind("<Key>", processtext)

App.mainloop()
