import re


# 数据清洗处理
class DataClean:
    def __init__(self, jmeter_datas):
        self.jmeter_datas = jmeter_datas

    def select_jmeter_data(self, host_name=None, filter_url=None, distinct=False):
        '''
        数据清洗,得到想要的数据
        :param host_name: HOST regexp匹配
        :param filter_url: 需要去除的url
        eg：/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$   ----> 过滤css|ico|jpg|png|gif|bmp|wav|js|jpe
        :return:
        '''
        select_jmeter_data = []
        # print(self.jmeter_datas)
        for i, jmeter_data in enumerate(self.jmeter_datas):
            # host 包含在给的的hosts中且不为空,url正则匹配满足
            try:
                if jmeter_data['server_name'] is not None \
                        and re.match(host_name, jmeter_data['server_name'], re.IGNORECASE) is not None \
                        and re.match(filter_url, jmeter_data['path'], re.IGNORECASE) is None:

                    # 过滤重复的url请求
                    if distinct and len(select_jmeter_data) > 0:
                        distinct_list = [f"{i['server_name']}{i['path']}" for i in select_jmeter_data]
                        if f"{jmeter_data['server_name']}{jmeter_data['path']}" in distinct_list:
                            # print(f"{jmeter_data['server_name']}{jmeter_data['path']}")
                            continue

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
