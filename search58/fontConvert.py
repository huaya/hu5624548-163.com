import requests
import woff2otf.woff2otf as wt
from fontTools.ttLib import TTFont

# wt.convert('xxxx.woff', 'maoyan.otf')
baseFont = TTFont('base.otf')  # base.otf是某一次访问获取的字体文件,然后人工识别内容,作为与后面获取字体的比对标本,从而让电脑自动获得后面获取字体的实际内容。
maoyanFont = TTFont('maoyan.otf')

glyf = maoyanFont['glyf'].glyphs
print(glyf)


uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()  # 解析otf字体后获得的数据
print(uniList)

# numList = []  # 解析otf字体数据转换成数字
# baseNumList = ['.','B','专','张','3','1','硕','本','2','科','杨','7','4','校','女','E','生','8','王','黄','M','技','中',
#                '周','博','李','大','士','验','6','9','赵','5','男','吴','无','A','应','以','经','刘','下','高','陈','0','届']
# baseUniCode = ['x', 'uniE047', 'uniE061', 'uniE0C6', 'uniE166', 'uniE276', 'uniE310', 'uniE33D', 'uniE39C', 'uniE3A4', 'uniE4B5', 'uniE556', 'uniE565', 'uniE585', 'uniE58B', 'uniE599', 'uniE5E6', 'uniE69A', 'uniE781', 'uniE7AE', 'uniE85F', 'uniE8E8', 'uniEA82', 'uniEAC0', 'uniEAE6', 'uniEB61', 'uniED51', 'uniED5C', 'uniEE0C', 'uniEE58', 'uniEF29', 'uniEF74', 'uniF039', 'uniF083', 'uniF09C',
#                'uniF0EF', 'uniF184', 'uniF255', 'uniF287', 'uniF2F7', 'uniF324', 'uniF63C', 'uniF6FB', 'uniF7CE', 'uniF7D8', 'uniF815']
# for i in range(1, 12):
#     maoyanGlyph = maoyanFont['glyf'][uniList[i]]
#     for j in range(11):
#         baseGlyph = baseFont['glyf'][baseUniCode[j]]
#         if maoyanGlyph == baseGlyph:
#             numList.append(baseNumList[j])
#             break
# uniList[1] = 'uni0078'
# new_dict = dict(zip(uniList[2:], numList[1:]))  # 实时获取字体映射关系
# print(new_dict)

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