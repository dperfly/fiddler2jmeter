class JmeterTemplate:
    def __init__(self):
        '''
        Jmx 模板文件
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
                    post_value=request_data['post_value'] or '',
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
