import time
import random

cookies={
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
}


def random_sleep():
    time.sleep(random.uniform(15, 20))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快


def random_sleep_short():
    time.sleep(random.uniform(2, 8))  # 这里配置延迟 现在是1到2.5秒的延迟.防止爬虫太快
