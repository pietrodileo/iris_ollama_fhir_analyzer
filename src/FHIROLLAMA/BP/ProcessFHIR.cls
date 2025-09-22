Class FHIROLLAMA.BP.ProcessFHIR Extends Ens.BusinessProcess
{

/// Configuration item(s) to which to send file stream messages
Property TargetConfigNames As %String(MAXLEN = 1000);

/// Configuration item(s) to which to send forward the FHIR request in order to be analyzed by Ollama
Property TransformerTarget As %String(MAXLEN = 1000);

Parameter SETTINGS = "TargetConfigNames:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId},TransformerTarget:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId}";

/// Sends the FHIR requests to the addressed target(s) with a synchronous call and then forwards the same request to another target asynchronously for further processing.
Method OnRequest(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {
        Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
        
        Set ResponseRequired = 0
        Set sc = ..SendRequestAsync(..TransformerTarget, pRequest, ResponseRequired)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
    } Catch ex {
        Set sc=ex.AsStatus()
        Do ex.Log()
    }
    Return sc
}

Storage Default
{
<Data name="ProcessFHIRDefaultData">
<Subscript>"ProcessFHIR"</Subscript>
<Value name="1">
<Value>TargetConfigNames</Value>
</Value>
<Value name="2">
<Value>TransformerTarget</Value>
</Value>
</Data>
<DefaultData>ProcessFHIRDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
