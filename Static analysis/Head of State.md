**Head of State Write Up**

Source: https://rev-kids20.forkbomb.ru/tasks/RE4_headofstate

Description: "Flag is flag. (Na na, na na na)"


There is some binary called headofstate.elf. The task is to make the program give me a flag.

Let's run it and see what it does:

<img width="417" height="191" alt="изображение" src="https://github.com/user-attachments/assets/9e931582-ebc1-4140-a666-e4ecdec8592c" />

When the binary starts, it asks me to enter some value. I entered "test" as usual, after which I saw something like this:

<img width="1895" height="281" alt="изображение" src="https://github.com/user-attachments/assets/ede96ee9-fb04-4945-bfdf-65ce45cc6846" />

The program says that my input is probably incorrect.

I go to IDA and see something incomprehensible:

```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char v4[512]; // [rsp+0h] [rbp-5D0h] BYREF Input
  char v5[967]; // [rsp+200h] [rbp-3D0h] BYREF strange format array
  unsigned int j; // [rsp+5C8h] [rbp-8h]
  int i; // [rsp+5CCh] [rbp-4h]

  puts("   Head of State.");                    // banner
  putchar(10);
  puts("  O --->  O ---> o");
  puts("         /^   __/");
  puts(" /!\\ <-- O <-'\n");
  qmemcpy(v5, &unk_14C0, 963uLL);
  memset(v4, 0, sizeof(v4));                    
  printf("Mr. Head of State, state your program:\n> ");
  __isoc99_scanf("%s", v4);                     // the program catches input in the form of a string
  ACTIVE_STATE = 1;                             // this global variable is a marker that determines whether the program will give me a flag or not
  for ( i = 0; i <= 499; ++i )                  // I am given 500 iterations to influence ACTIVE_STATE
  {
    printf("%d ", (unsigned int)ACTIVE_STATE);
    if ( ACTIVE_STATE == 1337 )                 // if ACTIVE_STATE becomes equal to 1337, then the function for printing the flag is called. The function itself, by the way, is an obfuscated mess
    {
      puts(
        "\n"
        "Congratulations, Mr. Head of State! You've lead your state to leetness. Take a look at the flag of your state.");
      obfuscated_print_the_flag();
      return 1;
    }
    for ( j = 0; j <= 106; ++j )                // during 106 iterations something happens with a strange array of 963 bytes and ACTIVE_STATE
    {
      if ( *(_DWORD *)&v5[9 * j] == ACTIVE_STATE && v5[9 * j + 4] == v4[i] )
      {
        ACTIVE_STATE = *(_DWORD *)&v5[9 * j + 5];
        break;
      }
      if ( *(_DWORD *)&v5[9 * j] == ACTIVE_STATE && !v5[9 * j + 4] )
      {
        ACTIVE_STATE = *(_DWORD *)&v5[9 * j + 5];
        break;
      }
    }
  }
  puts("\nDid not succeed, Mr. Head of State.");// If the flag could not be obtained, the program will display the following message at the end of all iterations
  return 0;
}
```

I didn't change anything, I just left comments.

Let's look at arrays v4 and v5. 

Array v4, as indicated in the code, is storage for our input, 512 bytes, no questions asked. But array v5 is storage for some array that is initialized outside main() and has a size of 967 bytes, which is a rather unusual size for an array.

Usually you can find some "nice" sizes like 100 bytes or 256 or 512, but here everything is not so and this is the first bell that this is not actually an array, but something else.

The first thing that catches your eye is 9 * j, which means that after each iteration we have a jump of 9 bytes, somewhere an additional 4 bytes, somewhere 5, this is very strange behavior for an array, usually iteration occurs element by element, so this is the second bell that this is not an array.

I also decided to make some calculations. We have 107 iterations of 9 bytes, 107 * 9 = 963 bytes, which is not surprising. As a result, an assumption appears that this is a structure, 9 bytes in size, and the objects simply refer to the same array from which 963 bytes of information are allegedly placed in v5.

Let's try to tell IDA that we have not an array here, but a structure:

<img width="707" height="265" alt="изображение" src="https://github.com/user-attachments/assets/3e8bc897-7afd-4d97-ba89-95a264b3336b" />

Let it be the myStruct structure for now, leaving one more byte at the end, because in IDA it will not be possible to create a structure entirely from uninitialized data.

Now we can specify that v5 is myStruct:

<img width="1026" height="211" alt="изображение" src="https://github.com/user-attachments/assets/2421a369-ecdd-4712-bd8d-9b6070f844d5" />

Now you can see a marker like gap0, but that's because the structure fields haven't been initialized with anything yet. gap0 points to the uninitialized first byte of the structure, I'll try to initialize it:

