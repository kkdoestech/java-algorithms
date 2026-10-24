import java.util.Scanner;

public class Main {

    // standard euclidean algorithm for GCD
    public static long gcd(long a, long b) {
        if (b == 0) return a;
        return gcd(b, a % b);   // recursive call
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();

        // use long cuz a[i] can be up to 10^9
        long[] a = new long[n];

        for (int i = 0; i < n; ++i) {
            a[i] = sc.nextLong();
        }

        // the answer -> is gcd of the entire array -> we can find it by taking gcd of first two, then gcd of that result with the third,
        // and so on...
        long ans = a[0];
        for (int i = 0; i < n; ++i) {
            ans = gcd(ans, a[i]);

            // optimize: if gcd = 1 -> it can never get smaller -> we can break early
            if (ans == 1) break;

        }

        System.out.println(ans);
        sc.close();
    }
}