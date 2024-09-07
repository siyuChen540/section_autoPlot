# section_autoPlot
自动绘制科学考察航测站点图，基于模板excel生成
excel模板(*.xlsx)：
| 站点名称 | 经度(度) | 经度(分) | 纬度(度) | 纬度(分) | 站点类型 | 站点编号 | 站点状态 | 
| --- | --- | --- | --- | --- | --- |               

运行环境：python3.8

运行方式：
```
python main.py
```

运行后，程序会自动打开excel模板，根据输入的站点信息自动生成相应的站点图。

生成的站点图保存在当前目录中的marineRsearch.png文件中。

注意：
1. 程序运行前请先安装所需依赖包，运行`pip install -r requirements.txt`命令安装。
2. 程序运行前请先将excel模板文件名修改为`station_info.xlsx`。   
3. 程序运行前请先将模板文件放置在程序所在目录下。   
4. 程序运行前请先将模板文件中的数据格式正确。   
5. 程序运行前请先将模板文件中的数据按站点名称排序。   

结果实例：
![marineRsearch.png](marineRsearch.png)