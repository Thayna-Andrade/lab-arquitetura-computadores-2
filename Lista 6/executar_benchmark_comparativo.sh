#!/bin/bash

echo "============================================================"
echo "   BENCHMARK COMPARATIVO: GCC vs CLANG"
echo "============================================================"

# Compilar com GCC
echo "Compilando com GCC..."
gcc -o algoritmo_gcc algoritmo_completo_c.c -lrt -O2

# Compilar com CLANG
echo "Compilando com CLANG..."
clang -o algoritmo_clang algoritmo_completo_c.c -lrt -O2

# Limpar arquivos anteriores
> resultados_gcc.txt
> resultados_clang.txt

echo ""
echo "Executando benchmarks..."

for tamanho in 100 1000 10000; do
    echo "--- Tamanho $tamanho ---"
    
    # GCC - 10 execuções
    for i in {1..10}; do
        ./algoritmo_gcc $tamanho >> resultados_gcc.txt
    done
    echo "  GCC: 10 execuções concluídas"
    
    # CLANG - 10 execuções
    for i in {1..10}; do
        ./algoritmo_clang $tamanho >> resultados_clang.txt
    done
    echo "  CLANG: 10 execuções concluídas"
done

echo ""
echo "✅ Benchmark concluído!"
echo "Resultados salvos em:"
echo "  - resultados_gcc.txt"
echo "  - resultados_clang.txt"