<img width="732" height="332" alt="изображение" src="https://github.com/user-attachments/assets/4b352991-410b-48a1-b10f-a85e53b7944e" />

Let's see how IDA reacts to this:

<img width="1074" height="238" alt="изображение" src="https://github.com/user-attachments/assets/43714a3d-6bb2-4336-9d3e-797accd6ea38" />

I see gap1 and that the memory offset has decreased by 1 byte, so we are on the right track! I think the first field is a dword and takes up 4 bytes, let's check:

<img width="830" height="223" alt="изображение" src="https://github.com/user-attachments/assets/e33fed34-79e8-4ff1-bd89-a20355655693" />
<img width="875" height="239" alt="изображение" src="https://github.com/user-attachments/assets/b9aa9d61-ca6f-47be-912c-6b9c47e64964" />

As you can see the field called "a" has been initialized, now all that's left is to initialize everything else, I think the 1 byte offset is char.

Well, in the remaining 4 bytes you can fit another dword.

<img width="695" height="167" alt="изображение" src="https://github.com/user-attachments/assets/51ce6ce8-f549-4a50-848e-3f4065f7be1a" />

Let's see what IDA has to say about this:

<img width="932" height="201" alt="изображение" src="https://github.com/user-attachments/assets/9f128a32-76ee-4348-8c10-49aa53c4f8d4" />

As you can see, everything fell into place, now I'll remove the casts so they don't get on your nerves, give the structure a name inside main() and give the structure fields more meaningful names:

<img width="966" height="216" alt="изображение" src="https://github.com/user-attachments/assets/4d4ab105-2216-4400-8041-ff16d69803e8" />

I called dwords integers because it is obviously int, and I called them symbol because it is compared with my input, and there is a string, it is obviously char.

Now only 9 bytes are left from the memory offsets, but I have already figured out why this happens.

Now I want to look at the array that is thrown into the structure variables, it should repeat the structure:

<img width="999" height="668" alt="изображение" src="https://github.com/user-attachments/assets/6788692c-f5b2-44b4-b70f-3638aef3d5c4" />

Here each element is 1 byte, but I can make some observations: 4 bytes go, then char, 4 bytes again, these are the 9 bytes that are transferred to the structure fields.

I considered it a thankless and time-consuming task to sort through 963 bytes manually, so I remembered IDAPython. In short, IDA has its own API and this will allow me to interact with the elements, including extracting this array byte by byte. I wrote a simple script:

<img width="1907" height="994" alt="изображение" src="https://github.com/user-attachments/assets/9cee38f6-1658-42bd-b1e5-2237dea8c545" />

I run it and get 321 array elements in the required format (see the output under the Execute script window)

Now we can work with it.

Let's take another look at the code and describe the next steps.

Iterates 963 bytes of heterogeneous data at 9 bytes per iteration. If the first field with a number is equal to the current ACTIVE_STATE and if the field with char is equal to the corresponding character of the string I enter, then ACTIVE_STATE becomes equal to the value of the third field of the structure and the iteration stops.

The same thing happens if char is not '0x00', that is, zero.

This entire pass through the data is repeated 500 times and if during this time I have not managed to make ACTIVE_STATE equal to 1337, then I will not receive the flag.

To make it easier for me to select characters, I also decided to transform the array into a more readable form:

