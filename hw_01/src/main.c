#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
#define SUCCESS 0
 
 
int main(void) {
 
    int array_len;                                              // (1)
 
    fscanf(stdin, "%d", &array_len);                            // (2)
    int *array = (int *) malloc(array_len * sizeof(int));       // (3)
 
    srand(time(NULL));                                          // (4)
    for (int i = 0; i < array_len; ++i) {                       // (5)
        array[i] = random() % 100;                              // (6)
    }
 
	int is_sorted = 0;                                          // (7)
	while (is_sorted == 0) {                                    // (8)
        is_sorted = 1;                                          // (9)
        int temp;                                               // (10)
 
        for (int i = 1; i < array_len - 1; i += 2) {            // (11)
            if (array[i] > array[i + 1]) {                      // (12)
                temp = array[i];                                // (13)
                array[i] = array[i + 1];                        // (14)
                array[i + 1] = temp;                            // (15)
				is_sorted = 0;                                  // (16)
            }
        }
 
        for (int i = 0; i < array_len - 1; i += 2) {            // (17)
            if (array[i] > array[i + 1]) {                      // (18)
                temp = array[i];                                // (19)
                array[i] = array[i + 1];                        // (20)
                array[i + 1] = temp;                            // (21)
				is_sorted = 0;                                  // (22)
            }
        }	
    }
 
    free(array);                                                // (23)
 
    return SUCCESS;
}