
from fontTools.ttLib import TTFont

# 加载字体文件：
font = TTFont('58.woff')

glyphs = font.getGlyphOrder()[2:]
tmp_dic = {}
for num, un_size in enumerate(glyphs):
    print(un_size,num)
    font_uni = un_size.replace('uni','0x').lower()
    print(font_uni)
    tmp_dic[font_uni] = numprint(tmp_dic)

