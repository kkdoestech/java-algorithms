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