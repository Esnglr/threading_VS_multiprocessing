import threading
import sys
import time

sys.setrecursionlimit(20000)

#values to be calculated
numbers = [1904,2495,432]
fib_values = [None] * len(numbers)
memo = {}
memo_lock = threading.Lock()
results_lock = threading.Lock()

def fibonacci(num):
    with memo_lock:
        if num in memo:
            return memo[num]
    if num <= 1:
        return num

    fib_value = fibonacci(num - 1) + fibonacci(num - 2)

    with memo_lock:
        memo[num] = fib_value
    
    return fib_value


def thread_fibonacci(num, index):
    fib_value = fibonacci(num)
   
    #to lock the shared variable when adding to the list
    with results_lock:
        fib_values[index] = fib_value

#creating the list of threads
threads = []
for index in range(len(numbers)):
    thread = threading.Thread(target=thread_fibonacci, args=(numbers[index],index))
    threads.append(thread)
    thread.start()


#exiting from all the threads when done with it
for thread in threads:
    thread.join()

#printing the fibpnacci values
for index in range(len(numbers)):
    print(f"Fibonacci of ({numbers[index]}) = {fib_values[index]}")