# 自动检测	auto	中文	zh	英语	en
# 粤语	yue	文言文	wyw	日语	jp
# 韩语	kor	法语	fra	西班牙语	spa
# 泰语	th	阿拉伯语	ara	俄语	ru
# 葡萄牙语	pt	德语	de	意大利语	it
# 希腊语	el	荷兰语	nl	波兰语	pl
# 保加利亚语	bul	爱沙尼亚语	est	丹麦语	dan
# 芬兰语	fin	捷克语	cs	罗马尼亚语	rom
# 斯洛文尼亚语	slo	瑞典语	swe	匈牙利语	hu
# 繁体中文	cht	越南语	vie	 	
# 
# QPS = 10 (每秒10次访问量)
import os
import requests
import time
import hashlib

def trans(q):
  key = "C4_azdaSXSfteFdUHZeyTommy"
  appid = '20200808000537597123'
  salt = str(time.time())
  sign = appid + q + salt + key
  m = hashlib.new("md5")  
  m.update(sign.encode(encoding="utf-8"))  # 注意使用utf-8编码
  msign = m.hexdigest() # 得到原始签名的MD5值
  data = {
  'q': q,
  'from': 'en',
  'to': 'zh',
  'appid': appid,
  'salt': salt,
  'sign': msign
  }
  url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
  r = requests.get(url,params=data)
  result = r.json()
  return result['trans_result'][0]['dst']

def rename_file(file_dir):   
  L = [] 
  index = 1
  for root, dirs, files in os.walk(file_dir):
    length = len(files)
    for file in files: 
      if os.path.splitext(file)[1] == '.mp4': 
        print('当前翻译进度：', str(index) +'/' + str(length))
        index = index + 1
        name_original = os.path.splitext(file)[0]
        name_translated = trans(os.path.splitext(file)[0]).rstrip()

        postfix = os.path.splitext(file)[1]
        os.rename(os.path.join(root, name_original + postfix), os.path.join(root, name_translated + ' #篮球' + postfix))
        L.append(name_translated + postfix)
  # print(L)
  print('翻译总览：' + str(index - 1) + '个文件已翻译完成，其中' + str(length - index + 1) + '个文件为非MP4文件',) 
  return L

start = time.time()
rename_file(r'/Users/tangyong/test/automation/douyin-of-automation/videos')
end = time.time()
print(end - start)