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
