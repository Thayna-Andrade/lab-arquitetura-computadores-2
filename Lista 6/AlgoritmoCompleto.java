import java.util.Locale;

public class AlgoritmoCompleto {
    
    public static int soma(int[] v, int n) {
        int s = 0;
        for (int i = 0; i < n; i++) {
            s += v[i];
        }
        return s;
    }
    
    public static int[] preencherVetor(int n) {
        int[] v = new int[n];
        for (int i = 0; i < n; i++) {
            v[i] = i + 1;
        }
        return v;
    }
    
    // Medição com System.currentTimeMillis() (milissegundos)
    public static double medirCurrentTimeMillis(int[] v, int n, int[] resultado) {
        long start = System.currentTimeMillis();
        resultado[0] = soma(v, n);
        long end = System.currentTimeMillis();
        return (end - start) / 1000.0;
    }
    
    // Medição com System.nanoTime() (nanossegundos)
    public static double medirNanoTime(int[] v, int n, int[] resultado) {
        long start = System.nanoTime();
        resultado[0] = soma(v, n);
        long end = System.nanoTime();
        long diff = end - start;
        // Tratar possível overflow
        if (diff < 0) {
            diff = Long.MAX_VALUE - start + end;
        }
        return diff / 1_000_000_000.0;
    }
    
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java AlgoritmoCompleto <tamanho_do_vetor>");
            System.exit(1);
        }
        
        int n = Integer.parseInt(args[0]);
        int[] v = preencherVetor(n);
        
        int[] resultado = new int[1];
        
        // Medições
        double t_millis = medirCurrentTimeMillis(v, n, resultado);
        int resultado1 = resultado[0];
        
        double t_nano = medirNanoTime(v, n, resultado);
        int resultado2 = resultado[0];
        
        // Saída formatada
        System.out.printf(Locale.US, "Java,%d,%d,%.9f,%.9f,0,0%n", 
                          n, resultado1, t_millis, t_nano);
    }
}