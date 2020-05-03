###项目名称：fiddler 或 Charles 文件转换为 jmeter脚本

####1.操作步骤
#####1.1 打开Fiddler录制请求
![Image text](img/img_01.jpg)
#####1.2 将需要的HTTP请求或数据保存为saz文件
![Image text](img/img_02.jpg)
#####1.3 执行脚本
#####1.3.1 参数说明
######1.3.1.1 需要导入的文件：saz文件（fiddler到处的文件）
######1.3.1.2 需要到处的文件：jmx文件（生成的jmeter脚本文件）
######1.3.1.3 过滤Http请求：不满足host则过滤，为正则匹配方式
######1.3.1.4 过滤Http请求，通过/path部分，满足则过滤，为正则匹配方式

#####1.3.2 页面效果
![Image text](img/img_03.jpg)
#####1.3.3 结果展示
![Image text](img/img_04.jpg)
#####1.4 jmeter运行结果
![Image text](img/img_05.jpg)

####2.TODO
#####1.目前只支持get和post请求
#####2.jmeter低版本暂不支持,目前导出的脚本是jmeter4.0
#####3.Charles脚本暂未支持