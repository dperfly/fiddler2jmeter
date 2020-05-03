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
