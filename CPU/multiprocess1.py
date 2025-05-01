import multiprocessing
import sys

# Set recursion limit
sys.setrecursionlimit(20000)

def fibonacci(num):
    if num <= 1:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)

def process_worker(num, i, results):
    results[i] = fibonacci(num)

if __name__ == '__main__':
    # Check if there are command-line arguments passed
    if len(sys.argv) < 2:
        print("Please provide a list of numbers to calculate Fibonacci.")
        sys.exit(1)

    # Parse the numbers from the command-line arguments
    try:
        numbers = []
        # Convert the arguments to integers
        for arg in sys.argv[1:]:
            numbers.append(int(arg))
        
    except ValueError:
        print("All arguments must be valid integers.")
        sys.exit(1)

    # Using Manager to create a shared list for results
    manager = multiprocessing.Manager()
    results = manager.list([None] * len(numbers))

    processes = []

    for i in range(len(numbers)):
        # Creating a new process for each calculation
        process = multiprocessing.Process(target=process_worker, args=(numbers[i], i, results))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Printing the results after all processes are done
    for i in range(len(numbers)):
        print(f"Fibonacci({numbers[i]}) = {results[i]}")