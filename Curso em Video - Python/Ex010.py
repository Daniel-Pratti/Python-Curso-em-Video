"""
Exercício Python 010 - Conversor de Moedas
Crie um programa que leia quanto dinheiro uma pessoa tem na carteira e mostre quantos dólares ela pode comprar.
"""
print ('Descubra quantos dólares você consegue comprar na cotação atual')
carteira = int(input('Quanto você tem na carteira:'))
print(f'Você pode comprar {carteira // 5.35} dólares na cotação atual 07/11/2025')