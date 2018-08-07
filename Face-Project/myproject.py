import urllib
import sys
import ssl
from urllib import request, parse
import json

# client_id 为官网获取的AK， client_secret 为官网获取的SK
# 获取token
# def get_token():
#     client_id = API Key
#     client_secret = Secret Key
#     host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=oxWSUmCiaxLARzcavNHsh4Sq&client_secret=feMOxxWatn53Gxp2IG8rpv5bR2fIKGry'%(client_id,client_secret)
#     req = request.Request(host)
#     req.add_header('Content-Type', 'application/json; charset=UTF-8')
#     response = request.urlopen(req)
#     # 获得请求结果
#     content = response.read()
#     # 结果转化为字符
#     content = bytes.decode(content)
#     # 转化为字典
#     content = eval(content[:-1])
#     return content['access_token']
def get_token():
    context = ssl._create_unverified_context()
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=oxWSUmCiaxLARzcavNHsh4Sq&client_secret=feMOxxWatn53Gxp2IG8rpv5bR2fIKGry'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request, context=context)
    content = response.read()
    content = bytes.decode(content)
    content = eval(content[:-1])
    return content['access_token']


# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(file1path, file2path):
    import base64
    f = open(r'%s' % file1path, 'rb')
    pic1 = base64.b64encode(f.read())
    f.close()
    f = open(r'%s' % file2path, 'rb')
    pic2 = base64.b64encode(f.read())
    f.close()
    # 将图片信息格式化为可提交信息，这里需要注意str参数设置
    # param1 = {"image": "str(pic1, 'utf-8')", "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}
    # param2 = {"image": "str(pic1, 'utf-8')", "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}
    params = json.dumps(
        [{"image": str(pic1, 'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
         {"image": str(pic2, 'utf-8'), "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}]
    )
    return params.encode(encoding='UTF8')


# 进行对比获得结果
def img(file1path, file2path):
    token = get_token()
    # 人脸识别API
    # url = 'https://aip.baidubce.com/rest/2.0/face/v2/detect?access_token='+token
    # 人脸对比API
    context = ssl._create_unverified_context()
    # url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + token
    params = imgdata(file1path, file2path)
    # # urlencode处理需提交的数据
    # data = parse.urlencode(params).encode('utf-8')
    # req = request.Request(url, data=data)
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # response = request.urlopen(req, context=context)
    # content = response.read()
    # content = bytes.decode(content)

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    request_url = request_url + "?access_token="+ token
    request = urllib.request.Request(url=request_url,data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request ,context=context)
    content = response.read()
    content = eval(content)
    con = content['result']['score']
    print(con)


    # globals = {
    #     'null': 0
    # }
    # content = eval(content)
    # # 获得分数
    # # try:
    # score = content['result'][0]['score']
    #     # print("----------")
    #     # print(score)
    #     # print("-------------")
    # # except BaseException:
    # if score > 80:
    #     return '照片相似度：' + str(score) + ',同一个人'
    # else:
    #     return '照片相似度：' + str(score) + ',不是同一个人'
    # scoure = content
    # print(scoure)

if __name__ == '__main__':
    file1path = '/Users/cagey/pic-test/1.jpg'
    file2path = '/Users/cagey/pic-test/2.jpg'
    res = img(file1path, file2path)
    print(res)
