import multiprocessing
from url_fetch import UrlFetcher
from control import Arranger
import utils.Queue


'''
def save():
    with open('queueData.pkl', 'wb') as file:
        file.write(pickle.dumps([queue, update_queue, update_queue_quick]))
    print("程序退出,进度已保存!")
'''

if __name__ == "__main__":
    queue = utils.Queue.Queue()
    update_queue = utils.Queue.Queue()
    update_queue_quick = utils.Queue.Queue()

    ''' 
   if os.path.isfile('queueData.pkl'):  # 如果文件存在就读取
        with open('queueData.pkl', 'rb') as f:
            queue, update_queue, update_queue_quick = pickle.loads(f.read())
    '''

    process_producer = UrlFetcher(queue)
    process_consumer = Arranger(queue, update_queue, update_queue_quick)

    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
