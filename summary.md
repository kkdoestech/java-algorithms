
/*

J04006 - Khai báo lớp sinh viên
    1. Core OOP Design Principles
        1. Class Design & Encapsulation ((private) fields)
        In OOP -> Encapsulation -> is the principle of hiding internal data (state) and only allowing access 
        through controlled methods.
            + By setting (name), (lop), (dob) and (gpa) to (private) -> we prevent external code (like the
            (main) method) -> from writing invalid data directly.
                -> For ex: no one can accidently do stu.gpa = -5.0 or stu.name = null from outside the class.

            + The field (msv) (Mã so sinh vien - Student ID) -> is pre-initialized to "B20DCCN001" -> because 
            this specific problem (J04006) -> requires a fixed, hardcoded student code for every student created.
                -> The problem statement asks for exactly this format.
        2. Constructor Chaining ( this("", "", "", 0f); )
            look at the default constructor:
                public Student() {
                    this("", "", "", 0f);
                }
                    
                    + This is called Constructor Chaining. -> Instead of manually writing ->
                    this.name = ""; this.lop = "";... -> we use this(...) -> to call the parameterized 
                    constructor right below it.
    





    Step 1: Build the Class & Encapsulation
        Your task: Create a (class Student). -> Inside, declare exactly 5 (private) attributes: (msv) (String),
        (name) (String), (lop) (String) (dob) (String) and (gpa) (float).
        
        Mentor Hints:
            + The ID: Initialize (msv) right there -> in the declaration: (private String msv = "B20DCCN001";)
                -> this is called an instance variable initializer.
            + The Constructors: Write 2 constructors
                + Constructor 1 (Default/No-arg): Takes zero parameters. Inside it, put just 1 line:
                    this("", "", "", 0f);
                + Constructor 2 (Parameterized): Takes (String name, String lop, String dob, float gpa).
                    -> Inside, assign the arguments to your (this) attributes.
            + Syntax Check: Remember, if your parameter name -> is the same as your attribute (ex: name)    
                -> you must use (this.name = name;) -> to tell Java which one is the class field.

    

    Step 2: The Date Standardization Method
        Your task: Write a (public) method named (formatDob()) -> that returns a (String).
            -> it should take the messy (dob) string (eg: 2/2/2002) -> and turn into a clean "02/02/2002"

        Mentor Hints:
            + The Tool: You need (SimpleDateFormat). -> create it like this:
                -> SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy")
            + The Flow (Crucial): You must PARSE the messy string -> into a (Date) object, then format that 
            (Date) object -> back into a fresh string.
                1. Date date = formatter.parse(dob);
                2. return formatter.format(date).
            + The Try-Catch trap: The .parse() method -> is dangerous - if the user types "02-02-2002" (with
            dashes) -> it crashed.
                -> java forced you to predict this.
                    -> Wrap formatter.parse(dob) -> inside a -> try {...} block -> and catch ParseException e.
                        -> In the (catch) -> just print the error and return ""; -> as a fallback.

    
    Step 3: Overriding toString() for Perfect Output
        Your task: Override the (toString()) method.
            -> It must return 1 single String -> combining the ID, name, class, standardized DOB, and formatted
            GPA, all seperated by spaces.

        + Mentor Hints:
            + The Annotation: Write @Override -> right above your method.
                -> this tells the Compiler "I know I'm replacing the parent method".
            + The GPA Format: Don't just add (gpa). -> Use String.format("%.2f", gpa) -> to force exactly 2
            decimal places (eg: 2 becomes 2.00).
            + The Return: Combine everything with the "+" operator.
            + Crucial Rule: => You must call formatDob() -> inside this return statement -> to get to the
            cleaned-up date, not the raw (dob).

    Step 4: Write the (main()) driver
        Your task: Write the (public static void main) -> inside a seperate public class named ...
            -> Read the inputs.
        + Mentor Hints:
            + Input Order: Name (nextLine) -> Class (nextLine) -> DOB (nextLine) -> GPA (nextFloat)
            + Creating the Object: After reading all 4 variables -> create your student:
                Student stu = new Student(name, lop, dob, gpa);
            + The Magic Print: -> Write System.out.println(stu);
                -> Remember -> because you overrode toString() -> Java automatically -> calls your method here
                -> You don't call it explicitly like => stu.toString().

*/


