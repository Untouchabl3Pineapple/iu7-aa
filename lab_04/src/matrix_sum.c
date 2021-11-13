#include "../include/thread.h"

void default_sum(int **const res_matrix, int **const left_matrix, int **const right_matrix,
                 const int matrix_size)
{
    for (size_t i = 0; i < matrix_size; ++i)
    {
        for (size_t j = 0; j < matrix_size; ++j)
        {
            res_matrix[i][j] = left_matrix[i][j] + right_matrix[i][j];
        }
    }
}

void *thread_sum(void *thread_data)
{
    thread_t *data = (thread_t *)thread_data;

    for (size_t i = data->start_pos; i < data->size; i += data->step)
    {
        for (size_t j = 0; j < data->size; ++j)
        {
            data->res_matrix[i][j] = data->left_matrix[i][j] + data->right_matrix[i][j];
        }
    }

    return NULL;
}

void threads_matrix_sum(int **const res_matrix, int **const left_matrix, int **const right_matrix,
                        const int matrix_size, const int threads_number)
{
    pthread_t *threads = (pthread_t *)malloc(sizeof(pthread_t) * threads_number);
    thread_t *threads_data = (thread_t *)malloc(sizeof(thread_t) * threads_number);

    for (size_t i = 0; i < threads_number; ++i)
    {
        threads_data[i].start_pos = i;
        threads_data[i].step = threads_number;

        threads_data[i].size = matrix_size;
        threads_data[i].left_matrix = left_matrix;
        threads_data[i].right_matrix = right_matrix;
        threads_data[i].res_matrix = res_matrix;

        pthread_create(&threads[i], NULL, thread_sum, &threads_data[i]);
    }

    for (size_t i = 0; i < threads_number; ++i)
        pthread_join(threads[i], NULL);

    free(threads);
    free(threads_data);
}

unsigned long long tick(void)
{
    unsigned long long d;
    __asm__ __volatile__("rdtsc"
                         : "=A"(d));

    return d;
}