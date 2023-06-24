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


def calculate_percentage_improvement(worse_result, better_result):
    improvement = worse_result - better_result
    percentage_improvement = (improvement / worse_result) * 100
    return percentage_improvement


def comparing_sort_time(min_data_size, max_data_size):
    max_num_processes = multiprocessing.cpu_count()
    best_function = ''
    best_amount_of_processes = 0
    #odrzucony pomysł z dwuwymiarową tablicą
    #final_array = []

    for x in range(min_data_size, max_data_size):
        # deklarowanie rekurencyjnych zmiennych
        data_array = create_data_array(x)
        best_time = float('inf')
        multiprocess_sort_best_time = float('inf')
        multiprocess_sort_best_process_amount = int()
        successful_sorting = True
        # obliczanie czasu dla pojedyńczego procesu
        single_process_time = single_process_sort_time(data_array)
        for y in range(2, max_num_processes):
            multiprocess_sort_time = multiprocess_parrallel_sort_time(data_array, y)
            if (single_process_time == -1 or multiprocess_sort_time == -1):
                print(f"Something went wrong with sorting for data size {len(data_array)}")
                successful_sorting = False
            else:
                if single_process_time < multiprocess_sort_time:
                    if single_process_time < best_time:
                        best_function = 'single_process_sort'
                        best_time = single_process_time
                        best_amount_of_processes = 1

                elif multiprocess_sort_time < single_process_time:
                    if multiprocess_sort_time < best_time:
                        best_function = 'multiprocess_parrallel_sort'
                        best_time = multiprocess_sort_time
                        best_amount_of_processes = y
                if multiprocess_sort_time < multiprocess_sort_best_time:
                    multiprocess_sort_best_time = multiprocess_sort_time
                    multiprocess_sort_best_process_amount = y

        if successful_sorting:
            if best_amount_of_processes > 1:
                print(
                    f"The best function is {best_function} with a time of {best_time} seconds for data size {len(data_array)} and {best_amount_of_processes} processes.\n"
                    f"Its better for this task {round(calculate_percentage_improvement(single_process_time, best_time), 2)}% more than single process function with {single_process_time} seconds.\n")
            else:
                print(
                    f"The best function is {best_function} with a time of {best_time} seconds for data size {len(data_array)} and {best_amount_of_processes} processes.\n"
                    f"Its better for this task {round(calculate_percentage_improvement(multiprocess_sort_best_time, best_time), 2)}% more than multi process function with best {multiprocess_sort_best_time} seconds and {multiprocess_sort_best_process_amount}.\m")

        ####################################################################################
        #odrzucony pomysł z dwuwymiarową tablicą
        # najpierw !!!!!![0]nazwa najlepszego procesu następnie jego [1]czas,  [2]ile procesów dla lepszej sytacji, ile [3]procent lepiej, [4]nalepsza ilość procesów dla najszybszego multi sortowania
        '''if successful_sorting:
            result_array = []
            if best_amount_of_processes>1:
                result_array.append(best_function)
                result_array.append(best_time)
                result_array.append(best_amount_of_processes)
                result_array.append(calculate_percentage_improvement(single_process_time, best_time))
                result_array.append(1)
            else:
                result_array.append(best_function)
                result_array.append(best_time)
                result_array.append(best_amount_of_processes)
                result_array.append(calculate_percentage_improvement(multiprocess_sort_best_time, best_time))
                result_array.append(multiprocess_sort_best_process_amount)
            final_array.append(result_array)

            #print(f"The best function is {best_function} with a time of {best_time} seconds for data size {len(data_array)} and {best_amount_of_processes} processes.")

    for result_array in final_array:'''
