import sys
import requests
import threading
import os

error = 0

def download_file(url, filename=None):
    global error
    
    try:
        print(f"Starting download from: {url}")
        
        response = requests.get(url)

        #if there is no valid response
        if response.status_code != 200: 
            print(f"Failed to reach the URL. Status code: {response.status_code}")
            return

        #if the user did not gave any filename it will be under this name
        if filename == None:
            filename = os.path.basename(url)

        #if the user provides us a existing filename
        counter = 0
        while os.path.exists(filename):
            counter = counter + 1
            base, extension = os.path.splitext(filename)
            filename = f"{base}({counter}){extension}"

        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Successfully downloaded: {filename}")
    except Exception as ex:
        print(f"An error occurred while downloading {url}: {ex}")
        error += 1

#if no urls are provided
if len(sys.argv) < 2:
    print("Example usage: python download_files.py <url1> <url2> ... (-o filename)")
    sys.exit(1)

#creating the list of urls provided and maybe the filename(s)
urls = []
filenames = []
i = 1
while i < len(sys.argv):
    #here we can catch the filename(s) that user wants spesificaly 
    if sys.argv[i] == "-o":
        for j in sys.argv[i+1:]:
            filenames.append(j)
        break
    urls.append(sys.argv[i])
    i = i +1

#creating the list of threads
threads = []
for i in range(len(urls)):
    url = urls[i]
    #filename could be provided less times than the urls
    try:
        filename = filenames[i]
    except Exception as ex:
        filename = None
    
    #if a filename is provided
    if filename:
        thread = threading.Thread(target=download_file, args=(url, filename))
    else:
        thread = threading.Thread(target=download_file, args=(url,))

    threads.append(thread)
    thread.start()


#exiting from all the threads when done with it
for thread in threads:
    thread.join()

if error == 0:
    print("All downloads completed successfully.")
else:
    print("Downloads completed but with errors.")

sys.exit(0)