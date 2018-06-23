#from urllib.request import urlopen
#from link_finder import LinkFinder

import requests
from general import *
from bs4 import BeautifulSoup


class Spider:

    #class variable - shared among all instances
    project_name = ""
    base_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        self.boot()
        self.crawl_page("First Spider", Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " crawling " + page_url)
            print("Queue " + str(len(Spider.queue)) + " | Crawled " + str(len(Spider.crawled)))
            links = Spider.gather_links(page_url)
            #Getting "NoneType object not iterable" error
            Spider.add_links_to_queue(links)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        try:
            NoneType = type(None)
            url = page_url
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            links = set()
            for link in soup.findAll("a", href=True):
                if not isinstance(link.get("href").strip(), NoneType):
                    links.add(link.get("href").strip())
            return links
        except:
            print("Error: Can not crawl page: ", page_url)

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url is None:
                continue
            if url in Spider.queue or url in Spider.crawled:
                continue
            #ensures spider stays on website eg. at that domain name
            if Spider.domain_name in url:
                Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)









