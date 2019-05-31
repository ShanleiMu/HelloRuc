# HelloRuc
本项目为中国人民大学19学年春季学期《智能信息检索》课程大作业，小组成员共同私有，只用于本课程。

## 程序运行说明
**运行环境**
- python3.6
- jieba分词组件 `pip install jieba`

**模块介绍**
- `data/` 存储相关数据
- `build_index/` 数据清洗和建立倒排索引程序
- `spider/` 存储爬虫程序
- `search_engine/` 存储搜索相关功能程序
- `web/` 存储前端程序
- `config.ini` 为配置文件

**运行说明**
1) 下载`ruc_content.txt`文件，放到`data/processed_data/`目录下。
2) 执行`build_index/build_index.py`生成倒排索引
3) 执行`main.py`

## 程序添加说明
其他功能请将相关类和方法写在一个py文件并放到`search_engine`目录，在main.py测试程序