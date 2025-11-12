"""
Exercício Python 019 - Sorteando um item na lista
Um professor quer sortear um dos seus quatro alunos para apagar o quadro.
Faça um programa que ajude ele, lendo o nome dos alunos e escrevendo na tela o nome do escolhido.
"""
from random import choice

print('Digite o nome dos alunos para o sorteio.')
aluno1 = str(input('Primeiro Aluno: '))
aluno2 = str(input('Segundo Aluno: '))
aluno3 = str(input('Terceiro Aluno: '))
aluno4 = str(input('Quarto aluno: '))

lista_alunos = [aluno1, aluno2, aluno3, aluno4]
aluno_escolhido = choice(lista_alunos)
print(f'O aluno escolhido foi o {aluno_escolhido}')