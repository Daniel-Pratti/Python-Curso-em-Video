"""
Exercício Python 014 - Conversor de Temperaturas
Escreva um programa que converta uma temperatura digitando em graus Celsius e converta para graus Fahrenheit.
"""
temp_c = float(input('Digite a temperatua em Graus Celsius: '))
temp_f = 9 * temp_c / 5 + 32
print(f'A temperatura {temp_c:.2f}°C equivale a {temp_f:.2f}°F')