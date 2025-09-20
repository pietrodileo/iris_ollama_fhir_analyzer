Class App.Installer
{

XData setup
{
<Manifest>
  <Log Level="3" Text="Start manifest" />
  <!-- Variables -->
  <Default Name="NAMESPACE" Value="FHIROLLAMA"/>
  <Default Name="DBNAME" Value="FHIROLLAMA"/>
  <Default Name="APPPATH" Dir="/opt/irisapp/" />
  <Default Name="SOURCESPATH" Dir="${APPPATH}src" />
  <Default Name="RESOURCE" Value="%DB_${DBNAME}" /> 
  <Default Name="PRODUCTION" Value="${NAMESPACE}.Production"/>

  <!-- Create namespace if it doesn't exist -->
  <If Condition='##class(%SYS.Namespace).Exists("${NAMESPACE}")=0'>
    <Log Level="3" Text="Namespace doesn't exist. Creating namespace ${NAMESPACE}" />
    <!-- Namespace definition (Enabled for Interoperability: Ensemble=1) -->
    <Namespace Name="${NAMESPACE}" Code="${DBNAME}-CODE" Data="${DBNAME}-DATA" Create="yes" Ensemble="1">
      <Configuration>
        <Database Name="${DBNAME}-CODE" Dir="${APPPATH}${DBNAME}-CODE" Create="yes" Resource="${RESOURCE}"/>
        <Database Name="${DBNAME}-DATA" Dir="${APPPATH}${DBNAME}-DATA" Create="yes" Resource="${RESOURCE}"/>
      </Configuration>
      <!-- Import source code -->
      <Import File="${SOURCESPATH}" Recurse="1"/>
      <!-- Start production in namespace -->
      <Production Name="${PRODUCTION}" AutoStart="1" /> 
    </Namespace>
  </If>

  <!-- Create Web Application -->
  <Invoke Class="App.Installer" Method="RegisterWebApplication" CheckStatus="1" Return="restsc"> 
  </Invoke>

  <Log Level="3" Text="End manifest" />
</Manifest>
}

ClassMethod setup(ByRef pVars, pLogLevel As %Integer = 3, pInstaller As %Installer.Installer, pLogger As %Installer.AbstractLogger) As %Status [ CodeMode = objectgenerator, Internal ]
{
    #; Let XGL document generate code for this method. 
    Quit ##class(%Installer.Manifest).%Generate(%compiledclass, %code, "setup")
}

ClassMethod RegisterWebApplication(pNameSpace As %String = "FHIROLLAMA", pName As %String = "/fhir", pClassName As %String = "EnsLib.REST.GenericService", pDescription As %String = "REST API to handle FHIR messages", verbose As %Boolean = 0) As %Status
{
    New $Namespace
    Set $Namespace = "%SYS"
    Set ret = $$$OK
    Set spec("AutheEnabled") = $$$AutheUnauthenticated
    Set spec("NameSpace") = pNameSpace
    Set spec("Description") = pDescription
    Set spec("IsNameSpaceDefault") = $$$NO
    Set spec("DispatchClass") = pClassName
    Set spec("MatchRoles")=":%All"

    If ('##class(Security.Applications).Exists(pName)) {
        If verbose Write !,"Creating Web application """_pName_"""..."
        Set ret = ##class(Security.Applications).Create(pName, .spec)
        If verbose Write !, "Web application """_pName_""" is created.",!
    }
    Else { // ensure configuration matches in case of updating from old terminal versions
        If verbose Write !, "Updating web application """_pName_"""..."
        Set ret = ##class(Security.Applications).Modify(pName, .spec)
        If verbose Write !, "Web application """_pName_""" is updated.",!
    }
    Return ret
}

}