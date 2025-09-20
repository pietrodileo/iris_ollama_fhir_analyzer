Class FHIROLLAMA.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="FHIROLLAMA.Production" LogGeneralTraceEvents="false">
  <Description>Analyze FHIR and extract structured data by using Ollama integration</Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="fhirOutput" Category="" ClassName="EnsLib.HTTP.GenericOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="HTTPPort">11434</Setting>
    <Setting Target="Adapter" Name="HTTPServer">host.docker.internal</Setting>
    <Setting Target="Host" Name="FailureTimeout">30</Setting>
    <Setting Target="Adapter" Name="URL">/api/chat</Setting>
  </Item>
  <Item Name="ProcessFHIR" Category="" ClassName="FHIROLLAMA.BP.ProcessFHIR" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">fhirOutput</Setting>
  </Item>
  <Item Name="entrypoint" Category="" ClassName="EnsLib.REST.GenericService" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigName">ProcessFHIR</Setting>
  </Item>
</Production>
}

}
