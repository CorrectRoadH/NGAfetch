import time
import random

cookies=[{
'bbsmisccookies':'%7B%22uisetting%22%3A%7B0%3A1%2C1%3A1628168742%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-36%2C1%3A1628010057%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1628010057%7D%7D',
'lastpath':'/',
'lastvisit':'1627980555',
'ngaPassportCid':'X96d6fqca5309dq2fkms9eo7qdhbmqicdsqan962',
'ngaPassportUid':'60714687',
'ngaPassportUrlencodedUname':'HdzXHL',
'ngacn0comInfoCheckTime':'1627980552',
'ngacn0comUserInfo':'HdzXHL%09HdzXHL%0939%0939%09%0910%090%094%090%090%09',
'ngacn0comUserInfoCheck':'8ab0b38375e848a26219bc728d848983',
'ngaPassportOid':'71555bde637ca1c31ee9bee06ce87d07',
'HMY_JC':'14cc34860a83a27fb3d2d6cd9e482265fe167df43980dd2a2da91a05fbc9b4ebbb,',
'HMF_CI':'7a7b92992b9534eeeb994b321d10ec34d2d15a61c6ea6fd6c94ac9794540bec454'
},{
'HMF_CI':'388e39eeed45c028d304dc09663aa8398a1815ef43c414a8f26b1a071a03d32fc7',
'PHPSESSID':'88fd41b868ef9cea8dc6bc4c5a4aafdd',
'ngaPassportOid':'c75bdc8c13be824d90fb5e7c4cb28a53',
'ngacn0comUserInfo':'inPlan%09inPlan%0939%0939%09%0910%090%094%090%090%09',
'ngacn0comUserInfoCheck':'d4c9e68ba9da01c3c4ed6870d1fd4cb9',
'ngacn0comInfoCheckTime':'1627979951',
'ngaPassportUid':'62757950',
'ngaPassportUrlencodedUname':'inPlan',
'ngaPassportCid':'X967qo45ubhuhd4vmbutgv0001mk5c9sv1t0pjdc',
'lastvisit':'1627979955',
'lastpath':'/thread.php?fid=-7',
'bbsmisccookies':'%7B%22uisetting%22%3A%7B0%3A1%2C1%3A1635558459%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-19%2C1%3A1628009893%7D%2C%22insad_views%22%3A%7B0%3A3%2C1%3A1628009893%7D%7D'    }]

UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15']


def random_sleep():
    time.sleep(random.uniform(15, 20))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快


def random_sleep_short():
    time.sleep(random.uniform(1, 2.1))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快
