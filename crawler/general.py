import os

#Each website will be a new project

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.makedirs(directory)

#create queue and crawled files

def create_data_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, "")

#create new file
#remember to optimise (with open as)

def write_file(path, data):
    with open(path, "w") as f:
        f.write(data)

##create_data_files("readwrite", "https://readwrite.com")

#Add data to existing file
def append_to_file(path, data):
    with open(path, "a") as f:
        f.write(data + "\n")

def delete_file_contents(path):
    open(path, "w").close()

#read file and convert line to set items
def file_to_set(filename):
    results = set()
    with open(filename, "rt") as f:
        for line in f:
            results.add(line.strip())
    return results

# Iterate through set, each item in set will be newline in file
def  set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)