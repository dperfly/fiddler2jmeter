import sys
import os
import re
import time
import html
import json
import zipfile

from urllib.parse import urlsplit, unquote
from optparse import OptionParser

Pyqt5_install = True
try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
except:
    Pyqt5_install = False


class DataClean:
    def __init__(self, jmeter_datas):
        self.jmeter_datas = jmeter_datas

    def select_jmeter_data(self, host_name=None, filter_url=None, distinct=False):
        '''
        数据清洗,得到想要的数据
        :param host_name: HOST regexp匹配
        :param filter_url: 需要去除的url
        eg：/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$   ----> 过滤css|ico|jpg|png|gif|bmp|wav|js|jpe
         :param distinct : distinct
        :return: select_jmeter_data
        '''
        select_jmeter_data = []
        for i, jmeter_data in enumerate(self.jmeter_datas):
            # host 包含在给的的hosts中且不为空,url正则匹配满足
            try:
                if jmeter_data['server_name'] is not None \
                        and re.match(host_name, jmeter_data['server_name'], re.IGNORECASE) is not None \
                        and re.match(filter_url, jmeter_data['path'], re.IGNORECASE) is None:

                    # distinct
                    if distinct and len(select_jmeter_data) > 0:
                        distinct_list = [f"{i['server_name']}{i['path']}" for i in select_jmeter_data]
                        if f"{jmeter_data['server_name']}{jmeter_data['path']}" in distinct_list:
                            continue

                    select_jmeter_data.append(jmeter_data)
            except Exception as e:
                print('regex problem :\nhostname: {} \nfilter_url: {}'.format(host_name, filter_url))

        return select_jmeter_data

    def get_header_parameter(self, select_jmeter_data, host_name=None):
        '''
        re.match(host_name, jmeter_data['server_name'], re.IGNORECASE) is not None
        提取公共的header
        :param select_jmeter_data: 数据集合
        :param host_name: 域名
        :return:
        '''
        # 获取一条数据进行交集计算
        header_parameter = set()
        if host_name is not None:
            for i in range(len(select_jmeter_data) - 1):
                # print(select_jmeter_data[i]['Header'][0])
                if re.match(host_name, select_jmeter_data[i]['Header'][0][1], re.IGNORECASE) is not None:
                    header_parameter = set(select_jmeter_data[i]['Header'])
                    break
        else:
            header_parameter = select_jmeter_data[0]['Header']

        # header交集计算
        for i in range(len(select_jmeter_data) - 1):
            if select_jmeter_data[i]['Header'] in [('Host', host_name)]:
                header_parameter = header_parameter & set(select_jmeter_data[i + 1]['Header'])
        return header_parameter


class Reader:
    def _set_request_line(self, request_line):
        '''
        设置请求头request line的值到http_request_dict
        :param request_line:
        eg:
            GET https://www.eg.com:8080/search?a=1&b=2 HTTP/1.1
            GET /search?a=1&b=2 HTTP/1.1
        :return:
        eg:
            http_requset_dict = {
                                    'server_name': www.eg.com,
                                    'port_number': 8080,
                                    'protocol_http': https,
                                    'path': /search?a=1&b=2,
                                    'method': GET,
                                }
        '''
        http_requset_dict = {
            'server_name': "",
            'port_number': "",
            'protocol_http': "",
            'path': "",
            'method': "",
        }
        request_line = re.findall("(.*) (.*) (.*)", request_line)[0]
        if len(request_line) == 3:
            method, url, http = request_line
            url_split = urlsplit(url)

            path = str(url_split.path) if str(url_split.query) == '' else str(url_split.path) + "?" + str(
                url_split.query)  # path = /index.html?a=10&b=20 or /index.html

            http_requset_dict['server_name'] = html.escape(
                str(url_split.hostname)) if url_split.hostname is not None else ""

            http_requset_dict['path'] = html.escape(str(path)) if path is not None else ""

            http_requset_dict['protocol_http'] = html.escape(
                str(url_split.scheme)) if url_split.scheme is not None else "http"

            http_requset_dict['port_number'] = html.escape(str(url_split.port)) if url_split.port is not None else ""

            http_requset_dict['method'] = method

            return http_requset_dict
        else:
            Exception("http request line is not divided into three parts , please check")


