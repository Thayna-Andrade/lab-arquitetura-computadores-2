#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

#define _POSIX_C_SOURCE 199309L

// Algoritmo de soma
int soma(int v[], int n) {
    int s = 0;
    for (int i = 0; i < n; i++)
        s += v[i];
    return s;
}

void preencherVetor(int v[], int n) {
    for (int i = 0; i < n; i++)
        v[i] = i + 1;
}

// Função para medir com clock()
double medir_clock(int v[], int n, int *resultado) {
    clock_t start = clock();
    *resultado = soma(v, n);
    clock_t end = clock();
    return (double)(end - start) / CLOCKS_PER_SEC;
}

// Função para medir com time()
double medir_time(int v[], int n, int *resultado) {
    time_t start = time(NULL);
    *resultado = soma(v, n);
    time_t end = time(NULL);
    return difftime(end, start);
}

// Função para medir com gettimeofday()
double medir_gettimeofday(int v[], int n, int *resultado) {
    struct timeval start, end;
    gettimeofday(&start, NULL);
    *resultado = soma(v, n);
    gettimeofday(&end, NULL);
    return (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1000000.0;
}

// Função para medir com clock_gettime()
double medir_clock_gettime(int v[], int n, int *resultado) {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    *resultado = soma(v, n);
    clock_gettime(CLOCK_MONOTONIC, &end);
    return (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <tamanho_do_vetor>\n", argv[0]);
        return 1;
    }
    
    int n = atoi(argv[1]);
    
    int *v = (int*) malloc(n * sizeof(int));
    if (v == NULL) {
        printf("Erro de alocação!\n");
        return 1;
    }
    
    preencherVetor(v, n);
    
    int resultado;
    
    // Medição com diferentes funções
    double t_clock = medir_clock(v, n, &resultado);
    double t_time = medir_time(v, n, &resultado);
    double t_gettimeofday = medir_gettimeofday(v, n, &resultado);
    double t_clock_gettime = medir_clock_gettime(v, n, &resultado);
    
    // Saída formatada (usando ponto como separador decimal)
    printf("C,%d,%d,%.9f,%.9f,%.9f,%.9f\n", 
           n, resultado, t_clock, t_time, t_gettimeofday, t_clock_gettime);
    
    free(v);
    return 0;
}