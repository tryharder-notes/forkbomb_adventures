**Cube Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE4_cube

Description: "Binary allocates flag inside some structure. Understand what the structure is and get the flag"


I got another binary compiled for Linux. I went to run the binary, and as a result I saw this:

<img width="442" height="129" alt="изображение" src="https://github.com/user-attachments/assets/687a3b2f-d40f-4ef6-a82e-e8ddeeafe2b6" />

Well, you can just run a debugger and monitor the memory, but that's not my way. As written, we will enjoy recreating structures.

So I went to Hex-Rays and started looking at what the decompiler would tell me.

main() function:

<img width="621" height="493" alt="изображение" src="https://github.com/user-attachments/assets/e81ec853-2958-4519-a85a-2bc1e6990292" />

Main immediately encounters some variables, pointers to some memory offsets, calls to some other functions, variables assign values to each other, inside the for loop, the variable v7 is assigned the result of calling a function located somewhere in the supposedly v5 array, and here you can also see other nonsense, so you can assume that v4, v5, v7 are not ints, but custom structures.

Let's look at the row_allocator() function:

<img width="353" height="235" alt="изображение" src="https://github.com/user-attachments/assets/012816b2-dbc8-4fce-93ba-9e83243490aa" />

A variable result is created, 4 bytes in size, at least Hex-Rays thinks so, but highlights it in yellow, so there is no 100% certainty. Immediately 0x10 bytes are allocated for result, that is, 16 bytes in the decimal system. And then some 4 segments are initialized, even with indexes.

Let's create some structure, then declare variables as this structure and see what happens:

<img width="539" height="148" alt="изображение" src="https://github.com/user-attachments/assets/f3edda06-4443-498f-9266-d8464bdfe025" />

Let's assume that there are 4 ints in the structure, which gives us 16 bytes.

Then row_allocator() starts to look like this:

<img width="351" height="225" alt="изображение" src="https://github.com/user-attachments/assets/2346c4ff-7f7b-4756-b1e7-91b5be280a74" />

In general, everything looks logical, but there is one nuance - the address of the row_allocator() function is placed in field_C, that is, to compile it, you need to write everything something like this:

```
result->field_C = (int)&row_allocator;
```

And here you can run into some limitations if you try to compile this on a 64-bit system, the thing is that int cannot accommodate 64-bit addresses, so you will probably need to use long int, or even better size_t:

```
result->field_C = (long int)&row_allocator;

OR

result->field_C = (size_t)&row_allocator;
```

But there are some nuances here too - for example, long int takes 4 bytes on Windows x64, if you replace int with long int here - you will, in principle, fit into 16 allocated bytes. But if you want to run this on Linux/MacOS, then long int takes 8 bytes, which means you will most likely get a "Segmentation fault" or something like that, so you will need to allocate 32 bytes via malloc() instead of 16.

For size_t, the situation is that this type takes 32 bits on 32-bit systems, and 64 bits on 64-bit systems, that is, 4 and 8 bytes respectively, this type is needed to store the maximum possible size of the machine's memory address, so whether you use size_t on Windows or Linux/MacOS will not make a difference - only the bit depth of the system will matter.

In general, you can do without writing the function address in the last field of the structure, but for now the task is to restore the logic of the program.

Now let's go back to main(), declare some variable as a structure and see how Hex-Rays reacts to this:

<img width="718" height="445" alt="изображение" src="https://github.com/user-attachments/assets/bd099987-50c2-4200-be14-4c857a76212c" />

Everything collapsed into one structure v4, I thought there were still some oddities.

Each field of the structure is an int and the fact that the function allocates the structure inside an int is wrong, besides, there is an offset of 8 bytes from the outer field field_C, from which I conclude that v4 is not the only structure and the variables v5 and v7 are also structures. Hex-Rays does not allow me to simply take and saw several structures here, it collapses everything into one, so I looked at the code that I showed at the beginning of the article and, relying on the byte offsets, as well as logic, began to rewrite the code in the editor, here is my version of the restored main():

