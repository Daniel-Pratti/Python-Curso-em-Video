"""
Exercício Python 017 - Catetos e Hipotenusa
Faça um programa que leia o comprimento do cateto oposto
e do cateto adjacente de um triângulo retângulo.
Calcule e mostre o comprimento da hipotenusa.
"""
from math import sqrt
cateto_adjacente = float(input ('Digite o cateto adjacente do Triângulo retângulo ? '))
cateto_oposto = float(input ('Digite o cateto oposto do Triângulo retângulo ? '))
hipotenusa = sqrt(cateto_adjacente ** 2 + cateto_oposto ** 2)

print(f'A hipotenusa do seu Triângulo retângulo é {hipotenusa}')


