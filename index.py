import win_unicode_console
win_unicode_console.enable()
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QApplication, QFileDialog, QComboBox)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import hashlib

class Translate(QWidget):
  def __init__(self):
    super(Translate, self).__init__()
    self.switch = True
    self.initUI()

  def initUI(self):
    # 源文件选择按钮和选择编辑框
    self.source_btn = QPushButton('源文件', self)
    self.source_btn.move(30, 30)
    self.source_btn.resize(80,30)
    self.source_btn.clicked.connect(self.select_source)
    self.source_le = QLineEdit(self)
    self.source_le.move(120, 30)
    self.source_le.resize(250,30)

    # 语言选择选择和提示
    self.qtyLabel = QLabel(self)
    self.qtyLabel.move(30, 75)
    self.qtyLabel.resize(100,30)
    self.qtyLabel.setText("语言选择：")
    self.combo_from = QComboBox(self)	
    # 保加利亚语	bul	爱沙尼亚语	est	丹麦语	dan
    # 芬兰语	fin	捷克语	cs	罗马尼亚语	rom
    # 斯洛文尼亚语	slo		匈牙利语	hu 	
    self.lan_from = '英语:en'
    self.combo_from.addItems(['英语:en', '中文:zh', '日语:jp', '韩语:kor', '法语:fra', '西班牙语:spa', '泰语:th', '阿拉伯语:ara', '俄语:ru', '葡萄牙语:pt', '德语:de', '意大利语:it', '希腊语:el', '荷兰语:nl', '波兰语:pl', '瑞典语:swe', '越南语:vie'])
    self.combo_from.activated[str].connect(self.onLanFromActivated)  
    self.combo_from.move(120, 75)
    self.combo_from.resize(120, 30)
    self.arrowLabel = QLabel(self)
    self.arrowLabel.move(240, 75)
    self.arrowLabel.resize(150,30)
    self.arrowLabel.setText("->")
    self.combo_to = QComboBox(self)
    self.lan_to = '中文:zh'
    self.combo_to.addItems(['中文:zh', '英语:en', '日语:jp', '韩语:kor', '法语:fra', '西班牙语:spa', '泰语:th', '阿拉伯语:ara', '俄语:ru', '葡萄牙语:pt', '德语:de', '意大利语:it', '希腊语:el', '荷兰语:nl', '波兰语:pl', '瑞典语:swe', '越南语:vie'])
    self.combo_to.activated[str].connect(self.onLanToActivated)  
    self.combo_to.move(255, 75)
    self.combo_to.resize(120, 30)

    # 话题输入框和提示
    self.topicLabel = QLabel(self)
    self.topicLabel.move(30, 120)
    self.topicLabel.resize(100,30)
    self.topicLabel.setText("添加话题：")
    self.topic_le = QLineEdit('#篮球', self)
    self.topic_le.move(120,120)
    self.topic_le.resize(250,30)

    #翻译按钮
    self.save_btn = QPushButton('开始翻译',self)
    self.save_btn.move(200, 200)
    self.save_btn.resize(140, 30)
    self.save_btn.clicked.connect(self.kick)

    #用户提示区
    self.result_le = QLabel('请选择源文件和翻译语言', self)
    self.result_le.move(30, 270)
    self.result_le.resize(340, 30)
    self.result_le.setStyleSheet('color: blue;')

    # 整体界面设置
    self.resize(450, 450)
    self.center()
    self.setWindowTitle('YouTube视频自动化下载')#设置界面标题名
    self.show()
  
  # 窗口居中函数
  def center(self):
    screen = QtWidgets.QDesktopWidget().screenGeometry()#获取屏幕分辨率
    size = self.geometry()#获取窗口尺寸
    self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))#利用move函数窗口居中

  # 打开的视频文件名称
  def select_source(self):
    dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "C:/")
    self.source_le.setText(str(dir_path))

  def onLanFromActivated(self, text):
    self.lan_from = text

  def onLanToActivated(self, text):
    self.lan_to = text

  def set_label_func(self, text):
    self.result_le.setText(text)

  def switch_func(self, bools):
    self.switch = bools

  def kick(self):
    source = self.source_le.text().strip()# 源文件路径
    lan_from = self.lan_from.strip()# 原语言
    lan_to = self.lan_to.strip()# 翻译语言
    topic = self.topic_le.text().strip()# 添加话题
    if self.switch and source != '' and lan_from != '' and lan_to != '':
      self.switch = False
      self.set_label_func('请耐心等待，正在翻译！')
      self.my_thread = MyThread(source, lan_from, lan_to, topic, self.set_label_func)#实例化线程对象
      self.my_thread.start()#启动线程
      self.my_thread.my_signal.connect(self.switch_func)

class MyThread(QThread):#线程类
  my_signal = pyqtSignal(bool)  #自定义信号对象。参数bool就代表这个信号可以传一个布尔值
  def __init__(self, source, lan_from, lan_to, topic, set_label_func):
    super(MyThread, self).__init__()
    self.source = source
    self.lan_from = lan_from
    self.lan_to = lan_to
    self.topic = topic
    self.set_label_func = set_label_func

  def run(self): #线程执行函数
    string = self.rename_file(self.source, self.lan_from, self.lan_to, self.topic, self.set_label_func)
    self.set_label_func(string)
    self.my_signal.emit(True)  #释放自定义的信号

  def transRequest(self, q, trans_from, trans_to):
    # key = "C4_azdaSXSfteFdUHZeyTommy"
    # appid = '20200808000537597123'
    key = "F4lvKuxL2iomgdv1I4G_TTdsp"
    appid = '20200825000551122123'
    salt = str(time.time())
    sign = appid + q + salt + key
    m = hashlib.new("md5")  
    m.update(sign.encode(encoding="utf-8"))  # 注意使用utf-8编码
    msign = m.hexdigest() # 得到原始签名的MD5值
    data = {
    'q': q,
    'from': trans_from,
    'to': trans_to,
    'appid': appid,
    'salt': salt,
    'sign': msign
    }
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    r = requests.get(url,params=data)
    result = r.json()
    return result['trans_result'][0]['dst']

  def rename_file(self, source, lan_from, lan_to, topic, set_label_func):   
    L = [] 
    index = 1
    trans_from = lan_from.split(':')[1]
    trans_to = lan_to.split(':')[1]
    for root, dirs, files in os.walk(source):
      length = len(files)
      for file in files: 
        if os.path.splitext(file)[1] == '.mp4' or os.path.splitext(file)[1] == '.webm': 
          tans_progress_str = '当前翻译进度：' + str(index) + '/' + str(length)
          print(tans_progress_str)
          self.set_label_func(tans_progress_str)
          index = index + 1
          name_original = os.path.splitext(file)[0]
          name_translated = self.transRequest(os.path.splitext(file)[0], trans_from, trans_to).rstrip()

          postfix = os.path.splitext(file)[1]
          os.rename(os.path.join(root, name_original + postfix), os.path.join(root, name_translated + ' ' + topic + postfix))
          L.append(name_translated + postfix)
    trans_result = '翻译总览：' + str(index - 1) + '个文件已翻译完成'
    print(trans_result) 
    return trans_result

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = Translate()
  ex.show()
  sys.exit(app.exec_())
