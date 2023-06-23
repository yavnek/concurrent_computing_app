import multiprocessing
import random
import time


def bubble_sort(arr):
    array = arr.copy()
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def single_process_sort_time(data_array):
    try:
        start_time = time.time()
        bubble_sort(data_array)
        single_process_time = time.time() - start_time

        return single_process_time
    except:
        return -1


def parallel_sort(arr, num_processes):
    chunk_size = len(arr) // num_processes
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    sorted_chunks = bubble_sort(chunks)

    sorted(sum(sorted_chunks, []))


# Przykładowe dane do posortowania
data_size = 10000


def create_data_array(data_size):
    return [random.randint(1, 100) for _ in range(data_size)]


def multiprocess_parrallel_sort_time(data_array, num_processes):
    processes = []
    try:
        for i in range(num_processes):
            p = multiprocessing.Process(target=parallel_sort, args=(data_array, num_processes))
            processes.append(p)

        start_time = time.time()

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        parallel_process_time = time.time() - start_time
        return parallel_process_time

    except:
        return


def comparing_sort_time(max_data_size):
    max_num_processes = multiprocessing.cpu_count()
    best_function = ''
    best_time = 100
    best_amount_of_processes = 0
    for x in range(1024, max_data_size, 1024):
        #print(f"size: {x}")
        data_array = create_data_array(x)
        for y in range(2, max_num_processes):
            single_process_time = single_process_sort_time(data_array)
            #print(f"\nsingle {single_process_time}")
            multiprocess_sort_time = multiprocess_parrallel_sort_time(data_array, y)
            #print(f"multi {multiprocess_sort_time}")
            if (single_process_time < multiprocess_sort_time):
                #if single_process_time < best_time:
                best_function = 'single_process_sort_time'
                best_time = single_process_time
                best_amount_of_processes = 1
            elif (multiprocess_sort_time < single_process_time):
                #if multiprocess_sort_time < best_time:
                best_function = 'multiprocess_parrallel_sort_time'
                best_time = multiprocess_sort_time
                best_amount_of_processes = y
        print(
        f"The best function is {best_function} with a time of {best_time} seconds for data size {len(data_array)} and {best_amount_of_processes} processes.")
        best_function = ''
        best_time = 100
        best_amount_of_processes = 0
