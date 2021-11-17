#include "../include/thread.h"

int main(void)
{
    size_t matrix_size, threads_number;
    // unsigned long time_start, time_end, time_res = 0;

    // clock_t time_start, time_end;
    // double time_res = 0;

    struct timespec start1, stop1;
    uint64_t time_res = 0;

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
            time_res = 0;

            printf("Input the number of threads: ");
            fscanf(stdin, "%zu", &threads_number);

            for (size_t i = 0; i < NUMBER_OF_RUNS; ++i)
            {
                clock_gettime(CLOCK_MONOTONIC_RAW, &start1);
                threads_matrix_sum(res_matrix, left_matrix, right_matrix, matrix_size, threads_number);
                clock_gettime(CLOCK_MONOTONIC_RAW, &stop1);

                time_res += (stop1.tv_sec - start1.tv_sec) * 1000000000 + (stop1.tv_nsec - start1.tv_nsec);
            }
            time_res /= NUMBER_OF_RUNS;
            printf("Time ticks: %llu\n", time_res);
        }

        if (rc == 3)
        {
            time_res = 0;

            for (size_t i = 0; i < NUMBER_OF_RUNS; ++i)
            {
                clock_gettime(CLOCK_MONOTONIC_RAW, &start1);
                default_sum(res_matrix, left_matrix, right_matrix, matrix_size);
                clock_gettime(CLOCK_MONOTONIC_RAW, &stop1);

                time_res += (stop1.tv_sec - start1.tv_sec) * 1000000000 + (stop1.tv_nsec - start1.tv_nsec);
            }
            time_res /= NUMBER_OF_RUNS;
            printf("Time ticks: %llu\n", time_res);
        }

        free_matrix(left_matrix, matrix_size);
        free_matrix(right_matrix, matrix_size);
        free_matrix(res_matrix, matrix_size);
    }

    return 0;
}