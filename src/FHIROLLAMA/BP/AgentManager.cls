/// Da deprecare o riutilizzare in seguito
Class FHIROLLAMA.BP.AgentManager Extends Ens.BusinessProcess
{

/// LLM model to use for generating responses
Property Model As %String(VALUELIST = ",gemma3:4b,other") [ InitialExpression = "gemma3:4b" ];

Property Prompt As %String(MAXLEN = 10000) [ InitialExpression = "Analyze the following FHIR resource and extract structured data in JSON format. Return only the JSON without any additional text. If the resource is not valid FHIR, return an error message in JSON format." ];

/// Configuration item(s) to which to send file stream messages
Property TargetConfigNames As %String(MAXLEN = 1000);

Parameter SETTINGS = "Prompt:LLMSettings,Model:LLMSettings,TargetConfigNames:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId},OllamaTarget:Basic:selector?multiSelect=1&context={Ens.ContextSearch/ProductionItems?targets=1&productionName=@productionId}";

Method OnRequest(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK
    Try {

        ; Get Stream from pRequest
        #; Set content = ..Prompt _ " Here is the FHIR resource: "_pRequest.Stream.Read()
        #; Set request = {
        #;     "model": (..Model),
        #;     "stream": false,
        #;     "messages": [
        #;         {
        #;             "role": "user",
        #;             "content": (content)
        #;         }
        #;     ]
        #; }

        #; Set llmRequest = ##class(%Stream.GlobalCharacter).%New()
        #; Do llmRequest.Write(request.%ToJSON())
        #; #; $$$LOGINFO("Request: "_request.%ToJSON())
        #; Set pRequest.Stream = llmRequest
        #; Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
        #; If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

        Do ..ProcessFHIR(pRequest,.pResponse)

        Set DynObj = {}.%FromJSON(pResponse.Stream)
        $$$LOGINFO("Response: "_DynObj."message"."content")
        $$$LOGINFO("Response: "_DynObj."response")

    } Catch ex {
        Set sc=ex.AsStatus()
        Do ex.Log()
    }
    Return sc
}

Method ProcessFHIR(pRequest As EnsLib.HTTP.GenericMessage, Output pResponse As EnsLib.HTTP.GenericMessage) As %Status
{
    Set sc = $$$OK

    Set Bundle = {}.%FromJSON(pRequest.Stream)
    Set entry = Bundle."entry"

    Set iter = entry.%GetIterator()
    While iter.%GetNext(.key, .value) {
        // Extract the i-th resource
        Set resource = value."resource"
        If $IsObject(resource) {
            set resourceType = resource."resourceType"
            If resourceType = "Encounter" {
                Set extraPrompt = "In FHIR Encounter represents an interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) or assessing the health status of a patient. "
                Set send = 1
            } ElseIf resourceType = "Patient" {
                Set extraPrompt = "In FHIR Patient represents an individual receiving or who has received healthcare services. "
                Set send = 1
            } ElseIf resourceType = "Observation" {
                Set extraPrompt = "In FHIR Observation represents measurements and simple assertions made about a patient, device, or other subject. "
                Set send = 1
            } ElseIf resourceType = "Condition" {
                Set extraPrompt = "In FHIR Condition represents detailed information about conditions, problems, or diagnoses recognized by a clinician. "
                Set send = 1
            } ElseIf resourceType = "Procedure" {
                Set extraPrompt = "In FHIR Procedure represents an action that is or was performed on or for a patient. "
                Set send = 1
            } ElseIf resourceType = "MedicationRequest" {
                Set extraPrompt = "In FHIR MedicationRequest represents an order or request for both supply of the medication and the instructions for administration of the medication to a patient. "
                Set send = 1
            } ElseIf resourceType = "Medication" {
                Set extraPrompt = "In FHIR Medication represents a specific medication, including its ingredients and packaging. "
                Set send = 1
            } ElseIf resourceType = "AllergyIntolerance" {
                Set extraPrompt = "In FHIR AllergyIntolerance represents a record of a clinical assessment of an allergy or intolerance, including the associated reaction information. "
                Set send = 1
            } ElseIf resourceType = "ServiceRequest" {
                Set extraPrompt = "In FHIR ServiceRequest represents a request for a service to be performed, such as a diagnostic test, treatment, or other clinical service. "
                Set send = 1
            } Else {
                Set extraPrompt = ""
                Set send = 0
            }       
            if send {
                Set content = ..Prompt_" "_extraPrompt_" Here is the FHIR resource: "_resource.%ToJSON()
                Set request = {
                    "model": (..Model),
                    "stream": false,
                    "prompt": (content)
                    #; "messages": [
                    #;     {
                    #;         "role": "user",
                    #;         "content": (content)
                    #;     }
                    #; ]
                }
                Set llmRequest = ##class(%Stream.GlobalCharacter).%New()
                Do llmRequest.Write(request.%ToJSON())
                Set pRequest.Stream = llmRequest
                Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
                If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
            }
        }
    }

    #; Set content = "Why sky is blue?"
    #; Set request = {
    #;     "model": (..Model),
    #;     "stream": false,
    #;     "prompt": "Why is the sky blue? Give the shortest answer possible in under 20 words"
    #;     #; "options":{
    #;     #; "num_thread": 12
    #;     #; },
    #;     #; "messages": [
    #;     #;     {
    #;     #;         "role": "user",
    #;     #;         "content": (content)
    #;     #;     }
    #;     #; ]
    #; }
    #; Set llmRequest = ##class(%Stream.GlobalCharacter).%New()
    #; Do llmRequest.Write(request.%ToJSON())
    #; Set pRequest.Stream = llmRequest
    #; Set sc = ..SendRequestSync(..TargetConfigNames, pRequest, .pResponse)
    #; If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)

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
<Value>Model</Value>
</Value>
<Value name="3">
<Value>Prompt</Value>
</Value>
</Data>
<DefaultData>ProcessFHIRDefaultData</DefaultData>
<Type>%Storage.Persistent</Type>
}

}
