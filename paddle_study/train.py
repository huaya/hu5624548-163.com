import paddle
import paddle.fluid as fluid
import numpy as np
from paddle_study.clazzs import MNIST

with fluid.dygraph.guard():
    model = MNIST()
    model.train()
    train_loader = paddle.batch(paddle.dataset.mnist.train(), batch_size=16)
    optimizer = fluid.optimizer.SGDOptimizer(learning_rate=0.001, parameter_list=model.parameters())
    EPOCH_NUM = 10
    for epoch_id in range(EPOCH_NUM):
        for batch_id, data in enumerate(train_loader()):
            # 准备数据，格式需要转换成符合框架要求的
            image_data = np.array([x[0] for x in data]).astype('float32')
            label_data = np.array([x[1] for x in data]).astype('float32').reshape(-1, 1)

            # 将数据转换成飞桨动态图格式
            image = fluid.dygraph.to_variable(image_data)
            label = fluid.dygraph.to_variable(label_data)

            # 面向计算过程
            predict = model(image)

            # 计算损失, 取一个批次样本损失的平均值
            loss = fluid.layers.square_error_cost(predict, label)
            avg_loss = fluid.layers.mean(loss)

            # 每训练一千批次的数据， 打印下当前loss的情况
            if  batch_id != 0 and batch_id % 1000 == 0:
                print("epoch: {}, batch: {}, loss is: {}".format(epoch_id, batch_id, avg_loss.numpy()))

            # 后向传播，更新参数的过程
            avg_loss.backward()
            optimizer.minimize(avg_loss)
            model.clear_gradients()

    # 保存模型
    fluid.save_dygraph(model.state_dict(), 'mnist')










