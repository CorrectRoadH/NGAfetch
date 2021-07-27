import time
import random

cookies=[{
'UM_distinctid':'17ad1d36cc4cfc-097cbe3de9b6b7-35637203-13c680-17ad1d36cc5b4d',
'ngacn0comUserInfo':'inPlan%09inPlan%0939%0939%09%0910%090%094%090%090%09',
'ngaPassportUid':'62757950',
'ngaPassportUrlencodedUname':'inPlan',
'ngaPassportCid':'X967qo45ubhuhd4vmbutgv0001mk5c9sv1t0pjdc',
'_cnzz_CV30043604':'forum%7Cfid-7%7C0',
'lastvisit':'1627092756',
'lastpath':'/',
'ngacn0comUserInfoCheck':'b6b9616c1757f94c75a7b1b47cae1f4d',
'ngacn0comInfoCheckTime':'1627092756',
'bbsmisccookies':'%7B%22uisetting%22%3A%7B0%3A1%2C1%3A1634823522%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-150%2C1%3A1627146042%7D%2C%22insad_views%22%3A%7B0%3A2%2C1%3A1627146042%7D%7D',
'CNZZDATA30043604':'cnzz_eid%3D1359942950-1627016655-%26ntime%3D1627092255'
},
{'ngaPassportOid':'67a17a018c11391bd7f88dd1dc059d7c',
'ngacn0comUserInfo':'HdzXHL%09HdzXHL%0939%0939%09%0910%090%094%090%090%09',
'ngacn0comUserInfoCheck':'8096dcca250bf3136c8e8826f07f4f05',
'ngacn0comInfoCheckTime':'1627353453',
'ngaPassportUid':'60714687',
'ngaPassportUrlencodedUname':'HdzXHL',
'ngaPassportCid':'X969kf79sfae3aq92j4vlkp2hbkee46hs2i0psv2',
'lastvisit':'1627353457',
'lastpath':'/thread.php?fid=-7',
'bbsmisccookies':'%7B%22uisetting%22%3A%7B0%3A%22e%22%2C1%3A1627353757%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-45%2C1%3A1627405210%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1627405210%7D%7D'
}]

UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15']


def random_sleep():
    time.sleep(random.uniform(15, 20))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快


def random_sleep_short():
    time.sleep(random.uniform(1, 2.1))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快
