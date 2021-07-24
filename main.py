import multiprocessing
from url_fetch import UrlFetcher
from control import Arranger
import utils.Queue


if __name__ == "__main__":
    queue = utils.Queue.Queue()

    process_producer = UrlFetcher(queue)
    process_consumer = Arranger(queue)

    process_producer.start()
    process_consumer.start()

    process_producer.join()
    process_consumer.join()

