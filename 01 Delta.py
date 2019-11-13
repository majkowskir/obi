import numpy as np
import time

# oczekiwana wartość na wyjściu, cel
#z = float(input("Podaj wartość celu: "))
z=0.123456789

# Xn - wektor wejścia
X = np.array([0.4, 0.2, 0.25, 0.98])
n=X.shape

# Wn - Wektor wag
W = np.random.rand(n[0])
# Create an array of the given shape and populate it with random samples from a uniform distribution over [0, 1).

# k - epoki, liczba określająca maksymalną ilość cykli uczenia neuronu (zmiany wag)
k = 50000

# parametr nauczania
parametr_nauczania = 0.001

# y - początkowa wartość wyjściowa neuronu
y = np.dot(X,W)
print(y)

filename=str(time.time())+".txt"
f = open(filename,"w+")

f.write("************* Zestaw parametrów eksperymentu ************\n\n")
f.write("Oczekiwana wartość na wyjściu: " + str(z) +"\n")
f.write("Wartości wejściowe: " + str(X) +"\n")
f.write("Współczynnik nauczania: " + str(parametr_nauczania) +"\n")
f.write("Liczba epok (iteracji): " + str(k) +"\n\n")

f.write("Wylosowane wartości wag: " + str(W) +"\n\n")
f.write("********************************************************* \n\n")

f.write("Nr iteracji;\tWyjście neuronu;\t\tWartosc funckji błędu;\t\t\t\tWagi \t\t\t   \r\n\n")

for i in range(k):
    f.write(str(i) + ";\t\t")
    
    y = np.dot(X,W) # If both a and b are 1-D arrays, it is inner product of vectors (without complex conjugation).
    f.write(str(format(y, '.20f')) + ";\t\t")

    Error_value=0.5*(z-y)**2
    f.write(str(format(Error_value, '.30f')) + ";\t\t")

    wagi=' '.join(str(x) for x in W)
    f.write(str(wagi) + ";\t\t\t")

    if y==z: 
        f.write("************* Wyjście równe oczekiwanemu ************\n\n")
        break
    else:
        for j in range (n[0]):
            korekta = parametr_nauczania * (z-y) * X[j]
            f.write(str(korekta)+";")
            W[j] = W[j] + korekta
        f.write("\n")



f.write("************* Zakończenie eksperymentu   ************\n\n")
f.close()
