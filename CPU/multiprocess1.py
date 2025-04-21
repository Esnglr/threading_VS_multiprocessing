import multiprocessing
import sys

sys.setrecursionlimit(20000)

#values to be calculated
numbers = [1904,2495,432]

def fibonacci(num,memo):
    if num in memo:
        return memo[num]
    if num <= 1:
        return num
   
    memo[num] = fibonacci(num - 1,memo) + fibonacci(num - 2,memo)
    return memo[num]

def process_fibonacci(num, index, fib_values,memo):
    fib_value = fibonacci(num,memo)
    fib_values[index] = fib_value

if __name__ == '__main__':
    #each process has its own memory space unlike threads so we should make the list shared manually
    manager = multiprocessing.Manager()
    fib_values = manager.list([None] * len(numbers))
    #a dictionary to store calculated fib values from recursive fibonacci function
    memo = manager.dict()

    #creating the list of processes
    processes = []
    for index in range(len(numbers)):
        process = multiprocessing.Process(target=process_fibonacci, args=(numbers[index], index, fib_values,memo))
        processes.append(process)
        process.start()

    #exiting from all the processes when done with it
    for process in processes:
        process.join()

    #printing the fibpnacci values
    for index in range(len(numbers)):
        print(f"Fibonacci of ({numbers[index]}) = {fib_values[index]}")