# fiddler 数据处理
class FiddlerReader(Reader):
    def __init__(self, saz_file_path):
        if saz_file_path is None:
            raise Exception("saz文件未指定")
        self.saz_file_path = saz_file_path
        self.zipfile_obj = zipfile.ZipFile(self.saz_file_path)

    def __get_fiddler_c(self):
        '''
        获取请求头request数据 文件名集合
        :return:
        '''
        name_list = self.zipfile_obj.namelist()
        c_name_lists = (i for i in name_list if '_c.txt' in i)
        return c_name_lists

    def __get_fiddler_s(self):
        '''
        获取响应response数据 文件名集合
        :return:
        '''
        name_list = self.zipfile_obj.namelist()
        s_name_list = (i for i in name_list if '_s.txt' in i)
        return s_name_list

    def __read_zip_txt(self, txt_path_name):
        return self.zipfile_obj.open(txt_path_name).readlines()

    def get_jmeter_data(self):
        '''
        将所有fiddler.saz 文件转换成list文件存储
        :return:
        '''
        data = []
        txt_path_names = self.__get_fiddler_c()
        while True:
            try:
                path_name = next(txt_path_names)
                request_line_dict = self.get_request_line_dict(path_name)
                data.append(request_line_dict)
            except StopIteration:
                break
        return data

    def get_request_line_dict(self, txt_path_name):
        '''
        获取单个文件转换成HTTP request 字典
        :param txt_path_name: 压缩包内的文件路径 /path
        eg:
            /raw/001_c.txt
        :return:返回url参数字典
        eg:
            {
                'server_name': 'www.baidu.com',
                'port_number': 80,
                'protocol_http': 'http',
                'encoding': None,
                'path': '/index.html?a=10&b=20',
                'method': 'GET',
                'follow_redirects': True,
                'auto_redirects': False,
                'use_keep_alive': True,
                'DO_MULTIPART_POST': False,
                'post_value': ''
            }
        '''
        is_data = False
        is_header_first = True
        http_dict = {
            'server_name': None,
            'port_number': None,
            'protocol_http': None,
            'encoding': None,
            'path': None,
            'method': None,
            'follow_redirects': True,
            'auto_redirects': False,
            'use_keep_alive': True,
            'DO_MULTIPART_POST': False,
            'post_value': None,
            'Cookie': None,
            'Header': []
        }
        http_value = ''
        request_data = list(self.__read_zip_txt(txt_path_name))
        if "CONNECT" in str(request_data[0]):
            pass
        else:
            for header in request_data:
                #  去除
                #       ^b'(.*)'$ ---> b\'\'
                #       \r\n ----> ''
                s = str(header).replace(r'\r\n', '')
                try:
                    s = re.findall("^b\'(.*)\'", s)[0]
                except Exception as e:
                    print(e)
                    continue
                # method uri version row
                if is_header_first is True:
                    request_line_dict = self._set_request_line(s)
                    http_dict.update(request_line_dict)
                    is_header_first = False
                else:
                    # space row
                    if s == '' or None:
                        is_data = True
                    # header row
                    if ': ' in s and is_data is False:
                        # Get request header
                        lists = re.findall("^(.*): (.*)$", s)

                        # TODO The cookie is directly stored in the header manger
                        # if lists[0][0] == 'Cookie':
                        #    pass

                        http_dict['Header'].append((lists[0][0], html.escape(lists[0][1])))
                    else:
                        http_value += s
            http_dict['post_value'] = html.escape(str(http_value))
        return http_dict


