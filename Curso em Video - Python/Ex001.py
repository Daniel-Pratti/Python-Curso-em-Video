"""
Exercício Python 001 - Deixando tudo pronto
Crie um programa que escreva "Olá, Mundo" na tela.
"""

def greeting(name):
    count = 0
    while count < 5:
        print(f'Hello, {name}!')
        count += 1
greeting('World')