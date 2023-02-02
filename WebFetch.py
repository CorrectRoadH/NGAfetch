import re
from config import random_sleep_short
from text import is_will_be_deleted
import utils.SQL
import utils.Log
import utils.http
import utils.analysis


async def fetch(url, sql):
    log = utils.Log.LogTool()
    # 打开网页
    r = await utils.http.get(f"https://bbs.nga.cn/read.php?tid={url}")

    # 解析
    # 处理帖子名
    try:
        state, title = utils.analysis.judge_post_state(r.text)
    except UnicodeDecodeError:
        print("看这里!!!!解码错误", r)
        return 2, url

    # 0 请更新 1 正常 2 找不到这个主题  3 未通过审核 4 特殊 5 超时 6 账号权限不足 7 帖子正等待审核
    if state == 0: # 本来在get_state是有解码错误的,但是反应过来是在r.text这里出错的.所以改了.
        return 2, url
    else:
        if state != 1:  # 如果不等于1也不等于0 就是帖子有事了,直接放弃了
            return 0, url

    print(f'标题:{title}')
    sql.insert(url, None, title[0])
    # todo 这里要改一下,插入帖子的时候插入时间
    count = 1
    last_floods = [-1]
    flag = False  # 敏感词的flag

    while True:
        r = await utils.http.get(f"https://bbs.nga.cn/read.php?tid={url}&page={count}")

        # 楼层处理
        try:
            floods = re.findall(r'<tr id=\'post1strow.+\' class=\'postrow row.\'>(?:.|\n)*?</tr>', r.text)
        except UnicodeDecodeError:
            print(f'{url}帖子已经遇到gbk解析出错,已返回')
            log.error(f'{url}帖子已经遇到gbk解析出错,已返回  而且要出错在上面应该就错了')
            return 2, url

        try:
            if floods[0] == last_floods[0]:  # 如果两页相同说明,上一页是最后一页了|但是有个问题,如果前一页有楼被删之类的,还会相同吗?
                break
            else:
                print(f"{title} 第{count}页")
        except IndexError:
            print(f'楼层出错{floods}')  # 就当被锁了,不能更新,不对阿,这是抓取怎么过期呢,想想有可能哦.要是抓一半被锁了呢.
            log.debug(f'{url} {count}页 楼层出错{floods} 可能是无页楼层')
            # 现在问题已经锁定了,是nga特殊的无页楼层
            return 2, url

        for flood in floods:
            flood_num, context, time, author = utils.analysis.analysis_flood_context(flood)
            if time == author == 0:
                return 2, url
            # 敏感词匹配
            flag = True if is_will_be_deleted(context[0]) else flag
            sql.update_reply(url, flood_num[0], time[0], context[0], author[0])
            # 这里可以新建一个api,inster而不是update,这样inster就不用查询了


            last_floods = floods
        count += 1
        random_sleep_short()  # 这里停止一下,不太爬太快,如果不要延时不要删这里,在config.py里改区间

    # 更新策略处理,是否有敏感词等
    result = (1 if flag else 2, url)
    return result


async def update(url, sql):
    log = utils.Log.LogTool()

    r = await utils.http.get(f"https://bbs.nga.cn/read.php?tid={url}")
    # 解析
    # 处理帖子名

    try:
        title = re.findall(r'<title>(.+) NGA玩家社区</title>', r.text)
    except UnicodeDecodeError:
        print(f'标题 {url}帖子已经遇到gbk解析出错,已返回')
        return 2, url

    if not title:  # 判断被锁与特殊情况.
        title = re.findall(r'<title>(.+)</title>', r.text)
        if title[0] == "找不到主题":
            sql.update_post_state(url, 2)
            return 0, url
        elif title[0] == "帖子审核未通过":
            sql.update_post_state(url, 3)
            return 0, url
        elif title[0] == "帐号权限不足":
            sql.update_post_state(url, 6)
            return 0, url
        else:
            sql.update_post_state(url, 4)
            print(f"特殊情况!!!{title}")
            return 0, url
    # 现在出现一个 标题:[],但为什么没有上面捕捉到.这是为什么呢? 我现在加一个超级特别情况,看看会不会被捕捉.估计是访问频率太高,被抓到了.
    # 现在有思路了,可能是第一次抓取的时候就遇到了锁帖

    if title == [] and "<!--msginfostart-->帖子发布或回复时间超过限制<!--msginfoend-->" in r.text:
        sql.update_post_state(url, 4)
        return 0, url

    print(f'标题:{title}')
    count = 1
    last_floods = [-1]
    flag = False  # 敏感词的flag

    while True:
        r = await utils.http.get(f"https://bbs.nga.cn/read.php?tid={url}&page={count}")

        # 楼层处理
        try:
            floods = re.findall(r'<tr id=\'post1strow.+\' class=\'postrow row.\'>(?:.|\n)*?</tr>', r.text)
        except UnicodeDecodeError:
            print(f'楼层 {url}帖子已经遇到gbk解析出错,已返回')
            with open('test.txt', 'a+') as f:
                f.write(r.text)
            return 2, url

        try:
            if floods[0] == last_floods[0]:  # 如果两页相同说明,上一页是最后一页了|但是有个问题,如果前一页有楼被删之类的,还会相同吗?
                break
            else:
                print(f"{title} 第{count}页")
        except IndexError:
            print(f'楼层出错{floods}')  # 就当被锁了,不能更新,不对阿,这是抓取怎么过期呢,想想有可能哦.要是抓一半被锁了呢.
            log.debug(f'{url} {count}页 楼层出错{floods} 可能是无页楼层')
            # 现在问题已经锁定了,是nga特殊的无页楼层
            return 2, url

        for flood in floods:
            if "<h4 class='silver subtitle'>改动</h4>" in flood:  # 说明这一层有改动

                flood_num, context, time, author = utils.analysis.analysis_flood_context(flood)
                if time == author == 0:
                    return 2, url

                # 敏感词匹配
                flag = True if is_will_be_deleted(context) else flag

                if sql.get_reply_latest(url, flood_num[0]) != context:
                    print(f'出现改动情况!!!~~~帖子:{url}楼层:{flood_num[0]}')
                    sql.update_reply(url, flood_num[0], time[0], context[0], author[0])
            last_floods = floods
        count += 1
        random_sleep_short()  # 这里停止一下,不太爬太快,如果不要延时不要删这里,在config.py里改区间

    # 更新策略处理,是否有敏感词等
    result = (1 if flag else 2, url)
    return result


if __name__ == '__main__':
    pass
