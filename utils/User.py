import sys
sys.path.append('../')
from config import cookies,UA
import random

class User:
    def __init__(self) -> None:
        self.cookie = cookies[random.randint(0,len(cookies)-1)] # 这里随机从config中拿一个
        self.UA = UA[random.randint(0,len(UA)-1)]
    @property
    def cookies(self):
        return self.cookie
    @cookies.setter
    def cookies(self,value):
        print("不允许设置!")
    @property
    def header(self):
        return {'User-Agent': self.UA,
                'Host': 'bbs.nga.cn',
                'Referer': 'https://bbs.nga.cn/thread.php?fid=-7'
                }
    
if __name__ == "__main__":
    user = User()
    print(user.header)