```
int main() {      
  
    struct line row1;    
    struct line row2;    
    struct line row3;
    
    row1 = row_allocator();    
    row2 = row1;
    
    allocate_cols(row1, 0);
    
    for (int i = 0; i <=2; i++) {
        row3 = row_allocator();        
        row3.line_3 = i + 1;        
        row2 = row3;
        
        allocate_cols(row3, i + 1);
    }        
    
    return 0;    
    
}
```

And here is the restored structure:

```
struct line { //we define the template according to which columns, rows and cells will be built

    int line_1;    
    int line_2;    
    int line_3;   
 
};
```
The last field with the address is missing because it is not used anywhere, only 3 fields are used.

Perhaps I am wrong and it would have been possible to manage this somehow with one structure, perhaps I didn’t understand it all correctly, but what happened, happened.

Let's move on - check allocate_cols():

<img width="490" height="405" alt="изображение" src="https://github.com/user-attachments/assets/9b0e5039-5845-466d-ba51-40654ca59e9b" />

I see that 2 arguments are passed to allocate_cols() - a structure and some decimal number, but in the function itself there are only 2 ints.

It should be noted that the structure passed here is not actually used anywhere, although the following expression appears here:

```
*(a1 + 4) = colmn_allocator();
v4 = *(a1 + 4);
```

What do I see? The colmn_allocator() function is thrown into the second field of the structure we passed, and then the value of this field is assigned to the variable v4.

Let's look at colmn_allocator():

<img width="340" height="228" alt="изображение" src="https://github.com/user-attachments/assets/2fe88be0-2ce0-4e65-82d3-b83922180e65" />

The function looks exactly like row_allocator and allocates a "column" rather than a "row".


So, Hex-Rays is trying to pass a structure to int again, but I know that this is wrong. In fact, v4 is a structure whose fields are initialized by the colmn_allocator() function. Why does this happen then? Let me explain:

The problem is most likely in the compiler's work (just a guess). Compilers can optimize the code in this way and as a result the compiler can make such an asm:

<img width="407" height="468" alt="изображение" src="https://github.com/user-attachments/assets/92e12b06-64fa-4fcc-8b1f-107399b7400c" />

Well, of course, Hex-Rays will pick this up and give me what I saw on the screenshot. Well, and most likely the row1 structure from main() is not passed to allocate cols().

I assume that in the allocate_cols() function the variables result, v4 and v5 are structures, and colmn_allocator() refers to the same line structure and also initializes the structure fields in allocate_cols():

<img width="454" height="238" alt="изображение" src="https://github.com/user-attachments/assets/4c5636ae-e093-4db7-9922-5a71af55fa57" />

Here is my restored version of the allocate_cols() function:

```
void allocate_cols(struct line a1, int a2) 
{
    struct line result;    
    struct line column1;    
    struct line column2;        
    
    column1 = colmn_allocator();    
    result = allocate_cells(a2, 0);
    
    for (int i = 0; i <= 2; i++) {
    
        column2 = colmn_allocator();        
        column2.line_3 = i + 1;        
        allocate_cells(a2, i + 1);        
        result = column1;
    }
}
```

Here I have given the function the type void() because it does not return anything and its result is not passed to any variable.

From all this we can conclude that the program builds some kind of matrix using structures, but there are no hints of a flag anywhere yet.

Let's move on and look at the next function - allocate_cells():

<img width="873" height="546" alt="изображение" src="https://github.com/user-attachments/assets/20bbb808-e1a2-4d7b-8546-d7430020275e" />

Again offsets by some number of bytes, again cell_allocator() and I think I even know what I will see there, there is a flag variable, which means I getting closer to solving this task.

Here is the expression:

```
*(flag + 100 * a2 + 10 * a3 + i + 1) == flag[100 * a2 + 10 * a3 + i + 1];
```

Because flag is a pointer to the beginning of the array, from where some number of bytes are counted and I get the value by the array index, unless, of course, I try to go beyond its limits, otherwise we will get a "Segmentation fault".