```
#include <stdio.h>

int array[321] = {1, 107, 2, 1, 104, 6, 2, 111, 3, 2, 115, 7, 3, 104, 2, 3, 117, 7, 4, 112, 3, 4, 105, 5, 4, 103, 11, 4, 0, 0, 5, 97, 1, 5, 102, 4, 5, 109, 6, 5, 0, 0, 6, 111, 7, 6, 0, 0, 7, 106, 8, 7, 0, 0, 8, 121, 5, 8, 117, 7, 8, 0, 0, 11, 101, 12, 11, 0, 0, 12, 117, 15, 13, 114, 11, 13, 107, 12, 13, 109, 14, 13, 118, 19, 13, 0, 0, 14, 115, 11, 15, 102, 13, 15, 99, 14, 16, 122, 17, 16, 108, 18, 16, 0, 0, 17, 112, 18, 17, 97, 20, 18, 102, 19, 18, 104, 21, 18, 106, 24, 18, 0, 0, 19, 111, 16, 20, 110, 18, 20, 98, 21, 21, 101, 19, 22, 109, 23, 23, 113, 22, 23, 106, 26, 23, 0, 0, 24, 101, 22, 25, 119, 22, 25, 107, 24, 25, 110, 26, 25, 116, 101, 26, 114, 27, 26, 0, 0, 27, 122, 25, 27, 111, 26, 101, 101, 104, 101, 122, 106, 101, 117, 107, 101, 108, 111, 101, 0, 0, 102, 100, 103, 102, 122, 1337, 102, 0, 0, 103, 108, 1337, 103, 0, 0, 104, 106, 105, 104, 0, 0, 105, 110, 105, 105, 104, 107, 105, 116, 111, 105, 0, 0, 106, 111, 107, 106, 120, 108, 106, 109, 110, 106, 0, 0, 107, 114, 111, 108, 103, 109, 108, 98, 112, 109, 111, 112, 110, 113, 112, 110, 120, 115, 110, 104, 120, 110, 0, 0, 111, 107, 105, 112, 111, 117, 113, 105, 119, 113, 103, 120, 114, 110, 103, 114, 121, 115, 114, 101, 116, 114, 112, 118, 114, 0, 0, 115, 109, 116, 115, 119, 118, 116, 110, 116, 117, 108, 109, 118, 113, 114, 119, 100, 113, 119, 105, 120, 119, 0, 0, 120, 105, 107, 120, 107, 113, 120, 115, 119, 120, 0, 0};


struct myStruct {

    int a;
    char b;
    int c;

};


int main() {

    struct myStruct main_Struct;


    for (int i = 0; i < 321; i += 3) {

        main_Struct.a = array[i];
        main_Struct.b = array[i + 1];
        main_Struct.c = array[i + 2];
    
        printf("%d ->", main_Struct.a);

        if(main_Struct.b == 0) {

            printf(" %d ->", main_Struct.b);

        } else {

            printf(" %c ->", main_Struct.b);

        }

        printf(" %d\n", main_Struct.c);


    }

}
```
And as a result I get the following table:

```
1 -> k -> 2
1 -> h -> 6
2 -> o -> 3
2 -> s -> 7
3 -> h -> 2
3 -> u -> 7
4 -> p -> 3
4 -> i -> 5
4 -> g -> 11
4 -> 0 -> 0
5 -> a -> 1
5 -> f -> 4
5 -> m -> 6
5 -> 0 -> 0
6 -> o -> 7
6 -> 0 -> 0
7 -> j -> 8
7 -> 0 -> 0
8 -> y -> 5
8 -> u -> 7
8 -> 0 -> 0
11 -> e -> 12
11 -> 0 -> 0
12 -> u -> 15
13 -> r -> 11
13 -> k -> 12
13 -> m -> 14
13 -> v -> 19
13 -> 0 -> 0
14 -> s -> 11
15 -> f -> 13
15 -> c -> 14
16 -> z -> 17
16 -> l -> 18
16 -> 0 -> 0
17 -> p -> 18
17 -> a -> 20
18 -> f -> 19
18 -> h -> 21
18 -> j -> 24
18 -> 0 -> 0
19 -> o -> 16
20 -> n -> 18
20 -> b -> 21
21 -> e -> 19
22 -> m -> 23
23 -> q -> 22
23 -> j -> 26
23 -> 0 -> 0
24 -> e -> 22
25 -> w -> 22
25 -> k -> 24
25 -> n -> 26
25 -> t -> 101
26 -> r -> 27
26 -> 0 -> 0
27 -> z -> 25
27 -> o -> 26
101 -> e -> 104
101 -> z -> 106
101 -> u -> 107
101 -> l -> 111
101 -> 0 -> 0
102 -> d -> 103
102 -> z -> 1337
102 -> 0 -> 0
103 -> l -> 1337
103 -> 0 -> 0
104 -> j -> 105
104 -> 0 -> 0
105 -> n -> 105
105 -> h -> 107
105 -> t -> 111
105 -> 0 -> 0
106 -> o -> 107
106 -> x -> 108
106 -> m -> 110
106 -> 0 -> 0
107 -> r -> 111
108 -> g -> 109
108 -> b -> 112
109 -> o -> 112
110 -> q -> 112
110 -> x -> 115
110 -> h -> 120
110 -> 0 -> 0
111 -> k -> 105
112 -> o -> 117
113 -> i -> 119
113 -> g -> 120
114 -> n -> 103
114 -> y -> 115
114 -> e -> 116
114 -> p -> 118
114 -> 0 -> 0
115 -> m -> 116
115 -> w -> 118
116 -> n -> 116
117 -> l -> 109
118 -> q -> 114
119 -> d -> 113
119 -> i -> 120
119 -> 0 -> 0
120 -> i -> 107
120 -> k -> 113
120 -> s -> 119
120 -> 0 -> 0
```

I went in the opposite direction, found 1337 in the table and started moving towards the symbol with code 1.

After a couple of minutes I picked up the combination, entered it into the binary and received a flag:

<img width="883" height="244" alt="изображение" src="https://github.com/user-attachments/assets/ea673c66-8ac3-4212-84ff-1c6c56511c2d" />
