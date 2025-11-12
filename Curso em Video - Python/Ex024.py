"""
Exercício Python 024 - Verificando as primeiras letras de um texto
Faça um programa que leia o nome de uma cidade
e diga se ela começa ou não com o nome "Santo".
"""
cidade = input('Digite o nome da cidade: ').upper().strip()
if cidade[:5] == 'SANTO':
    print('O nome da Cidade começa com Santo')
else:
    print('O nome da Cidade não começa com Santo')