Check cell_allocator():

<img width="323" height="212" alt="изображение" src="https://github.com/user-attachments/assets/d237e2b8-0f2f-4db2-ae11-da9f323b4b9d" />

There are some differences here - 3 fields are initialized, one with the address of this function, which means only 2 are used. In theory, this should be a different structure, but the fields here are the same 4-byte, so while it is possible to define lines structure here, it is not possible to do this correctly here in IDA - I will simply define it in the restored code:

```
struct line cell_allocator() {

    struct line *result;
    result = malloc(12); 
       
    result->line_1 = 0;    
    result->line_2 = 0;    
    result->line_3 = 0;
    
    return *result;
}
```

Accordingly, the variables in the allocate_cells() function are structures, my restored version of allocate_cells() looks like this:

```
struct line allocate_cells(int a2, int a3) {

    struct line cell1;    
    struct line cell2;    
    struct line result;
    
    cell1 = cell_allocator();
    
    if (check(a2, a3, 0)) {
    
        result = cell1;        
        cell1.line_2 = ((100 * a2 + 10 * a3) % 255) ^ flag[100 * a2 + 10 * a3];        printf("%c", cell1.line_2);
    
    }
    
    for (int i = 0; i <= 2; i++) {
    
        cell2 = cell_allocator();        
        cell2.line_3 = i + 1;        
        cell1.line_1 = cell2.line_3;
        
        if ( check(a2, a3, i + 1) ) {
        
            cell1.line_2 = ((100 * a2 + 10 * a3 + i + 1) % 255) ^ flag[100 * a2 + 10 * a3 + i + 1];            
            printf("%c", cell1.line_2);    
                            
        }
        
        result = cell2;        
        cell1 = cell2;
        
    }
    
    return result;
    
}
```

I have already inserted printf() here to read cell1.line_2. There is also a check() function, let's take a look at it:

<img width="403" height="209" alt="изображение" src="https://github.com/user-attachments/assets/3215f252-d4ac-4d65-811f-1fdd38ddba72" />

Everything is simple here, the function returns Boolean values, that is, 0 or 1.

Restored version:

```
int check(int a1, int a2, int a3) {

    if(a1 != a2)        
        return 0;  
          
    if (!a3 || a3 == 3)        
        return 1;
    
    if (a1 == 3)        
        return 1;
    
    return !a1;
    
}
```

In general, I can say that the program logic has been restored, the flag variable is an array of 335 numbers, this array can be seen in the restored code below.

The binary source code looked something like this:

