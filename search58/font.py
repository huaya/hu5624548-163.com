
from fontTools.ttLib import TTFont

# 加载字体文件：
font = TTFont('58.woff')

# 转为xml文件：
font.saveXML('58.xml')