/*
J04007 - Khai báo lớp nhân viên
    -> This (Staff) class -> is almost a twin of the Student class we just built, but with 7 attributes and
    NO DATE FORMATTING.
    
    1. OOP Structures & Constructor Delegation
        + Encapsulation ((private) attributes)
        All 7 fields (mnv, name, sex, dob, address, tax, date) -> are (private) for the same reasons as before:
            + Data Protection: Prevents external classes -> from directly setting invalid or null values (eg:
            someone can't accidently do sta.name = null from (main)).
            + Controlled Interface: If you later need to validate that -> 'Nam' -> is only "Male/Female"    
                -> you would add a setter method - without breaking the code that calls it.
        
        Constructor Delegation (this(...)):
            public Staff() {
                this("00001", "", "", "", "", "", "", "");
            }

                + When someone calls -> new Staff() -> with no arguments -> it immediately jumps to the 7-
                parameter constructor -> passing a hardcoded ID "00001" and empty strings for everything else.

                Why is this useful, even though main() -> doesn't use this?
                    + Even though main() -> use the full constructor directly -> this default constructor
                        -> is defensive programming.
                            -> it ensures that => if another developer (or future you) -> tries to create a
                            Staff object without providing data (new Staff()) -> the program won't crash with
                            null pointer errors.
                        -> It also centralizes all initialization logic -> in 1 place (the 7-param constructor)
                            -> so if you add logging or validation  -> you only add it once.
                
                + Hardcoded Attribute Requirements (mnv = "00001"):
                    The problem specification (J04007) -> explicitly states the staff ID -> must be "00001".
                        -> it's not part of the input.
                            -> that's why main() -> passes it directly as a literal -> instead of reading it
                            with sc.nextLine()
                                -> the default constructor -> also has it baked in for safety.



    2. Line-by-line I/O Mechanics
        sc.nextLine() vs sc.next():
            => classic pitfall!
                + sc.next() -> reads only 1 TOKEN (stops at whitespace)
                + sc.nextLine() -> reads the entire token, including spaces.

            Look at the sample input: (Mo Lao-Ha Dong-Ha Noi) -> has spaces.
                -> if used sc.next() -> it would only stores "Mo".
                    => nextLine() -> is mandatory to capture the FULL address as 1 string.

        String Formatting in -> toString():
            The code uses simple concatenation: (mnv + " " + name + ...)
                + Why is this enough? -> because every field -> is already a String, and there is no requirement
                -> to pad numbers or force decimal places (like GPA).
                + It is perfectly sufficient -> here. String.format() -> is useful when you specific formatting
                (%.2f) or padding (%10s) -> but for plain text -> + -> is faster.

        Implicit Method Calls:
            When you write -> System.out.println(sta) -> the Java compiler -> sees you're passing an Object
            (a Staff instance).
                -> the (println) method -> internally calls (sta.toString()) -> to convert the object -> into
                a printable (String).
                    -> Because you overrode (toString()) -> with @Override -> your custom String is used
                    instead of the default garbage (like -> Staff@15db9742).


*/



