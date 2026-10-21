public class HelloException {
    public static void main(String[] args) {
        System.out.println("Two");
        // phép chia hợp lệ
        int value = 10 / 2;
        System.out.println("One");
        // chia cho 0: ngoại lệ phát sinh tại đây
        value = 10 / 0;
        // Dòng này không được thực thi
        System.out.println("Let's go");
    }
}