# fiddler script 数据处理
class FiddlerScriptReader(Reader):
    def __init__(self, args):
        self.url_data_lists = [unquote(i).split("\n") for i in args]

    def get_jmeter_data(self):
        return [self.get_request_line_dict(request_data) for request_data in self.url_data_lists]

    def get_request_line_dict(self, request_data):
        is_data = False
        is_header_first = True
        http_dict = {
            'server_name': None,
            'port_number': None,
            'protocol_http': None,
            'encoding': None,
            'path': None,
            'method': None,
            'follow_redirects': True,
            'auto_redirects': False,
            'use_keep_alive': True,
            'DO_MULTIPART_POST': False,
            'post_value': None,
            'Cookie': None,
            'Header': []
        }
        http_value = ''
        if "CONNECT" in str(request_data[0]):
            pass
        else:
            for s in request_data:
                # method uri version row
                if is_header_first is True:
                    request_line_dict = self._set_request_line(s)
                    http_dict.update(request_line_dict)
                    is_header_first = False
                else:
                    # space row
                    if s == '' or None:
                        is_data = True
                    # header row
                    if ': ' in s and is_data is False:
                        # Get request header
                        lists = re.findall("^(.*): (.*)$", s)

                        if lists[0][0] == "Host":
                            http_dict["server_name"] = str(lists[0][1]).strip()

                        # TODO The cookie is directly stored in the header manger
                        # if lists[0][0] == 'Cookie':
                        #    pass

                        http_dict['Header'].append((str(lists[0][0]).strip(), html.escape(str(lists[0][1]).strip())))
                    else:

                        http_value += s
            http_dict['post_value'] = html.escape(str(http_value))
        return http_dict


# Charles data
class CharlesReader(Reader):
    def __init__(self, chls_file_path):
        self.chls_file_path = chls_file_path

    def __get_charles_data(self):
        if self.chls_file_path is None and str(self.chls_file_path).endswith(".chlsj"):
            raise Exception("Chls file is not specified or is not in chlsj format")
        data = json.load(open(self.chls_file_path, encoding='utf-8'))
        return data

    def __get_charles_request_body(self, request: dict):
        if "body" in request.keys():
            return request['body']['text']
        else:
            return None

    def get_jmeter_data(self):
        '''
        获取charles的数据，默认去掉connect
        :return: [{},{}...]
        '''
        charles_data = self.__get_charles_data()
        jmeter_data = []
        for data in charles_data:
            if str(data['method']).lower() == 'connect' or str(data['protocolVersion']) == 'HTTP/2.0':
                # TODO  charles to jmeter：Unsupported request type : http/2.0 ,Automatic filtering
                continue
            else:
                try:
                    request_data = data['request']
                    headers = request_data['header']['headers']
                    first_line = request_data['header']['firstLine']
                    http_dict = {
                        'server_name': data['host'] if data['host'] != '' else None,
                        'port_number': data['actualPort'] if data['actualPort'] != '' else None,
                        'protocol_http': data['scheme'] if data['scheme'] != '' else None,
                        'encoding': None,
                        'path': self._set_request_line(first_line)['path'],
                        'method': data['method'] if data['method'] != '' else None,
                        'follow_redirects': True,
                        'auto_redirects': False,
                        'use_keep_alive': True,
                        'DO_MULTIPART_POST': False,
                        'post_value': self.__get_charles_request_body(request_data),
                        'Cookie': None,
                        'Header': [(i['name'], html.escape(i['value'])) for i in headers]
                    }
                    jmeter_data.append(http_dict)
                except Exception as e:
                    print("Error:{}".format(e))
                    continue
        return jmeter_data


