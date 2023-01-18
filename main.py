import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import requests, re
from bs4 import BeautifulSoup
from io import BytesIO

def haeKuva(index):
	#print(index, len(kuvalista.get()))
	if(len(kuvalista.get()) == 0):
		print("Et ole valinnut sarjakuvaa!")
	else:
		linkit = kuvalista.get().split(" ")
		
		#for linkki in linkit:
		#	print(linkki)
		#print(len(linkit))
		
		vastaus = requests.get(linkit[index - 1])
		kuva = Image.open(BytesIO(vastaus.content))
		
		#with open(linkit[0],"wb") as handler:
		#	handler.write(kuva)
		#half = 0.5
		#out = kuva.resize( [int(half * s) for s in kuva.size] )
		print(kuva.size)
		width, height = kuva.size
		kuva = kuva.resize((int(width / 2), int(height / 2)), Image.ANTIALIAS)
		
		render = ImageTk.PhotoImage(kuva)
		img.configure(image=render)
		img.image = render

def edellinen():
	if(len(kuvalista.get()) == 0):
		print("Et ole valinnut sarjakuvaa!")
	else:
		print(sivu.get())
		if 1 < sivu.get():
			edellinen = sivu.get() - 1
			sivu.set(edellinen)
			window.title(str(sarjikset[var.get()])+ " " + str(edellinen))
			haeKuva(sivu.get())
		else:
			print("Ollaan kuvalistan alussa!")

def seuraava():
	if(len(kuvalista.get()) == 0):
		print("Et ole valinnut sarjakuvaa!")
	else:
		print(sivu.get())
		if sivu.get() < 10:
			seuraava = sivu.get() + 1
			sivu.set(seuraava)
			window.title(str(sarjikset[var.get()]) + " " + str(seuraava))
			haeKuva(sivu.get())
		else:
			print("Ollaan kuvalistan lopussa!")

def sel():
	sivu.set(1)
	print("Haetaan kuvalistaa", sarjikset[var.get()])
	kuvat = ""
	#kuva regex  hs.*1920.*\.jpg
	url = "https://www.hs.fi/" + sarjikset[var.get()].lower() + "/"
	print(url)
	html = requests.get(url)
	soppa = str(BeautifulSoup(html.content, "html.parser"))
	#print(soppa)
	rivit = soppa.split()
	for rivi in rivit:
		if len(rivi) < 100 and ".jpg" in rivi and "1920" in rivi:
			linkki = re.findall("hs.*1920.*\.jpg", rivi)
			kuvat = kuvat + "https://" + linkki[0] + " "
			#print("Rivi", len(rivi), rivi)
	#print(kuvat)
	kuvalista.set(kuvat)
	window.title(sarjikset[var.get()] + " " + str(sivu.get()))
	haeKuva(sivu.get())

def poistu():
    print("Heippa!")
    window.destroy()

window = tk.Tk()

window.title("DC:n hieno sarjakuvaohjelma!")
window.minsize(900,400)


sarjikset = ["Fingerpori", "ViivijaWagner", "Wumo"]
linkit = []
kuvalista = tk.StringVar()
name = tk.StringVar()
var = tk.IntVar() 
sivu = tk.IntVar()
sivu.set(1)
"""
label = ttk.Label(window, text = "Enter Your Name")
label.grid(column = 0, row = 0)
selection = "You selected the option " + str(var.get())
label.config(text = selection)

nameEntered = ttk.Entry(window, width = leveys, textvariable = name)
nameEntered.grid(column = 0, row = 1)
button3 = ttk.Button(window, text = "Click Me", command = clickMe)
button3.grid(column= 0, row = 2)
"""
poistu = ttk.Button(window, text = "Poistu", command = poistu)
poistu.grid(column= 0, row = 0)
R1 = Radiobutton(window, text="Fingerpori", variable=var, value=0, command=sel, justify = LEFT, cursor = "dot")
R1.grid(column = 1, row = 0)
R2 = Radiobutton(window, text="Viivi ja Wagner", variable=var, value=1, command=sel, justify = LEFT, cursor = "dot")
R2.grid(column = 2, row = 0)
R3 = Radiobutton(window, text="Wumo", variable=var, value=2, command=sel, justify = LEFT, cursor = "dot")
R3.grid(column = 3, row = 0)
button1 = ttk.Button(window, text = "Edellinen", command = edellinen, cursor = "dot")
button1.grid(column= 0, row = 1)
button2 = ttk.Button(window, text = "Seuraava", command = seuraava, cursor = "dot")
button2.grid(column= 1, row = 1)

load = Image.open("fingerporilogo.png")
render = ImageTk.PhotoImage(load)
img = ttk.Label(window, image=render)
img.image = render
img.place(x=5, y=60)

# ~ window.bind("<Left>", edellinen)
# ~ window.bind("<Right>", seuraava)
window.mainloop()
