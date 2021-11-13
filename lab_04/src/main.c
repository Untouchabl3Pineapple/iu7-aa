#include "../include/thread.h"

int main(void)
{
    size_t matrix_size, threads_number;
    unsigned long time_start, time_end, time_res;

    int rc;

    while (1)
    {
        printf("\n_________МЕНЮ_________\n\n");
        printf("1. Сгенерировать две матрицы и сложить их.\n");
        printf("2. Замерить время при параллельном сложении матриц.\n");
        printf("3. Замерить время при последовательном сложении матриц.\n");
        printf("0. Выход.\n");

        printf("\nВыберите действие: ");
        fscanf(stdin, "%d", &rc);

        if (rc == 0)
        {
            return 0;
        }

        printf("Input matrix size: ");
        fscanf(stdin, "%zu", &matrix_size);

        int **left_matrix = (int **)malloc(sizeof(int *) * matrix_size);
        int **right_matrix = (int **)malloc(sizeof(int *) * matrix_size);
        int **res_matrix = (int **)malloc(sizeof(int *) * matrix_size);

        for (size_t i = 0; i < matrix_size; ++i)
        {
            left_matrix[i] = (int *)malloc(sizeof(int) * matrix_size);
            right_matrix[i] = (int *)malloc(sizeof(int) * matrix_size);
            res_matrix[i] = (int *)calloc(sizeof(int), matrix_size);
        }

        srand(time(NULL));
        fill_matrix(left_matrix, matrix_size);
        fill_matrix(right_matrix, matrix_size);

        if (rc == 1)
        {
            default_sum(res_matrix, left_matrix, right_matrix, matrix_size);

            printf("Left matrix:\n");
            print_matrix(left_matrix, matrix_size);
            printf("Right matrix:\n");
            print_matrix(right_matrix, matrix_size);
            printf("Result matrix:\n");
            print_matrix(res_matrix, matrix_size);
        }

        if (rc == 2)
        {
            printf("Input the number of threads: ");
            fscanf(stdin, "%zu", &threads_number);

            for (size_t i = 0; i < NUMBER_OF_RUNS; ++i)
            {
                time_start = tick();
                threads_matrix_sum(res_matrix, left_matrix, right_matrix, matrix_size, threads_number);
                time_end = tick();
                time_res += time_end - time_start;
            }
            time_res /= NUMBER_OF_RUNS;
            printf("Time ticks: %lu\n", time_res);
        }

        if (rc == 3)
        {
            for (size_t i = 0; i < NUMBER_OF_RUNS; ++i)
            {
                time_start = tick();
                default_sum(res_matrix, left_matrix, right_matrix, matrix_size);
                time_end = tick();
                time_res += time_end - time_start;
            }
            time_res /= NUMBER_OF_RUNS;
            printf("Time ticks: %lu\n", time_res);
        }

        free_matrix(left_matrix, matrix_size);
        free_matrix(right_matrix, matrix_size);
        free_matrix(res_matrix, matrix_size);
    }

    return 0;
}