
# threading code
import multiprocessing
import threading


thr_count = multiprocessing.cpu_count()

class Crawl_thread(threading.Thread):
    def __init__(self, i, url, info_list, crawler):
        threading.Thread.__init__(self)
        self.num = i
        self.url = url
        self.list = info_list
        self.crwl = crawler

    def run(self):
        print('{} running'.format(self.num))
        print("Getting product from url {}".format(self.url))
        info = self.crwl.get_product_info(self.url)
        self.list.append(info)
        


def thread_tasks(links, info_list, crawler, batch_count):

    print('Running batch {}'.format(batch_count))
    # run multiple threds at once in line with the number of cores on machine
    for i in range(0, thr_count):
        if links:
            l = links.pop(0)
            thrd = Crawl_thread(i, l, info_list, crawler)
            thrd.start()
        else:
            pass

    
    while threading.active_count() > 1:
        #Runs until extra threads are finished
        pass
    
    print('Batch finished {}'.format(batch_count))
        