/*
J04012 - Tính công
        Imagine you run a small shop. You have 1 empolyee (for now).
        Each day show up -> you pay them daily wage (like 45,000 VND per day).

        + At the end of the month -> you count how many days they worked - say 23 days
            + Base salary = daily wage * days worked
            + Bonus - if they worked more than 25 days -> they get a 20% bonus on base salary
            if they worked a decent amount (22-24) -> 10% bonus; otherwise -> no bonus.
            + Allowance - if they are a manager (GD); senior manager (PGD), team leader (TP),
            or regular staff (NV) -> you give them a fixed monthly addition.

        + You also need to give them an official employee ID - starting at NV01 (since this is
        the first employee)

        The goal: input the person's details, compute all 3 parts (salary, bonus, allowance), sum
        them up, and print everything nicely in 1 line.

    Step 2: Creating the Officer object
        We call the constructor -> new Officer(name, wage, workingDays, role).
            -> Inside that constructor:
                + (this.id = "NV01";) - fixed because we only have 1 employee for now.
                + (this.name = name;) - store the name.
                + (this.salary = wage * workingDays;) - 45,000 * 23 = 1,035,000
                + Now determine (bonus):
                    + (workingDays > 25) ? No (23 < 25)
                    + (workingDays >= 22) ? Yes (23 >= 22) -> 10% bonus = 103,500
                    + (int)(salary * 0.1f) -> (int)(1,035,000 * 0.1) = 103,500
                + Determine (allowance) using a (switch) on (role):
                    + (role) is "PGD" -> so case "PGD" -> allowance = 200,000
        
        -> At the end of the constructor -> we have:
            + id = "NV01"
            + name = "Nguyen Van A"
            + salary = 1,035,000
            + bonus = 103,500
            + allowance = 200,000

    Step 3: Computing income & printing
        The (toString()) method -> is called automatically when we do (System.out.println(officer)).
            -> it concatenates:
            id + " " + name + " " + salary + " " + bonus + " " + allowance + " " + getIncome()
                
                + getIncome() -> returns salary + bonus + allowance = 1,338,500
            
        so the printed line becomes:
            NV01 Nguyen Van A 1035000 103500 200000 1338500




    3. Line-by-line Java Code Breakdown
        The Officer class (fields + constructor)
            class Officer {
                private string id, name;
                private int salary, bonus, allowance;

                public Officer(String name, int wage, int workingDays, String role) {
                    this.id = "NV01";
                    this.name = name;
                    this.salary = wage * workingDays;

                        }
                }
            
            
            
            }
*/


/* 
import java.util.Scanner;

class SanPham {
    private String ma;
    private String ten;
    private int soLuong;
    private String nhaSX;
    private double gia;
    
    // Biến static để tự động tăng mã sản phẩm
    private static int dem = 1;

    // Constructor: Chú ý thứ tự tham số phải khớp với hàm main
    public SanPham(String ten, int soLuong, String nhaSX, double gia) {
        this.ten = ten;
        this.soLuong = soLuong;
        this.nhaSX = nhaSX;
        this.gia = gia;
        // Tạo mã sản phẩm: Tên NSX viết hoa + "-" + số thứ tự 3 chữ số
        this.ma = nhaSX.toUpperCase() + "-" + String.format("%03d", dem++);
    }

    public String getMa() {
        return ma;
    }

    public double getThanhTien() {
        if (soLuong < 20) {
            return soLuong * gia;
        } else {
            // Giảm 10% => nhân với 0.9
            return soLuong * gia * 0.9;
        }
    }

    @Override
    public String toString() {
        // Định dạng giá và thành tiền lấy 1 số lẻ, thêm \n vì hàm main dùng print
        return ma + " " + ten + " " + soLuong + " " + 
               String.format("%.1f", gia) + " " + 
               String.format("%.1f", getThanhTien()) + "\n";
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());
        SanPham s;
        for (int i = 0; i < n; i++) {
            s = new SanPham(sc.nextLine(),
                            Integer.parseInt(sc.nextLine()),
                            sc.nextLine(),
import java.util.Scanner;

class DaThuc {
    private int n;
    private double[] a;

    // Constructor khởi tạo theo bậc n
    public DaThuc(int n) {
        this.n = n;
        this.a = new double[n + 1];
    }

    // Constructor khởi tạo từ mảng hệ số có sẵn
    public DaThuc(double[] a) {
        this.a = a;
        this.n = a.length - 1;
    }

    public int getBac() {
        return this.n;
    }

    public double[] getA() {
        return this.a;
    }

    // Nhập n + 1 hệ số theo bậc tăng dần (từ bậc 0 đến bậc n)
    public void input(Scanner in) {
        for (int i = 0; i <= this.n; i++) {
            this.a[i] = in.nextDouble();
        }
    }

    // In đa thức theo định dạng: c0 * X^0 + c1 * X^1 + ... + cn * X^n
    public void out() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= this.n; i++) {
            sb.append(this.a[i]).append(" * X^").append(i);
            if (i < this.n) {
                sb.append(" + ");
            }
        }
        System.out.println(sb.toString());
    }

    // Nhân 2 đa thức: bậc mới = n + m
    public DaThuc nhan(DaThuc b) {
        int m = b.getBac();
        int bacMoi = this.n + m;
        double[] heSoMoi = new double[bacMoi + 1];
        double[] bA = b.getA();

        for (int i = 0; i <= this.n; i++) {
            for (int j = 0; j <= m; j++) {
                heSoMoi[i + j] += this.a[i] * bA[j];
            }
        }

        return new DaThuc(heSoMoi);
    }
}
                            Double.parseDouble(sc.nextLine()));
            System.out.print(s.toString());
        }
    }
}

*/

