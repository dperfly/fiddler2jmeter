from file_reader import FiddlerReader, CharlesReader
from data_clean import DataClean
from jmeter_writer import JmeterWriter


def run(file_path, filter_url, host_name, output_jmxScript):
    # filter_url = R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$"
    # host_name = R'^livetv\.sx$'
    if file_path == "":
        return '导入fiddler.saz文件为空'
    if output_jmxScript == "":
        return 'output_jmxScript内容为空'
    if host_name == "":
        return 'host_name内容为空'
    if filter_url == "":
        return 'filter_url内容为空'

    try:
        if file_path.endswith(".saz"):
            f = FiddlerReader(file_path)

        elif file_path.endswith(".chlsj"):
            f = CharlesReader(file_path)
    except IOError as io:
        return "导入文件不存在{},或为不支持的后缀名，目前fiddler文件支持saz格式，charles支持chlsj格式".format(saz_file_path)

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
    charles_touch_path = os.path.join(run_path, 'charles')
    saz_file_path = charles_touch_path + R"\test2.chlsj"

    filter_url = R"/(.*)\.(css|ico|jpg|png|gif|bmp|wav|js|jpe)(\?.*)?$"
    host_name = R"^.*$"  # R'^livetv\.sx$'

    output_jmxScript = result_touch_path + R'\charles2_to_jmeter.jmx'
    run(saz_file_path, filter_url, host_name, output_jmxScript)
