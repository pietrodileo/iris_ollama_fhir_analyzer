Class FHIROLLAMA.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="FHIROLLAMA.Production" LogGeneralTraceEvents="false">
  <Description>Analyze FHIR and extract structured data by using Ollama integration</Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="toFHIRmockServer" Category="" ClassName="EnsLib.HTTP.GenericOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="HTTPPort">5000</Setting>
    <Setting Target="Adapter" Name="HTTPServer">host.docker.internal</Setting>
    <Setting Target="Host" Name="FailureTimeout">30</Setting>
    <Setting Target="Adapter" Name="URL">/fhirmock</Setting>
  </Item>
  <Item Name="ProcessFHIR" Category="" ClassName="FHIROLLAMA.BP.ProcessFHIR" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">toFHIRmockServer</Setting>
    <Setting Target="Host" Name="OllamaTarget">transformToVector</Setting>
    <Setting Target="Host" Name="TransformerTarget">ExtractFHIRData</Setting>
  </Item>
  <Item Name="entrypoint" Category="" ClassName="EnsLib.REST.GenericService" PoolSize="0" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigName">ProcessFHIR</Setting>
    <Setting Target="Adapter" Name="Port"></Setting>
  </Item>
  <Item Name="transformToVector" Category="" ClassName="EnsLib.REST.GenericOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="HTTPPort">5000</Setting>
    <Setting Target="Adapter" Name="HTTPServer">host.docker.internal</Setting>
    <Setting Target="Adapter" Name="URL">/transform</Setting>
  </Item>
  <Item Name="ExtractFHIRData" Category="" ClassName="FHIROLLAMA.BP.ExtractFHIRData" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">transformToVector</Setting>
  </Item>
  <Item Name="VectorSearchManager" Category="" ClassName="FHIROLLAMA.BP.VectorSearchManager" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">transformToVector</Setting>
  </Item>
  <Item Name="vectorSearch" Category="" ClassName="EnsLib.REST.GenericService" PoolSize="0" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigName">VectorSearchManager</Setting>
    <Setting Target="Adapter" Name="Port"></Setting>
  </Item>
</Production>
}

}
