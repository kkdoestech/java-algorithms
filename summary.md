<a id="top"></a>

# ☕ Java Algorithms — Study Notes

Personal notes and solutions for Java OOP and algorithm exercises, one chunk per problem: idea → walkthrough → full solution.

## 📚 Table of Contents

| # | Problem | Topic | Key technique |
|---|---|---|---|
| 1 | [J04006 — Khai báo lớp sinh viên](#j04006) | OOP · Encapsulation | Constructor chaining, `SimpleDateFormat`, `toString()` |
| 2 | [J04007 — Khai báo lớp nhân viên](#j04007) | OOP · I/O | Constructor delegation, `nextLine()` vs `next()` |
| 3 | [J04012 — Tính công](#j04012) | OOP | Bonus rules, `switch` allowance |
| 4 | [Sản phẩm (SanPham)](#sanpham) | OOP · static counter | Auto-increment code `NSX-001`, discount |
| 5 | [Đa thức (DaThuc)](#dathuc) | Arrays · Math | Polynomial multiplication |
| 6 | [MyFunction](#myfunction) | String · HashMap | `Character` checks, `LinkedHashMap` + sort |
| 7 | [Người công (NguoiCong / QLNC)](#nguoicong) | OOP · static counter | Auto code `E001`, object array |
| 8 | [Nhân viên (NhanVien)](#nhanvien) | OOP · String | Name normalization, `switch` allowance |
| 9 | [JKT014 — Đầu tư chứng khoán](#jkt014) | Stack | Monotonic stack + sentinel |
| 10 | [J08010 — Tìm từ thuận nghịch dài nhất](#j08010) | String · Sorting | Two pointers, custom comparator |
| 11 | [J08011 — Liệt kê và đếm](#j08011) | HashMap · Sorting | Frequency count + tie-breaker |
| 12 | [Đếm cặp có tổng bằng k](#pair-sum-k) | Binary search | Sort + lower / upper bound |
| 13 | [Kiểm tra dãy ngoặc hợp lệ](#valid-brackets) | Stack | Push open, match close |
| 14 | [AtCoder ABC118 C — Monsters Battle Royale](#atcoder-monsters) | Math · GCD | Euclidean algorithm |

---

<a id="j04006"></a>

## 🧩 J04006 — Khai báo lớp sinh viên

> 💡 **Key idea:** `private` fields + constructor chaining + a `formatDob()` helper + an overridden `toString()`.

### 🧠 Core OOP design principles

#### 1. Class design & encapsulation (`private` fields)

In OOP, **encapsulation** is the principle of hiding internal data (state) and only allowing access through controlled methods.

- By setting `name`, `lop`, `dob` and `gpa` to `private`, we prevent external code (like the `main` method) from writing invalid data directly.
  - For example: no one can accidentally do `stu.gpa = -5.0` or `stu.name = null` from outside the class.
- The field `msv` (Mã số sinh viên — Student ID) is pre-initialized to `"B20DCCN001"`, because this specific problem (J04006) requires a fixed, hardcoded student code for every student created.
  - The problem statement asks for exactly this format.

#### 2. Constructor chaining (`this("", "", "", 0f);`)

Look at the default constructor:

```java
public Student() {
    this("", "", "", 0f);
}
```

- This is called **constructor chaining**. Instead of manually writing `this.name = ""; this.lop = "";...`, we use `this(...)` to call the parameterized constructor right below it.

### 🪜 Step-by-step build

#### Step 1 — Build the class & encapsulation

**Your task:** Create a `class Student`. Inside, declare exactly 5 `private` attributes: `msv` (String), `name` (String), `lop` (String), `dob` (String) and `gpa` (float).

> [!TIP]
> **Mentor hints**
> - **The ID:** Initialize `msv` right there in the declaration: `private String msv = "B20DCCN001";`
>   - This is called an *instance variable initializer*.
> - **The constructors:** Write 2 constructors.
>   - **Constructor 1 (default / no-arg):** takes zero parameters. Inside it, put just 1 line: `this("", "", "", 0f);`
>   - **Constructor 2 (parameterized):** takes `(String name, String lop, String dob, float gpa)`. Inside, assign the arguments to your `this` attributes.
> - **Syntax check:** If your parameter name is the same as your attribute (e.g. `name`), you must use `this.name = name;` to tell Java which one is the class field.

#### Step 2 — The date standardization method

**Your task:** Write a `public` method named `formatDob()` that returns a `String`.
- It should take the messy `dob` string (e.g. `2/2/2002`) and turn it into a clean `"02/02/2002"`.

> [!TIP]
> **Mentor hints**
> - **The tool:** You need `SimpleDateFormat`. Create it like this: `SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy")`
> - **The flow (crucial):** You must **parse** the messy string into a `Date` object, then **format** that `Date` object back into a fresh string.
>   1. `Date date = formatter.parse(dob);`
>   2. `return formatter.format(date)`.
> - **The try-catch trap:** The `.parse()` method is dangerous — if the user types `"02-02-2002"` (with dashes), it crashes.
>   - Java forces you to predict this.
>   - Wrap `formatter.parse(dob)` inside a `try {...}` block and `catch ParseException e`.
>   - In the `catch`, just print the error and `return "";` as a fallback.

#### Step 3 — Overriding `toString()` for perfect output

**Your task:** Override the `toString()` method.
- It must return 1 single String combining the ID, name, class, standardized DOB, and formatted GPA, all separated by spaces.

> [!TIP]
> **Mentor hints**
> - **The annotation:** Write `@Override` right above your method. This tells the compiler *"I know I'm replacing the parent method"*.
> - **The GPA format:** Don't just add `gpa`. Use `String.format("%.2f", gpa)` to force exactly 2 decimal places (e.g. `2` becomes `2.00`).
> - **The return:** Combine everything with the `+` operator.

> [!IMPORTANT]
> **Crucial rule:** You must call `formatDob()` inside this return statement to get the cleaned-up date, not the raw `dob`.

#### Step 4 — Write the `main()` driver

**Your task:** Write the `public static void main` inside a separate public class named ... and read the inputs.

> [!TIP]
> **Mentor hints**
> - **Input order:** Name (`nextLine`) → Class (`nextLine`) → DOB (`nextLine`) → GPA (`nextFloat`)
> - **Creating the object:** After reading all 4 variables, create your student: `Student stu = new Student(name, lop, dob, gpa);`
> - **The magic print:** Write `System.out.println(stu);`
>   - Remember: because you overrode `toString()`, Java automatically calls your method here.
>   - You don't call it explicitly like `stu.toString()`.

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="j04007"></a>

## 🧩 J04007 — Khai báo lớp nhân viên

> 💡 **Key idea:** This `Staff` class is almost a twin of the `Student` class we just built, but with 7 attributes and **no date formatting**.

### 🧠 1. OOP structures & constructor delegation

#### Encapsulation (`private` attributes)

All 7 fields (`mnv`, `name`, `sex`, `dob`, `address`, `tax`, `date`) are `private` for the same reasons as before:
- **Data protection:** Prevents external classes from directly setting invalid or null values (e.g. someone can't accidentally do `sta.name = null` from `main`).
- **Controlled interface:** If you later need to validate that `'Nam'` is only "Male/Female", you would add a setter method — without breaking the code that calls it.

#### Constructor delegation (`this(...)`)

```java
public Staff() {
    this("00001", "", "", "", "", "", "", "");
}
```

- When someone calls `new Staff()` with no arguments, it immediately jumps to the 7-parameter constructor, passing a hardcoded ID `"00001"` and empty strings for everything else.

**Why is this useful, even though `main()` doesn't use it?**
- Even though `main()` uses the full constructor directly, this default constructor is **defensive programming**.
  - It ensures that if another developer (or future you) tries to create a `Staff` object without providing data (`new Staff()`), the program won't crash with null pointer errors.
- It also centralizes all initialization logic in 1 place (the 7-param constructor).
  - So if you add logging or validation, you only add it once.

#### Hardcoded attribute requirements (`mnv = "00001"`)

The problem specification (J04007) explicitly states the staff ID must be `"00001"`.
- It's not part of the input.
- That's why `main()` passes it directly as a literal instead of reading it with `sc.nextLine()`.
- The default constructor also has it baked in for safety.

### ⌨️ 2. Line-by-line I/O mechanics

#### `sc.nextLine()` vs `sc.next()`

> [!WARNING]
> **Classic pitfall!**
> - `sc.next()` reads only 1 **token** (stops at whitespace).
> - `sc.nextLine()` reads the entire line, including spaces.

Look at the sample input: `Mo Lao-Ha Dong-Ha Noi` has spaces.
- If we used `sc.next()`, it would only store `"Mo"`.
- ⇒ `nextLine()` is mandatory to capture the FULL address as 1 string.

#### String formatting in `toString()`

The code uses simple concatenation: `mnv + " " + name + ...`
- **Why is this enough?** Because every field is already a `String`, and there is no requirement to pad numbers or force decimal places (like GPA).
- It is perfectly sufficient here. `String.format()` is useful when you need specific formatting (`%.2f`) or padding (`%10s`) — but for plain text, `+` is faster.

#### Implicit method calls

When you write `System.out.println(sta)`, the Java compiler sees you're passing an `Object` (a `Staff` instance).
- The `println` method internally calls `sta.toString()` to convert the object into a printable `String`.
- Because you overrode `toString()` with `@Override`, your custom String is used instead of the default garbage (like `Staff@15db9742`).

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="j04012"></a>

## 🧩 J04012 — Tính công

> 💡 **Key idea:** income = base salary (wage × days) + bonus (by days worked) + allowance (by role).

### 🧠 Step 1 — The idea

Imagine you run a small shop. You have 1 employee (for now). Each day they show up, you pay them a daily wage (like 45,000 VND per day).

At the end of the month, you count how many days they worked — say 23 days:
- **Base salary** = daily wage × days worked
- **Bonus** — if they worked more than 25 days, they get a 20% bonus on base salary; if they worked a decent amount (22–24), 10% bonus; otherwise no bonus.
- **Allowance** — if they are a manager (`GD`), senior manager (`PGD`), team leader (`TP`), or regular staff (`NV`), you give them a fixed monthly addition.

You also need to give them an official employee ID — starting at `NV01` (since this is the first employee).

> [!NOTE]
> **The goal:** Input the person's details, compute all 3 parts (salary, bonus, allowance), sum them up, and print everything nicely in 1 line.

### 🔍 Step 2 — Creating the `Officer` object

We call the constructor `new Officer(name, wage, workingDays, role)`. Inside that constructor:
- `this.id = "NV01";` — fixed because we only have 1 employee for now.
- `this.name = name;` — store the name.
- `this.salary = wage * workingDays;` — 45,000 × 23 = 1,035,000
- Now determine `bonus`:
  - `workingDays > 25`? No (23 < 25)
  - `workingDays >= 22`? Yes (23 >= 22) → 10% bonus = 103,500
  - `(int)(salary * 0.1f)` → `(int)(1,035,000 * 0.1)` = 103,500
- Determine `allowance` using a `switch` on `role`:
  - `role` is `"PGD"` → so `case "PGD"` → allowance = 200,000

At the end of the constructor we have:

| Field | Value |
|---|---|
| `id` | `"NV01"` |
| `name` | `"Nguyen Van A"` |
| `salary` | 1,035,000 |
| `bonus` | 103,500 |
| `allowance` | 200,000 |

### 🖨️ Step 3 — Computing income & printing

The `toString()` method is called automatically when we do `System.out.println(officer)`. It concatenates:

```java
id + " " + name + " " + salary + " " + bonus + " " + allowance + " " + getIncome()
```

- `getIncome()` returns `salary + bonus + allowance` = 1,338,500

So the printed line becomes:

```text
NV01 Nguyen Van A 1035000 103500 200000 1338500
```

### 💻 Code breakdown — the `Officer` class (fields + constructor)

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="sanpham"></a>

## 🧩 Sản phẩm (SanPham) — mã tự tăng & thành tiền

> 💡 **Key idea:** A `static` counter (`dem`) builds the product code `NSX-001`, `NSX-002`, …; quantity ≥ 20 gets a 10% discount (× 0.9).

### ✅ Full solution

```java
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
                            Double.parseDouble(sc.nextLine()));
            System.out.print(s.toString());
        }
    }
}
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="dathuc"></a>

## 🧩 Đa thức (DaThuc) — nhân hai đa thức

> 💡 **Key idea:** Store the coefficients in `a[0..n]`. Multiplying gives a polynomial of degree `n + m`, where `heSoMoi[i + j] += a[i] * b[j]`.

### ✅ Full solution

```java
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
```

### 🔁 Variant — the same class with comments (class only)

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="myfunction"></a>

## 🧩 MyFunction — đếm ký tự đặc biệt & tần suất từ

> 💡 **Key idea:** `f1` counts characters that are neither a letter/digit nor whitespace. `f2` counts each lowercase word with a `LinkedHashMap` (keeps first-appearance order), then sorts by count, highest first.

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="nguoicong"></a>

## 🧩 Người công (NguoiCong / QLNC) — mã tự tăng E001

> 💡 **Key idea:** A `static` counter `sma` gives each new object the code `E001`, `E002`, …; age = 2026 − birth year; `QLNC` holds the array and prints every person.

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="nhanvien"></a>

## 🧩 Nhân viên (NhanVien) — chuẩn hóa tên & thu nhập

> 💡 **Key idea:** `chuanHoa()` capitalizes the first letter of each word in the name. Income = base × days + allowance (by `chucVu`) + bonus (20% if ≥ 25 days, 10% if ≥ 22 days).

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="jkt014"></a>

## 🧩 JKT014 — Đầu tư chứng khoán (Stock Span)

> 💡 **Key idea:** Keep a stack of day **indices** with a sentinel day 0 (huge price). Pop every day whose price is ≤ today's; the span is `i - st.peek()`.

### 📝 Problem

Nhiệm vụ hằng ngày của bạn: tính nhịp tăng giảm của phiên chứng khoán trong N ngày để có thể bắt kịp thị trường.

> **Nhịp chứng khoán** của ngày thứ i được định nghĩa là: số ngày liên tiếp từ ngày thứ i trở về mà giá chứng khoán ≤ giá chứng khoán ngày thứ i.

**Input**
- Dòng 1: Số lượng test T ($1 \le T \le 10$) — số bộ dữ liệu
- Dòng 2: Số nguyên dương N ($1 \le N \le 10^6$) — số ngày giao dịch
- Dòng 3: N số nguyên dương a[i] ($1 \le a_i \le 10^9$) — giá chứng khoán của ngày thứ i

**Output**
- In ra N số B1, B2, …, BN trong đó Bi là nhịp chứng khoán của ngày thứ i.

### 📥 Input / 📤 Output

```text
Input:
1
7
100 80 60 70 60 75 85

Output:
1 1 1 2 1 4 6
```

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="j08010"></a>

## 🧩 J08010 — Tìm từ thuận nghịch dài nhất

> 💡 **Key idea:** Keep only palindromes, count them in a list of `word` objects (string + count + first index), then sort by length (longest first) and first appearance.

### 📝 Problem

Cho dữ liệu vào dạng văn bản. Hãy tìm ra từ thỏa mãn tính chất thuận nghịch có độ dài lớn nhất trong file đó và cho biết từ đó xuất hiện bao nhiêu lần. Nếu có nhiều từ cùng có độ dài lớn nhất thì in ra tất cả các từ đó theo thứ tự xuất hiện trong file ban đầu.

### 📥 Input / 📤 Output

```text
Input:
AAA BAABA HDHDH ACBSD SRGTDH DDDDS
DUAHD AAA AD DA HDHDH AAA AAA AAA AAA
DDDAS HDHDH HDH AAA AAA AAA AAA AAA
AAA AAA AAA
DHKFKH DHDHDD HDHDHD DDDHHH HHHDDD
TDTD

Output:
HDHDH 3
```

### 🧠 1. Explained

- **Palindrome:** A word that reads the same forwards and backwards (e.g. `"AAA"`, `"HDHDH"`).
- **Tie-breaker:** If there are multiple words with the same maximum length (e.g. `"AAA"` and `"BBB"`), we must print them in the order they first appeared in the text.
- **Count:** We also need to print how many times each longest palindrome appeared.

### 🧱 2. The OOP approach

Why did we create a `static class word` instead of just using a `String` array? Because a word in this context has 3 pieces of information attached to it:

1. `w`: the actual string.
2. `cnt`: how many times it appears.
3. `stt`: its first appearance index (to handle the tie-breaker).

By creating a class, we bundle this data together.
- When we sort, we sort the entire package, keeping the word, its count, and its original position together.

### 🔍 3. Line-by-line walkthrough

#### Step 1 — The custom class

```java
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
```

- `toString()`: this is magic. When we later call `System.out.println(e)`, Java will automatically call this method to format the output as `Word Count`.

#### Step 2 — The palindrome checker

```java
static boolean tn(String s) {
    for (int i = 0; i < s.length() / 2; ++i) {
        if (s.charAt(i) != s.charAt(s.length() - 1 - i)) {
            return false;
        }
    }
    return true;
}
```

- This is the **two-pointer technique**. It compares the first character with the last, the second with the second-to-last, etc. If any pair doesn't match, it's not a palindrome.
- `s.length() / 2` ensures we only loop up to the middle, preventing double-checking.

#### Step 3 — Reading input & filtering

```java
Scanner sc = new Scanner(System.in);
ArrayList<word> a = new ArrayList<>();
int index = 0;
while (sc.hasNext()) {
    String s = sc.next();
    if (!tn(s)) continue;
    // ... check if word exists...
}
```

- `while (sc.hasNext())`: the input spans multiple lines and we don't know exactly how many words there are. `hasNext()` keeps reading until the end of the file (EOF).
- `sc.next()`: reads 1 word at a time (ignores spaces and newlines).
- `if (!tn(s)) continue;`: if it's not a palindrome, skip it.

#### Step 4 — Counting frequencies (the $O(N^2)$ part)

```java
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
```

This is the **search and count** pattern. Imagine you're keeping a guest list for a party:
- `ArrayList<word> a` is your notebook.
- `String s` is the new person arriving at the door.
- Your job: check the notebook. If the person is already inside, add a tally mark next to their name. If they are not, write their name in the notebook.

**Breakdown:**

1. `boolean oke = true;` — we assume a "default state": we start by assuming this is a brand new word we have never seen before.
2. `for (int i = 0; i < a.size(); ++i)` — this is our search loop. We go through our notebook (`ArrayList a`) from the very first page (`i = 0`) to the very last page (`i < a.size()`).
3. `if (a.get(i).w.compareTo(s) == 0)` — this is the comparison:
   - `a.get(i)` gets the `word` object at position `i`.
   - `.w` accesses the actual string.
   - `.compareTo(s)` compares that stored string with the current string `s` we just read from the keyboard.
   - `== 0`: in Java, `compareTo` returns 0 if 2 strings are identical (or use `.equals(s)` — but `compareTo` works fine).
4. `oke = false` — we found it.
5. `a.get(i).cnt += 1` — we update the counter.

```java
if (oke) {
    a.add(new word(s, index));
}
```

- **What it does:** we create a brand new `word` object (with count initialized to 1) and add it to our notebook (`.add()`).

```java
index++;
```

- **What it does:** we increment our global tracker. The first new word we ever find gets `stt = 0`, the second gets `stt = 1`, etc. This is crucial for the tie-breaker sorting later!

#### Step 5 — Sorting (the brain of the code)

```java
a.sort((word x, word y)) -> {
    if (x.w.length() == y.w.length()) {
        return x.stt - y.stt;   //tie-breaker: smaller index (appeared first) goes first
    }
    return y.w.length() - x.w.length();     // descending order of length
};
```

**Sort logic:**
1. If lengths are equal, sort by `stt` ascending (`x.stt - y.stt`).
2. If lengths differ, sort by length descending (`y.w.length() - x.w.length()`).
   - Notice `y - x`? That puts the longest word at the very top (index 0).

#### Step 6 — Printing the result

```java
a.forEach(e -> {
    if (e.w.length() == a.get(0).w.length()) System.out.println(e);
});
```

- Because we sorted the list, `a.get(0)` is the longest palindrome.
- We loop over the list. If a word has the same length as `a.get(0)`, we print it.
  - As soon as the lengths drop (because it's sorted), the `forEach` still loops but the `if` condition fails, so nothing else is printed.

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="j08011"></a>

## 🧩 J08011 — Liệt kê và đếm

> 💡 **Key idea:** Filter the non-decreasing numbers, count them with a `HashMap` (instant lookup), then sort by count (descending) and first appearance.

### 📝 Problem

Cho một dãy các số nguyên dương không quá 9 chữ số, mỗi số cách nhau vài khoảng trống, có thể xuống dòng. Hãy tìm các số không giảm (các chữ số theo thứ tự từ trái qua phải tạo thành dãy không giảm) và đếm số lần xuất hiện của các số đó.

- **Input:** Gồm các số nguyên dương không quá 9 chữ số. Không quá 10000 số.
- **Output:** Ghi ra các số không giảm kèm theo số lần xuất hiện. Các số được liệt kê theo thứ tự sắp xếp số lần xuất hiện giảm dần. Các số có số lần xuất hiện bằng nhau thì số nào xuất hiện trước in ra trước.

### 📥 Input / 📤 Output

```text
Input:
123 321 23456 123 123 23456 3523 123 321 4567 8988 78 7654 9899 3456 123 678 999 78 3456 987654321 4546 63543 4656 13432 4563 123471 659837 454945 34355 9087 9977 98534 3456 23134

Output:
123 5
3456 3
23456 2
78 2
4567 1
678 1
999 1
```

### 🧠 1. Problem analysis

- **"Non-decreasing" (Không giảm):** The digits from left to right must be equal or larger. For example: `123` (1 ≤ 2 ≤ 3) is valid. `23456` is valid. `999` is valid. `321` is invalid (3 > 2).
- **Input:** Unknown number of integers, up to 9 digits long. (We read them as `String` because we need to check digits — 9 digits can safely fit in an `int`, but reading as `String` makes digit checking easier.)
- **Output:** Valid numbers and their counts, sorted by frequency (descending), then by first appearance (ascending).

### 📖 2. The "why" and "how" of HashMap

Imagine you have a massive library:
- **ArrayList:** you have to walk shelf by shelf to find a book (slow).
- **HashMap:** you go to the librarian, give them the book title (the **Key**), and they instantly give you the book (the **Value**).

In your code:
- **Key:** the number as a `String` (e.g. `"123"`).
- **Value:** the custom `num` object (which holds the string, count, and index).

### 🔍 3. Line-by-line walkthrough

#### Step 1 — The check function

```java
static boolean check(String a) {
    for (int i = 1; i < a.length(); ++i) {
        if (a.charAt(i) < a.charAt(i - 1)) return false;
    }
    return true;
}
```

- We loop from the second digit (`i = 1`).
- We compare the current digit (`a.charAt(i)`) with the previous digit (`a.charAt(i - 1)`).
- If the current digit is strictly smaller than the previous one, it's not "non-decreasing" → `return false`.
  - If the loop finishes, `return true`.

#### Step 2 — The custom class (`num`)

```java
static class num {
    String num;
    int cnt, stt;

    public num(String num, int cnt, int stt) {
        this.num = num;
        this.cnt = cnt;
        this.stt = stt;
    }

    @Override
    public String toString() {
        return num + " " + cnt;
    }
}
```

- Just like the palindrome problem, we bundle the data: `num` is the string, `cnt` is the frequency, `stt` is the original index (to handle ties).

#### Step 3 — The main logic (reading & counting)

```java
Scanner sc = new Scanner(System.in);
HashMap<String, num> hm = new HashMap<>();
ArrayList<num> a = new ArrayList<>();
int i = 0;

while (sc.hasNext()) {
    String s = sc.next();
    if (!check(s)) continue;  // skip if invalid

    if (hm.get(s) == null) {
        // BRAND NEW NUMBER
        num x = new num(s, 1, i);
        hm.put(s, x);   // add to dictionary
        a.add(x);       // add to list (for sorting later)
        i++;            // increase first-appearance index
    }
    else {
        // NUMBER ALREADY EXISTS
        hm.get(s).cnt += 1;
    }
}
```

- `hm.get(s) == null`: this is the magic of HashMap. It asks the dictionary: *"Do you have the key `s`?"* If the answer is `null`, we haven't seen this number before.
- If it's new, we create it (`cnt = 1`), put it in the HashMap, and add it to the ArrayList. We also assign it an `stt` (index `i`) and increment `i`.
- If it's not `null`, we found a duplicate → we use `hm.get(s)` to instantly grab the object and increase its `cnt` by 1.
  - Notice we don't need a `break` or a loop here. It's instant.

#### Step 4 — Sorting

```java
a.sort((num x, num y) -> {
    if (x.cnt == y.cnt) return x.stt - y.stt;   // tie breaker: smaller index first
    return y.cnt - x.cnt;   // descending order of count
})
```

#### Step 5 — Printing

```java
a.forEach(e -> System.out.println(e));
```

- Loops through the sorted list and prints every object using its `toString()` method.

### ✅ Full solution

```java
import java.util.*;

public class Main {
    static boolean check(String a) {
        for (int i = 1; i < a.length(); ++i) {
            if (a.charAt(i) < a.charAt(i - 1)) return false;
        }
        return true;
    }
    static class num {
        String num;
        int cnt, stt;

        public num(String num, int cnt, int stt) {
            this.num = num;
            this.cnt = cnt;
            this.stt = stt;
        }

        @Override
        public String toString() {
            return num + " " + cnt;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        HashMap<String, num> hm = new HashMap<>();
        ArrayList<num> a = new ArrayList<>();
        int i = 0;
        while (sc.hasNext()) {
            String s = sc.next();
            if (!check(s)) continue;

            if (hm.get(s) == null) {
                num x = new num(s   , 1, i);
                hm.put(s, x);
                a.add(x);
            }
            else hm.get(s).cnt += 1;
        }
        a.sort((num x, num y) -> {
            if (x.cnt == y.cnt) return x.stt - y.stt;
            return y.cnt - x.cnt;
        });
        a.forEach(e -> System.out.println(e));
    }
}
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="pair-sum-k"></a>

## 🧩 Đếm cặp có tổng bằng k (Binary Search)

> 💡 **Key idea:** Sort the array. For each `a[j]`, the partner must be `k - a[j]`; use `lower_bound` / `upper_bound` to count how many times it appears after `j`.

### 📝 Problem

Cho dãy số `a[]` gồm có n phần tử → đếm xem có bao nhiêu cặp (i, j) mà `a[i] + a[j] = k` cho trước.

- **Input:**
  - Dòng 1: `t` (số test)
  - Mỗi test: `n` và `k`
  - Dòng tiếp: `a[i]`...
- **Output:** đáp án

### 📥 Input / 📤 Output

```text
Input:
4
4 6
1 5 7 -1
5 6
1 5 7 -1 5
4 2
1 1 1 1
13 11
10 12 10 15 -1 7 6 5 4 2 1 1 1

Output:
2
3
6
9
```

### 🧠 1. The core idea (the "what")

We need to find pairs `(a[i], a[j])` such that `a[i] + a[j] = k`.
- Imagine you have a sorted array. If you pick 1 number, say `a[j]`, you instantly know what the other number must be: `k - a[j]`.
- Because the array is sorted, all instances of `k - a[j]` will be sitting right next to each other. Your code uses 2 special binary search functions (`lower_bound` and `upper_bound`) to instantly jump to the first and last occurrence of that target number.

### 🔍 2. Step by step

#### Step 1 — Read & sort

```java
Scanner sc = new Scanner(System.in);
int t = sc.nextInt();
while (t-- > 0) {
    int n = sc.nextInt();
    long k = sc.nextLong();     // target sum k
    long[] a = new long[n];
    for (int j = 0; j < n; ++j) {
        a[j] = sc.nextLong();
    }
    Array.sort(a);      // sorting is the key
}
```

- **Why `long`?** The problem states $A[i] \le 10^{18}$ and $K \le 10^9$. An `int` can only hold up to $\approx 2 \times 10^9$. If you use `int`, it will overflow. `long` is mandatory here.
- **Why sort?** Sorting allows us to use binary search later. Once sorted, all duplicate numbers are grouped together.

#### Step 2 — The main loop

```java
long ans = 0;
for (int j = 0; j < n - 1; ++j) {
    long up = upper_bound(a, j + 1, n - 1, k - a[j]);
    long dow = lower_bound(a, j + 1, n - 1, k - a[j]);

    if (dow <= n - 1) {
        ans += up - down + 1;
    }
}
System.out.println(ans);
```

- We loop `j` from `0` to `n - 2` (because the second number must be after the first).
- `k - a[j]` is our **target** → we need to find how many times this target exists in the array from index `j + 1` to the end.
- `lower_bound` finds the **first** index where the target appears.
- `upper_bound` finds the **last** index where the target appears.
- The math `up - down + 1`: if the first occurrence is at index 3 and the last is at index 5, the number of occurrences is `5 - 3 + 1 = 3`.
- `if (dow <= n - 1)`: if the target doesn't exist at all, `lower_bound` returns `r + 1` (which is `n`) → this check prevents adding a garbage number to `ans`.

### 🎯 3. Demystifying the binary search functions

They find the boundaries of where the target exists.

#### `lower_bound` — finds the FIRST occurrence

```java
public static long lower_bound(long[] a, int l, int r, long x) {
    long ans = r + 1;       // default if not found
    while (l <= r){
        int m = (l + r) / 2;
        if (a[m] == x) {
            ans = m;
            r = m - 1;  // keep searching left to find the earliest one
        } else if (a[m] >= x) {
            r = m - 1;
        }
        else l = m + 1;
    }
    return ans;
}
```

#### `upper_bound` — finds the LAST occurrence

```java
public static void upper_bound(long[] a, int l, int r, long x) {
    long ans = r + 1;       // default if not found
    while (l <= r) {
        int m = (l + r) / 2;
        if (a[m] == x) {
             ans = x;
             r = m - 1; // but keep searching the RIGHT to find latest
        }
        else if (a[m] >= x) {
            r = m - 1;
        }
        else l = m + 1;
    }
    return ans;
}
```

### 🧪 Dry run

Let's say `a = [1, 2, 2, 2, 5]` and `K = 4`.

| `j` | `a[j]` | Target | `lower_bound` | `upper_bound` | Result |
|---|---|---|---|---|---|
| 0 | 1 | 3 | 5 (= n, not found) | 5 | `dow <= 4` is **false** → `ans` stays 0 |
| 1 | 2 | 2 | first `2` at index 1 | last `2` at index 3 | `ans += 3 - 1 + 1 = 3` (because there are 3 pairs) |

### ✅ Full solution

```java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        while (t-- > 0) {
             int n = sc.nextInt();
             long k = sc.nextLong();
             long[] a = new long[n];
             for (int j = 0; j < n; ++j) {
                a[j] = sc.nextLong();
             }
             Arrays.sort(a);

             long ans = 0;
             for (int j = 0; j < n - 1; ++j) {
                long up = upper_bound(a, j + 1, n - 1, k - a[j]);
                long dow = lower_boud(a, j + 1, n - 1, k - a[j]);
                if (dow <= n - 1) {
                    ans += up - dow + 1;
                }
             }
             System.out.println(ans);
        }
    }

    public static long lower_boud(long[] a, int l, int r, long x) {
        long ans = r + 1;
        while (l <= r) {
            int m = (l + r) / 2;
            if (a[m] == x) {
                ans = m;
                r = m - 1;
            }
            else if (a[m] >= x) {
                r = m - 1;
            }
            else l = m + 1;
        }
        return ans;
    }

    public static long upper_bound(long[] a, int l, int r, long x) {
        long ans = r + 1;
        while (l <= r) {
            int m = (l + r) / 2;
            if (a[m] == x) {
                ans = m;
                l = m + 1;
            }
            else if (a[m] >= x) {
                r = m - 1;
            }
            else l = m + 1;
        }
        return ans;
    }
}
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="valid-brackets"></a>

## 🧩 Kiểm tra dãy ngoặc hợp lệ (Stack)

> 💡 **Key idea:** Push every opening bracket. On a closing bracket, the top of the stack must be its matching opener — otherwise the string is invalid.

### 📥 Input / 📤 Output

```text
Input:
2
[()]{}{()()}
[(])

Output:
YES
NO
```

### 🧠 1. Why a stack?

Valid parentheses → use a **stack**.
- Imagine you're washing dishes. You stack clean plates on top of each other. When you need a plate, you take the one on the very top.
  - You can't pull one from the bottom without knocking everything over.
  - This is a stack (**LIFO**: last in, first out).
- For brackets to be valid, they must be **properly nested**.
  - This means the most recently opened bracket must be the first one to close.

Example: in `{[()]}`, the `(` opens last, so it must close first with `)`. Then `[` closes, then `{`.

A stack is perfect because we can just push opening brackets on top, and when we see a closing bracket, we just check the top of the pile.

### 🔍 2. The `isValid` function (the brain)

```java
public static boolean isValid(String s) {
    Stack<Character> st = new Stack<>();
}
```

- We initialize an empty `Stack` that will hold `Character` values (letters/symbols).

```java
for (int i = 0; i < s.length(); ++i) {
    char k = s.charAt(i);
}
```

- We loop through the string 1 character at a time. `k` is the current character we are looking at.

#### Handling closing brackets

```java
switch(k) {
    case ')':
        if (st.empty() || st.peek() != '(') return false;
        st.pop();
        break;
}
```

- `st.empty()`: if we see a closing bracket `)` but our stack is completely empty, there's no opening bracket to match it (e.g. the string is `")("` → invalid).
- `st.peek() != '('`: `peek()` looks at the top plate in the pile. If the top plate is `[` but we need to close with `)`, they don't match! Invalid.
- `st.pop()`: if both checks pass, the `(` is matched. We `pop()` (remove) the `(` from the top of the stack and continue.

#### Handling opening brackets

```java
default:
    st.push(k);
    break;
```

- If the character is not a closing bracket, it must be an opening bracket (`(`, `[`, `{`). We `push()` it onto the top of our stack.

#### The final check (the fix)

```java
    }
    return st.empty();
}
```

> [!IMPORTANT]
> **Why is this so important?** Imagine the input is `"((("`.
> - The loop will push all three `(` onto the stack. The loop ends. There were no errors inside the loop.
> - If we just `return true;`, we would say `"((("` is valid, which is wrong!
> - If the stack is empty at the end, every opening bracket was successfully matched and popped. If there are still brackets left, it's invalid. `st.empty()` returns `true` if valid, and `false` if invalid.

### ⌨️ 3. The `main` function (handling input)

```java
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int t = sc.nextInt(); // Read number of test cases
    while (t-- > 0) {
        String s = sc.next(); // Read the string
        if (isValid(s)) {
            System.out.println("YES");
        } else {
            System.out.println("NO");
        }
    }
    sc.close();
}
```

### 🧪 4. Visual dry run

**Valid string:** `{[()]}`

| Read | Action | Stack after |
|---|---|---|
| `{` | Push | `[ { ]` |
| `[` | Push | `[ {, [ ]` |
| `(` | Push | `[ {, [, ( ]` |
| `)` | Top is `(` → match, pop | `[ {, [ ]` |
| `]` | Top is `[` → match, pop | `[ { ]` |
| `}` | Top is `{` → match, pop | `[ ]` (empty) |

Loop ends. `st.empty()` is `true` → **Output: YES**.

**Invalid string:** `([)]`

| Read | Action | Stack after |
|---|---|---|
| `(` | Push | `[ ( ]` |
| `[` | Push | `[ (, [ ]` |
| `)` | Top is `[` → does `[` match `)`? **NO** | — |

Instantly `return false` → **Output: NO**. (Notice how we didn't even finish reading the string — we already knew it was invalid!)

### ✅ Full solution

```java
import java.util.Scanner;
import java.util.Stack;

public class Main {
    public static int Check(String s) {
        Stack<Character> st = new Stack<>();
        for (int i = 0; i < s.length(); ++i) {
            char k = s.charAt(i);
            switch(k) {
                case ')':
                    if (st.empty() || st.peek() != '(') {
                        return 0;
                    }
                    st.pop();
                    break;
                case ']':
                    if (st.empty() || st.peek() != '[') {
                        return 0;
                    }
                    st.pop();
                    break;
                case '}':
                    if (st.empty() || st.peek() != '{'){
                        return 0;
                    }
                    st.pop();
                    break;
                default:
                    st.push(k);
                    break;
            }
        }
        return 1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        while (t-- > 0) {
            String s = sc.next();
            if (Check(s) == 1) {
                System.out.println("YES");
            }
            else {
                System.out.println("NO");
            }
        }
        sc.close();
    }
}
```

<p align="right"><a href="#top">⬆ Back to top</a></p>

---

<a id="atcoder-monsters"></a>

## 🧩 AtCoder ABC118 C — Monsters Battle Royale (GCD)

> 💡 **Key idea:** "attacked health −= attacker's health" is exactly the Euclidean algorithm, so the minimum final health is the GCD of all healths.

🔗 Problem: [atcoder.jp/contests/abc118/tasks/abc118_c](https://atcoder.jp/contests/abc118/tasks/abc118_c)

### 📝 Problem

There are N monsters, numbered 1, 2, ..., N. Initially, the health of Monster i is $A_i$. Below, a monster with at least 1 health is called **alive**.

Until there is only 1 alive monster, the following is repeated:
- A random alive monster attacks another random alive monster.
- As a result, the health of the monster attacked is reduced by the amount equal to the current health of the monster attacking.

Find the **minimum possible final health** of the last monster alive.

**Constraints**
- All values in input are integers.
- $2 \le N \le 10^5$
- $1 \le A_i \le 10^9$

**Input format** (from Standard Input)

```text
N
A1 A2 ... AN
```

**Output:** Print the minimum possible final health of the last monster alive.

### 📥 Input / 📤 Output

**Sample 1**

```text
Input:
4
2 10 8 40

Output:
2
```

When only the first monster keeps on attacking, the final health of the last monster will be 2, which is minimum.

**Sample 2**

```text
Input:
4
5 13 8 1000000000

Output:
1
```

**Sample 3**

```text
Input:
3
1000000000 1000000000 1000000000

Output:
1000000000
```

### 🧠 1. The "Aha!" moment: the Euclidean algorithm

Take Sample 1 (`2 10 8 40` → `2`) and look at what happens when Monster A (health = 10) and Monster B (health = 8) fight:
- If A attacks B, B's health becomes 8 − 10 = −2 → Monster B dies.
- Wait, the problem says "health is reduced by". So if A attacks B, B becomes 8 − 10 = −2 (dead). But what if B attacks A? A becomes 10 − 8 = 2.

Let's trace Monster A (10) and Monster B (8):

| # | Attack | Result |
|---|---|---|
| 1 | B attacks A | A becomes 2 |
| 2 | A (2) attacks B (8) | B becomes 6 |
| 3 | A (2) attacks B (6) | B becomes 4 |
| 4 | A (2) attacks B (4) | B becomes 2 |
| 5 | A (2) attacks B (2) | B becomes 0 (B dies) → A survives with 2 health |

Look at that result: **2**. What is the Greatest Common Divisor (GCD) of 10 and 8? It's **2**!

> [!IMPORTANT]
> Whenever two monsters fight until one dies, the survivor's health will always be the GCD of their initial healths. The attack mechanic (`b = b - a`) is exactly how the Euclidean algorithm works mathematically.

### 🧠 2. Extending to N monsters

If you have many monsters, they can all attack the same monster, or fight each other. But no matter what order they fight in, the final surviving health will always be a multiple of the GCD of the entire array.

To get the minimum possible final health, we want to reduce it as much as possible. By carefully choosing who attacks whom, we can always force the final survivor's health to be exactly:

$$\gcd(A_1, A_2, A_3, \dots, A_N)$$

![GCD check on the samples](image-1.png)

### ✅ Full solution

```java
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
```

<p align="right"><a href="#top">⬆ Back to top</a></p>
