Class FHIROLLAMA.BP.VectorSearchManager Extends Ens.BusinessProcess
{

/// Configuration item(s) to which to send file stream messages
Property TargetConfigNames As %String(MAXLEN = 1000);

Parameter SETTINGS = "TargetConfigNames:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId},OllamaTarget:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId}";

/// Handle an incoming HTTP request containing a query description and number of rows to return <br>
/// <li>Extracts the description and number of rows from the JSON request body</li>
/// <li>Sends the description to the transformer API to obtain its vector representation</li
/// <li>Performs a vector search in the VectorRepository table to find the most similar vectors</li>
/// <li>Returns the search results as a JSON response</li>
/// <br>
Method OnRequest(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {
        Set jsonReq = {}.%FromJSON(pRequest.Stream)
        Set queryDesc = jsonReq."query_desc"
        Set rowsNum = jsonReq."rows"

        ; Get the vector for the query description
        Set json = { "description": (queryDesc) }
        Set pQueryReq = ##class(EnsLib.HTTP.GenericMessage).%New()
        Set queryStream = ##class(%Stream.GlobalCharacter).%New()
        Do queryStream.Write(json.%ToJSON())
        Set pQueryReq.Stream = queryStream
        Set headers = "content-length="_pQueryReq.Stream.Size_",content-type=application/json"
        Do pQueryReq.SetHTTPHeaders(.headers)
        ; Send the request to the Ollama transformer
        Set sc = ..SendRequestSync(..TargetConfigNames, pQueryReq, .pQueryRes)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

        ; Extract the vector and save it to the database
        Set jsonRes = {}.%FromJSON(pQueryRes.Stream)
        Set queryVector = jsonRes."vector".%ToJSON()
        Set (desc, ID, similarity) = ""
        Set sc = ##class(FHIROLLAMA.Table.VectorRepository).VectorSearch(queryVector, rowsNum, .VectorSearchResults)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

        ; Return the vector search results
        Set pResponse = ##class(EnsLib.HTTP.GenericMessage).%New()
        Set res = {
            "results": (VectorSearchResults)
        }
        Set resStream = ##class(%Stream.GlobalCharacter).%New()
        Do resStream.Write(res.%ToJSON())
        Set pResponse.Stream = resStream
    } Catch ex {
        Set sc=ex.AsStatus()
        Do ex.Log()
    }
    Return sc
}

Storage Default
{
<Data name="VectorSearchManagerDefaultData">
<Subscript>"VectorSearchManager"</Subscript>
<Value name="1">
<Value>TargetConfigNames</Value>
</Value>
</Data>
<DefaultData>VectorSearchManagerDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
