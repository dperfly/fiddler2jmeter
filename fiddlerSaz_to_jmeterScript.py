import zipfile
import re
import html
from urllib.parse import urlsplit
from jmeter_template import JmeterTemplate


# fiddler 数据处理
class FiddlerReader:
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

    def __set_request_line(self, request_line):
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
                s = re.findall("^b\'(.*)\'", s)[0]
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
                        request_line_dict = self.__set_request_line(s)
                        http_dict.update(request_line_dict)
                        header_flag = True
                    else:
                        http_value = s + http_value
            http_dict['post_value'] = html.escape(str(http_value))
        return http_dict


# 数据清洗处理
class DataClean:
    def __init__(self, jmeter_datas):
        self.jmeter_datas = jmeter_datas

    def select_jmeter_data(self, host_name=None, filter_url=None):
        '''
        数据清洗,得到想要的数据
        :param host_name: HOST regexp匹配
        :param filter_url: 需要去除的url
        eg：/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$   ----> 过滤css|ico|jpg|png|gif|bmp|wav|js|jpe
        :return:
        '''
        select_jmeter_data = []
        for i, jmeter_data in enumerate(self.jmeter_datas):
            # host 包含在给的的hosts中且不为空,url正则匹配满足
            try:
                if jmeter_data['server_name'] is not None \
                        and re.match(host_name, jmeter_data['server_name'], re.IGNORECASE) is not None \
                        and re.match(filter_url, jmeter_data['path'], re.IGNORECASE) is None:
                    select_jmeter_data.append(jmeter_data)
            except Exception as e:
                print('正则表达式存在问题:\nhostname: {} \nfilter_url: {}'.format(host_name, filter_url))

        return select_jmeter_data

    def get_header_parameter(self, select_jmeter_data, host_name=None):
        '''
        re.match(host_name, jmeter_data['server_name'], re.IGNORECASE) is not None
        提取公共的header
        :param select_jmeter_data: 数据集合
        :param host_name: 域名
        TODO  host_name 暂未设置成正则匹配
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
        print(header_parameter)
        return header_parameter


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

        # 组黄 header manager
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
            # 组装get
            if request_data['method'].lower() == 'get':
                all_request = all_request + self.get_sampler.format(
                    server_name="${" + str(domain[request_data['server_name']]) + "}",  # 参数化设置domain,
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
            # 组装post
            elif request_data['method'].lower() == 'post':
                all_request = all_request + self.post_sampler.format(
                    post_value=request_data['post_value'],
                    server_name="${" + str(domain[request_data['server_name']]) + "}",  # 参数化设置domain
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
            else:
                print('暂不支持的请求类型，method 为 {}'.format(request_data['method'].lower()))
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
        模板总装成jmxScript 脚本
        TODO 根据不同版本适应 暂时使用4.0的版本
        :param select_data:
        :param public_header_manager:
        :return:
        '''
        return self.temp.format(
            test_plan=self.__set_test_plan(select_data)[0],
            thread_group=self.thread_group,
            sample_data_list=self.__set_request(select_data, public_header_manager),
            header_manager=self.__set_header_manager(public_header_manager, 'public'))


def run(saz_file_path, filter_url, host_name, output_jmxScript):
    # filter_url = R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$"
    # host_name = R'^livetv\.sx$'
    if saz_file_path == "":
        return '导入fiddler.saz文件为空'
    if output_jmxScript == "":
        return 'output_jmxScript内容为空'
    if host_name == "":
        return 'host_name内容为空'
    if filter_url == "":
        return 'filter_url内容为空'

    try:
        f = FiddlerReader(saz_file_path)
    except IOError as io:
        return "导入fiddler.saz文件不存在{}".format(saz_file_path)

    jmeter_data = f.get_jmeter_data()
    clear = DataClean(jmeter_data)
    select_data = clear.select_jmeter_data(host_name, filter_url)
    public_header_manager = clear.get_header_parameter(select_data, host_name)
    jw = JmeterWriter()
    jmx_script = jw.get_jmeter_script(select_data, public_header_manager)

    try:
        with open(output_jmxScript, 'w') as o:
            o.write(str(jmx_script))
    except IOError as io:
        return "导出jmx文件不存在：{}".format(output_jmxScript)

    return "生成成功文件地址为:{}\n内容如下：\n\n{}".format(output_jmxScript, jmx_script)


if __name__ == '__main__':
    import os

    run_path = os.path.dirname(os.path.realpath(__file__))
    fiddler_touch_path = os.path.join(run_path, 'fiddler')
    result_touch_path = os.path.join(run_path, 'result')

    saz_file_path = fiddler_touch_path + R"\test.saz"
    filter_url = R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$"
    host_name = R"^.*$"  # R'^livetv\.sx$'

    output_jmxScript = result_touch_path + R'\fiddler_to_jmeter.jmx'
    run(saz_file_path, filter_url, host_name, output_jmxScript)
