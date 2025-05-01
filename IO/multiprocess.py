import sys
import requests
import os
from multiprocessing import Process, Manager

def download_file(url, filename=None, error=0):
    try:
        print(f"Starting download from: {url}")
        
        response = requests.get(url)

        # if there is no valid response
        if response.status_code != 200:
            print(f"Failed to reach the URL. Status code: {response.status_code}")
            error.value += 1  # Increment the error counter in the shared variable
            return

        # if the user did not give any filename, it will be under this name
        if filename is None:
            filename = os.path.basename(url)

        # if the user provides us an existing filename
        counter = 0
        while os.path.exists(filename):
            counter += 1
            base, extension = os.path.splitext(filename)
            filename = f"{base}({counter}){extension}"

        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Successfully downloaded: {filename}")
    except Exception as ex:
        print(f"An error occurred while downloading {url}: {ex}")
        error.value += 1  # Increment the error counter in the shared variable

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Example usage: python download_files.py <url1> <url2> ... (-o filename)")
        sys.exit(1)

    # creating the list of urls provided and maybe the filename(s)
    urls = []
    filenames = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-o":
            for j in sys.argv[i+1:]:
                filenames.append(j)
            break
        urls.append(sys.argv[i])
        i += 1

    # creating a Manager to share the error variable
    with Manager() as manager:
        error = manager.Value('i', 0)  # Shared integer to track errors (initialized to 0)

        processes = []
        for i in range(len(urls)):
            url = urls[i]
            # filename could be provided fewer times than the urls
            try:
                filename = filenames[i]
            except IndexError:
                filename = None

            if filename:
                process = Process(target=download_file, args=(url, filename, error))
            else:
                process = Process(target=download_file, args=(url, None, error))

            processes.append(process)
            process.start()

        # waiting for all processes to finish
        for process in processes:
            process.join()

        # Checking the error count
        if error.value == 0:
            print("All downloads completed successfully.")
        else:
            print("Downloads completed but with errors.")
    
    sys.exit(0)