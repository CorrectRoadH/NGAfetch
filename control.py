import multiprocessing
import asyncio
from WebFetch import fetch, update
import utils.Queue
import time as T
from config import random_sleep, random_sleep_short
import yappi
from yappi import get_func_stats, COLUMNS_FUNCSTATS
import os
import sys


def print_all(stats, out, limit=None):
    if stats.empty():
        return
    sizes = [36, 5, 8, 8, 8]
    columns = dict(zip(range(len(COLUMNS_FUNCSTATS)), zip(COLUMNS_FUNCSTATS, sizes)))
    show_stats = stats
    if limit:
        show_stats = stats[:limit]
    out.write(os.linesep)
    for stat in show_stats:
        stat._print(out, columns)


class Arranger(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue  # 这个是等待队列,这里都是第一次
        self.update_queue = utils.Queue.Queue()  # 这里是更新队列,等待更新的
        self.update_queue_quick = utils.Queue.Queue()  # 紧急更新队列
        self.time = 0
        self.count = 0

    async def new_post(self):
        start_time = T.time()
        u1, u2, u3, u4 = self.queue.get(), self.queue.get(), self.queue.get(), self.queue.get()
        print(f'取出帖子{u1} {u2} {u3} {u4}')
        p1, p2, p3, p4 = await asyncio.gather(fetch(u1), fetch(u2), fetch(u3), fetch(u4),)

        posts = [p1, p2, p3, p4]

        for post in posts:
            flag, url = post
            if flag == 1:
                print(f"{url}加入紧急更新队列")
                self.update_queue_quick.put(url)
            elif flag == 2:
                print(f"{url}加入更新队列")

                self.update_queue.put(url)
            else:  # 当flag为0时是被锁了
                pass

        # 记录时间
        self.time += (T.time() - start_time)
        self.count += 4

    async def update_post(self):
        if self.update_queue.qsize() >= 4:
            u1, u2, u3, u4 = self.update_queue.get(), self.update_queue.get(), self.update_queue.get(), self.update_queue.get()
            print(f'取出待更新帖子{u1} {u2} {u3} {u4}')
            p1, p2, p3, p4 = await asyncio.gather(update(u1), update(u2), update(u3), update(u4),)

            posts = [p1, p2, p3, p4]

            for post in posts:
                flag, url = post
                if flag == 1:
                    print(f"{url}加入紧急更新队列")
                    self.update_queue_quick.put(url)
                elif flag == 2:
                    print(f"{url}加入更新队列")
                    self.update_queue.put(url)
                else:  # 当flag为0时是被锁了
                    pass
        else:
            print("待更新的帖子太少")

    def update_post_quick(self):  # 紧急更新的帖子就不等什么了,直接tm的更新上.
        url = self.update_queue_quick.get()
        post = asyncio.run(update(url))

        flag, url = post
        if flag == 1:
            self.update_queue_quick.put(url)
        else:  # 当flag为0时是被锁了,并且应该没有为2的情况,除非敏感词被删了.
            pass

    def run(self):
        yappi.start()

        # 这里逻辑要怎么写呢?因为没有东西时是阻塞.
        # 这里不能这样,不然就是抓取4个帖子然后更新4个帖子,这不合适.更新和抓取不是同步的.
        while True:
            if self.queue.qsize() >= 4:  # 这样设置的就不会阻塞一定要有4个帖子才抓取与更新
                # 获取新的帖子
                asyncio.run(self.new_post())
                # 更新帖子
                print(f"平均每个帖子用时{self.time / self.count}s")

                # 那现在问题就是前期需要抓的时候,抓8个才更新4个.
                if self.queue.qsize() < self.update_queue.qsize():
                    asyncio.run(self.update_post())
            else:
                print("更新帖子")
                # 如果队列里没有帖子直接更新帖子
                if not self.update_queue_quick.empty():  # 防止没有紧急更新的帖子,而上面又进不去.
                    self.update_queue_quick()
                else:
                    print("没有帖子需要紧急更新")
            random_sleep_short()
            # Stats sorted by total time
            stats = get_func_stats().sort(
                sort_type='totaltime', sort_order='desc')
            # returns all stats with sorting applied

            print_all(stats, sys.stdout, limit=10)



