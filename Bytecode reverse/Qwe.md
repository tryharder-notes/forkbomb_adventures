**Qwe Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE9_qwe

Description: "Disassembly is ready, mylord!"

The task gives you JVM bytecode that needs to be parsed. The easiest way to do this is to convert it to decompiled Java code, but for this, the JVM bytecode needs to be compiled.

To do this, I used the ```jasmin``` utility, but the utility alone is not enough, because the assembler code itself needs to be edited. The thing is, ```jasmin``` complains about the syntax, so I started to understand these errors and bring the code to the desired form.

<img width="825" height="115" alt="изображение" src="https://github.com/user-attachments/assets/627f377d-6571-44a4-9e91-f9c0eb6407cd" />

The following code was given:

```Compiled from "Qwe.java"
public class spbctf.re.Qwe {
  public spbctf.re.Qwe();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: new           #2                  // class java/math/BigInteger
       3: dup
       4: aload_0
       5: iconst_0
       6: aaload
       7: invokespecial #3                  // Method java/math/BigInteger."<init>":(Ljava/lang/String;)V
      10: astore_1
      11: new           #2                  // class java/math/BigInteger
      14: dup
      15: aload_0
      16: iconst_1
      17: aaload
      18: invokespecial #3                  // Method java/math/BigInteger."<init>":(Ljava/lang/String;)V
      21: astore_2
      22: new           #2                  // class java/math/BigInteger
      25: dup
      26: aload_0
      27: iconst_2
      28: aaload
      29: invokespecial #3                  // Method java/math/BigInteger."<init>":(Ljava/lang/String;)V
      32: astore_3
      33: getstatic     #4                  // Field java/math/BigInteger.ZERO:Ljava/math/BigInteger;
      36: astore        4
      38: aload         4
      40: aload_1
      41: invokevirtual #5                  // Method java/math/BigInteger.compareTo:(Ljava/math/BigInteger;)I
      44: ifge          60
      47: aload         4
      49: getstatic     #6                  // Field java/math/BigInteger.ONE:Ljava/math/BigInteger;
      52: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
      55: astore        4
      57: goto          38
      60: aload_2
      61: invokevirtual #8                  // Method java/math/BigInteger.longValue:()J
      64: l2i
      65: istore        5
      67: aload_2
      68: invokevirtual #8                  // Method java/math/BigInteger.longValue:()J
      71: lstore        6
      73: iconst_0
      74: istore        8
      76: iload         8
      78: iload         5
      80: if_icmpge     96
      83: lload         6
      85: lload         6
      87: lmul
      88: lstore        6
      90: iinc          8, 1
      93: goto          76
      96: aload         4
      98: ldc2_w        #9                  // long 5l
     101: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     104: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     107: astore        8
     109: aload_2
     110: ldc2_w        #13                 // long 4l
     113: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     116: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     119: astore        9
     121: aload_3
     122: ldc2_w        #13                 // long 4l
     125: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     128: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     131: astore        10
     133: aload         8
     135: aload         9
     137: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     140: aload         10
     142: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     145: ldc2_w        #15                 // long 11l
     148: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     151: invokevirtual #17                 // Method java/math/BigInteger.equals:(Ljava/lang/Object;)Z
     154: ifne          166
     157: getstatic     #18                 // Field java/lang/System.out:Ljava/io/PrintStream;
     160: ldc           #19                 // String nope
     162: invokevirtual #20                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
     165: return
     166: aload         4
     168: ldc2_w        #13                 // long 4l
     171: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     174: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     177: astore        8
     179: aload_2
     180: ldc2_w        #9                  // long 5l
     183: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     186: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     189: astore        9
     191: aload_3
     192: ldc2_w        #13                 // long 4l
     195: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     198: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     201: astore        10
     203: aload         8
     205: aload         9
     207: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     210: aload         10
     212: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     215: ldc2_w        #21                 // long 8l
     218: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     221: invokevirtual #17                 // Method java/math/BigInteger.equals:(Ljava/lang/Object;)Z
     224: ifne          236
     227: getstatic     #18                 // Field java/lang/System.out:Ljava/io/PrintStream;
     230: ldc           #19                 // String nope
     232: invokevirtual #20                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
     235: return
     236: aload         4
     238: ldc2_w        #13                 // long 4l
     241: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     244: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     247: astore        8
     249: aload_2
     250: ldc2_w        #13                 // long 4l
     253: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     256: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     259: astore        9
     261: aload_3
     262: ldc2_w        #9                  // long 5l
     265: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     268: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     271: astore        10
     273: aload         8
     275: aload         9
     277: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     280: aload         10
     282: invokevirtual #7                  // Method java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     285: ldc2_w        #23                 // long 7l
     288: invokestatic  #11                 // Method java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
     291: invokevirtual #17                 // Method java/math/BigInteger.equals:(Ljava/lang/Object;)Z
     294: ifne          306
     297: getstatic     #18                 // Field java/lang/System.out:Ljava/io/PrintStream;
     300: ldc           #19                 // String nope
     302: invokevirtual #20                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
     305: return
     306: aload_2
     307: getstatic     #6                  // Field java/math/BigInteger.ONE:Ljava/math/BigInteger;
     310: invokevirtual #25                 // Method java/math/BigInteger.subtract:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     313: astore        11
     315: new           #2                  // class java/math/BigInteger
     318: dup
     319: ldc           #26                 // String cafebabedeadbeef
     321: bipush        16
     323: invokespecial #27                 // Method java/math/BigInteger."<init>":(Ljava/lang/String;I)V
     326: aload         11
     328: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     331: aload         4
     333: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     336: aload_3
     337: invokevirtual #12                 // Method java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
     340: astore        12
     342: getstatic     #18                 // Field java/lang/System.out:Ljava/io/PrintStream;
     345: ldc           #28                 // String bingo spbctf{%s}\n
     347: iconst_1
     348: anewarray     #29                 // class java/lang/Object
     351: dup
     352: iconst_0
     353: aload         12
     355: aastore
     356: invokevirtual #30                 // Method java/io/PrintStream.printf:(Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
     359: pop
     360: return
}
```

