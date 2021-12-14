 - **db.config** - 配合文件，生产数据库、redis
 - **clean_goods_basic_reference.py** - 表tb_goods_basic_reference中basic_id关联表tb_goods_basic中的id, 若在后者不存在，则删除
 - **clean_goods_reference.py** - 表tb_goods_reference中goods_id关联表tb_goods中的id, 若在后者找不到，则删除
 - **update_queue_goods_check.py** - 清理队列，其中值在tb_goods_basic中不存在，则移除。清理数据是大量更新basicId，无效id阻塞队列
 - **switch_es.py** - 切换站点es, 步骤如下：
   1. 通过接口更新两台es-canal服务中站点es映射map. 最新数据变动更新至切换后的es中，此时站点es还是旧的，且不在实时变动；
   2. 更新escanal监听的主表数据，触发更新es任务，将最新数据写入目标es；
   3. 运费和价格es在独立系统中，通过指定esClient，调用接口将站点最新价格及运费同步到es中；
   