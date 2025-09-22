Class FHIROLLAMA.vectorTest Extends %RegisteredObject
{

ClassMethod CreateTable() As %Status
{
    // Create table with the help of embedded SQL
    &SQL(CREATE TABLE VectorLab (
        description	VARCHAR(2000),
        description_vector VECTOR(DOUBLE, 384))  
        )
    if (SQLCODE '= 0) 
    {
    //Create index
    &SQL(CREATE COLUMNAR INDEX IVectorLab on VectorLab(description_vector))
    }
    return $$$OK
}

// Function to save vector data

ClassMethod SaveVector(desc As %String, descvec As %DynamicArray) As %Status
{
    //Insert data to VectorLab table
    &sql(INSERT INTO SQLUser.VectorLab  VALUES (:desc,TO_VECTOR(:descvec)))
    if SQLCODE '= 0 {
        write !, "Insert failed, SQLCODE= ", SQLCODE, ! ,%msg
        quit
    }
    return $$$OK
}

}
