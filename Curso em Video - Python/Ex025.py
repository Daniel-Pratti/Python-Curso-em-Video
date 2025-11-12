"""
Exercício Python 025 - Procurando uma string dentro de outra
Faça um programa que leia o nome de uma pessoa
e diga se ela tem "Silva" no nome.
"""
nome = input('Digite seu nome completo: ').upper()
if 'SILVA' in nome:
    print('Você tem Silva no nome')
else:
    print('Você não tem Silva no nome')
    