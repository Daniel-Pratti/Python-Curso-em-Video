"""
Exercício Python 010 - Conversor de Moedas
Crie um programa que leia quanto dinheiro uma pessoa tem na carteira e mostre quantos dólares ela pode comprar.
"""
print ('Descubra quantos dólares você consegue comprar na cotação atual')
carteira = float(input('Quanto você tem na carteira?R$'))
print(f'Com R${carteira} você pode comprar ${carteira // 5.35:.2f} dólares na cotação atual 07/11/2025')