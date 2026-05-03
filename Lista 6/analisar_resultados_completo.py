import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def extrair_dados_c(arquivo):
    """Extrai dados do arquivo C"""
    dados = {'clock': [], 'time': [], 'gettimeofday': [], 'clock_gettime': []}
    tamanhos = []
    
    with open(arquivo, 'r') as f:
        for linha in f:
            # Formato: C,100,5050,0.000001,0.000000,0.000001,0.000001
            match = re.search(r'C,(\d+),(\d+),([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+)', linha)
            if match:
                tamanho = int(match.group(1))
                tamanhos.append(tamanho)
                dados['clock'].append(float(match.group(3)))
                dados['time'].append(float(match.group(4)))
                dados['gettimeofday'].append(float(match.group(5)))
                dados['clock_gettime'].append(float(match.group(6)))
    
    return tamanhos, dados

def extrair_dados_python(arquivo):
    """Extrai dados do arquivo Python"""
    dados = {'time': [], 'perf_counter': [], 'perf_counter_ns': [], 'process_time': []}
    tamanhos = []
    
    with open(arquivo, 'r') as f:
        for linha in f:
            # Formato: Python,100,5050,0.000001,0.000001,0.000001,0.000001
            match = re.search(r'Python,(\d+),(\d+),([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+)', linha)
            if match:
                tamanho = int(match.group(1))
                tamanhos.append(tamanho)
                dados['time'].append(float(match.group(3)))
                dados['perf_counter'].append(float(match.group(4)))
                dados['perf_counter_ns'].append(float(match.group(5)))
                dados['process_time'].append(float(match.group(6)))
    
    return tamanhos, dados

def extrair_dados_java(arquivo):
    """Extrai dados do arquivo Java"""
    dados = {'currentTimeMillis': [], 'nanoTime': []}
    tamanhos = []
    
    with open(arquivo, 'r') as f:
        for linha in f:
            # Formato: Java,100,5050,0.000001,0.000001,0,0
            match = re.search(r'Java,(\d+),(\d+),([0-9.]+),([0-9.]+),0,0', linha)
            if match:
                tamanho = int(match.group(1))
                tamanhos.append(tamanho)
                # Filtrar valores negativos ou muito grandes
                tempo_milli = float(match.group(3))
                tempo_nano = float(match.group(4))
                
                # Só adicionar se for positivo e razoável (menos que 1 segundo para nano)
                if tempo_milli >= 0 and tempo_milli < 1:
                    dados['currentTimeMillis'].append(tempo_milli)
                if tempo_nano > 0 and tempo_nano < 1:
                    dados['nanoTime'].append(tempo_nano)
    
    return tamanhos, dados

def calcular_estatisticas(valores):
    """Calcula média, desvio padrão, min, max"""
    if not valores:
        return {'media': 0, 'std': 0, 'min': 0, 'max': 0}
    return {
        'media': np.mean(valores),
        'std': np.std(valores),
        'min': np.min(valores),
        'max': np.max(valores)
    }

def criar_tabela_comparativa():
    """Cria tabela comparativa das funções de tempo"""
    print("\n" + "="*100)
    print("TABELA COMPARATIVA DAS FUNÇÕES DE MEDIÇÃO DE TEMPO")
    print("="*100)
    print(f"{'Função':<25} {'Linguagem':<12} {'Resolução':<15} {'Overhead':<12} {'Uso Principal':<30}")
    print("-"*100)
    
    tabela = [
        ("clock()", "C", "~1 µs", "Baixo", "Tempo de CPU"),
        ("time()", "C", "1 segundo", "Muito baixo", "Tempo real (baixa precisão)"),
        ("gettimeofday()", "C", "1 µs", "Médio", "Tempo real (obsoleto)"),
        ("clock_gettime()", "C", "1 ns", "Médio", "Tempo real (recomendado)"),
        ("time.time()", "Python", "1 µs-1s", "Médio", "Tempo real"),
        ("time.perf_counter()", "Python", "~1 ns", "Médio", "Tempo real (alta precisão)"),
        ("time.perf_counter_ns()", "Python", "1 ns", "Médio", "Tempo real (nanossegundos)"),
        ("time.process_time()", "Python", "~1 µs", "Baixo", "Tempo de CPU"),
        ("System.currentTimeMillis()", "Java", "1 ms", "Baixo", "Tempo real (ms)"),
        ("System.nanoTime()", "Java", "1 ns", "Médio", "Tempo real (alta precisão)")
    ]
    
    for func, lang, res, overhead, uso in tabela:
        print(f"{func:<25} {lang:<12} {res:<15} {overhead:<12} {uso:<30}")
    
    print("="*100)

