Class FHIROLLAMA.Table.VectorRepository Extends %Persistent
{

/// A textual description or identifier that represents the content of the resource (it is associated with the vector)
Property Description As %String(MAXLEN = 3000);

/// ID of the FHIR Bundle containing the resource
Property BundleID As %String;

/// ID of the FHIR resource within the Bundle
Property ResourceID As %String;

/// Type of the FHIR resource
Property ResourceType As %String;

/// ID of the patient associated with the resource
Property PatientID As %String;

Index idxPatient On PatientID;

Index idxBundle On BundleID;

/// The embedding vector stored as a FLOAT array with a fixed length of 384
Property Vector As %Library.Vector(DATATYPE = "FLOAT", LEN = 384);

/// Insert a new embedding vector into the repository with its associated description
/// <br>
/// <b>Inputs:</b><br>
/// <li>embedding: The vector to be stored (as a JSON array string)</li>
/// <li>description: A textual description or identifier for the vector</li>
/// <li>bundleId: (Optional) The ID of the FHIR Bundle containing the resource</li>
/// <li>resourceId: (Optional) The ID of the FHIR resource within the Bundle</li>
/// <li>resourceType: (Optional) The type of the FHIR resource</li>
/// <li>patientId: (Optional) The ID of the patient associated with the resource</li>
/// <br>
/// <b>Output:</b><br>
/// <li>Returns a status code indicating success or failure of the operation</li>
ClassMethod InsertEmbeddings(embedding As %String, description As %Integer, bundleId As %String = "", resourceId As %String = "", resourceType As %String = "", patientId As %String = "") As %Status
{
    Set sc=$$$OK
    Try {
        Set query = "INSERT INTO FHIROLLAMA_Table.VectorRepository (Description, BundleID, ResourceID, ResourceType, PatientID, Vector)" 
                    _"VALUES (?, ?, ?, ?, ?, TO_VECTOR(?,FLOAT))"
        Set tStatement = ##class(%SQL.Statement).%New()
        $$$ThrowOnError(tStatement.%Prepare(query))

        Set rset = tStatement.%Execute(description, bundleId, resourceId, resourceType, patientId, embedding)
        If (rset.%SQLCODE < 0) {
            Throw ##class(%Exception.SQL).CreateFromSQLCODE(rset.%SQLCODE,rset.%Message)
        }
    } Catch ex {
        Set sc = ex.AsStatus()
        Do ex.Log()
        Return sc
    }
    Return sc
}

/// Perform a vector search using the provided query vector and return the top N most similar vectors <br>
/// <li>Uses cosine similarity for comparison</li>
/// <li>Returns the ID, Description, and Similarity score for each matching vector</li>
/// <br>
/// <b>Input:</b><br>
/// <li>@queryVector The vector to search for similar vectors </li>
/// <li>@NumberOfRows The number of similar vectors to return (default is 5) </li>
/// <br>
/// <b>Output:</b><br>
/// <li>@results Output parameter that will contain the array of similar vectors with their IDs, Descriptions, and Similarity scores </li>
/// <li>@return Status code indicating success or failure of the operation </li>
ClassMethod VectorSearch(queryVector As %String, NumberOfRows As %Integer = 5, Output results As %DynamicArray) As %Status
{
    Set sc = $$$OK
    Try {        
        Set query = "SELECT TOP ? ID, Description, VECTOR_COSINE(Vector, TO_VECTOR(?,float)) AS Similarity " _
                    "FROM FHIROLLAMA_Table.VectorRepository " _
                    "ORDER BY VECTOR_DOT_PRODUCT(Vector,TO_VECTOR(?,float)) DESC"

        Set sqlStatement = ##class(%SQL.Statement).%New()
        Set sc = sqlStatement.%Prepare(.query)
        If $$$ISERR(sc) Throw ##class(%Exception.StatusException).CreateFromStatus(sc)
        Set sqlResults = sqlStatement.%Execute(NumberOfRows, queryVector, queryVector)
        If sqlResults.%SQLCODE < 0 {
            Set ErrorText = "error: SQL query failed" _ $CHAR(10) _
                            "SQLcode: "_sqlResults.%SQLCODE _ $CHAR(10) _
                            "query: "_query
            Throw ##class(%Exception.StatusException).CreateFromStatus($$$ERROR($$$GeneralError,ErrorText))
        } ElseIf sqlResults.%SQLCODE = 100 {
            Set ErrorText = "error: no data found" _ $CHAR(10) _
                            "SQLcode: "_sqlResults.%SQLCODE _ $CHAR(10) _
                            "query: "_query
            Throw ##class(%Exception.StatusException).CreateFromStatus($$$ERROR($$$GeneralError,ErrorText))
        }
        // Iterate over the results
        Set results = []
        While sqlResults.%Next() { 
            Do results.%Push({
                "ID": (sqlResults.ID),
                "Description": (sqlResults.Description),
                "Similarity": (sqlResults.Similarity)
            })
        }
    } Catch ex {
        Set sc=ex.AsStatus()
    }    
    Return sc
}

Storage Default
{
<Data name="VectorRepositoryDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Description</Value>
</Value>
<Value name="3">
<Value>Vector</Value>
</Value>
<Value name="4">
<Value>TESTVector</Value>
</Value>
<Value name="5">
<Value>BundleID</Value>
</Value>
<Value name="6">
<Value>ResourceID</Value>
</Value>
<Value name="7">
<Value>ResourceType</Value>
</Value>
<Value name="8">
<Value>PatientID</Value>
</Value>
</Data>
<DataLocation>^FHIROLLAMADB04.VectorReposD1C9D</DataLocation>
<DefaultData>VectorRepositoryDefaultData</DefaultData>
<IdLocation>^FHIROLLAMADB04.VectorReposD1C9D</IdLocation>
<IndexLocation>^FHIROLLAMADB04.VectorReposD1C9I</IndexLocation>
<StreamLocation>^FHIROLLAMADB04.VectorReposD1C9S</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
