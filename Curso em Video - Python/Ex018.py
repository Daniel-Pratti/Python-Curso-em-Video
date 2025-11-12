"""
Exercício Python 018 - Seno, Cosseno e Tangente
Faça um programa que leia um ângulo qualquer e mostre na tela
o valor do seno, cosseno e tangente desse ângulo.
"""
import math
angulo = float(input('Qual o valor do seu ângulo? '))
angulo_em_radianos = math.radians(angulo)
seno = math.sin(angulo_em_radianos)
cosseno = math.cos(angulo_em_radianos)
tangente = math.tan(angulo_em_radianos)

print(f'O Cosseno de {angulo} é {cosseno:.2f}')
print(f'O Seno de {angulo} é {seno:.2f}')
if angulo % 180 == 90:
    print(f'A tangente de {angulo} é indefinida')
else:
    print(f'A Tangente de {angulo}, é {tangente:.2f}')