class JmeterTemplate:
    def __init__(self):
        '''
        Jmx model
        '''
        self.temp = '''<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="4.0" jmeter="4.0 r1823414">
<hashTree>
    {test_plan}
    <hashTree>
    {thread_group}
    <hashTree>
            <ConstantTimer guiclass="ConstantTimerGui" testclass="ConstantTimer" testname="Constant Timer" enabled="true">
                <stringProp name="ConstantTimer.delay">1000</stringProp>
            </ConstantTimer>
            <hashTree/>
            {header_manager}
            <CookieManager guiclass="CookiePanel" testclass="CookieManager" testname="HTTP Cookie Manager" enabled="true">
                <collectionProp name="CookieManager.cookies"/>
                <boolProp name="CookieManager.clearEachIteration">false</boolProp>
            </CookieManager>
            <hashTree/>
            <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="View Results Tree" enabled="true">
              <boolProp name="ResultCollector.error_logging">false</boolProp>
              <objProp>
                <name>saveConfig</name>
                <value class="SampleSaveConfiguration">
                  <time>true</time>
                  <latency>true</latency>
                  <timestamp>true</timestamp>
                  <success>true</success>
                  <label>true</label>
                  <code>true</code>
                  <message>true</message>
                  <threadName>true</threadName>
                  <dataType>true</dataType>
                  <encoding>false</encoding>
                  <assertions>true</assertions>
                  <subresults>true</subresults>
                  <responseData>true</responseData>
                  <samplerData>true</samplerData>
                  <xml>true</xml>
                  <fieldNames>true</fieldNames>
                  <responseHeaders>true</responseHeaders>
                  <requestHeaders>true</requestHeaders>
                  <responseDataOnError>false</responseDataOnError>
                  <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                  <assertionsResultsToSave>0</assertionsResultsToSave>
                  <bytes>true</bytes>
                  <sentBytes>true</sentBytes>
                  <url>true</url>
                  <fileName>true</fileName>
                  <hostname>true</hostname>
                  <threadCounts>true</threadCounts>
                  <sampleCount>true</sampleCount>
                  <idleTime>true</idleTime>
                  <connectTime>true</connectTime>
                </value>
              </objProp>
              <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
            <ResultCollector guiclass="SummaryReport" testclass="ResultCollector" testname="Summary Report" enabled="true">
              <boolProp name="ResultCollector.error_logging">false</boolProp>
              <objProp>
                <name>saveConfig</name>
                <value class="SampleSaveConfiguration">
                  <time>true</time>
                  <latency>true</latency>
                  <timestamp>true</timestamp>
                  <success>true</success>
                  <label>true</label>
                  <code>true</code>
                  <message>true</message>
                  <threadName>true</threadName>
                  <dataType>true</dataType>
                  <encoding>false</encoding>
                  <assertions>true</assertions>
                  <subresults>true</subresults>
                  <responseData>true</responseData>
                  <samplerData>true</samplerData>
                  <xml>true</xml>
                  <fieldNames>true</fieldNames>
                  <responseHeaders>true</responseHeaders>
                  <requestHeaders>true</requestHeaders>
                  <responseDataOnError>false</responseDataOnError>
                  <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                  <assertionsResultsToSave>0</assertionsResultsToSave>
                  <bytes>true</bytes>
                  <sentBytes>true</sentBytes>
                  <url>true</url>
                  <fileName>true</fileName>
                  <hostname>true</hostname>
                  <threadCounts>true</threadCounts>
                  <sampleCount>true</sampleCount>
                  <idleTime>true</idleTime>
                  <connectTime>true</connectTime>
                </value>
              </objProp>
              <stringProp name="filename"></stringProp>
            </ResultCollector>
            <hashTree/>
            {sample_data_list}
        </hashTree>
    </hashTree>
</hashTree>
</jmeterTestPlan>
'''
        self.thread_group = '''<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="FiddlerToJmeter" enabled="true">
<stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
<elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
  <boolProp name="LoopController.continue_forever">false</boolProp>
  <stringProp name="LoopController.loops">1</stringProp>
</elementProp>
<stringProp name="ThreadGroup.num_threads">1</stringProp>
<stringProp name="ThreadGroup.ramp_time">1</stringProp>
<boolProp name="ThreadGroup.scheduler">false</boolProp>
<stringProp name="ThreadGroup.duration"></stringProp>
<stringProp name="ThreadGroup.delay"></stringProp>
</ThreadGroup>
'''
        self.get_sampler = '''<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{server_name}{path}" enabled="true">
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
  <stringProp name="HTTPSampler.domain">{server_name}</stringProp>
  <stringProp name="HTTPSampler.port">{port_number}</stringProp>
  <stringProp name="HTTPSampler.protocol">{protocol_http}</stringProp>
  <stringProp name="HTTPSampler.contentEncoding">{encoding}</stringProp>
  <stringProp name="HTTPSampler.path">{path}</stringProp>
  <stringProp name="HTTPSampler.method">{method}</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">{follow_redirects}</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">{auto_redirects}</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">{use_keep_alive}</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">{DO_MULTIPART_POST}</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
</HTTPSamplerProxy>
'''
        self.post_sampler = '''<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{server_name}{path}" enabled="true">
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <boolProp name="HTTPArgument.always_encode">false</boolProp>
        <stringProp name="Argument.value">{post_value}</stringProp>
        <stringProp name="Argument.metadata">=</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
  <stringProp name="HTTPSampler.domain">{server_name}</stringProp>
  <stringProp name="HTTPSampler.port">{port_number}</stringProp>
  <stringProp name="HTTPSampler.protocol">{protocol_http}</stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path">{path}</stringProp>
  <stringProp name="HTTPSampler.method">{method}</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">{follow_redirects}</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">{auto_redirects}</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">{use_keep_alive}</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">{DO_MULTIPART_POST}</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
</HTTPSamplerProxy>
'''
        self.test_plan = '''<TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Test Plan" enabled="true">
  <stringProp name="TestPlan.comments"></stringProp>
  <boolProp name="TestPlan.functional_mode">false</boolProp>
  <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
  <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
  <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
    <collectionProp name="Arguments.arguments">
    {test_plan_value}
    </collectionProp>
  </elementProp>
  <stringProp name="TestPlan.user_define_classpath"></stringProp>
</TestPlan>
'''
        self.test_plan_value = '''<elementProp name="{domain}" elementType="Argument">
    <stringProp name="Argument.name">{domain}</stringProp>
    <stringProp name="Argument.value">{domain_value}</stringProp>
    <stringProp name="Argument.metadata">=</stringProp>
  </elementProp>
'''
        self.header_manager = '''<HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager" enabled="true">
  <collectionProp name="HeaderManager.headers">
    {header_manager_value}
  </collectionProp>
</HeaderManager>
<hashTree/> 
        '''
        self.header_manager_value = '''<elementProp name="" elementType="Header">
  <stringProp name="Header.name">{header_name}</stringProp>
  <stringProp name="Header.value">{header_value}</stringProp>
</elementProp>
'''


