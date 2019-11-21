# Wyznaczanie maksimum funkcji algorytmem ewolucyjnym
# Radosław Majkowski 233256 
# Mateusz Witomski 233270

import os, math
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from collections import Counter

# funckja przystosowania, wpisana zgodnie z warunkami zadania laboratoryjnego
# uwaga 1: dziedzina funkcji wyklucza zero
# uwaga 2: reguła ruletki nie dopuszcza ujemnych wartości funkcji celu; znamy orientacyjne wartości w interesującyjm przedziale,
# dlatego "podnosimy" wartość o bezpieczne 7

shift = 7 # przesunięcie wartości funkcji w osi Y
iteracja = 0 # wartość startowa, warunek dla iteracja = Gen

def funkcja(argument):
    try:
        y = (math.exp(argument) * math.sin(10*math.pi*argument)+1)/argument
        # y = math.sin(argument) # testowa funkcja kontrolna, w testowym zakresie max=1
    except:
        print("UWAGA! Błąd obliczania wartości funkcji dla argumentu x = %s" % argument) 
        y = 0
    return(y+shift)

# Obecnie dobrane optymalne warunki początkowe dla funkcji laboratoryjnej:
# 2000 pokolen
# pop_size=200
# Pc=0.5 oraz Pm=0.0001


# Parametry początkowe programu: liczba pokoleń (Gen), liczba zmiennych w funkcji (k), przedział (Xmin, Xmax), dokładność (d)
Gen = 200

# pop_size - liczebność populacji, dobrze, aby była parzysta
pop_size = 250

# prawdopodobieństwa: krzyżowania (Pc) oraz mutacji (Pm)
Pc = 0.5
Pm = 0.0001

# Funkcja celu jest funkcją jednej zmiennej (k), nie jest używana w tej wersji programu
k = 1

# przedział w którym badamy funkcję (Xmin do Xmax)
# uwaga: w zadaniu występują tylko wartości dodatnie, nie ma potrzeby przesuwania przedziału
Xmin = 0.5
Xmax = 2.5

# dokładność: 3 miejsca po kropce dziesiętnej
d = 3

# obliczamy, ile wartości musimy zakodować binarnie: mi
mi = ((Xmax-Xmin)*10**d)+1

# ...oraz ile bitów potrzebujemy, aby zakodować tyle wartości: m
# używamy logarytmu o podstawie 2 oraz funkcji ceiling (zwraca najbliższą liczbę całkowitą - większą lub równą wskazanej)
# uwaga: badamy funkcję jednej zmiennej (k=1), program nie przewiduje wielu zmiennych!
m = math.ceil(math.log(mi,2)) 

print("Dla zadanej dokładności i przedziału niezbędne jest zakodowanie %s wartości, użyjemy do tego %s bitów." % (mi, m))

# obsadzamy pierwszą populację (pop_size) losowymi wartościami 0/1 wg wyliczonej liczby bitów; pomiędzy chromosoamami nie unikamy powtórzeń

def f_Pokolenie_zero(f_pop_size, f_m, output=False):
    pokolenie_zero = np.random.choice(a=[0, 1], size=(f_pop_size, f_m)) # macierz o rozmiarach populacja x bitowość, losowo 0/1
    if output: print(*pokolenie_zero, sep = "\n")
    print("Wygenerowano losową populację %s osobników, długość chromosomu: %s." % (f_pop_size, f_m))
    return(pokolenie_zero)

# Sprawdzamy dopasowanie danej populacji, obliczając wartość funkcji dla każdego chromosomu 
# (po dekodowaniu dziesiętnym, dekodowanie2dec)

def f_Ewaluacja(pula, output=False):
    ewaluacja = list() # usunięcie danych z listy do przechowywania wartosci funkcji dla danego pokolenia
    for i in range(pop_size):
        my_lst = pula[i] 
        str1=""
        str1 = "".join(map(str, my_lst)) # łączenie elementów listy w string
        dekodowanie2dec = int(str1, 2) # dekodowanie binarki do liczby dziesiętnej 
        mapowanie = ((Xmax-Xmin)*dekodowanie2dec)/((2**m)-1)+Xmin # mapowanie chromosomu do wartości x z zakresu (Xmin,Xmax)
        ewal = funkcja(mapowanie) # wartość funkcji w punkcie x
        ewaluacja.append(ewal) # dodanie wartości do listy
        F = sum(ewaluacja) # obliczamy dopasowanie całej populacji (F)
    if output:
        print("\nDopasowanie poszczególnych osobników populacji do funkcji celu: ")
        print(*ewaluacja, sep="\n")
        print("\nSuma dopasowań dla populacji: "+ str(F))
    return(ewaluacja)
    
    # Prawdopodobieństwo selekcji (wyboru, Ps) dla każdego chromosomu
# f_Pselekcji() - przyjmuje zestaw wartości funkcji, docelowo wynik działania f_Ewaluacja()
# zwraca - lista wartości z zakresu 0-1, dystrybuanta; niezbędna do działania f_Ruletka() 

