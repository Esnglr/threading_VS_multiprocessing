import subprocess
import time
import psutil
import matplotlib.pyplot as plt

urls = [
    "https://www.w3.org/TR/PNG/iso_8859-1.txt",
    "https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg",
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
]

filenames = ["text_file.txt", "image_file.png", "pdf_file.pdf"]

# measuring the execution time and monitoring CPU and memory usage
def run_script(command):
    start_time = time.time()

    # Start the subprocess and monitor it using psutil
    process = subprocess.Popen(command)
    
    cpu_usage = []
    memory_usage = []

    # Monitor the process while it runs
    while process.poll() is None:  # process is still running
        cpu_usage.append(psutil.cpu_percent(interval=0.1))  # track CPU usage
        memory_usage.append(psutil.virtual_memory().percent)  # track memory usage

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

    return execution_time, cpu_usage, memory_usage

# test for threading version
print("Testing Threading Version:")
threading_command = ["python3", "./I/O/thread.py"] + urls + ["-o"] + filenames
threading_time, threading_cpu, threading_memory = run_script(threading_command)

# test for multiprocessing version
print("\nTesting Multiprocessing Version:")
multiprocessing_command = ["python3", "./I/O/multiprocess.py"] + urls + ["-o"] + filenames
multiprocessing_time, multiprocessing_cpu, multiprocessing_memory = run_script(multiprocessing_command)

# Plotting the execution time results
labels = ['Threading', 'Multiprocessing']
times = [threading_time, multiprocessing_time]

plt.bar(labels, times, color=['blue', 'orange'])
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Comparison: Threading vs Multiprocessing')

plt.savefig('io_bound.pdf')

# Plotting CPU usage
plt.figure()
plt.plot(threading_cpu, label='Threading CPU Usage', color='blue')
plt.plot(multiprocessing_cpu, label='Multiprocessing CPU Usage', color='orange')
plt.xlabel('Time (seconds)')
plt.ylabel('CPU Usage (%)')
plt.legend()
plt.title('CPU Usage Comparison')
plt.savefig('cpu_usage.pdf')

# Plotting Memory usage
plt.figure()
plt.plot(threading_memory, label='Threading Memory Usage', color='blue')
plt.plot(multiprocessing_memory, label='Multiprocessing Memory Usage', color='orange')
plt.xlabel('Time (seconds)')
plt.ylabel('Memory Usage (%)')
plt.legend()
plt.title('Memory Usage Comparison')
plt.savefig('memory_usage.pdf')
