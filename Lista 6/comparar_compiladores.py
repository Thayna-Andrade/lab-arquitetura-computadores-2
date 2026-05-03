# comparar_compiladores.py
import re

def analisar_arquivo(nome_arquivo, nome_compilador):
    dados = {'clock': [], 'clock_gettime': []}
    
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            match = re.search(r'C,(\d+),(\d+),([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+)', linha)
            if match:
                dados['clock'].append(float(match.group(3)))
                dados['clock_gettime'].append(float(match.group(6)))
    
    print(f"\n{nome_compilador}:")
    print(f"  clock (média): {sum(dados['clock'])/len(dados['clock']):.9f} s")
    print(f"  clock_gettime (média): {sum(dados['clock_gettime'])/len(dados['clock_gettime']):.9f} s")

print("="*50)
print("COMPARAÇÃO GCC vs CLANG")
print("="*50)
analisar_arquivo('resultados_gcc.txt', 'GCC')
analisar_arquivo('resultados_clang.txt', 'CLANG')