"""
Exercício Python 016 - Quebrando um número
Crie um programa que leia um número Real qualquer pelo teclado e mostre na tela a sua porção Inteira.
"""
from math import trunc

numero = float(input("Digite um número: "))
print(f'O número digitado foi {numero} sua porção inteira é {trunc(numero)}')
