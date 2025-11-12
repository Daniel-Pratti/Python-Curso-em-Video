"""
Exercício Python 022 - Analisador de Textos
Crie um programa que leia o nome completo de uma pessoa e mostre:
- O nome com todas as letras maiúsculas e minúsculas.
- Quantas letras ao todo (sem considerar espaços).
- Quantas letras tem o primeiro nome.
"""

nome = str(input('Digite o seu nome:')).strip()
print(nome.upper())
print(nome.lower())
print(len(nome.replace(' ', '')))
nome_lista = nome.split()
print(len(nome_lista[0]))