# 项目名称：fiddler 或 Charles 文件转换为 jmeter脚本

解决脚本录制问题,可以将fiddler或Charles转换成对应的jmeter脚本,实现部分内容的参数化配置

## 操作步骤
1.1 打开Fiddler录制请求<br>
![Image text](img/img_01.jpg)<br>
1.2 将需要的HTTP请求或数据保存为saz文件<br>
![Image text](img/img_02.jpg)<br>
1.3 执行脚本<br>
1.3.1 参数说明<br>
1.3.1.1 需要导入的文件：saz文件（fiddler到处的文件）<br>
1.3.1.2 需要到处的文件：jmx文件（生成的jmeter脚本文件）<br>
1.3.1.3 过滤Http请求：不满足host则过滤，为正则匹配方式<br>
1.3.1.4 过滤Http请求，通过/path部分，满足则过滤，为正则匹配方式<br>
1.3.2 页面效果<br>
![Image text](img/img_03.jpg)<br>
1.3.3 结果展示<br>
![Image text](img/img_04.jpg)<br>
1.4 jmeter运行结果<br>
![Image text](img/img_05.jpg)<br>

## TODO
1.目前只支持get和post请求<br>
2.jmeter低版本暂不支持,目前导出的脚本是jmeter4.0<br>
3.Charles脚本暂未支持<br>
