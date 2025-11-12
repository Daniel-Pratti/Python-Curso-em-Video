"""
Exercício Python 013 - Reajuste Salarial
Faça um algoritmo que leia o salário de um funcionário e mostre seu novo salário, com 15% de aumento.
"""

salario = float(input('Digite seu sálario: R$'))
salario_com_aumento = salario + (salario * 15 / 100)
print(f'Parabéns pela promoção, você teve um aumento de 15%. Seu sálario foi de {salario:.2f} para {salario_com_aumento:.2f}')