```
#include <stdio.h>
#include <stdlib.h>

int flag[335] = {102, 109, 99, 100, 125, 70, 81, 96, 66, 76, 70, 111, 79, 120, 61, 57, 39, 88, 120, 124, 110, 120, 113, 70, 66, 79, 64, 43, 95, 41, 120, 83, 79, 16, 87, 75, 104, 111, 113, 18, 101, 30, 96, 99, 31, 69, 69, 85, 106, 120, 97, 107, 5, 6, 90, 77, 15, 64, 120, 81, 105, 15, 70, 82, 14, 38, 42, 33, 49, 44, 52, 113, 50, 49, 11, 15, 59, 127, 52, 12, 4, 105, 48, 49, 99, 57, 37, 13, 17, 24, 19, 56, 104, 46, 8, 42, 22, 83, 37, 50, 1, 51, 48, 10, 4, 1, 60, 95, 5, 60, 49, 61, 32, 24, 28, 39, 6, 60, 31, 1, 53, 44, 61, 66, 31, 39, 31, 43, 213, 228, 178, 203, 241, 234, 206, 238, 208, 186, 198, 206, 199, 233, 188, 199, 213, 164, 250, 234, 214, 207, 160, 199, 214, 169, 172, 172, 247, 213, 212, 215, 244, 233, 197, 210, 214, 149, 247, 244, 156, 254, 207, 250, 156, 226, 214, 197, 199, 246, 219, 225, 251, 193, 247, 219, 140, 212, 215, 250, 229, 248, 218, 237, 177, 134, 148, 247, 146, 245, 167, 140, 169, 252, 155, 130, 148, 167, 158, 165, 185, 133, 148, 131, 165, 183, 129, 176, 151, 232, 159, 235, 175, 235, 234, 128, 169, 211, 137, 142, 174, 128, 214, 129, 170, 138, 129, 154, 158, 219, 165, 151, 178, 186, 185, 162, 184, 145, 144, 163, 145, 190, 179, 200, 178, 174, 142, 87, 85, 102, 106, 49, 100, 54, 70, 70, 104, 64, 101, 69, 120, 69, 55, 72, 91, 39, 36, 103, 95, 121, 84, 84, 120, 77, 120, 75, 105, 95, 102, 22, 96, 86, 19, 67, 84, 126, 16, 107, 77, 70, 100, 101, 125, 28, 76, 3, 118, 122, 94, 117, 64, 84, 112, 117, 116, 9, 106, 13, 75, 123, 126, 44, 56, 8, 32, 13, 13, 127, 2, 124, 48, 63, 45, 32, 44, 41};

struct line {
 
 int line_1;
 int line_2;
 int line_3;
 
};

struct line row_allocator() {
 
 struct line *result;

 result = malloc(12);
 result->line_1 = 0;
 result->line_2 = 0;
 result->line_3 = 0;
 
 return *result;
 
}

struct line colmn_allocator() {

 struct line *result;

   result = malloc(12);
   result->line_1 = 0;
   result->line_2 = 0;
   result->line_3 = 0;

   return *result;

}


struct line cell_allocator() {

 struct line *result;

 result = malloc(12);
 result->line_1 = 0;
 result->line_2 = 0;
 result->line_3 = 0;

 return *result;

}

int check(int a1, int a2, int a3) {

 if(a1 != a2)
  return 0;
 
 if (!a3 || a3 == 3)
  return 1;

 if (a1 == 3)
  return 1;

 return !a1;

}


struct line allocate_cells(int a2, int a3) {

 struct line cell1;
 struct line cell2;
 struct line result;

 cell1 = cell_allocator();

 if (check(a2, a3, 0)) {

  result = cell1;
  cell1.line_2 = ((100 * a2 + 10 * a3) % 255) ^ flag[100 * a2 + 10 * a3];
  printf("%c", cell1.line_2);

 }

 for (int i = 0; i <= 2; i++) {

  cell2 = cell_allocator();
  cell2.line_3 = i + 1;
  cell1.line_1 = cell2.line_3;


  if ( check(a2, a3, i + 1) ) {

   cell1.line_2 = ((100 * a2 + 10 * a3 + i + 1) % 255) ^ flag[100 * a2 + 10 * a3 + i + 1];
   printf("%c", cell1.line_2);
   
  }

  result = cell2;
  cell1 = cell2;


 }

 return result;

}


void allocate_cols(struct line a1, int a2) {

 struct line result;
 struct line column1;
 struct line column2;
    
 column1 = colmn_allocator();
 result = allocate_cells(a2, 0);

 for (int i = 0; i <= 2; i++) {

  column2 = colmn_allocator();
  column2.line_3 = i + 1;
  allocate_cells(a2, i + 1);
  result = column1;

 }

}


int main() {
 
 struct line row1;
 struct line row2;
 struct line row3;

    row1 = row_allocator();
 row2 = row1;

 allocate_cols(row1, 0);

 for (int i = 0; i <=2; i++) {

  row3 = row_allocator();
  row3.line_3 = i + 1;
  row2 = row3;

  allocate_cols(row3, i + 1);

 }
 
 return 0;
 
}
```

I launched the restored code in the online compiler, some numbers were falling in cell1.line_2, and I just read them, I realized that these are ascii codes, so in printf there is a descriptor "%c". As a result, I get some phrase:

<img width="1496" height="398" alt="изображение" src="https://github.com/user-attachments/assets/b0a96ced-1ede-4226-9db4-947da261564d" />