/* 
import java.util.Scanner;

class DaThuc {
    private int n;
    private double[] a;

    public DaThuc(int n) {
        this.n = n;
        this.a = new double[n + 1];
    }

    public DaThuc(double[] a) {
        this.a = a;
        this.n = a.length - 1;
    }

    public int getBac() {
        return n;
    }

    public double[] getA() {
        return a;
    }

    public void input(Scanner in) {
        for (int i = 0; i <= n; i++) {
            a[i] = in.nextDouble();
        }
    }

    public void out() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            sb.append(a[i]).append(" * X^").append(i);
            if (i < n) {
                sb.append(" + ");
            }
        }
        System.out.println(sb.toString());
    }

    public DaThuc nhan(DaThuc b) {
        int bacMoi = this.n + b.n;
        double[] heSoMoi = new double[bacMoi + 1];
        for (int i = 0; i <= this.n; i++) {
            for (int j = 0; j <= b.n; j++) {
                heSoMoi[i + j] += this.a[i] * b.a[j];
            }
        }
        return new DaThuc(heSoMoi);
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        DaThuc u = new DaThuc(n);
        u.input(sc);
        u.out();
        int m = sc.nextInt();
        DaThuc v = new DaThuc(m);
        v.input(sc);
        v.out();
        DaThuc t = u.nhan(v);
        t.out();
    }
}

*/

/* 
import java.util.*;

class MyFunction {
    public int f1(String st) {
        if (st == null) return 0;
        int count = 0;
        for (int i = 0; i < st.length(); i++) {
            char c = st.charAt(i);
            if (!Character.isLetterOrDigit(c) && !Character.isWhitespace(c)) {
                count++;
            }
        }
        return count;
    }

    public void f2(String st) {
        if (st == null || st.trim().isEmpty()) {
            return;
        }
        String[] words = st.trim().toLowerCase().split("\\s+");
        Map<String, Integer> map = new LinkedHashMap<>();
        for (String w : words) {
            map.put(w, map.getOrDefault(w, 0) + 1);
        }

        List<Map.Entry<String, Integer>> list = new ArrayList<>(map.entrySet());
        list.sort((e1, e2) -> e2.getValue().compareTo(e1.getValue()));

        for (Map.Entry<String, Integer> entry : list) {
            System.out.println(entry.getKey() + ":" + entry.getValue());
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s1 = sc.nextLine();
        String s2 = sc.nextLine();
        MyFunction mf = new MyFunction();
        System.out.println(mf.f1(s1));
        mf.f2(s2);
    }
}


*/

