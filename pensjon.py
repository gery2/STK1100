#pensjonsforsikring
import numpy as np
import matplotlib.pyplot as plt
plt.matplotlib.rcParams.update({'font.size': 22})

ald = np.arange(0, 107)

infile = open('dodssannsynlighet-felles.txt', 'r')
dod = []
for line in infile:
    words = line.split()
    dod.append(float(words[1]))
qx = [x/1000 for x in dod]  #omregner promille til sannsynlighetene.

# Fx=1-np.cumprod(1-qx[30:107]) gir denne feilmeldingen:
# TypeError: unsupported operand type(s) for -: 'int' and 'list'
# Min versjon av Python liker ikke substraksjon av liste inni cumprod
# lager min egen løsning:
Fx = np.zeros(72)
prodsum = (1 - qx[35])
Fx[0] = 1 - (1 - qx[35])
for i in range(71):
    prodsum *= 1 - qx[i+36]
    Fx[i+1] = 1 - prodsum
x = np.arange(0,72)
'''
plt.step(x,Fx,where="post")
plt.xlabel("Gjenstående levetid")
plt.ylabel("Kumulativ fordeling")
plt.show()
'''
px = np.zeros(72)
px[0] = Fx[0]
for i in range(1,72):
    px[i] = Fx[i] - Fx[i-1]

width=1
plt.bar(x,px,width,edgecolor="black")
plt.xlabel("Gjenstående levetid")
plt.ylabel("Punktsannsynlighet")
plt.show()

hx = np.zeros(72)
for i in range(32,72):
    hx[i] = (100000/1.03**32)*((1 - (1/1.03)**(i-31))/(1 - 1/1.03))

EhX = 0 # forventet nåverdi av pensjonsutbetalingene
for i in range(72):
    EhX += hx[i]*px[i]

gx = np.zeros(72)
for i in range(32):
    gx[i] = (1 - (1/1.03)**(i+1))/(1 - 1/1.03)

EgX = 0 #  forventet nåverdi av mannens samlede premieinnbetalinger
for i in range(72):
    EgX += gx[i]*px[i]

K = EhX/EgX
print(K/32)

""" kjøreeksempel
PS C:\python\stk1100> python pensjon.py
10118.64656123571
"""
