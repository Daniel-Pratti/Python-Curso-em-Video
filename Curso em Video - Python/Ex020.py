"""
Exercício Python 020 - Sorteando uma ordem na lista
O mesmo professor do desafio 019 quer sortear a ordem de
apresentação de trabalhos dos alunos. Faça um programa que
leia o nome dos quatro alunos e mostre a ordem sorteada.
"""
from random import shuffle
lista_estudantes = []
num = 1
while num <= 4:
    estudante = str(input(f'Digite o nome do {num}° estudante: '))
    lista_estudantes.append(estudante)
    num += 1
shuffle(lista_estudantes)
print(f'A ordem de apresentação dos trabalhos será {lista_estudantes}')