/* 
import java.util.Scanner;

class NguoiCong {
    private String ma;
    private String hoVaTen;
    private int namSinh;
    private double hsl;
    private String dienThoai;
    private static int sma = 1;

    public NguoiCong() {
        this.ma = String.format("E%03d", sma++);
    }

    public void input(Scanner in) {
        this.hoVaTen = in.nextLine();
        this.namSinh = Integer.parseInt(in.nextLine().trim());
        this.hsl = Double.parseDouble(in.nextLine().trim());
        this.dienThoai = in.nextLine().trim();
    }

    public String getMa() {
        return ma;
    }

    public int getTuoi() {
        return 2026 - namSinh;
    }

    @Override
    public String toString() {
        return ma + " " + hoVaTen + " " + getTuoi() + " " + dienThoai + " " + (hsl * 10000);
    }
}

class QLNC {
    private NguoiCong[] a;

    public QLNC(NguoiCong[] a) {
        this.a = a;
    }

    public void out() {
        for (NguoiCong nc : a) {
            System.out.println(nc);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());
        NguoiCong[] ds = new NguoiCong[n];
        for (int i = 0; i < n; i++) {
            ds[i] = new NguoiCong();
            ds[i].input(sc);
        }
        QLNC ql = new QLNC(ds);
        ql.out();
    }
}


*/



/* 
import java.util.Scanner;

class NhanVien {
    private String hoTen;
    private String chucVu;
    private int soNgay;
    private long luongcb;

    public NhanVien() {
    }

    private String chuanHoa(String hoTen) {
        if (hoTen == null || hoTen.trim().isEmpty()) {
            return "";
        }
        String[] words = hoTen.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            String w = words[i].toLowerCase();
            sb.append(Character.toUpperCase(w.charAt(0))).append(w.substring(1));
            if (i < words.length - 1) {
                sb.append(" ");
            }
        }
        return sb.toString();
    }

    public void input(Scanner in) {
        String name = "";
        while (name.isEmpty() && in.hasNextLine()) {
            name = in.nextLine().trim();
        }
        this.hoTen = chuanHoa(name);
        this.luongcb = Long.parseLong(in.nextLine().trim());
        this.soNgay = Integer.parseInt(in.nextLine().trim());
        this.chucVu = in.nextLine().trim();
    }

    public double getPhuCap(String chucVu) {
        if (chucVu == null) return 0.0;
        switch (chucVu.toUpperCase()) {
            case "GD":
                return 250000.0;
            case "PGD":
                return 200000.0;
            case "TP":
                return 180000.0;
            case "NV":
                return 150000.0;
            default:
                return 0.0;
        }
    }

    public double getThuNhap(int soNgay) {
        double luongThang = (double) this.luongcb * soNgay;
        double thuong = 0.0;
        if (soNgay >= 25) {
            thuong = 0.20 * luongThang;
        } else if (soNgay >= 22) {
            thuong = 0.10 * luongThang;
        }
        return luongThang + getPhuCap(this.chucVu) + thuong;
    }

    @Override
    public String toString() {
        double luongThang = (double) this.luongcb * this.soNgay;
        double phuCap = getPhuCap(this.chucVu);
        double thuNhap = getThuNhap(this.soNgay);
        return hoTen + " " + luongThang + " " + phuCap + " " + thuNhap;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        NhanVien nv = new NhanVien();
        nv.input(in);
        System.out.println(nv);
    }
}
*/

/*
JKT014 - Đầu tư chứng khoán

Nhiệm vụ hằng ngày của bạn -> tính nhịp tăng giảm của phiên chứng khoán trong N ngày để có thể
bắt kịp thị trường.
    -> Nhịp chứng khoán của ngày thứ i được định nghĩa là: số ngày liên tiếp từ ngày thứ i trở
    về mà giá chứng khoán <= giá chứng khoán ngày thứ i

    input:
        + Dòng 1: Số lượng test T (1 ≤ T ≤ 10) -> số bộ dữ liệu
        + Dòng 2: Số nguyên dương N (1 ≤ N ≤ 10^6) -> số ngày giao dịch
        + Dòng 3: N số nguyên dương a[i] (1 ≤ a[i] ≤ 10^9) -> giá chứng khoán của ngày thứ i

    output:
        In ra N số B1, B2, …, BN trong đó Bi là nhịp chứng khoán của ngày thứ i.



    vd:
        input:
            1
            7
            100 80 60 70 60 75 85
        output:
            1 1 1 2 1 4 6   



import java.util.Scanner;
import java.util.Stack;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            int n = sc.nextInt();

            // we use n + 1 becuz we use 1-based indexing for easier understanding
            int[] a = new int[n + 1];

            // Sentinel: A fake day 0 with an infinite price
            a[0] = 1000000000;

            // Read stock prices starting from index 1
            for (int i = 1; i <= n; ++i) {
                a[i] = sc.nextInt();    
            }

            // Stack to store INDICES of the days
            Stack<Integer> st = new Stack<>();
            st.push(0);     // push the sentinel index

            for (int i = 1; i <= n; ++i) {
                // While the current price is >= the price at the top of the stack...
                while (!st.isEmpty() && a[i] >= a[st.peek()]) {
                    st.pop();  // ... if curr price > a[st.peek()] -> FALSE -> pop that day
                }
                // The span is the distance to the nearest greater day
                System.out.print(i - st.peek() + " ");

                // push the current day's index onto the stack
                st.push(i);
            }
            System.out.println();  // move to the next line for the next test case
        }
        sc.close();
    }
}
*/












































