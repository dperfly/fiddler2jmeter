# Fiddler or Charles to Jmeter Script
![Image text](img/img_06.png)<br>
To solve the problem of script recording , you can convert Fiddler or Charles into the corresponding Jmeter script to realize the parameterization of partial content. By modifying some parameters or parameterization can perform automation test or simple stress test for the interface of HTTP protocol.<br>

Chinese documents(中文文档)：https://www.cnblogs.com/fbyyx/p/12827415.html

## Steps
1.1 Open Fiddler/Charles to record the request<br>
1.1.1 Recording Fiddler<br>
![Image text](img/img_01.jpg)<br>
1.1.2 Recording Charles<br>
![Image text](img/img_08.jpg)<br>
1.2 Export needed HTTP request<br>
1.2.1 Export Fiddler recording as saz format<br>
![Image text](img/img_02.jpg)<br>
1.2.1 Export Charles recording as chlsj format<br>
![Image text](img/img_07.jpg)<br>
1.3 Execute script<br>
1.3.1 Parameter elucidation<br>
1.3.1.1 Files to import: saz files(Fiddler files), chlsi files(Charles files)<br>
1.3.1.2 Files to export: jmx files(Generated Jmeter script file)<br>
1.3.1.3 Filter HTTP request: regex mode<br>
1.3.2 Page effect<br>
![Image text](img/img_03.jpg)<br>
1.3.3 Conversion results<br>
![Image text](img/img_04.jpg)<br>
1.4 Run JMeter results<br>
![Image text](img/img_05.jpg)<br>
## Remarks
1.Ignore data with method connect.<br>
2.Only Windows systems are supported.<br>
3.Only GET and POST requests are supported.<br>
4.JMeter version greater than 4.0 is required.<br>
5.Charles doesn't support http2.0 conversion, so it's filtered out directly.<br>

## TODO
1.Support for Charles other file formats<br>
2.Run as a fiddler plug-in with FiddlerScript<br>


## ENV
```buildoutcfg
python >=  3.6  
PyQt5  ==  5.15.2
```

## Contact Information
1.Issues.<br>
2.WeChat ID:dongpengfei826153155<br>
3.E-mail: dongpengfei826153155@gmail.com<br>

