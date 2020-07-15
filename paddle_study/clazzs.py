from paddle import fluid
from paddle.fluid.dygraph.nn import Linear

class MNIST(fluid.dygraph.Layer):
    def __init__(self):
        super(MNIST, self).__init__()

        # 定义一层全连接层，输出维度是1，激活函数为None，即不使用激活函数
        self.fc = Linear(input_dim=784, output_dim=1, act=None)

    # 定义网络结构的前向计算过程
    def forward(self, inputs):
        outputs = self.fc(inputs)
        return outputs
