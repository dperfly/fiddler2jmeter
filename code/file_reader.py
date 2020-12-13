import zipfile
import re
import html
import json
from urllib.parse import urlsplit


class Reader:
    def _set_request_line(self, request_line):
        '''
        设置请求头request line的值到http_request_dict
        :param request_line:
        eg:
            GET https://www.eg.com:8080/search?a=1&b=2 HTTP/1.1
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
            'server_name': None,
            'port_number': None,
            'protocol_http': None,
            'path': None,
            'method': None,
        }
        request_line = re.findall("(.*) (.*) (.*)", request_line)[0]
        if len(request_line) == 3:
            method, url, http = request_line
            url_split = urlsplit(url)

            path = str(url_split.path) if str(url_split.query) == '' else str(url_split.path) + "?" + str(
                url_split.query)  # path = /index.html?a=10&b=20 or /index.html

            http_requset_dict['server_name'] = html.escape(str(url_split.hostname))
            http_requset_dict['path'] = html.escape(str(path))
            http_requset_dict['protocol_http'] = html.escape(str(url_split.scheme))
            http_requset_dict['port_number'] = html.escape(str(url_split.port))
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
        header_flag = False
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

                # TODO 目前支持windows系统
                s = str(header).replace(r'\r\n', '')
                print(s)
                try:
                    s = re.findall("^b\'(.*)\'", s)[0]
                except Exception as e:
                    print(e)
                    continue
                if s == '' or None:
                    pass
                # ': ' 对应的是请求header
                elif ': ' in s:
                    # 取到请求头
                    lists = re.findall("^(.*): (.*)$", s)

                    # TODO 暂时不管cookie，直接存到header中
                    # if lists[0][0] == 'Cookie':
                    #    pass

                    http_dict['Header'].append((lists[0][0], html.escape(lists[0][1])))
                else:
                    # 取到请求体头和参数
                    if header_flag is False:
                        request_line_dict = self._set_request_line(s)
                        http_dict.update(request_line_dict)
                        header_flag = True
                    else:
                        http_value = s + http_value
            http_dict['post_value'] = html.escape(str(http_value))
        return http_dict


# Charles 数据处理
class CharlesReader(Reader):
    def __init__(self, chls_file_path):
        self.chls_file_path = chls_file_path

    def __get_charles_data(self):
        if self.chls_file_path is None and str(self.chls_file_path).endswith(".chlsj"):
            raise Exception("chls文件未指定或不是chlsj格式")
        data = json.load(open(self.chls_file_path, encoding='utf-8'))
        return data

    def get_jmeter_data(self):
        '''
        获取charles的数据，默认去掉connect
        :return: [{},{}...]
        '''
        charles_data = self.__get_charles_data()
        jmeter_data = []
        for data in charles_data:
            if str(data['method']).lower() == 'connect':
                pass
            if str(data['protocolVersion']) == 'HTTP/2.0':
                # TODO 后续处理charles http2.0 / IPv6的兼容
                pass
            else:
                try:
                    # print(data)
                    headers = data['request']['header']['headers']
                    first_line = data['request']['header']['firstLine']

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
                        'post_value': None,
                        'Cookie': None,
                        'Header': [(i['name'], html.escape(i['value'])) for i in headers]
                    }
                    jmeter_data.append(http_dict)
                except Exception as e:
                    # 硬处理处理不了的数据
                    print("Error:{}".format(e))
                    continue
        return jmeter_data