# jmeter script组装类
class JmeterWriter(JmeterTemplate):
    def __set_header_manager(self, header_manager, type):
        '''
        组装header manager
        :param header_manager: []list集合
        :param type: public：公共部分的header manager
                    private：单个http sample中的header manager
        :return: xml header manager string
        '''
        if header_manager is None or '':
            print("http header is None")
            return ''

        # 组装 header manager
        jmx_header_manager = self.header_manager
        header_manager_values = ''
        for i in header_manager:
            header_manager_values = header_manager_values + (
                self.header_manager_value.format(header_name=i[0], header_value=i[1]))
        jmx_header_manager = jmx_header_manager.format(header_manager_value=header_manager_values)

        # 如果是public 则是总的公共部分的header manager
        # 如果不是public 则是每个http sample中的header manager
        if str(type).lower() == 'public':
            return jmx_header_manager
        else:
            return "<hashTree>" + jmx_header_manager + "</hashTree>"

    def __set_request(self, select_data, public_header):
        '''
        组装 request 部分
        :param select_data: http数据list
        :param public_header: 公共的header
        :return: 组装好的 jmeter script http sample部分
        '''
        _, domain = self.__set_test_plan(select_data)
        all_request = ''
        for request_data in select_data:
            # get
            if request_data['method'].lower() == 'get':
                all_request = all_request + self.get_sampler.format(
                    server_name="${" + str(domain[request_data['server_name']]) + "}",  # setting domain,
                    port_number=request_data['port_number'] or '',
                    protocol_http=request_data['protocol_http'] or 'http',
                    encoding=request_data['encoding'] or '',
                    path=request_data['path'] or '',
                    method=request_data['method'] or '',
                    follow_redirects=request_data['follow_redirects'] or 'True',
                    auto_redirects=request_data['auto_redirects'] or 'False',
                    use_keep_alive=request_data['use_keep_alive'] or 'True',
                    DO_MULTIPART_POST=request_data['DO_MULTIPART_POST'] or 'False',
                )
            # post
            else:
                all_request = all_request + self.post_sampler.format(
                    post_value=request_data['post_value'] or '',
                    server_name="${" + str(domain[request_data['server_name']]) + "}",  # setting domain
                    port_number=request_data['port_number'] or '',
                    protocol_http=request_data['protocol_http'] or 'http',
                    encoding=request_data['encoding'] or '',
                    path=request_data['path'] or '',
                    method=request_data['method'] or '',
                    follow_redirects=request_data['follow_redirects'] or 'True',
                    auto_redirects=request_data['auto_redirects'] or 'False',
                    use_keep_alive=request_data['use_keep_alive'] or 'True',
                    DO_MULTIPART_POST=request_data['DO_MULTIPART_POST'] or 'False',
                )
            # else:
            #     print('Unsupported request type，method : {}'.format(request_data['method'].lower()))
            # 设置不同地方的header内容
            difference_header = list(set(request_data['Header']).difference(set(public_header)))
            all_request = all_request + self.__set_header_manager(difference_header, 'private')
        return all_request

    def __set_test_plan(self, select_data):
        '''
        组装test plan部分，设置domain 后续进行${domain}参数化
        :param select_data:
        :return: jmeter script test plan xml str,
                domain list
        '''
        test_plan_domain_value = ''
        domain = {}
        i = 1
        for data in select_data:
            if data['server_name'] not in domain.keys():
                test_plan_domain_value = test_plan_domain_value + self.test_plan_value.format(
                    domain_value=data['server_name'],
                    domain="domian" + str(i))
                domain[data['server_name']] = "domian" + str(i)
                i = i + 1
        return self.test_plan.format(test_plan_value=test_plan_domain_value), domain

    def get_jmeter_script(self, select_data, public_header_manager):
        '''
        :param select_data:
        :param public_header_manager:
        :return:
        '''
        return self.temp.format(
            test_plan=self.__set_test_plan(select_data)[0],
            thread_group=self.thread_group,
            sample_data_list=self.__set_request(select_data, public_header_manager),
            header_manager=self.__set_header_manager(public_header_manager, 'public'))


