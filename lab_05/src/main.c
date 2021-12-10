#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define NUMBER_OF_RUNS 200
#define THREADS_NUMBER 3


typedef struct kekw thread_t;
struct kekw
{
    unsigned long long int val;
    int power;
    int tasks_val;
};


int getPower(thread_t *const data) {
    int res = data->val;

    for (int i = 1; i < data->power; ++i) {
        res *= data->val;
    }

    return res;
}

int isPrime(thread_t *const data) {
    int counter = 0;
    

    for (int i = 2; i < data->val / 2 + 1; ++i) {
        if (data->val % i == 0) {
            ++counter;
        }
    }

    return counter == 0;
}

int getFibNumb(thread_t *const data) {
    int fib1 = 1, fib2 = 1;

    for (int i = 2, temp; i < data->val; ++i) {
        temp = fib1;
        fib1 = fib2;
        fib2 += temp;
    }

    return fib2;
}

int tasks_val, ind = -1;
int thread_1_status = 0, thread_2_status = 0, thread_3_status = 0;

void *wrapper(void *threads_data) {
    /*
        0  - поток не запущен
        1  - поток запущен
    */
    thread_t *data = (thread_t *)threads_data;
    int res;

    while (1) {                                             // Ожидание первого продукта
        if (thread_1_status == 0 && ind < tasks_val - 1) {
            thread_1_status = 1;
            ++ind;
            // puts("q 1");
            data[ind].val = getPower(&data[ind]);
            // printf("power: %llu\n", data[ind].val);
            while (1) {                                     // Поступление нового продукта в позицию 1
                if (thread_2_status == 0) {                 // и продолжение упаковки предыдущего продукта
                    thread_2_status = 1;
                    // puts("q 2");
                    res = isPrime(&data[ind]);
                    // printf("prime: %d\n", res);
                    thread_1_status = 0;
                    while (1) {                             // Поступление новых продуктов в позиции 1 и 2
                        if (thread_3_status == 0) {         // и продолжение упаковки предыдущего продукта
                            thread_3_status = 1;
                            // puts("q 3");
                            res = getFibNumb(&data[ind]);
                            // printf("fib: %d\n", res);
                            thread_3_status = 0;
                            thread_2_status = 0;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        else {
            break;
        }
    }

    return NULL;
}

int parallel_conveyor(void) {
    pthread_t *threads = (pthread_t *)malloc(sizeof(pthread_t) * THREADS_NUMBER);
    thread_t *threads_data = (thread_t *)malloc(sizeof(thread_t) * tasks_val);

    srand(time(NULL));
    for (int i = 0, random; i < THREADS_NUMBER; ++i) {
        random = rand() % 10;

        threads_data[i].val = random > 3 ? random - 3 : random;
        threads_data[i].power = 2;
    }

    pthread_create(&threads[0], NULL, wrapper, threads_data);
    pthread_create(&threads[1], NULL, wrapper, threads_data);
    pthread_create(&threads[2], NULL, wrapper, threads_data);

    for (size_t i = 0; i < THREADS_NUMBER; ++i)
        pthread_join(threads[i], NULL);

    free(threads);
    free(threads_data);

    return 0;
}

int consistent_conveyor(const int loops_counter) {
    thread_t *some_data = (thread_t *)malloc(sizeof(thread_t) * loops_counter);

    srand(time(NULL));
    for (int i = 0, random; i < loops_counter; ++i) {
        random = rand() % 10;

        some_data[i].val = random > 5 ? random - 3 : random;
        some_data[i].power = 2;

        getPower(some_data);
        isPrime(some_data);
        getFibNumb(some_data);
    }

    free(some_data);

    return 0;
}


int main(void) {
    struct timespec start1, stop1;
    uint64_t time_res = 0;

    printf("Введите количество задач: ");
    fscanf(stdin, "%d", &tasks_val);

    for (size_t i = 0; i < NUMBER_OF_RUNS; ++i) {
        clock_gettime(CLOCK_MONOTONIC_RAW, &start1);
        parallel_conveyor();
        clock_gettime(CLOCK_MONOTONIC_RAW, &stop1);

        time_res += (stop1.tv_sec - start1.tv_sec) * 1000000000 + (stop1.tv_nsec - start1.tv_nsec);
    }
    time_res /= NUMBER_OF_RUNS;
    printf("Параллельный конвейер: %llu\n", time_res);

    for (size_t i = 0; i < NUMBER_OF_RUNS; ++i) {
        clock_gettime(CLOCK_MONOTONIC_RAW, &start1);
        consistent_conveyor(tasks_val);
        clock_gettime(CLOCK_MONOTONIC_RAW, &stop1);

        time_res += (stop1.tv_sec - start1.tv_sec) * 1000000000 + (stop1.tv_nsec - start1.tv_nsec);
    }
    time_res /= NUMBER_OF_RUNS;
    printf("Последовательный конвейер: %llu\n", time_res);

    return 0;
}
