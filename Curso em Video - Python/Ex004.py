"""
Exercício Python 004 - Dissecando uma Variável
Faça um programa que leia algo pelo teclado e mostre na tela
o seu tipo primitivo e todas as informações possíveis sobre ele.
"""
print ('Bem vindo ao descobridor de tipos Python')
typed_by_user = input ('Digite algo:')
print ('O tipo primitivo deste valor é: ',type(typed_by_user))
print ('Só tem espaços? ',typed_by_user.isspace())
print ('É um número?',typed_by_user.isnumeric())
print ('É alfabético? ',typed_by_user.isalpha())
print ('É alfanumérico? ',typed_by_user.isalnum())
print ('Está em minúsculas? ',typed_by_user.islower())
print ('Está em maiúsculas? ',typed_by_user.isupper())
print ('Está capitalizada? ',typed_by_user.istitle())