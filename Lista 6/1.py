import time
import sys

def soma(v, n):
    s = 0
    for i in range(n):
        s += v[i]
    return s

def preencher_vetor(n):
    return list(range(1, n + 1))

def medir_time(v, n):
    """Medição com time.time()"""
    start = time.time()
    resultado = soma(v, n)
    end = time.time()
    return resultado, end - start

def medir_perf_counter(v, n):
    """Medição com time.perf_counter() (alta precisão)"""
    start = time.perf_counter()
    resultado = soma(v, n)
    end = time.perf_counter()
    return resultado, end - start

def medir_perf_counter_ns(v, n):
    """Medição com time.perf_counter_ns() (nanossegundos)"""
    start = time.perf_counter_ns()
    resultado = soma(v, n)
    end = time.perf_counter_ns()
    return resultado, (end - start) / 1e9

def medir_process_time(v, n):
    """Medição com time.process_time() (tempo de CPU)"""
    start = time.process_time()
    resultado = soma(v, n)
    end = time.process_time()
    return resultado, end - start

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python algoritmo_completo_python.py <tamanho_do_vetor>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    v = preencher_vetor(n)
    
    # Medições com diferentes funções
    r1, t1 = medir_time(v, n)
    r2, t2 = medir_perf_counter(v, n)
    r3, t3 = medir_perf_counter_ns(v, n)
    r4, t4 = medir_process_time(v, n)
    
    # Saída formatada
    print(f"Python,{n},{r1},{t1:.9f},{t2:.9f},{t3:.9f},{t4:.9f}")