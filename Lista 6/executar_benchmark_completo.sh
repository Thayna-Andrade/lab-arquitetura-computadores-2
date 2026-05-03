#!/bin/bash

echo "============================================================"
echo "   BENCHMARK COMPLETO - Análise de Funções de Tempo"
echo "============================================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar arquivos
echo -e "${BLUE}[1/6] Verificando arquivos...${NC}"

if [ ! -f "algoritmo_completo_c.c" ]; then
    echo -e "${RED}ERRO: algoritmo_completo_c.c não encontrado!${NC}"
    exit 1
fi

if [ ! -f "algoritmo_completo_python.py" ]; then
    echo -e "${RED}ERRO: algoritmo_completo_python.py não encontrado!${NC}"
    exit 1
fi

if [ ! -f "AlgoritmoCompleto.java" ]; then
    echo -e "${RED}ERRO: AlgoritmoCompleto.java não encontrado!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Todos os arquivos encontrados${NC}"
echo ""

# Compilar C
echo -e "${BLUE}[2/6] Compilando programa em C...${NC}"
gcc -o algoritmo_c_completo algoritmo_completo_c.c -lrt -O2
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Compilação C concluída${NC}"
else
    echo -e "${RED}✗ Erro na compilação C${NC}"
    exit 1
fi
echo ""

# Compilar Java
echo -e "${BLUE}[3/6] Compilando programa em Java...${NC}"
javac AlgoritmoCompleto.java
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Compilação Java concluída${NC}"
else
    echo -e "${RED}✗ Erro na compilação Java${NC}"
    exit 1
fi
echo ""

# Limpar arquivos antigos
echo -e "${BLUE}[4/6] Preparando para coleta de dados...${NC}"
> resultados_c.txt
> resultados_python.txt
> resultados_java.txt
> resultados_completos.txt

# Cabeçalho do arquivo de resultados
echo "# Resultados Completos do Benchmark" > resultados_completos.txt
echo "# Formato: Linguagem,Tamanho,Resultado,Time1,Time2,Time3,Time4" >> resultados_completos.txt
echo "# C: Time1=clock, Time2=time, Time3=gettimeofday, Time4=clock_gettime" >> resultados_completos.txt
echo "# Python: Time1=time.time, Time2=perf_counter, Time3=perf_counter_ns, Time4=process_time" >> resultados_completos.txt
echo "# Java: Time1=currentTimeMillis, Time2=nanoTime, Time3=0, Time4=0" >> resultados_completos.txt
echo "============================================================" >> resultados_completos.txt
echo "" >> resultados_completos.txt

echo -e "${GREEN}✓ Arquivos preparados${NC}"
echo ""

# Executar benchmarks
echo -e "${BLUE}[5/6] Executando benchmarks...${NC}"
echo ""

for tamanho in 100 1000 10000; do
    echo -e "${YELLOW}--- Testando tamanho $tamanho ---${NC}"
    
    # C - 10 execuções
    echo -n "  C: "
    for i in {1..10}; do
        ./algoritmo_c_completo $tamanho >> resultados_c.txt
        echo -n "."
    done
    echo -e " ${GREEN}10 execuções concluídas${NC}"
    
    # Python - 10 execuções
    echo -n "  Python: "
    for i in {1..10}; do
        python3 algoritmo_completo_python.py $tamanho >> resultados_python.txt
        echo -n "."
    done
    echo -e " ${GREEN}10 execuções concluídas${NC}"
    
    # Java - 10 execuções
    echo -n "  Java: "
    for i in {1..10}; do
        java AlgoritmoCompleto $tamanho >> resultados_java.txt
        echo -n "."
    done
    echo -e " ${GREEN}10 execuções concluídas${NC}"
    
    echo ""
done

# Combinar resultados
echo -e "${BLUE}[6/6] Consolidando resultados...${NC}"
cat resultados_c.txt >> resultados_completos.txt
cat resultados_python.txt >> resultados_completos.txt
cat resultados_java.txt >> resultados_completos.txt

echo -e "${GREEN}✓ Resultados salvos em resultados_completos.txt${NC}"
echo ""

# Executar análise
echo -e "${BLUE}Executando análise estatística...${NC}"
echo ""

# Verificar se python3 está disponível
if command -v python3 &> /dev/null; then
    python3 analisar_resultados_completo.py
else
    echo -e "${RED}Python3 não encontrado. Execute o script de análise manualmente.${NC}"
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}   BENCHMARK CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Arquivos gerados:"
echo "  - resultados_c.txt        (dados brutos do C)"
echo "  - resultados_python.txt   (dados brutos do Python)"
echo "  - resultados_java.txt     (dados brutos do Java)"
echo "  - resultados_completos.txt (todos os dados)"
echo ""