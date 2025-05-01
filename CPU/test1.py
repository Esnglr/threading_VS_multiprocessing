import subprocess
import psutil
import matplotlib.pyplot as plt
import time


def run_script(command):
    start_time = time.time()

    process = subprocess.Popen(command)
    cpu_usage = []
    memory_usage = []

    while process.poll() is None:
        cpu_usage.append(psutil.cpu_percent(interval=None))
        memory_usage.append(psutil.virtual_memory().percent)
        time.sleep(0.1)  # sample every 0.1 seconds

    end_time = time.time()
    return end_time - start_time, cpu_usage, memory_usage

# File paths for new scripts
numbers = [14, 38, 25]
threading_command = ["python3", "./CPU/thread1.py"] + list(map(str, numbers))
multiprocessing_command = ["python3", "./CPU/multiprocess1.py"] + list(map(str, numbers))

# === Run and Collect Data ===
threading_time, threading_cpu, threading_memory = run_script(threading_command)
multiprocessing_time, multiprocessing_cpu, multiprocessing_memory = run_script(multiprocessing_command)

# === Plot 1: Execution Time ===
plt.figure()
labels = ['Threading', 'Multiprocessing']
times = [threading_time, multiprocessing_time]
plt.bar(labels, times, color=['blue', 'orange'])
plt.ylabel('Execution Time (seconds)')
plt.title('CPU-Bound Task: Execution Time')
plt.savefig('cpu_bound_time.pdf')
plt.close()

# === Plot 2: CPU Usage ===
plt.figure()
plt.plot(threading_cpu, label='Threading CPU Usage', color='blue')
plt.plot(multiprocessing_cpu, label='Multiprocessing CPU Usage', color='orange')
plt.xlabel('Time (samples)')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.legend()
plt.savefig('cpu_bound_cpu_usage.pdf')
plt.close()

# === Plot 3: Memory Usage ===
plt.figure()
plt.plot(threading_memory, label='Threading Memory Usage', color='blue')
plt.plot(multiprocessing_memory, label='Multiprocessing Memory Usage', color='orange')
plt.xlabel('Time (samples)')
plt.ylabel('Memory Usage (%)')
plt.title('Memory Usage Over Time')
plt.legend()
plt.savefig('cpu_bound_memory_usage.pdf')
plt.close()