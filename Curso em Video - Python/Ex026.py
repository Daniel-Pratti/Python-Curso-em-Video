"""
Exercício Python 026 - Primeira e última ocorrência de uma string
Faça um programa que leia uma frase pelo teclado e mostre:
- Quantas vezes aparece a letra 'A'
- Em que posição ela aparece a primeira vez
- Em que posição ela aparece a última vez
"""
frase = str(input('Digite uma Frase Qualquer: ')).upper().strip()
print(f"A letra A aparece {frase.count('A')}x na frase")
print(f'A primeira letra A apareceu na posição {frase.find('A')+1}')
print(f'A ultima letra A apareceu na posição {frase.rfind('A')+1}')