def f_Pselekcji(ewaluacja):
    Ps=list() # prawdopodobieństwo wyboru (selekcji, Ps) dla każdego chromosomu
    for i in range(pop_size):
        Ps.append(ewaluacja[i]/sum(ewaluacja))
    return(Ps)
    
    # selekcja - metoda koła ruletki (sektory dla Ps)
# f_Ruletka() - przyjmuje: listę prawdopodobieńst selekcji (z f_Pselekcji) oraz populacja, z której pobierany jest osobnik ()
# zwraca pulę rodzicielską, przeznaczoną do krzyżowania i mutacji

def f_Ruletka(p_selekcji, populacja, output=False):
    ruletka = list() # lista z wartościami początkowymi kolejnych przedziałów ruletki
    sektor = 0 # sektor początkowy, sektory będziemy liczyć od zera: sektor 0: (0,Ps), sektor 1: (Ps[i], Ps+Ps[i+1])

    for i in range(pop_size):
        sektor = sektor + p_selekcji[i] 
        ruletka.append(sektor) # dodawanie do listy wartości brzegowej sektora

    pula_rodzicielska = list() # pula osobników, generowana na podstawie dostosowania metodą koła ruletki

    for i in range(pop_size): 
        losowa = rand.random() # losujemy liczbę z przedziału (0,1) tyle razy, ile osobników w populacji
        sektor = 0 # zaczynamy od sektora zero
        for j in range(len(ruletka)): # sprawdzamy, do którego sektora na kole ruletki wpadła wylosowana liczba
            if losowa > ruletka[j]:
                sektor=sektor+1
        if output:
            print("Losowa liczba %s wpada do sektora %s" % (losowa, sektor))
        pula_rodzicielska.append(populacja[sektor]) # do puli rodzicielskiej dodajemy osobnika z puli zero
    return(pula_rodzicielska)
    
    # Krzyżowanie osobników: z puli rodzicielskiej losujemy pop_size/2 par z powtórzeniami
# losujemy losowe_Pc prawdopodobieństwo krzyżowania Pc
# tutaj pytanie, czy losujemy parę dla każdego osobnika z populacji? czy osobnik może wylosować sam siebie?

# funkcja f_Krzyzowanie() przyjmuje pulę osobników do krzyżowania,
# zwraca pulę osobników potomnych

def f_Krzyzowanie(pula, output=False):
    pula_potomkow=list()
#     for i in range(int(pop_size/2)): # metodoa doboru par z powtórzeniami, dziala gorzej 
#         parent_1 = rand.choice(pula)
#         parent_2 = rand.choice(pula)

    rand.shuffle(pula) # tasowanie osobników w puli
    for i in range(int(pop_size-1)): # metoda doboru par bez powtórzeń
        parent_1 = pula[i]
        parent_2 = pula[i+1]
        i=i+1
    
        losowe_Pc = rand.random() # czy zachodzi zdarzenie mutacji?
    
        if losowe_Pc < Pc:  
            punkt_krzyzowania = rand.randrange(1, m-1, 1) # punkt krzyżowania, przecięcie chromosomu najwcześniej za pierwszym bitem, najpóźniej za przedostatnim
            #print("\nPara rodziców: "+ str(parent_1) +" / "+ str(parent_2) +", Krzyżowanie po bicie: " + str(punkt_krzyzowania))
            if output: print("\nPara rodziców: %s / %s, Krzyżowanie po bicie: %s" % (parent_1, parent_2, punkt_krzyzowania))
            potomek_1 = np.concatenate((parent_1[:punkt_krzyzowania], parent_2[punkt_krzyzowania:]), axis=None)   
            potomek_2 = np.concatenate((parent_2[:punkt_krzyzowania], parent_1[punkt_krzyzowania:]), axis=None)
            pula_potomkow.append(parent_1)
            pula_potomkow.append(parent_2)

            if output: print("Para potomków: %s | %s" % (potomek_1, potomek_2))
        else:
            if output: print("\nPara rodziców %s / %s, Brak krzyżowania" % (parent_1, parent_2))
            pula_potomkow.append(parent_1)
            pula_potomkow.append(parent_2)
    return(pula_potomkow)
    
    # Mutacje osobników z populacji potomnej (na pewno można to zrobić ładniej ale już nie zdążę)

# funkcja f_Mutagen() przyjmuje pulę osobników do mutacji,
# zwraca pulę osobników mutowanych, którą możemy poddać procesowi ewaluacji, krzyżowania i mutacji.

