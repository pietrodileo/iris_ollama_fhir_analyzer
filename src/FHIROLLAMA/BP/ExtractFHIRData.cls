Class FHIROLLAMA.BP.ExtractFHIRData Extends Ens.BusinessProcess
{

/// Configuration item(s) to which to send file stream messages
Property TargetConfigNames As %String(MAXLEN = 1000);

Parameter SETTINGS = "TargetConfigNames:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId},OllamaTarget:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId}";

Method OnRequest(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {
        #; ; Create an example of request for transformer
        #; Set desc = "Patient Data: Test; Patient Name: Mark Robinson; Patient DOB: 04/12/1991, Patient Gender: Male."
        #; Set json = {
        #;     "description": (desc) 
        #; }
        #; Set req = ##class(%Stream.GlobalCharacter).%New()
        #; Do req.Write(json.%ToJSON())
        #; Set pRequest.Stream = req
        #; Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
        #; If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

        Set sc = ..ProcessFHIR(pRequest)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

        Set json = {
            "message": ("FHIR data processed and embeddings stored successfully.") 
        }
        Set pResponse = ##class(EnsLib.HTTP.GenericMessage).%New()
        Set Stream = ##class(%Stream.GlobalCharacter).%New()
        Do Stream.Write(json.%ToJSON())
        Set pResponse.Stream = Stream

    } Catch ex {
        Set sc=ex.AsStatus()
        Do ex.Log()
    }
    Return sc
}

Method ProcessFHIR(pRequest As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {
        Set Bundle = {}.%FromJSON(pRequest.Stream)
        Set entry = Bundle."entry"
        Set bundleId = Bundle."id"
        Set iter = entry.%GetIterator()
        Set infoStr = ""
        While iter.%GetNext(.key, .value) {
            // Extract the i-th resource
            Set resource = value."resource"
            If $ISOBJECT(resource) {
                Set resourceStr = ""
                Set resourceType = resource."resourceType"
                // For each resource, extract the most relevant information
                If resourceType = "Appointment" {
                    Set sc = ..GetResourceProperties(resource, "status,cancellationReason,specialty,appointmentType,priority,description,minutesDuration,start,end,created,cancellationDate", .resourceId, .ApptStr)
                    Set resourceStr = "Appointment Information: "_ApptStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Patient" {
                    Set sc = ..GetResourceProperties(resource, "active,name,telecom,gender,birthDate,address,communication", .resourceId, .patStr)
                    Set resourceStr = "Patient Information: "_patStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Practitioner" {
                    Set sc = ..GetResourceProperties(resource, "active,name,telecom,gender,birthDate,address,qualification,communication", .resourceId, .pracStr)
                    Set resourceStr = "Practitioner Information: "_pracStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Location" {
                    Set sc = ..GetResourceProperties(resource, "status,name,description,contact,address,hoursOfOperation", .resourceId, .locStr)
                    Set resourceStr = "Location Information: "_locStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Slot" {
                    Set sc = ..GetResourceProperties(resource, "specialty,start,end,status,overbooked,comment", .resourceId, .slotStr)
                    Set resourceStr = "Slot Information: "_slotStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Organization" {
                    Set sc = ..GetResourceProperties(resource, "active,description,contact", .resourceId, .orgStr)
                    Set resourceStr = "Organization Information: "_orgStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Observation" {
                    Set sc = ..GetResourceProperties(resource, "status,category,issued,value,interpretation,note,bodySite,method,referenceRange,component", .resourceId, .obsStr)
                    Set resourceStr = "Observation Information: "_obsStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Condition" {
                    Set sc = ..GetResourceProperties(resource, "clinicalStatus,verificationStatus,category,severity,code,bodySite,recordedDate,note", .resourceId, .condStr)
                    Set resourceStr = "Condition Information: "_condStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "MedicationRequest" {
                    Set sc = ..GetResourceProperties(resource, "status,medication,statusReason,statusChanged,intent,category,priority,doNotPerform,authoredOn,reported,performerType,note,renderedDosageInstruction,effectiveDosePeriod,dosageInstruction,substitution", .resourceId, .medStr)
                    Set resourceStr = "MedicationRequest Information: "_medStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Composition" {
                    Set sc = ..GetResourceProperties(resource, "status,type,category,date,name,title,note,event", .resourceId, .compStr)
                    Set resourceStr = "Composition Information: "_compStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "DiagnosticReport" {
                    Set sc = ..GetResourceProperties(resource, "status,category,code,issued,note", .resourceId, .diagStr)
                    Set resourceStr = "DiagnosticReport Information: "_diagStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "ServiceRequest" {
                    Set sc = ..GetResourceProperties(resource, "intent,status,priority,quantityQuantity,occurrencePeriod,occurrenceDateTime,authoredOn,note", .resourceId, .servStr)
                    Set resourceStr = "ServiceRequest Information: "_servStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "Specimen" {
                    Set sc = ..GetResourceProperties(resource, "status,type,receivedTime,combined,collection,processing,container,condition,note", .resourceId, .specStr)
                    Set resourceStr = "Specimen Information: "_specStr
                    Set infoStr = infoStr_" | "_resourceStr
                } ElseIf resourceType = "AllergyIntolerance" {
                    Set sc = ..GetResourceProperties(resource, "clinicalStatus,verificationStatus,type,category,criticality,code,reaction", .resourceId, .allStr)
                    Set resourceStr = "AllergyIntolerance Information: "_allStr
                    Set infoStr = infoStr_" | "_resourceStr
                } Else {
                    continue
                }
                If resourceStr'="" {
                    ; Get the embedding from transformer
                    Set json = {
                        "description": (resourceStr) 
                    }
                    ; Save the vector and associated information to the database
                    Set transformReq = ##class(EnsLib.HTTP.GenericMessage).%New()
                    Set transformStream = ##class(%Stream.GlobalCharacter).%New()
                    Do transformStream.Write(json.%ToJSON())
                    Set transformReq.Stream = transformStream
                    Set headers = "content-length="_transformReq.Stream.Size_",content-type=application/json"
                    Do transformReq.SetHTTPHeaders(.headers)
                    Set sc = ..SendRequestSync(..TargetConfigNames, transformReq, .transformRes)
                    If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
                    ; Extract the vector and save it to the database
                    Set jsonRes = {}.%FromJSON(transformRes.Stream)
                    Set vector = jsonRes."vector".%ToJSON()
                    Set sc = ##class(FHIROLLAMA.Table.VectorRepository).InsertEmbeddings(vector, resourceStr, bundleId, resourceId, resourceType)
                    If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
                }
            }
        }
    } Catch ex {
        Set sc=ex.AsStatus()
    }
    Return sc
}

Method GetResourceProperties(resource As %DynamicObject, properties As %String, Output id As %String, Output infoStr As %String) As %Status
{
    Set sc = $$$OK
    Set ptr = 0
    Set infoStr = ""
    Set id = resource."id"
    While $LISTNEXT($LISTFROMSTRING(properties, ","), ptr, prop) {
        Set value = resource.%Get(prop)
        If $ISOBJECT(value) {
            Set valueStr = value.%ToJSON()
            ; Remove new line characters for better formatting
            Set valueStr = $REPLACE(valueStr, $CHAR(10), " ")
            Set infoStr = infoStr_"; "_valueStr
        }
    }
    Return sc
}

Storage Default
{
<Data name="TransformerHandlerDefaultData">
<Subscript>"TransformerHandler"</Subscript>
<Value name="1">
<Value>TargetConfigNames</Value>
</Value>
</Data>
<DefaultData>TransformerHandlerDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
