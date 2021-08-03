import pickle
import os
posts = []

if os.path.isfile('postsData.pkl'):  # 如果文件存在就读取
    with open('postsData.pkl', 'rb') as f:
        posts = pickle.loads(f.read())
# 有个问题,如果加一个post就写一次数据实在太麻烦了


def save():
    with open('postsData.pkl', 'wb') as file:
        file.write(pickle.dumps(posts))


def is_fetched(url):
    if url in posts:
        return True
    else:
        posts.append(url)
        save()
        return False