def f_Mutagen(pula, output = False):
    pula_mutantow = list() # pula wyjściowa dla funkcji f_Mutagen()
    for i in range(pop_size):
        losowe_Pm = rand.random() # losujemy prawdopodobienstwo mutacji dla każdego osobnika w puli (tutaj w puli potomkow)
        if losowe_Pm < Pm: # jesli wylosowana liczba jest mniejsza od założonej Pm, przechodzimy do mutacji osobnika
            mutant = list() # osobnik mutowany
            pozycja_mutacji = list() # przechowuje informację, które geny zostały zmienione

            for j in range(m): 
                zmiana_genu = bool(rand.getrandbits(1)) # dla każdego bitu losujemy true/false i zmieniamy (lub nie) gen na przeciwny
                if zmiana_genu:
                    mutant.append(int (not(pula[i][j]))) # tutaj jest brzydko, bool rzutujemy na int aby później wrócić do np.asarray 
                    pozycja_mutacji.append(j)
                else:
                    mutant.append(int(pula[i][j]))
            pula_mutantow.append(np.asarray(mutant))
            if output: print(str(pula[i]) +" uległ mutacji na pozycji: "+ str(pozycja_mutacji) +", obecnie wygląda tak: "+ str(np.asarray(mutant)))
        else:
            if output: print("%s nie uległ mutacji" % pula[i])
            pula_mutantow.append(pula[i])
    return(pula_mutantow)
    
    # f_Pokolenie() - wyznacza kolejną pulę osobników z uwzględnieniem algorytmu genetycznego 

wartosc_srednia_ew=[]

def f_Pokolenie(pula):    
    pokolenie_ew = f_Ewaluacja(pula)
    pokolenie_sel = f_Pselekcji(pokolenie_ew)
    pokolenie_rodzicow = f_Ruletka(pokolenie_sel, pula)
    pokolenie_potomkow = f_Krzyzowanie(pokolenie_rodzicow)
    pokolenie_mutantow = f_Mutagen(pokolenie_potomkow)
    global iteracja
    global wartosc_srednia_ew
    wartosc_srednia_ew.append(sum(pokolenie_ew)/pop_size) #  przebieg średniej wartości funkcji dopasowania pokolenia w funkcji nr pokolenia
    iteracja = iteracja + 1
    
    if iteracja == Gen:
        return(pokolenie_mutantow)
    else:
        return(f_Pokolenie(pokolenie_mutantow))

# generowanie pierwszego pokolenia
pierwsze_pokolenie = f_Pokolenie_zero(pop_size, m)

# iteracje przed pokolenia
iteracja = 0
ostatnie_pokolenie = f_Pokolenie(pierwsze_pokolenie)

# "maksymalny" osobnik w ostatnim pokoleniu
print(max(f_Ewaluacja(ostatnie_pokolenie)))

# średnie wartości ewaluacji dla kolejnych pokoleń
print(*wartosc_srednia_ew, sep="\n")

def form_button():
    global iteracja 
    global wartosc_srednia_ew
    
    global pop_size
    global Gen
    
    pop_size=int(form_pop_size.get())
    Gen = int(form_gen.get())
    
    iteracja =0
    wartosc_srednia_ew=[]
    
    start = time.time()
    ostatnie_pokolenie=f_Pokolenie(pierwsze_pokolenie)
    end = time.time()

    the_chosen_one = max(f_Ewaluacja(ostatnie_pokolenie))
    form_max_value.set(the_chosen_one)
    print("guru is happy")
    
root=tk.Tk()

root.title("Laboratorium 3: Algorytm genetyczny, wyznaczanie max funkcji. R.Majkowski (233256), M. Witomski (233270)")
root.configure(bg='white', padx=20, pady=20)

form_pop_size = StringVar()
form_pop_size.set(pop_size)
tk.Entry(root, bg="white", textvariable=form_pop_size).grid(row=0, column=0, padx=10, sticky=tk.W)
tk.Label(root, text="Liczba osobników: ", bg="white", padx = 10).grid(row=1, column=0, padx=10, sticky=tk.W)

form_gen = StringVar()
form_gen.set(Gen)
tk.Entry(root, bg="white", textvariable=form_gen).grid(row=0, column=1, padx=10, sticky=tk.W)
tk.Label(root, text="Liczba pokoleń: ", bg="white", padx = 10).grid(row=1, column=1, padx=10, sticky=tk.W)

form_Pcross = StringVar()
form_Pcross.set(Pc)
tk.Entry(root, bg="white", textvariable=form_Pcross).grid(row=0, column=2, padx=10, sticky=tk.W)
tk.Label(root, text="P. krzyżowania: ", bg="white", padx = 10).grid(row=1, column=2, padx=10, sticky=tk.W)

form_Pmutation = StringVar()
form_Pmutation.set(Pm)
tk.Entry(root, bg="white", textvariable=form_Pmutation).grid(row=0, column=3, padx=10, sticky=tk.W)
tk.Label(root, text="P. mutacji: ", bg="white", padx = 10).grid(row=1, column=3, padx=10, sticky=tk.W)

tk.Button(text="Uruchom", command=form_button).grid(row=0, column=4, padx=10, sticky=tk.W)

form_max_value = StringVar()
form_max_value.set(the_chosen_one)
tk.Label(root, textvariable=form_max_value, bg="white", padx = 10).grid(row=2, column=0, padx=10, sticky=tk.W)

root.mainloop()

