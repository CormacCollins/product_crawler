
# threading code
import multiprocessing
import threading
'''
Allows for threading of crawl activities between available cores
Should accept any 'Crawler' type. 
This does not show big speed up effects for crawlers that write considerably to csv.
'''

thr_count = multiprocessing.cpu_count()

class Crawl_thread(threading.Thread):
    def __init__(self, i, url, info_list, crawler, store_name, file_path):
        threading.Thread.__init__(self)
        self.num = i
        self.url = url
        self.list = info_list
        self.crwl = crawler
        self.store = store_name
        self.path = file_path

    def run(self):
        print('{} running'.format(self.num))
        print("Getting product from url {}".format(self.url))
        info = self.crwl.get_product_info(self.url, store_name=self.store, path=self.path)
        self.list.append(info)
        


def thread_tasks(links, info_list, crawler, batch_count, store, file_path):
    print('Running batch {}'.format(batch_count))
    # run multiple threds at once in line with the number of cores on machine
    for i in range(0, thr_count):
        if links:
            l = links.pop(0)
            thrd = Crawl_thread(i, l, info_list, crawler, store, file_path)
            thrd.start()
        else:
            pass

    
    while threading.active_count() > 1:
        #Runs until extra threads are finished
        pass
    
    print('Batch finished {}'.format(batch_count))
        
