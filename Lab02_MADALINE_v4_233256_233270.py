import sys, os, fnmatch
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from math import sqrt

np.set_printoptions(precision=4, linewidth=115, suppress=False)

#folder="./data/zestaw_1/" 
folder="./data/"+ str(sys.argv[1]+"/")
output=list() # lista wektorów normalizowanych z danych obrazowych

def zgodnosc():
    wzorzec=int(sign.get())-1
    for j in range(len(output)):    
        
        # iloczyn dwóch wektorów
        Label(root, text=np.dot(output[wzorzec],output[j]), padx = 20).grid(row=3, column=j+1, padx=10, sticky=tk.W) 
        
        # wynik procentowy
        wynik=np.dot(output[wzorzec],output[j])*100 # wynik procentowy
        
        if wynik>95:
            Label(root, text=round(wynik,2), bg="lightgreen", padx = 20).grid(row=4, column=j+1, padx=10, sticky=tk.W) 
        else: 
            Label(root, text=round(wynik,2), bg="#faa", padx = 20).grid(row=4, column=j+1, padx=10, sticky=tk.W) 
            
    
root=Tk()

sign = tk.IntVar() # obsługa radio button

root.title("Laboratorium 2: MADALINE, rozpoznawanie znaków. R.Majkowski (233256), M. Witomski (233270)")
root.configure(bg='white', width=800, height=800, padx=15, pady=15)

Label(root, text="Znak: ", bg="white", padx = 20).grid(row=0, column=0, padx=10, sticky=tk.W)
Label(root, text="Wybierz znak wzorcowy:", bg="white", padx = 20).grid(row=1, column=0, padx=10, sticky=tk.W)
Label(root, text="Wektor normalizowany:", bg="white", padx = 20).grid(row=2, column=0, padx=10, sticky=tk.W)
Label(root, text="Iloczyn wektorów (wzorzec*kolumna):", bg="white", padx = 20).grid(row=3, column=0, padx=10, sticky=tk.W)
Label(root, text="Wynik procentowy:", bg="white", padx = 20).grid(row=4, column=0, padx=10, sticky=tk.W)

i = 1
for file in os.listdir(folder):
    if fnmatch.fnmatch(file, '*.bmp'):
        znak=Image.open(folder + file)
        
        # normalizacja
        np_znak = np.array(znak).flatten() # splaszczona tablica dla odczytanego znaku
        np_znak = np.invert(np_znak) # inwersja, True dla czarnych pikseli
        number_of_true = np.count_nonzero(np_znak) # liczba czarnych pikseli
        if number_of_true:
            output.append(np_znak/sqrt(number_of_true)) # normalizowany wektor wag dla pojedynczego znaku
        else:
            output.append(0)
        
        # wyświetlenie znaku
        render = ImageTk.PhotoImage(znak)
        label = Label(root, image=render)
        label.image = render
        label.grid(row=0, column=i, padx=10)
        tk.Radiobutton(root, text=str(i), bg="white", padx = 20, variable=sign, value=i, command=zgodnosc).grid(row=1, column=i, padx=10)        
        
        # wyświetlenie wektora normalizowanego
        Label(root, text=output[i-1], bg="white", padx = 20).grid(row=2, column=i, padx=10) 
        i=i+1
       # if i>3: break # ucieczka z pętli dla pierwszych trzech wczytanych znaków

root.mainloop()
    
