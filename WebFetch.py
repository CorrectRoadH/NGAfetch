import asyncio
import httpx
import re
from config import cookies, random_sleep_short
from text import is_will_be_deleted
import utils.SQL
import utils.User


async def fetch(url):
    user = utils.User.User()
    # 打开网页
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    except httpx.ConnectTimeout:
        print(f"帖子{url} 访问超时,启用备用手段")
        r = httpx.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    except httpx.ProxyError:
        print(f"帖子{url} 访问 代理错误,启用备用手段")
        r = httpx.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)

    # 解析
    # 处理帖子名

    try:
        title = re.findall(r'<title>(.+) NGA玩家社区</title>', r.text)
    except UnicodeDecodeError:
        print(f'{url}帖子已经遇到gbk解析出错,已返回')
        return 2, url

    # todo 判断是不是被锁了,如果被锁了就不需要更新了
    print(f'标题:{title}')
    sql = utils.SQL.SQL()
    sql.insert(url, None, title[0])
    count = 1
    last_floods = [-1]
    flag = False  # 敏感词的flag

    while True:
        r = None
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}&page={count}", cookies=user.cookies, headers=user.header)
        except httpx.ConnectTimeout:
            print(f"帖子{url}第{count}页 访问超时,启用备用手段")
            r = httpx.get(f'https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)
        except httpx.ProxyError:
            print(f"帖子{url}第{count}页 代理错误,启用备用手段")
            r = httpx.get(f'https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)

        # 楼层处理
        try:
            floods = re.findall(r'<tr id=\'post1strow.+\' class=\'postrow row.\'>(?:.|\n)*?</tr>', r.text)
        except UnicodeDecodeError:
            print(f'{url}帖子已经遇到gbk解析出错,已返回')
            return 2, url

        try:
            if floods[0] == last_floods[0]:  # 如果两页相同说明,上一页是最后一页了|但是有个问题,如果前一页有楼被删之类的,还会相同吗?
                break
            else:
                print(f"{title} 第{count}页")
        except IndexError:
            print(f'楼层出错{floods}')  # 就当被锁了,不能更新,不对阿,这是抓取怎么过期呢,想想有可能哦.要是抓一半被锁了呢.
            print(f'https://bbs.nga.cn/read.php?tid={url}&page={count}')

        for flood in floods:
            flood_num = re.findall(r'<tr id=\'post1strow(.+)\' class=\'postrow row.\'>(?:.|\n)*</tr>', flood)
            context = re.findall(r'<span id=\'postcontent.+\' class=\'postcontent ubbcode\'>(.+)</span>', flood)
            if not context:  # 首楼不是<span>而是<p>
                context = re.findall(r'<p id=\'postcontent0\' class=\'postcontent ubbcode\'>(.+)</p>', flood)
            # 敏感词匹配
            flag = True if is_will_be_deleted(context) else flag

            sql.update_reply(url, flood_num[0], None, context[0])
            last_floods = floods
        count += 1
        random_sleep_short()  # 这里停止一下,不太爬太快,如果不要延时不要删这里,在config.py里改区间

    # 更新策略处理,是否有敏感词等
    result = (1 if flag else 2, url)
    return result


async def update(url):
    user = utils.User.User()

    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    # 解析
    # 处理帖子名

    try:
        title = re.findall(r'<title>(.+) NGA玩家社区</title>', r.text)
    except UnicodeDecodeError:
        print(f'{url}帖子已经遇到gbk解析出错,已返回')
        return 2, url

    if not title:  # 判断被锁与特殊情况.
        title = re.findall(r'<title>(.+)</title>', r.text)
        if title[0] == "找不到主题":
            return 0, url
        elif title[0] == "帖子审核未通过":
            return 0, url
        else:
            print(f"特殊情况!!!{title}")
            return 0, url

    print(f'标题:{title}')
    sql = utils.SQL.SQL()
    count = 1
    last_floods = [-1]
    flag = False  # 敏感词的flag

    while True:
        r = None
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}&page={count}", cookies=user.cookies, headers=user.header)
        except httpx.ConnectTimeout:
            print(f"帖子{url}第{count}页 访问超时,启用备用手段")
            r = httpx.get('https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)
        # 楼层处理
        try:
            floods = re.findall(r'<tr id=\'post1strow.+\' class=\'postrow row.\'>(?:.|\n)*?</tr>', r.text)
        except UnicodeDecodeError:
            print(f'{url}帖子已经遇到gbk解析出错,已返回')
            return 2, url

        try:
            if floods[0] == last_floods[0]:  # 如果两页相同说明,上一页是最后一页了|但是有个问题,如果前一页有楼被删之类的,还会相同吗?
                break
            else:
                print(f"{title} 第{count}页")
        except IndexError:
            print(f'楼层出错{floods}')  # 就当被锁了,不能更新,不对阿,这是抓取怎么过期呢,想想有可能哦.要是抓一半被锁了呢.
            print(f'https://bbs.nga.cn/read.php?tid={url}&page={count}')

        for flood in floods:
            if "<h4 class='silver subtitle'>改动</h4>" in flood:  # 说明这一层有改动

                flood_num = re.findall(r'<tr id=\'post1strow(.+)\' class=\'postrow row.\'>(?:.|\n)*</tr>', flood)
                context = re.findall(r'<span id=\'postcontent.+\' class=\'postcontent ubbcode\'>(.+)</span>', flood)
                if not context:  # 首楼不是<span>而是<p>
                    context = re.findall(r'<p id=\'postcontent0\' class=\'postcontent ubbcode\'>(.+)</p>', flood)
                # 敏感词匹配
                flag = True if is_will_be_deleted(context) else flag

                if sql.get_reply_latest(url, flood_num[0]) != context:
                    print(f'出现改动情况!!!~~~帖子:{url}楼层:{flood_num[0]}')
                    sql.update_reply(url, flood_num[0], None, context[0])
            last_floods = floods
        count += 1
        random_sleep_short()  # 这里停止一下,不太爬太快,如果不要延时不要删这里,在config.py里改区间

    # 更新策略处理,是否有敏感词等
    result = (1 if flag else 2, url)
    return result


if __name__ == '__main__':
    print(asyncio.run(update("27740179")))
