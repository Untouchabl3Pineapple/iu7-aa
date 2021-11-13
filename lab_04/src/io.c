#include "../include/thread.h"

void free_matrix(int **const matrix, const int matrix_size)
{
    for (size_t i = 0; i < matrix_size; ++i)
    {
        free(matrix[i]);
    }

    free(matrix);
}

void fill_matrix(int **const matrix, const int matrix_size)
{
    for (size_t i = 0; i < matrix_size; ++i)
    {
        for (size_t j = 0; j < matrix_size; ++j)
        {
            matrix[i][j] = rand() % 10;
        }
    }
}

void print_matrix(int **const matrix, const int matrix_size)
{
    for (size_t i = 0; i < matrix_size; ++i)
    {
        for (size_t j = 0; j < matrix_size; ++j)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}