def run(file_path, filter_url, host_name, output_jmxScript, distinct, args=None):
    # filter_url = R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$"
    # host_name = R'^livetv\.sx$'
    if file_path == "" and args is None:
        return 'input file path cannot be empty'
    if output_jmxScript == "":
        return 'output_jmxScript cannot be empty'
    if host_name == "" or None:
        host_name = R"^.*$"
    if filter_url == "":
        return 'filter_url cannot be empty'

    # fix drag file bug
    if file_path is not None and file_path.startswith('file:/'):
        file_path = file_path[6:]
    if file_path is not None and file_path.startswith('//'):
        file_path = file_path[2:]
    if output_jmxScript.startswith('file:/'):
        output_jmxScript = output_jmxScript[6:]
    if output_jmxScript.startswith('//'):
        output_jmxScript = output_jmxScript[2:]

    if file_path is None and args is not None:
        f = FiddlerScriptReader(args)
    elif file_path.endswith(".saz"):
        f = FiddlerReader(file_path)
    elif file_path.endswith(".chlsj"):
        f = CharlesReader(file_path)
    else:
        return f"The imported file does not exist or has an unsupported suffix:{file_path}." \
               f"\nCurrently, Fiddler file only supports SAZ format and Charles only supports chlsj format"

    jmeter_data = f.get_jmeter_data()
    clear = DataClean(jmeter_data)
    select_data = clear.select_jmeter_data(host_name, filter_url, distinct)
    public_header_manager = clear.get_header_parameter(select_data, host_name)
    jw = JmeterWriter()
    jmx_script = jw.get_jmeter_script(select_data, public_header_manager)

    with open(output_jmxScript, 'w', encoding='utf-8') as o:
        o.write(str(jmx_script))

    return f"run success,jmx file saved in : {output_jmxScript}\njmx content：\n\n{jmx_script}"


