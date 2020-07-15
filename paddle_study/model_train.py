# 导入图像读取第三方库
import numpy as np
from PIL import Image
from paddle import fluid
from paddle_study.clazzs import MNIST

# 读取一张本地的样例图片，转变成模型输入的格式
def load_image(img_path):
    # 从img_path中读取图像，并转为灰度图
    im = Image.open(img_path).convert('L')
    print(np.array(im))
    im = im.resize((28, 28), Image.ANTIALIAS)
    im = np.array(im).reshape(1, -1).astype(np.float32)
    # 图像归一化，保持和数据集的数据范围一致
    im = 1 - im / 127.5
    return im


# 定义预测过程
with fluid.dygraph.guard():
    model = MNIST()
    params_file_path = 'mnist'
    img_path = './work/example_0.png'
    # 加载模型参数
    model_dict, _ = fluid.load_dygraph("mnist")
    model.load_dict(model_dict)
    # 灌入数据
    model.eval()
    tensor_img = load_image(img_path)
    result = model(fluid.dygraph.to_variable(tensor_img))
    #  预测输出取整，即为预测的数字，打印结果
    print("本次预测的数字是", result.numpy().astype('int32'))
