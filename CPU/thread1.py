import threading
import sys

# Extending the recursion limit
sys.setrecursionlimit(20000)

# Read numbers from command-line arguments
try:
    numbers = []
    for arg in sys.argv[1:]:
        numbers.append(int(arg))

except ValueError:
    print("Please provide valid integers as arguments.")
    sys.exit(1)

# Index is important
results = [None] * len(numbers)

def fibonacci(num):
    if num <= 1:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)

def thread_worker(num, i):
    results[i] = fibonacci(num)

threads = []

# Creating and running the threads
for i in range(len(numbers)):
    thread = threading.Thread(target=thread_worker, args=(numbers[i], i))
    threads.append(thread)
    thread.start()

# Wait for all threads
for thread in threads:
    thread.join()

# Printing the outputs
for i in range(len(numbers)):
    print(f"Fibonacci({numbers[i]}) = {results[i]}")