J08010 - tìm từ thuận nghịch dài nhất


Cho dữ liệu vào dạng văn bản.
    -> Hãy tìm ra từ thỏa mãn tính chất thuận nghịch có độ dài lớn nhất trong file đó và cho biết từ đó xuất hiện bao nhiêu lần. Nếu có nhiều từ cùng có độ dài lớn nhất thì in ra tất cả các từ đó theo thứ tự xuất hiện trong file ban đầu.
    
    input:
        AAA BAABA HDHDH ACBSD SRGTDH DDDDS
        DUAHD AAA AD DA HDHDH AAA AAA AAA AAA
        DDDAS HDHDH HDH AAA AAA AAA AAA AAA
        AAA AAA AAA
        DHKFKH DHDHDD HDHDHD DDDHHH HHHDDD
        TDTD
    output:
        HDHDH 3


Explained:
    + Palindrone: A word that reads the same forwards and backwards (eg: "AAA", "HDHDH")

    + Tie-breaker: If there are multiple words with the same maximum length (e.g., "AAA" and "BBB"), we must print them in the order they first appeared in the text.

    + Count: We also need to print how many times each longest palindrome appeared.

-> 2. The OOP Approach
    -> Why did we create a (static class word) instead of just using a (String) array?
        Because a word in this context -> has 3 pieces of information attached to it:
            1. (w): The actual string.
            2. (cnt): how many times it appears.
            3. (stt): Its first appearance index (to handle the tie-breaker).

        -> By creating a class, we bundle this data together.
            -> When we sort, we sort the entire package, keeping the word, its count, and its original position together.