def gerar_graficos(dados_c, dados_py, dados_java, tamanhos_c, tamanhos_py, tamanhos_java):
    """Gera gráficos comparativos incluindo Java"""
    
    tamanhos = [100, 1000, 10000]
    
    # Gráfico 1: Comparação das funções em C
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Comparação das Funções de Tempo em C', fontsize=14)
    
    funcs_c = ['clock', 'time', 'gettimeofday', 'clock_gettime']
    for idx, func in enumerate(funcs_c):
        ax = axes[idx//2, idx%2]
        medias = []
        stds = []
        for t in tamanhos:
            vals = [dados_c[func][i] for i, sz in enumerate(tamanhos_c) if sz == t][:10]
            if vals:
                medias.append(np.mean(vals))
                stds.append(np.std(vals))
            else:
                medias.append(0)
                stds.append(0)
        ax.bar(range(len(tamanhos)), medias, yerr=stds, capsize=5)
        ax.set_xticks(range(len(tamanhos)))
        ax.set_xticklabels(tamanhos)
        ax.set_title(f'C - {func}')
        ax.set_ylabel('Tempo (segundos)')
        ax.set_xlabel('Tamanho do vetor')
    
    plt.tight_layout()
    plt.savefig('comparacao_c.png', dpi=150)
    print("\n✓ Gráfico 1 salvo: comparacao_c.png")
    
    # Gráfico 2: Comparação Python vs C
    plt.figure(figsize=(10, 6))
    for lang, dados, tamanhos_lista, label in [
        ('C', dados_c, tamanhos_c, 'C - clock_gettime'),
        ('Python', dados_py, tamanhos_py, 'Python - perf_counter_ns')
    ]:
        medias = []
        for t in tamanhos:
            if lang == 'C':
                vals = [dados['clock_gettime'][i] for i, sz in enumerate(tamanhos_lista) if sz == t][:10]
            else:
                vals = [dados['perf_counter_ns'][i] for i, sz in enumerate(tamanhos_lista) if sz == t][:10]
            if vals:
                medias.append(np.mean(vals))
            else:
                medias.append(0)
        plt.plot(tamanhos, medias, marker='o', label=label)
    
    plt.yscale('log')
    plt.xlabel('Tamanho do vetor')
    plt.ylabel('Tempo (segundos) - escala log')
    plt.title('Comparação de Desempenho: C vs Python')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('comparacao_c_python.png', dpi=150)
    print("✓ Gráfico 2 salvo: comparacao_c_python.png")
    
    # Gráfico 3: Comparação Java (funções de tempo)
    fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
    fig2.suptitle('Comparação das Funções de Tempo em Java', fontsize=14)
    
    # Gráfico 3a: currentTimeMillis
    ax1 = axes2[0]
    medias_millis = []
    stds_millis = []
    for t in tamanhos:
        vals = [dados_java['currentTimeMillis'][i] for i, sz in enumerate(tamanhos_java) if sz == t][:10]
        if vals and np.mean(vals) > 0:
            medias_millis.append(np.mean(vals))
            stds_millis.append(np.std(vals))
        else:
            medias_millis.append(0)
            stds_millis.append(0)
    ax1.bar(range(len(tamanhos)), medias_millis, yerr=stds_millis, capsize=5, color='orange')
    ax1.set_xticks(range(len(tamanhos)))
    ax1.set_xticklabels(tamanhos)
    ax1.set_title('Java - currentTimeMillis()')
    ax1.set_ylabel('Tempo (segundos)')
    ax1.set_xlabel('Tamanho do vetor')
    
    # Gráfico 3b: nanoTime
    ax2 = axes2[1]
    medias_nano = []
    stds_nano = []
    for t in tamanhos:
        vals = [dados_java['nanoTime'][i] for i, sz in enumerate(tamanhos_java) if sz == t][:10]
        if vals and np.mean(vals) > 0:
            medias_nano.append(np.mean(vals))
            stds_nano.append(np.std(vals))
        else:
            medias_nano.append(0)
            stds_nano.append(0)
    ax2.bar(range(len(tamanhos)), medias_nano, yerr=stds_nano, capsize=5, color='green')
    ax2.set_xticks(range(len(tamanhos)))
    ax2.set_xticklabels(tamanhos)
    ax2.set_title('Java - System.nanoTime()')
    ax2.set_ylabel('Tempo (segundos)')
    ax2.set_xlabel('Tamanho do vetor')
    
    plt.tight_layout()
    plt.savefig('comparacao_java.png', dpi=150)
    print("✓ Gráfico 3 salvo: comparacao_java.png")
    
    # Gráfico 4: Comparação das MELHORES funções das 3 linguagens
    plt.figure(figsize=(12, 7))
    
    # C - clock_gettime
    medias_c = []
    for t in tamanhos:
        vals = [dados_c['clock_gettime'][i] for i, sz in enumerate(tamanhos_c) if sz == t][:10]
        if vals:
            medias_c.append(np.mean(vals))
        else:
            medias_c.append(0)
    
    # Python - perf_counter_ns
    medias_py = []
    for t in tamanhos:
        vals = [dados_py['perf_counter_ns'][i] for i, sz in enumerate(tamanhos_py) if sz == t][:10]
        if vals:
            medias_py.append(np.mean(vals))
        else:
            medias_py.append(0)
    
    # Java - nanoTime
    medias_java = []
    for t in tamanhos:
        vals = [dados_java['nanoTime'][i] for i, sz in enumerate(tamanhos_java) if sz == t][:10]
        if vals and np.mean(vals) > 0:
            medias_java.append(np.mean(vals))
        else:
            medias_java.append(0)
    
    # Plotar as três linguagens
    x = range(len(tamanhos))
    width = 0.25
    
    plt.bar([i - width for i in x], medias_c, width, label='C (clock_gettime)', color='blue', alpha=0.7)
    plt.bar(x, medias_py, width, label='Python (perf_counter_ns)', color='red', alpha=0.7)
    plt.bar([i + width for i in x], medias_java, width, label='Java (nanoTime)', color='green', alpha=0.7)
    
    plt.xlabel('Tamanho do vetor')
    plt.ylabel('Tempo médio (segundos)')
    plt.title('Comparação de Desempenho: C vs Python vs Java')
    plt.xticks(x, tamanhos)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras (apenas se > 0)
    for i, (c, p, j) in enumerate(zip(medias_c, medias_py, medias_java)):
        if c > 0:
            plt.text(i - width, c + (c*0.02), f'{c:.6f}', ha='center', va='bottom', fontsize=8)
        if p > 0:
            plt.text(i, p + (p*0.02), f'{p:.6f}', ha='center', va='bottom', fontsize=8)
        if j > 0:
            plt.text(i + width, j + (j*0.02), f'{j:.6f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('comparacao_3_linguagens.png', dpi=150)
    print("✓ Gráfico 4 salvo: comparacao_3_linguagens.png")
    
    # Gráfico 5: Gráfico em escala log das 3 linguagens
    plt.figure(figsize=(10, 6))
    
    # Filtrar apenas dados válidos ( > 0)
    medias_c_validas = [m if m > 0 else None for m in medias_c]
    medias_py_validas = [m if m > 0 else None for m in medias_py]
    medias_java_validas = [m if m > 0 else None for m in medias_java]
    
    plt.plot(tamanhos, medias_c_validas, marker='o', label='C (clock_gettime)', linewidth=2, markersize=8)
    plt.plot(tamanhos, medias_py_validas, marker='s', label='Python (perf_counter_ns)', linewidth=2, markersize=8)
    plt.plot(tamanhos, medias_java_validas, marker='^', label='Java (nanoTime)', linewidth=2, markersize=8)
    
    plt.yscale('log')
    plt.xlabel('Tamanho do vetor', fontsize=12)
    plt.ylabel('Tempo médio (segundos) - escala log', fontsize=12)
    plt.title('Comparação de Desempenho: C vs Python vs Java (escala log)', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, which='both')
    plt.savefig('comparacao_3_linguagens_log.png', dpi=150)
    print("✓ Gráfico 5 salvo: comparacao_3_linguagens_log.png")
    
    print("\n" + "="*50)
    print("RESUMO DOS GRÁFICOS GERADOS:")
    print("="*50)
    print("1. comparacao_c.png                    - Funções de tempo em C")
    print("2. comparacao_c_python.png             - Comparação C vs Python")
    print("3. comparacao_java.png                 - Funções de tempo em Java")
    print("4. comparacao_3_linguagens.png         - Comparação C vs Python vs Java")
    print("5. comparacao_3_linguagens_log.png     - Comparativo em escala log")
    print("="*50)

def main():
    print("\n" + "="*100)
    print("ANÁLISE ESTATÍSTICA DOS RESULTADOS DO BENCHMARK")
    print("="*100)
    
    try:
        # Extrair dados
        tamanhos_c, dados_c = extrair_dados_c('resultados_c.txt')
        tamanhos_py, dados_py = extrair_dados_python('resultados_python.txt')
        tamanhos_java, dados_java = extrair_dados_java('resultados_java.txt')
        
        # Agrupar por tamanho único
        tamanhos_unicos = sorted(set(tamanhos_c))
        
        # Tabela de resultados
        print("\nRESULTADOS MÉDIOS (em segundos):")
        print("-"*100)
        print(f"{'Linguagem':<12} {'Função':<22} {'Tamanho 100':<15} {'Tamanho 1000':<15} {'Tamanho 10000':<15}")
        print("-"*100)
        
        # Dados do C
        for func in ['clock', 'time', 'gettimeofday', 'clock_gettime']:
            linha = f"{'C':<12} {func:<22}"
            for tamanho in tamanhos_unicos:
                idx = [i for i, t in enumerate(tamanhos_c) if t == tamanho]
                valores = [dados_c[func][i] for i in idx[:10]]
                if valores:
                    media = np.mean(valores)
                    linha += f" {media:.9f}     "
                else:
                    linha += f" {'N/A':<15}"
            print(linha)
        
        print("-"*100)
        
        # Dados do Python
        for func in ['time', 'perf_counter', 'perf_counter_ns', 'process_time']:
            linha = f"{'Python':<12} {func:<22}"
            for tamanho in tamanhos_unicos:
                idx = [i for i, t in enumerate(tamanhos_py) if t == tamanho]
                valores = [dados_py[func][i] for i in idx[:10]]
                if valores:
                    media = np.mean(valores)
                    linha += f" {media:.9f}     "
                else:
                    linha += f" {'N/A':<15}"
            print(linha)
        
        print("-"*100)
        
        # Dados do Java
        for func in ['currentTimeMillis', 'nanoTime']:
            linha = f"{'Java':<12} {func:<22}"
            for tamanho in tamanhos_unicos:
                idx = [i for i, t in enumerate(tamanhos_java) if t == tamanho]
                valores = [dados_java[func][i] for i in idx[:10]]
                if valores:
                    media = np.mean(valores)
                    linha += f" {media:.9f}     "
                else:
                    linha += f" {'N/A':<15}"
            print(linha)
        
        print("="*100)
        
        # Criar tabela comparativa das funções
        criar_tabela_comparativa()
        
        # Análise crítica
        print("\n" + "="*100)
        print("ANÁLISE CRÍTICA DAS FUNÇÕES DE MEDIÇÃO")
        print("="*100)
        
        print("\n1. **clock() - C**")
        print("   ✓ Vantagens: Mede tempo de CPU (usuário + sistema), portável")
        print("   ✗ Desvantagens: Não mede tempo de parede, pode overflow")
        
        print("\n2. **time() - C**")
        print("   ✓ Vantagens: Muito simples, portável")
        print("   ✗ Desvantagens: Precisão de apenas 1 segundo - INÚTIL para benchmarks!")
        
        print("\n3. **gettimeofday() - C**")
        print("   ✓ Vantagens: Microssegundos, boa precisão")
        print("   ✗ Desvantagens: Obsoleto, sujeito a ajustes do sistema")
        
        print("\n4. **clock_gettime() - C**")
        print("   ✓ Vantagens: Nanossegundos, CLOCK_MONOTONIC evita ajustes")
        print("   ✗ Desvantagens: Disponível apenas em sistemas POSIX")
        
        print("\n5. **time.perf_counter() - Python**")
        print("   ✓ Vantagens: Alta precisão, inclui sleep")
        print("   ✗ Desvantagens: Overhead da linguagem interpretada")
        
        print("\n6. **System.nanoTime() - Java**")
        print("   ✓ Vantagens: Nanossegundos, alta precisão")
        print("   ✗ Desvantagens: Overhead da JVM, warmup necessário")
        
        print("\n" + "="*100)
        print("CONCLUSÃO: A MELHOR FUNÇÃO É...")
        print("="*100)
        print("""
        🏆 clock_gettime() (C) / time.perf_counter_ns() (Python) / System.nanoTime() (Java)
        
        Motivos:
        1. Maior precisão (nanossegundos)
        2. Não são afetadas por ajustes de hora do sistema
        3. São as recomendadas pela indústria para benchmarks
        4. Permitem medir diferentes tipos de tempo
        
        Para comparações precisas de desempenho em nível de sistema,
        recomenda-se SEMPRE usar funções de alta resolução como 
        clock_gettime() com CLOCK_MONOTONIC em C, perf_counter_ns() 
        em Python, ou nanoTime() em Java.
        """)
        
        print("="*100)
        
        # Gerar gráficos (agora com Java incluído!)
        try:
            gerar_graficos(dados_c, dados_py, dados_java, tamanhos_c, tamanhos_py, tamanhos_java)
        except Exception as e:
            print(f"\n⚠️ Não foi possível gerar gráficos: {e}")
            print("   (matplotlib pode não estar instalado)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("   Execute o benchmark primeiro com: ./executar_benchmark_completo.sh")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()