In the end it became like this:

```
;Compiled from "Qwe.java"
;public class spbctf.re.Qwe {
;public spbctf.re.Qwe();
.method public <init>()V
    aload_0
	
    invokespecial java/lang/Object/<init>:()V
    return   
.end method

  public static void main(java.lang.String[]);
    Code:
       new java/math/BigInteger
       dup
       aload_0
       iconst_0
       aaload
       invokespecial java/math/BigInteger."<init>":(Ljava/lang/String;)V
       astore_1
       new java/math/BigInteger
       dup
       aload_0
       iconst_1
       aaload
       invokespecial java/math/BigInteger."<init>":(Ljava/lang/String;)V
       astore_2
       new java/math/BigInteger
       dup
       aload_0
       iconst_2
       aaload
       invokespecial java/math/BigInteger."<init>":(Ljava/lang/String;)V
       astore_3
       getstatic java/math/BigInteger.ZERO:Ljava/math/BigInteger;
       astore        4
       aload         4
       aload_1
       invokevirtual java/math/BigInteger.compareTo:(Ljava/math/BigInteger;)I
       ifge          60
       aload         4
       getstatic java/math/BigInteger.ONE:Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        4
       goto          38
       aload_2
       invokevirtual java/math/BigInteger.longValue:()J
       l2i
       istore        5
       aload_2
       invokevirtual java/math/BigInteger.longValue:()J
       lstore        6
       iconst_0
       istore        8
       iload         8
       iload         5
       if_icmpge     96
       lload         6
       lload         6
       lmul
	   
       lstore        6
       iinc          8, 1
       goto          76
	   
       aload         4
       ldc2_w long 5l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        8
       aload_2
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        9
       aload_3
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        10
       aload         8
       aload         9
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       aload         10
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       ldc2_w long 11l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.equals:(Ljava/lang/Object;)Z
       ifne          166
       getstatic java/lang/System.out:Ljava/io/PrintStream;
       ldc nope
       invokevirtual java/io/PrintStream.println:(Ljava/lang/String;)V
       return
       aload         4
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        8
       aload_2
       ldc2_w long 5l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        9
       aload_3
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        10
       aload         8
       aload         9
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       aload         10
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       ldc2_w long 8l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.equals:(Ljava/lang/Object;)Z
       ifne          236
       getstatic java/lang/System.out:Ljava/io/PrintStream;
       ldc nope
       invokevirtual java/io/PrintStream.println:(Ljava/lang/String;)V
       return
       aload         4
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        8
       aload_2
       ldc2_w long 4l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        9
       aload_3
       ldc2_w long 5l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        10
       aload         8
       aload         9
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       aload         10
       invokevirtual java/math/BigInteger.add:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       ldc2_w long 7l
       invokestatic java/math/BigInteger.valueOf:(J)Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.equals:(Ljava/lang/Object;)Z
       ifne          306
       getstatic java/lang/System.out:Ljava/io/PrintStream;
       ldc nope
       invokevirtual java/io/PrintStream.println:(Ljava/lang/String;)V
       return
       aload_2
       getstatic java/math/BigInteger.ONE:Ljava/math/BigInteger;
       invokevirtual java/math/BigInteger.subtract:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        11
       new java/math/BigInteger
       dup
       ldc cafebabedeadbeef
       bipush        16
       invokespecial java/math/BigInteger."<init>":(Ljava/lang/String;I)V
       aload         11
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       aload         4
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       aload_3
       invokevirtual java/math/BigInteger.multiply:(Ljava/math/BigInteger;)Ljava/math/BigInteger;
       astore        12
       getstatic java/lang/System.out:Ljava/io/PrintStream;
       ldc bingo spbctf{%s}\n
       iconst_1
       anewarray java/lang/Object
       dup
       iconst_0
       aload         12
       aastore
       invokevirtual java/io/PrintStream.printf:(Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
       pop
       return
}
```

On top of that I changed the file extension to ```.j``` - this is required by ```jasmin```.

After which you can start compiling. This is done like this:

```java -jar jasmin.jar %path_to_file%```

As a result, ```%filename%.class``` appears in the directory where ```jasmin.jar``` is located.

Using Java Decompiler I opened what jasmin gave me:

<img width="1229" height="742" alt="изображение" src="https://github.com/user-attachments/assets/486f04f8-d192-42cd-85c7-98ccf826a25c" />

Basically, it's just a system of equations. I wrote the solution in Python using z3:

```
from z3 import *

def main():
    
    solver = Solver()
    
    x = Int('x')
    y = Int('y')
    z = Int('z')
    
    solver.add((5 * x) + (4 * y) + (4 * z) == 11)
    solver.add((4 * x) + (4 * y) + (5 * z) == 7)
    solver.add((4 * x) + (5 * y) + (4 * z) == 8)
    
    if solver.check() == sat:
        
        model = solver.model()
        
        print(model)
    
if __name__ == '__main__':
    main()
```

Launched and received a solution:

<img width="490" height="69" alt="изображение" src="https://github.com/user-attachments/assets/cc3c310d-6402-4fb8-9dfc-5e6933feae11" />

Then I ran ```.class```, passed the resulting numbers as input, and got a flag:

<img width="442" height="30" alt="изображение" src="https://github.com/user-attachments/assets/47c54046-7c1b-4e32-926b-8bb8c232627c" />
