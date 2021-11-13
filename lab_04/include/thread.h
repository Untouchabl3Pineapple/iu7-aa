#ifndef __THREAD_H__
#define __THREAD_H__

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define NUMBER_OF_RUNS 100

typedef struct
{
    size_t start_pos;
    size_t step;

    size_t size;
    int **left_matrix;
    int **right_matrix;
    int **res_matrix;
} thread_t;

// io.c
void free_matrix(int **const matrix, const int matrix_size);
void fill_matrix(int **const matrix, const int matrix_size);
void print_matrix(int **const matrix, const int matrix_size);

// matrix_sum.c
void default_sum(int **const res_matrix, int **const left_matrix, int **const right_matrix,
                 const int matrix_size);
void *thread_sum(void *thread_data);
void threads_matrix_sum(int **const res_matrix, int **const left_matrix, int **const right_matrix,
                        const int matrix_size, const int threads_number);
unsigned long long tick(void);

#endif // __THREAD_H__