import sys
import requests
import os
from concurrent.futures import ThreadPoolExecutor

error = 0

def download_file(url, filename=None):
    global error
    
    try:
        print(f"Starting download from: {url}")
        
        response = requests.get(url)

        # If there is no valid response
        if response.status_code != 200:
            print(f"Failed to reach the URL. Status code: {response.status_code}")
            error += 1
            return

        # If the user did not give any filename, use the URL's basename
        if filename is None:
            filename = os.path.basename(url)

        # If the user provides an existing filename, modify it
        counter = 0
        while os.path.exists(filename):
            counter += 1
            base, extension = os.path.splitext(filename)
            filename = f"{base}({counter}){extension}"

        # Write content to the file
        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Successfully downloaded: {filename}")
    except Exception as ex:
        print(f"An error occurred while downloading {url}: {ex}")
        error += 1


def main():
    if len(sys.argv) < 2:
        print("Example usage: python download_files.py <url1> <url2> ... (-o filename)")
        sys.exit(1)

    # Parse the provided URLs and filenames
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

    # Prepare the argument list for ThreadPoolExecutor
    tasks = []
    i = 0
    while i < len(urls):
        filename = filenames[i] if i < len(filenames) else None
        tasks.append((urls[i], filename))
        i += 1

    # Unpack tuples for executor.map
    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: download_file(*args), tasks)

    if error == 0:
        print("All downloads completed successfully.")
    else:
        print("Downloads completed but with errors.")

    sys.exit(0)


if __name__ == "__main__":
    main()