import time
import random

cookies=[{
'ngacn0comUserInfo':'HdzXHL%09HdzXHL%0939%0939%09%0910%090%094%090%090%09',
'ngaPassportUid':'60714687',
'ngaPassportUrlencodedUname':'HdzXHL',
'ngaPassportCid':'X96avufleuqlj9bo4nor37k8jlg86h4r8gjdc6jv',
'HMF_CI':'388e39eeed45c028d304dc09663aa8398a1815ef43c414a8f26b1a071a03d32fc7',
'ngacn0comUserInfoCheck':'cb298574237a78a8a2fd674fba609cd2',
'ngacn0comInfoCheckTime':'1627902873',
'lastvisit':'1627903395',
'lastpath':'/thread.php?fid=-7',
'HMY_JC':'e9af71d69f70dd5aa58e948b62ad8b392ae3d462bbdbc65a9693a58d836ad3029e,',
'bbsmisccookies':'%7B%22uisetting%22%3A%7B0%3A1%2C1%3A1635558459%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-765%2C1%3A1627923603%7D%2C%22insad_views%22%3A%7B0%3A4%2C1%3A1627923603%7D%7D'

}]

UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15']


def random_sleep():
    time.sleep(random.uniform(15, 20))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快


def random_sleep_short():
    time.sleep(random.uniform(1, 2.1))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快
