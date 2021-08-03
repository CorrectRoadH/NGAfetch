import MySQLdb
import datetime


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


# 这里用单例模式写
@singleton
class SQL:
    def __init__(self):
        self.db = MySQLdb.connect("0.0.0.0", "root", "hxhl0804", "NGA", charset='utf8')

    def insert(self, post_id, time, title):

        cursor = self.db.cursor()
        post_id = int(post_id)
        sql = f'INSERT INTO post (`post_id`, `time`, `title`, `state`) VALUES ({post_id}, NULL, "{title}", 1);'

        cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()


    def get_reply_num(self, post_id, flood_num):
        cursor = self.db.cursor()
        sql = f'select count(*) from reply where `post_id`={post_id} and `flood_num`={flood_num};'
        cursor.execute(sql)
        results = cursor.fetchone()[0]
        return results

    def update_reply(self, post_id, flood_num, time, context, author):
        cursor = self.db.cursor()
        # 缺点查询次数太多了,看看有没有办法少一点.
        edit_count = self.get_reply_num(post_id, flood_num)
        post_id = int(post_id)
        flood_num = int(flood_num)
        sql = f'INSERT INTO reply (`post_id`, `flood_num`, `edit_count`, `time`, `context`, `author`) VALUES ({post_id}, {flood_num}, {edit_count}, "{time}", "{context}", "{author}");'
        cursor.execute(sql)
        self.db.commit()

    def get_reply_latest(self, post_id, flood_num):
        cursor = self.db.cursor()
        sql = f'select context from reply where `post_id`={post_id} and `flood_num`={flood_num};'
        cursor.execute(sql)
        try:
            results = cursor.fetchall()[-1][0]
        except IndexError:
            # 可能的原因,第一次抓取的时候没有.然后update的之前,他发了还编辑了
            print(f"特殊Bug,sql{sql}")
            results = ""
        return results

    def update_post_state(self, post_id, state):
        # 1 正常 2 找不到这个主题  3 未通过审核 4 特殊 5 超时 6 账号权限不足 7 帖子正等待审核
        cursor = self.db.cursor()
        post_id = int(post_id)
        sql = f'UPDATE post SET state={state} WHERE post_id={post_id};'

        cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()


class TestSQL:  # 单元测试时用的sql
    def __init__(self):
        self.floods = {}
        '''
        {
        postid:{
                '0':['wq','ww']
            }
        }
        '''
        self.posts = {}

    def insert(self, post_id, time, title):
        post_id = str(post_id)
        self.posts[post_id] = title
        self.floods[post_id] = {}

    def get_reply_num(self, post_id, flood_num):
        post_id = str(post_id)

        if str(flood_num) not in self.floods[post_id]:
            return 0
        return len(self.floods[post_id][str(flood_num)])

    def update_reply(self, post_id, flood_num, time, context, author):
        post_id = str(post_id)

        if self.get_reply_num(post_id, flood_num) == 0:  # 这不是更新是新回复
            self.floods[post_id][str(flood_num)] = [context]
        else:
            self.floods[post_id][str(flood_num)].append(context)

    def get_reply_latest(self, post_id, flood_num):
        pass

    def update_post_state(self, post_id, state):
        pass


if __name__ == '__main__':
    mysql = SQL()
    # mysql.update_reply(3244, 0,None,"我是你爹2")
    # mysql.insert(3244,None,"Fuck")
    print(mysql.get_reply_latest(27761015,3))

