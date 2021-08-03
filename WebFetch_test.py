import pytest
import WebFetch
import utils.SQL
import asyncio


def test_fetch_old_return_state():
    sql = utils.SQL.TestSQL()
    value, url = asyncio.run(WebFetch.fetch(27732836, sql))
    assert value == 0


def test_fetch_normal():
    sql = utils.SQL.TestSQL()
    value, url = asyncio.run(WebFetch.fetch(23204010, sql))
    assert value == 2  # 判断返回值
    assert sql.posts['23204010'] == "求科普一下国内cs职业水平的情况"
    assert sql.floods['23204010']['0'][0] == "最近在看WDNMD比赛，天禄输给了LVG，然后LVG又输给了D13(好像是蒙古战队)，国内除了tyloo、VG，其他的ig lvg onethree是不是都很菜啊？然后蒙古很强吗？感觉cncs很菜的样子..."
    assert sql.floods['23204010']['11'][0] == "职业环境太差 吸引不了新鲜血液  完美拿下了国服  但是运营和资本能力差了腾讯10条街<br/><br/>等valorant过审  腾讯操作起来   csgo国内的职业更不可能有新鲜血液  人都是要吃饭的  理想和梦想不能当饭吃<br/><br/>CNCS注定就这样了"
