"""
Exercício Python 015 - Aluguel de Carros
Escreva um programa que pergunte a quantidade de Km percorridos
por um carro alugado e a quantidade de dias pelos quais ele foi alugado.
Calcule o preço a pagar, sabendo que o carro custa R$60 por dia e R$0,15 por Km rodado.
"""
km = int(input('Quantos KM foram percorridos com o carro? '))
dias = int(input('Por quantos dias o carro foi alugado? '))

print(f"Você Rodou {km}km com o carro em {dias} dias, você deve um total de {float((60 * dias) + (km * 0.15))}R$")