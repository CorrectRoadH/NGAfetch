import asyncio
import httpx
import re
from config import random_sleep_short
from text import is_will_be_deleted
import utils.SQL
import utils.User
import utils.Log


async def fetch(url, sql):
    log = utils.Log.LogTool()
    user = utils.User.User()
    # 打开网页
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    except httpx.ConnectTimeout:
        print(f"帖子{url} 访问超时,启用备用手段")
        log.error(f"帖子{url} 访问超时,启用备用手段")
        r = httpx.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    except httpx.ProxyError:
        print(f"帖子{url} 访问 代理错误,启用备用手段")
        log.error(f"帖子{url} 访问 代理错误,启用备用手段")
        r = httpx.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)

    # 解析
    # 处理帖子名
    title = []
    try:
        title = re.findall(r'<title>(.+) NGA玩家社区</title>', r.text)
    except UnicodeDecodeError:
        print(f'{url}帖子已经遇到gbk解析出错,已返回')
        log.error(f'{url}帖子已经遇到gbk解析出错,已返回')
        return 2, url

    if not title:  # 判断被锁与特殊情况.
        title = re.findall(r'<title>(.+)</title>', r.text)
        if title[0] == "找不到主题":
            return 0, url
        elif title[0] == "帖子审核未通过":  # 这种情况下连原来的数据都没有抓到也没有保存的必要了.
            return 0, url
        elif title[0] == "帐号权限不足":
            return 0, url
        else:
            print(f"特殊情况!!!{title}")
            print(f'{url}帖子已经遇到gbk解析出错,已返回')
            return 0, url

    if title == [] and "<!--msginfostart-->帖子发布或回复时间超过限制<!--msginfoend-->" in r.text:
        print("帖子发布超时")
        log.error(f"帖子发布超时 {url}")  # 因为fetch应该没有超时贴
        return 0, url

    print(f'标题:{title}')
    sql.insert(url, None, title[0])
    #todo 这里要改一下,插入帖子的时候插入时间
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
            log.error(f"帖子{url}第{count}页 访问超时,启用备用手段")
            return 1, url
            r = httpx.get(f'https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)
        except httpx.ProxyError:
            print(f"帖子{url}第{count}页 代理错误,启用备用手段")
            log.error(f"帖子{url}第{count}页 代理,启用备用手段")  # 备用手段也不行了呢?直接返回吧
            return 1, url
            r = httpx.get(f'https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)

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
            flood_num = re.findall(r'<tr id=\'post1strow(.+)\' class=\'postrow row.\'>(?:.|\n)*</tr>', flood)
            context = re.findall(r'<span id=\'postcontent.+\' class=\'postcontent ubbcode\'>(.+)</span>', flood)
            if not context:  # 首楼不是<span>而是<p>
                context = re.findall(r"<p id='postcontent0' class='postcontent ubbcode'>(.+)</p>", flood)

            time = re.findall(r'<span id=\'postdate.+\' title=\'reply time\'>(.+)</span>', flood)
            author = re.findall(r"<a href='nuke.php\?func=ucp&uid=(.+)' id='postauthor.+' class='author b'>", flood)
            # 敏感词匹配
            flag = True if is_will_be_deleted(context) else flag

            sql.update_reply(url, flood_num[0], time[0], context[0], author[0])
            last_floods = floods
        count += 1
        random_sleep_short()  # 这里停止一下,不太爬太快,如果不要延时不要删这里,在config.py里改区间

    # 更新策略处理,是否有敏感词等
    result = (1 if flag else 2, url)
    return result


async def update(url, sql):
    log = utils.Log.LogTool()
    user = utils.User.User()

    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}", cookies=user.cookies, headers=user.header)
    # 解析
    # 处理帖子名

    try:
        title = re.findall(r'<title>(.+) NGA玩家社区</title>', r.text)
    except UnicodeDecodeError:
        print(f'标题 {url}帖子已经遇到gbk解析出错,已返回')
        log.error(f'{url}帖子已经遇到gbk解析出错,已返回')
        with open('test.txt', 'a+') as f:
            f.write(r.text)
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
        r = None
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"https://bbs.nga.cn/read.php?tid={url}&page={count}", cookies=user.cookies, headers=user.header)
        except httpx.ConnectTimeout:
            print(f"帖子{url}第{count}页 访问超时,启用备用手段")
            return 1, url
            r = httpx.get('https://bbs.nga.cn/read.php?tid={url}&page={count}', cookies=user.cookies, headers=user.header)
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

                flood_num = re.findall(r'<tr id=\'post1strow(.+)\' class=\'postrow row.\'>(?:.|\n)*</tr>', flood)
                context = re.findall(r'<span id=\'postcontent.+\' class=\'postcontent ubbcode\'>(.+)</span>', flood)
                if not context:  # 首楼不是<span>而是<p>
                    context = re.findall(r'<p id=\'postcontent0\' class=\'postcontent ubbcode\'>(.+)</p>', flood)
                time = re.findall(r'<span id=\'postdate.+\' title=\'reply time\'>(.+)</span>', flood)
                author = re.findall(r"<a href='nuke.php\?func=ucp&uid=(.+)' id='postauthor.+' class='author b'>", flood)

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
    print(asyncio.run(update(27815561)))
