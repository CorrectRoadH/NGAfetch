import re


def judge_post_state(text):
    # 0 请更新 1 正常 2 找不到这个主题  3 未通过审核 4 特殊 5 超时 6 账号权限不足 7 帖子正等待审核

    title = re.findall(r'<title>(.+) NGA玩家社区</title>', text)

    if not title:  # 判断被锁与特殊情况.
        title = re.findall(r'<title>(.+)</title>', text)

        if title[0] == "找不到主题":
            return 2, title
        elif title[0] == "帖子审核未通过":  # 这种情况下连原来的数据都没有抓到也没有保存的必要了.
            return 3, title
        elif title[0] == "帐号权限不足":
            return 6, title
        elif title[0] == "帖子正等待审核":
            return 7, title
        elif "<!--msginfostart-->帖子发布或回复时间超过限制<!--msginfoend-->" in text:
            return 5, title
        else:
            print(f"特殊情况!!!{title}")
            return 4, title
    else:
        return 1, title



def analysis_flood_context(html):
    try:
        flood_num = re.findall(r"<tr id='post1strow(.+)' class='postrow row.'>(?:.|\n)*</tr>", html)
        context = re.findall(r"<span id='postcontent.+' class='postcontent ubbcode'>(.+)</span>", html)
        if not context:  # 首楼不是<span>而是<p>
            context = re.findall(r"<p id='postcontent0' class='postcontent ubbcode'>(.+)</p>", html)
        time = re.findall(r"<span id='postdate.+' title='reply time'>(.+)</span>", html)
        author = re.findall(r"<a href='nuke.php\?func=ucp&uid=(.+)' id='postauthor.+' class='author b'>", html)
        return flood_num, context, time, author
    except UnicodeDecodeError:
        print("解析错误:{html}")
        return 0, 0, 0, 0
