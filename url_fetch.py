import multiprocessing
import httpx
import re
from config import cookies, random_sleep
import utils.fetch


class UrlFetcher(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            r = httpx.get('https://bbs.nga.cn/thread.php?fid=-7', cookies=cookies)
            try:
                posts = re.findall(r'<a href=\'/read\.php\?tid=(.*)\' id=\'t_tt1_.*\' class=\'topic\'>.*</a>', r.text)
            except UnicodeDecodeError:
                print(r)

            # print(posts)
            for post in posts:
                if not utils.fetch.is_fetched(post):
                    self.queue.put(post)  # 直接传post的id,其实在这里获取到了post的title,这里直接传更好,但是为了结构好这只能这样
                    print(f'压入帖子{post}')
                else:
                    # print("重复")
                    pass
            random_sleep()


if __name__ == '__main__':
    print("start")
    queue = multiprocessing.Queue()
    process_producer = UrlFetcher(queue)
    process_producer.start()
    process_producer.join()
