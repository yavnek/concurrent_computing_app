import random
import time
from multiprocessing import Pool
import multiprocessing


def bubble_sort(arr):
    array = arr.copy()
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def parallel_sort(arr, num_processes):
    chunk_size = len(arr) // num_processes
    if chunk_size == 0:
        chunk_size = 1
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    with Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(bubble_sort, chunks)
    sorted_arr = sorted(sum(sorted_chunks, []))
    return sorted_arr


def create_data_array(data_size):
    return [random.randint(1, 100) for _ in range(data_size)]


def single_process_sort_time(data_array):
    try:
        start_time = time.time()
        sorted_data_single = bubble_sort(data_array)
        single_process_time = time.time() - start_time
        del sorted_data_single
        return single_process_time
    except:
        return -1


# coś nie tak z tą funkcją
def multiprocess_parrallel_sort_time(data_array, num_processes):
    try:
        start_time = time.time()
        sorted_data_parallel = parallel_sort(data_array, num_processes)
        parallel_process_time = time.time() - start_time
        del sorted_data_parallel
        return parallel_process_time
    except:
        return -1


def comparing_sort_time(max_data_size):
    max_num_processes = multiprocessing.cpu_count()
    best_function = ''
    best_amount_of_processes = 0
    for x in range(10000, max_data_size):
        data_array = create_data_array(x)
        best_time = float('inf')
        single_process_time = single_process_sort_time(data_array)
        successful_sorting = True
        for y in range(2, max_num_processes):
            multiprocess_sort_time = multiprocess_parrallel_sort_time(data_array, y)
            if (single_process_time == -1 or multiprocess_sort_time == -1):
                print(f"Something went wrong with sorting for data size {len(data_array)}")
                successful_sorting = False
            else:
                if single_process_time < multiprocess_sort_time:
                    if single_process_time < best_time:
                        best_function = 'single_process_sort_time'
                        best_time = single_process_time
                        best_amount_of_processes = 1
                elif multiprocess_sort_time < single_process_time:
                    if multiprocess_sort_time < best_time:
                        best_function = 'multiprocess_parrallel_sort_time'
                        best_time = multiprocess_sort_time
                        best_amount_of_processes = y
        if (successful_sorting):
            print(f"The best function is {best_function} with a time of {best_time} seconds for data size {len(data_array)} and {best_amount_of_processes} processes.")
