"""
Exercício Python 011 - Pintando Parede
Faça um programa que leia a largura e a altura de uma parede em metros,
calcule a sua área e a quantidade de tinta necessária para pintá-la,
sabendo que cada litro de tinta pinta uma área de 2 metros quadrados.
"""

altura = float(input('Digite a altura da sua parede: '))
largura = float(input('Digite a largura da sua parede: '))
area = altura * largura
tinta = area / 2
print(f'Sua parede tem {area:.2f} metros quadrados, você precisa de {tinta:.2f} baldes de tinta para pintar essa parede')