-> 3. Line-by-line Walkthrough
    Step 1: The Custom Class
        static class word {
            String w;
            int cnt, stt;
            
            public word(String w, int i) {
                this.w = w;
                this.cnt = 1;   // Initially appears 1 time
                this.stt = 1;   // Store its original position
            }

            @Override
            public String toString() {
                return w + " " + cnt;
            }
        }

            -> toString() : this is magic. When we later call System.out.println(e) -> java will automatically call this method to format the output as Word Count.

    Step 2: The Palindrone Checker
        static boolean tn(String s) {
            for (int i = 0; i < s.length() / 2; ++i) {
                if (s.charAt(i) != s.charAt(s.length() - 1 - i)) {
                    return false;
                }
            }
            return true;
        }

            + This is the Two-Pointer technique. It compares the first character with the last, the second with the second-to-last, etc. If any pair doesn't match, it's not a palindrome.

            + s.length() / 2 ensures we only loop up to the middle, preventing double-checking.

    Step 3: Reading Input & Filtering
        Scanner sc = new Scanner(System.in);
        ArrayList<word> a = new ArrayList<>();
        int index = 0;
        while (sc.hasNext()) {
            String s = sc.next();
            if (!tn(s)) continue;
            // ... check if word exists...
        }

            + while (sc.hasNext()): the input spans multiple lines and we don't know exactly how many words there are. hasNext() -> keeps reading until the end of the file (EOF).
            + sc.next(): Reads 1 word at a time (ignores spaces and newlines)
            + if (!tn(s)) continue : if it's not palindrone -> skip it.

    Step 4: Counting Frequencies -> The O(N^2) Part
        boolean oke = true;
        for (int i = 0; i < a.size(); ++i) {
            if (a.get(i).w.compareTo(s) == 0) {
                oke = false;
                a.get(i).cnt += 1;      // increase its count   
                break;
            }
        }
        if (oke) {
            a.add(new word(s, index));
            index++;
        }

            -> This is seach and count pattern. -> Imagine you're keeping a guess list for a party.
                + ArrayList<word> a -> is your notebook.
                + String s -> is the new person arriving at the door.
                + Your job: Check the notebook. If the person is already inside -> add a tally mark next to their name. if they are not -> write their name in the notebook.

        Breakdown:
            1. boolean oke = true;
                -> we assume a "default state". -> we start by assuming this is a brand new word we have never seen before.
            2. for (int i = 0; i < a.size(); ++i)
                -> this is our search loop. we go through our notebook (ArrayList a) from the very first page (i = 0) to the very last page (i < a.size())
            3. if (a.get(i).w.compareTo(s) == 0)
                -> This is the comparison
                    + a.get(i) -> gets the (word) object at position i
                    + .w -> access the actual string
                    + .compareTo(s) -> compare that stored string with the current string s we just read from the keyboard.
                    + ==0 -> in Java? -> compareTo -> returns 0 -> if 2 strings are identical.
                        (or .equals(s) -> but compareTo works fine).

            4. oke = false -> we fount it
            5. a.get(i).cnt += 1
                -> we update the counter

            if (oke) {
                a.add(new word(s, index));
            }
                -> What it does: we create a brand new (word) object (with count initialized to 1) -> and add it to our notebook (.add())

            index++;
                -> What it does: We increment our global tracker. The first new word we ever find gets stt = 0, the second gets stt = 1, etc. This is crucial for the tie-breaker sorting later!

        
    Step 5: Sorting (The Brain of the Code)
        a.sort((word x, word y)) -> {
            if (x.w.length() == y.w.length()) {
                return x.stt - y.stt;   //tie-breaker: smaller index (appeared first) goes first
            }
            return y.w.length() - x.w.length();     // descending order of length
        };

            -> Sort logic:
                1. if lengths are equal, sort by (stt) ascending (x.stt - y.stt)
                2. if lengths differ -> sort by (length) descending -> y.w.length() - x.w.length()
                    (notice y - x? -> that puts the longest word at the very top (index 0))

    Step 6: Printing the result:
        a.forEach(e -> {
            if (e.w.length() == a.get(0).w.length()) System.out.println(e);
        });

            + because we sort the list -> a.get(0) -> longest palindrone
            + we loop the list. if a word has the same length as a.get(0) -> we print it.
                -> as soon as the lengths drop (because it's sorted) -> the (forEach) still loops but the if condition fails -> nothing else is printed.




    

import java.util.*;

public class Main {
    static class word {
        String w;
        int cnt, stt;

        public word(String w, int i) {
            this.w = w;
            this.cnt = 1;
            this.stt = i;
        }

        @Override
        public String toString() {
            return w + " " + cnt;
        }
    }
    
    static boolean tn(String s) {
        for (int i = 0; i < s.length() / 2; ++i) {
            if (s.charAt(i) != s.charAt(s.length() - 1 - i)) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<word> a = new ArrayList<>();
        int index = 0;
        while (sc.hasNext()) {
            String s = sc.next();
            if (!tn(s)) continue;

            boolean oke = true;
            for (int i = 0; i < a.size(); ++i) {
                if (a.get(i).w.compareTo(s) == 0) {
                    a.get(i).cnt += 1;
                    oke = false;
                    break;
                }
            }
            if (oke) {
                a.add(new word(s, index));
                index++;
            }
        }
        a.sort((word x, word y) -> {
            if (x.w.length() == y.w.length()) {
                return x.stt - y.stt;
            }
            return y.w.length() - x.w.length();
        });

        a.forEach(e -> {
            if (e.w.length() == a.get(0).w.length()) {
                System.out.println(e);
            }
        });

    }
    
}

    
    


        