# ===================================================GUI===================================================

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("FiddlerCharles2Jmeter")
        MainWindow.resize(800, 521)
        MainWindow.setWindowTitle("Fiddler or Charles Convert to jmeter Script")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.cmd_result = QtWidgets.QTextEdit(self.centralwidget)
        self.cmd_result.setGeometry(QtCore.QRect(10, 240, 781, 251))
        self.cmd_result.setObjectName("cmd_result")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 779, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 240, 16))
        self.label_3.setObjectName("label_3")
        self.select_input_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.select_input_textEdit.setGeometry(QtCore.QRect(250, 10, 440, 31))
        self.select_input_textEdit.setObjectName("select_input_textEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 240, 16))
        self.label_4.setObjectName("label_4")
        self.select_output_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.select_output_textEdit.setGeometry(QtCore.QRect(250, 60, 440, 31))
        self.select_output_textEdit.setObjectName("select_output_textEdit")

        self.select_distinct_path = QtWidgets.QCheckBox(self.centralwidget)
        self.select_distinct_path.setGeometry(QtCore.QRect(250, 193, 30, 35))
        self.select_distinct_path.setObjectName("select_distinct")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(270, 205, 440, 15))
        self.label_5.setObjectName("label_5")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 170, 151, 16))
        self.label_2.setObjectName("label_2")
        self.host_name_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.host_name_textEdit.setGeometry(QtCore.QRect(250, 120, 440, 31))
        self.host_name_textEdit.setObjectName("host_name_textEdit")
        self.filter_url_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.filter_url_textEdit.setGeometry(QtCore.QRect(250, 160, 440, 31))
        self.filter_url_textEdit.setObjectName("filter_url_textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 130, 240, 16))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 100, 801, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 220, 801, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(700, 130, 75, 51))
        self.run.setObjectName("run")
        self.select_input_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_input_btn.setGeometry(QtCore.QRect(700, 10, 75, 31))
        self.select_input_btn.setObjectName("select_input_btn")

        self.select_output_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_output_btn.setGeometry(QtCore.QRect(700, 60, 75, 31))
        self.select_output_btn.setObjectName("select_output_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_fiddler = QtWidgets.QAction(MainWindow)
        self.action_fiddler.setCheckable(True)
        self.action_fiddler.setObjectName("action_fiddler")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setCheckable(True)
        self.action_3.setObjectName("action_3")
        self.action_jmeter_4_0 = QtWidgets.QAction(MainWindow)
        self.action_jmeter_4_0.setCheckable(True)
        self.action_jmeter_4_0.setObjectName("action_jmeter_4_0")
        self.menu.addAction(self.action_fiddler)
        self.menu.addAction(self.action_3)
        self.menu.addSeparator()
        self.menu.addAction(self.action_jmeter_4_0)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.select_input_btn.clicked.connect(self.select_input_file)
        self.select_output_btn.clicked.connect(self.select_output_file)
        self.filter_url_textEdit.setText(R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$")
        self.host_name_textEdit.setText(R"^.*$")
        self.run.clicked.connect(self.run_script)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* input Fiddler/Charles file</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* output jmx file</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\">* Filter url(regex)</span></p></body></html>"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:10pt;\">* Filter host name(regex)</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:10pt;\"> distinct(Exactly the same url address)</span></p></body></html>"))
        self.run.setText(_translate("MainWindow", "RUN"))
        self.select_input_btn.setText(_translate("MainWindow", "select"))
        self.select_output_btn.setText(_translate("MainWindow", "select"))

        # self.menu.setTitle(_translate("MainWindow", "文件"))
        # self.action_fiddler.setText(_translate("MainWindow", "导入Fiddler文件"))
        # self.action_fiddler.setChecked(True)
        # self.action_3.setText(_translate("MainWindow", "导入Charles文件(暂不支持)"))
        # self.action_3.setChecked(False)
        # self.action_jmeter_4_0.setText(_translate("MainWindow", "导出jmeter 4.0脚本"))
        # self.action_jmeter_4_0.setChecked(True)

    def select_input_file(self):
        openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', '')
        self.select_input_textEdit.setText(openfile_name[0])

    def select_output_file(self):
        openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', '')
        self.select_output_textEdit.setText(openfile_name[0])

    def run_script(self):
        filter_url = self.filter_url_textEdit.toPlainText()
        host_name = self.host_name_textEdit.toPlainText()
        input_file = self.select_input_textEdit.toPlainText()
        output_file = self.select_output_textEdit.toPlainText()
        is_distinct = self.select_distinct_path.isChecked()
        result = run(file_path=input_file, filter_url=filter_url, host_name=host_name,
                     output_jmxScript=output_file, distinct=is_distinct)
        self.cmd_result.setText(result)


def runGui():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# ===================================================GUI===================================================


if __name__ == '__main__':
    # cmd run
    optParser = OptionParser(
        usage="Generate JMeter script command example:\n\n\tFiddlerCharles2Jmeter.py -n -i fiddler/charles_file_path -o jmeter_script_file_path --filter-host-name='' --filter_url='' --distinct")

    optParser.add_option("-n",
                         "--no_gui",
                         action='store_true',
                         default=False,
                         dest='no_gui',
                         help="no gui model"
                         )
    optParser.add_option("-i",
                         "--input_file_path",
                         action='store',
                         type='string',
                         dest='input_file_path',
                         help="fiddler/charles_file_path"
                         )
    optParser.add_option("-o",
                         "--output_file_path",
                         action='store',
                         type='string',
                         dest='output_jmxScript',
                         help="jmeter_script_file_path "
                         )
    optParser.add_option("-u",
                         "--filter_url",
                         action='store',
                         type='string',
                         dest='filter_url',
                         default="\n" + R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$",
                         help="filter_url regex default=%default%"
                         )
    optParser.add_option("-f",
                         "--filter-host-name",
                         action='store',
                         type='string',
                         dest='host_name',
                         default=R"^.*$",
                         help="filter-host-name regex default=%default"
                         )
    optParser.add_option("-d",
                         "--distinct",
                         action='store_false',
                         dest='distinct',
                         default=False,
                         help="distinct: Filter duplicate requests , default=%default"
                         )
    # is fiddler4 client run
    optParser.add_option("-s",
                         "--is-fiddler-script-model",
                         action='store_true',
                         default=False,
                         dest='fiddler_script_model',
                         help="fiddler script model :default=%default"
                         )
    (option, args) = optParser.parse_args()

    if option.no_gui is False:
        # GUI model run
        if not Pyqt5_install:
            print(
                "Warning: Please install pyqt5:\n\tpip install PyQt5 -i https://pypi.douban.com/simple\n"
                "or run in no-gui mode:\n\tView help documentation: fiddler2jmeter_start.py -h")
        else:
            runGui()
    else:
        if option.input_file_path is None and option.fiddler_script_model is False:
            print("fiddler or Charles not found")
            exit(-1)
        if option.output_jmxScript is None:
            print("output_jmxScript not found")
            exit(-1)

        input_file_path = option.input_file_path
        host_name = option.host_name
        filter_url = option.filter_url
        output_jmxScript = option.output_jmxScript
        distinct = option.distinct

        if option.input_file_path is not None and not os.path.isabs(input_file_path):
            input_file_path = os.path.abspath(os.path.dirname(input_file_path))
            if not os.path.isfile(input_file_path):
                print("input_file_path is not found. "
                      "Check whether there are special characters, such as special spaces..."
                      f"\nerror path: {os.path.dirname(output_jmxScript)}")
                exit(-1)
        if not os.path.isabs(output_jmxScript):
            output_jmxScript = os.path.join(os.getcwd(), output_jmxScript)
            if not os.path.isdir(os.path.dirname(output_jmxScript)):
                print(os.path.dirname(output_jmxScript))
                print("output_file_path the current directory is not a folder. "
                      "Check whether there are special characters, such as special spaces..."
                      f"\nerror path: {os.path.dirname(output_jmxScript)}")
                exit(-1)

        run(input_file_path, filter_url, host_name, output_jmxScript, distinct, args)

        print(f"run success,jmx file saved in : {output_jmxScript}")

        # View results
        if option.fiddler_script_model is True:
            time.sleep(3)
