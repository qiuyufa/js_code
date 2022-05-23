import requests,re
import execjs,time,datetime
from loguru import logger

def get_sin(boardId,page):
    with open('dxy.js','r',encoding='utf8') as f:
        jscode = f.read()
    timeStampNum = int(time.time()*1000)
    res = execjs.compile(jscode).call('decryptDxy',boardId,timeStampNum,page)
    return res

def get_detailSin(aid):
    with open('dxy.js','r',encoding='utf8') as f:
        jscode = f.read()
    timeStampNum = int(time.time()*1000)
    serverTime = timeStampNum-312647
    res = execjs.compile(jscode).call('decryptDetail',aid,timeStampNum,serverTime)
    return res

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
             'referer': 'https://www.dxy.cn/bbs/newweb/pc/board/151'}
def request_list():
    url = 'https://www.dxy.cn/bbs/newweb/board/post/page?'
    for page in range(1,10):
        data=get_sin(151,page)
        params={
        "boardId": "151",
        "subBoardId": "0",
        "postType": "0",
        "orderType": "2",
        "pageNum": f"{page}",
        "pageSize": "30",
        "showType": "0",
        "serverTimestamp": "1653232072170",
        "timestamp": f"{data[2]}",
        "noncestr": f"{data[0]}",
        "sign": f"{data[1]}"}
        res=requests.get(url,params=params,headers=headers)
        if res.status_code==200:
            print(f'爬取了第{page}页')
            # return print(res.json())
        else:
            print(f'获取失败！{res.status_code}')
def request_detail():
    url='https://www.dxy.cn/bbs/newweb/post/detail?'
    data=get_detailSin(46505521)
    params={
        "postId": "46505521",
        "serverTimestamp": f"{data[3]}",
        "timestamp": f"{data[2]}",
        "noncestr": f"{data[0]}",
        "sign": f"{data[1]}"
    }
    res=requests.get(url,headers=headers,params=params)
    if res.status_code==200:
        return res.json()
    else:
        return f'没有数据-{res.status_code}'

if __name__ == '__main__':
    request_list()#获取列表页
    request_detail()#获取文章详情页
    
