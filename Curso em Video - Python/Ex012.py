"""
Exercício Python 012 - Calculando Descontos
Faça um algoritmo que leia o preço de um produto e mostre seu novo preço, com 5% de desconto.
"""
preço = float(input ('Qual o preço do produto?R$ '))
print(f'O preço do produto com 5% de desconto é {float(preço - (preço * 5 / 100))}')