# Data文件介绍
- `raw_data` 存储未经处理的数据，每一个网站的数据存在一个文件
- `distinct_data` 存储去重后的数据，每一个网站去重后的数据存储在一个文件
- `processed_data` 存储清洗后的数据，`ruc_content.txt` 记录了所有清洗后的数据，以`id|||标题|||时间|||url|||内容`格式存储，
其中id前三位为网站id，后四位为该网站下的数据id
- `department2index.txt` 网站id和网站名称对应表
- `stop_words.txt` 停用词表


