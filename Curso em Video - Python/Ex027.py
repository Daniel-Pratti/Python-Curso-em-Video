"""
Exercício Python 027 - Primeiro e último nome de uma pessoa
Faça um programa que leia o nome completo de uma pessoa
moastrando em seguido o primeiro e ultimo nome separadamente.
"""
nome = str(input('Digite o seu nome Completo: ')).strip()
nome_listado = nome.split()
print(f'Seu primeiro nome é {nome_listado[0]}')
print(f'Seu último nome é {nome_listado[len(nome_listado) - 1]}')
