import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


PROJECT_NAME = input("Enter the name of your project: ")
HOMEPAGE = input("Enter the homepage url of the website to be crawled: ")
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 8

#thread queue
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

#spider threads, stops when main exists
def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True   #ensures it dies when main exists
        t.start()

#crawls next job in queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


#crawl items from queue
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links in the queue.")
        create_jobs()


create_spiders()
crawl()
