import paddle
import paddle.fluid as fluid
from paddle.fluid.dygraph.nn import Linear
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

trainset = paddle.dataset.mnist.train()
train_reader = paddle.batch(trainset, batch_size=8)

for batch_id, data in enumerate(train_reader()):
    # 获取图像数据，并转化为float32类型的数组
    image_data = np.array([x[0] for x in data]).astype('float32')
    # 获取图像标签数据，并转化为float32的数组
    label_data = np.array([x[1] for x in data]).astype('float32')

    # 打印图像数据
    # print("图像数据形状和对应数据为：", image_data.shape, image_data[0])
    # print("图像标签形状和对应数据为：", label_data.shape, label_data[0])
    break

print("\n打印第一个batch的第一个图像，对应标签数字为{}".format(label_data[0]))
# 显示第一batch的第一个图像
img = np.array(image_data[0] + 1) * 127.5
img = np.reshape(img, [28, 28]).astype(np.uint8)

plt.figure("Image")  # 图像窗口名称
plt.imshow(img)
plt.axis('on')  # 关掉坐标轴为 off
plt.title('image')  # 图像题目
plt.show()
