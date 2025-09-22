/// Probabilmente da deprecare in favore di FLask Python mock server
Class FHIROLLAMA.API.REST Extends %CSP.REST [ Abstract ]
{

XData UrlMap
{
<Routes>
    <Route Url="/" Method="POST" Call="OperationOutcome" Cors="true"/>
    <Route Url="/" Method="GET" Call="OperationOutcome" Cors="true"/>
</Routes>
}

Parameter HandleCorsRequest = 1;

Parameter CHARSET = "utf-8";

ClassMethod OperationOutcome() As %Status
{
    Set response = {
        "resourceType": "Bundle",
        "id": ($system.Util.CreateGUID()),
        "type": "FHIR-response",
        "timestamp": ($ZDATE($H,3)_"_"_$ZTIME($H,1)),
        "entry": [
            {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "information",
                        "code": "informational",
                        "details": {
                            "text": "Operation completed successfully"
                        }
                    }
                ]
            }
        ]
    }
    Return ..WriteResponse(.response,$$$OK)
}

ClassMethod WriteResponse(ByRef response As %DynamicObject = "", sc As %Status, responseStatusCode As %Integer = 200) As %Status
{
    If '$ISOBJECT(response) {
        Set response = {}
    }
    Set %response.ContentType = ..#CONTENTTYPEJSON
    ; Ripristina l'output REST per restituire all'IO di default (risposta REST) il contenuto dell'oggetto response
    Set %response.IgnoreRESTOutput=0
    If $$$ISERR(sc) {
        Set response = {"error": ("Error: "_$SYSTEM.Status.GetErrorText(sc))}
        Set %response.Status = responseStatusCode
    }
    // Return the response as a JSON
    If $ISOBJECT(response) {
        If response.%IsA("%DynamicAbstractObject") {
            Do response.%ToJSON()
        } Else {
            Do response.OutputToDevice()
        }
    } Else {
        Write response 
    }
	Set %response.IgnoreRESTOutput=1
    Return sc
}

}
