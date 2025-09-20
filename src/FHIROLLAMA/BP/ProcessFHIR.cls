Class FHIROLLAMA.BP.ProcessFHIR Extends Ens.BusinessProcess
{

/// Configuration item(s) to which to send file stream messages
Property TargetConfigNames As %String(MAXLEN = 1000);

Parameter SETTINGS = "TargetConfigNames:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId}";

Method OnRequest(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {
        Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
        
        ; Get Stream from pResponse
        Set DynObj = {}.%FromJSON(pResponse.Stream)
        $$$LOGINFO("Response: "_DynObj."message"."content")

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
</Data>
<DefaultData>ProcessFHIRDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
