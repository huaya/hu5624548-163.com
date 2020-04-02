import requests
import woff2otf.woff2otf as wt
from fontTools.ttLib import TTFont

wt.convert('58.woff', 'maoyan.otf')
baseFont = TTFont('base.otf')  # base.otf是某一次访问获取的字体文件，然后人工识别内容，作为与后面获取字体的比对标本，从而让电脑自动获得后面获取字体的实际内容。
maoyanFont = TTFont('maoyan.otf')

uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()  # 解析otf字体后获得的数据
print(uniList)

numList = []  # 解析otf字体数据转换成数字
baseNumList = ['.', '3', '5', '1', '2', '7', '0', '6', '9', '8', '4']
baseUniCode = ['x', 'uniE78E', 'uniF176', 'uniEFE6', 'uniF074', 'uniE9C8', 'uniE912', 'uniEA71', 'uniE74E','uniE4B8', 'uniEE71']
for i in range(1, 12):
    maoyanGlyph = maoyanFont['glyf'][uniList[i]]
    for j in range(11):
        baseGlyph = baseFont['glyf'][baseUniCode[j]]
        if maoyanGlyph == baseGlyph:
            numList.append(baseNumList[j])
            break
uniList[1] = 'uni0078'
new_dict = dict(zip(uniList[2:], numList[1:]))  # 实时获取字体映射关系
print(new_dict)

# def get_font_regx(url ,html):
#     # resp = requests.get(url)
#     # with open('maoyan.woff', 'wb') as fontfile:
#     #     for chunk in resp.iter_content(chunk_size=1024):
#     #         if chunk:
#     #             fontfile.write(chunk)  # 将字体下载到本地
#
#     return html

# html = html.replace('&#x', 'uni')
#     for key in new_dict.keys():
#         initstr = key.lower() + ';'
#         html = html.replace(initstr, new_dict[key])