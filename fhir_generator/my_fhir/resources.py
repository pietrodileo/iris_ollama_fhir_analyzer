from random import randint
import uuid
from datetime import datetime

class Resource:
    """Base class for all FHIR resources."""

    def __init__(self, id=""):
        if id == "":
            id = uuid.uuid4()
        self.id = id
        self.full_url = f"{self.resourceType}/{self.id}"

    def to_dict(self):
        """Converts resource to a dictionary for JSON serialization."""
        return {
            "resourceType": self.resourceType,
            "id": self.id
        }

    def to_fhir_json(self):
        """Converts to FHIR compliant JSON."""
        return self.to_dict()

class MessageHeader(Resource):
    def __init__(self, id="", source="", source_endpoint="", eventCoding=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.source = source
        self.source_endpoint = source_endpoint
        self.eventCoding = eventCoding
        self.focus = []

    def add_focus(self, focused_resource_reference=""):
        self.focus.append({"reference": focused_resource_reference})
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["eventCoding"] = {
            "system": "http://hl7.org/fhir/message-events",
            "code": self.eventCoding
        }
        fhir_data["source"] = {
            "name": self.source,
            "endpoint": self.source_endpoint
        }
        fhir_data["focus"] = self.focus
        return fhir_data

class Appointment(Resource):
    def __init__(self, id="", type="", type_desc="", description="", slot_reference=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = randint(0, 100000)
        self.type = type
        self.type_desc = type_desc
        self.description = description
        self.participant = []
        self.slot_reference = slot_reference
        
    def add_actor(self, reference = "", display="", status="needs-action"):
        self.participant.append(
            {
                "actor": {
                    "reference": reference,
                    "display": display
                },
                "required": "required",
                "status": status
            }
        )
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = "proposed"
        fhir_data["serviceCategory"] = [
            {
                "coding": [
                    {
                        "system": "http://example.org/service-category",
                        "code": "gp",
                        "display": "General Practice"
                    }
                ]
            }
        ]
        fhir_data["specialty"] = [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "394814009",
                        "display": "General Practice"
                    }
                ]
            }
        ]
        fhir_data["appointmentType"] = [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
                        "code": self.type,
                        "display": self.type_desc
                    }
                ]
            }
        ]
        fhir_data["reasonCode"] = [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "413095006"
                    }
                ],
                "text": "Clinical Review"
            }
        ]
        fhir_data["priority"] = randint(1, 10)
        fhir_data["description"] = self.description
        fhir_data["minutesDuration"] = randint(10, 60)
        fhir_data["slot"] = [
            {
                "reference": self.slot_reference
            }
        ]
        fhir_data["participant"] = self.participant

        return fhir_data

class Practitioner(Resource):
    def __init__(self, id="", identifier="", family_name="", given_name="", gender="", state = "", city="", postalCode = "", address="", telecom=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.gender = gender
        self.family_name = family_name
        self.given_name = given_name
        self.gender = gender
        self.identifier = identifier
        self.address = address
        self.telecom = telecom
        self.state = state  
        self.city = city
        self.postalCode = postalCode

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["gender"] = self.gender
        fhir_data['active']="true"
        fhir_data["name"] = [
            {
                "use": "official",
                "family": self.family_name,
                "given": [
                    self.given_name
                ]
            }
        ]  
        fhir_data["address"] = [
            {
                "use": "home",
                "type": "both",
                "text": f"{self.address}, {self.city}, {self.state} {self.postalCode}",
                "line": [
                    self.address
                ],
                "city": self.city,
                "state": self.state,
                "postalCode": self.postalCode
            }
        ]
        fhir_data["telecom"] = [
            {
                "system": "phone",
                "value": self.telecom,
                "use": "mobile"
            }
        ]

        return fhir_data

class Patient(Resource):
    def __init__(self, id="", identifier="", family_name="", given_name="", gender="", state = "", city="", postalCode = "", address="", telecom="", birthDate=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.family_name = family_name
        self.given_name = given_name
        self.birthDate = birthDate
        self.gender = gender
        self.address = address
        self.telecom = telecom
        self.identifier = identifier
        self.state = state  
        self.city = city
        self.postalCode = postalCode
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["gender"] = self.gender
        fhir_data['active']="true"
        fhir_data['birthDate']=self.birthDate
        fhir_data["name"] = [
            {
                "use": "official",
                "family": self.family_name,
                "given": [
                    self.given_name
                ]
            }
        ]  
        fhir_data["telecom"] = [
            {
                "system": "phone",
                "value": self.telecom,
                "use": "mobile"
            }
        ]
        fhir_data["address"] = [
            {
                "use": "home",
                "type": "both",
                "text": f"{self.address}, {self.city}, {self.state} {self.postalCode}",
                "line": [
                    self.address
                ],
                "city": self.city,
                "state": self.state,
                "postalCode": self.postalCode
            }
        ]
        fhir_data["identifier"] = [
            {
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR"
                        }
                    ]
                },
                "system": "urn:oid:1.2.36.146.595.217.0.1",
                "value": self.identifier,
                "period": {
                    "start": "2001-05-06"
                },
                "assigner": {
                    "display": "Acme Healthcare"
                }
            }
        ]
        return fhir_data

class Location(Resource):
    def __init__(self, id="", name="", telecom="", email="", address="", state = "", city="", postalCode = ""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.address = address
        self.name = name
        self.address = address
        self.telecom = telecom
        self.email = email
        self.state = state  
        self.city = city
        self.postalCode = postalCode

    def add_organization(self, reference = ""):
        self.organization_reference = reference
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["address"] = self.address
        fhir_data['active']="true"
        fhir_data["telecom"] = [
            {
                "system": "phone",
                "value": self.telecom,
                "use": "work"
            },
            {
                "system": "email",
                "value": self.email,
                "use": "work"
            }
        ]
        fhir_data["address"] = [
            {
                "use": "home",
                "type": "both",
                "text": f"{self.address}, {self.city}, {self.state} {self.postalCode}",
                "line": [
                    self.address
                ],
                "city": self.city,
                "state": self.state,
                "postalCode": self.postalCode
            }
        ]
        fhir_data["name"] = self.name
        fhir_data['position'] ={
            "longitude": -83.6945691,
            "latitude": 42.25475478,
            "altitude": 0
        },
        fhir_data['managingOrganization'] = {
            "reference": "Organization/example"
        },
        fhir_data['characteristic'] = [
            {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/location-characteristic",
                        "code": "wheelchair",
                        "display": "Wheelchair accessible"
                    }
                ]
            }
        ]
        fhir_data["managingOrganization"] = [
            {
                "reference": self.organization_reference
            }
        ]
        return fhir_data

class Slot(Resource):
    def __init__(self, id="", start="", end="", specialty="", schedule=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.start = start
        self.end = end
        self.specialty = specialty
        self.schedule_reference = schedule
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["start"] = self.start
        fhir_data["end"] = self.end
        fhir_data['status']="free"
        fhir_data["specialty"] = [
            {
                "coding": [
                    {
                        "code": "408480009",
                        "display": self.specialty
                    }
                ]
            }
        ]
        fhir_data['schedule'] = {
            "reference": self.schedule_reference
        }

        return fhir_data

class Organization(Resource):
    def __init__(self, id="", name="", endpoint=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.name = name
        self.endpoint_reference = endpoint
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["name"] = self.name
        fhir_data['endpoint'] = {
            "reference": self.endpoint_reference
        }

        return fhir_data

class Endpoint(Resource):
    def __init__(self, id="", endpoint=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.endpoint = endpoint
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = "active"
        fhir_data['connectionType'] = {
            "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
            "code": "hl7-fhir-rest"
        }
        fhir_data["address"] = "https://acme.example.org/fhir"

        return fhir_data

class Schedule(Resource):
    def __init__(self, id="", description="", start="", end=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.description = description
        self.start = start
        self.end = end
        self.actors = []
        
    def add_actor(self, reference = "", description=""):
        self.actors.append({
            "reference": reference,
            "display": description
        })
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data['serviceCategory'] = [
            {
                "coding": [
                    {
                        "code": "17",
                        "display": self.description
                    }
                ]
            }
        ]
        fhir_data["planningHorizon"] = {
            "start": self.start,
            "end": self.end
        }
        fhir_data["actor"] = self.actors

        return fhir_data

class Bundle(Resource):
    def __init__(self, id="", type="message"):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.type = type
        self.entry = []

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["type"] = self.type
        fhir_data["timestamp"] = datetime.now().isoformat()
        fhir_data["entry"] = self.entry
        return fhir_data
    
    def add_entry(self, entry_list:list[Resource]):
        for entry in entry_list:
            self.entry.append({
                "fullUrl": entry.full_url,
                "resource": entry.to_fhir_json()
            })
                 
class Encounter(Resource):
    def __init__(self, id="", status="planned", subject_reference="", condition_reference="",):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.status = status
        self.subject_reference = subject_reference
        self.condition_reference = condition_reference
        self.basedOn = []
        
    def add_basedOn(self, reference = ""):
        self.basedOn.append({
            "reference": reference,
        })
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = self.status
        fhir_data["basedOn"] = self.basedOn
        fhir_data["subject"] = {
            "reference": self.subject_reference
        }
        fhir_data["diagnosis"] = [{
            "condition": {
                "reference": self.condition_reference
            }
        }]

        return fhir_data

class Condition(Resource):
    def __init__(self, id="", identifier="", clinicalStatus="active", subject_reference="", pathology="Type 2 Diabetes"):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = identifier
        self.clinicalStatus = clinicalStatus
        self.subject_reference = subject_reference
        self.pathology = pathology
        
    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["identifier"] = [
            {
                "system": "http://hospital.smarthealthit.org/diagnosis-ids",
                "value": self.identifier
            }
        ]
        fhir_data["clinicalStatus"] = self.clinicalStatus
        fhir_data["subject"] = {
            "reference": self.subject_reference
        }
        fhir_data["severity"] = {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "44054006",
                        "display": "Severe"
                    }
                ],
                "text": "Type 2 Diabetes"
        }
        fhir_data["category"] = {
                "coding": [
                    {
                        "system": "http://snomed.info/pathologytype",
                        "code": "394577000",
                        "display": "Main condition"
                    }
                ],
                "text": "Type 2 Diabetes"
        }
        fhir_data["code"] = {
                "coding": [
                    {
                        "system": "http://snomed.info/pathologycode",
                        "code": "44054006",
                        "display": self.pathology
                    }
                ]
        }

        return fhir_data

class ServiceRequest(Resource):
    def __init__(self, id="", identifier="", status="active", intent="order", subject_reference="", encounter_reference="", organization_reference="", doctor_reference="", specimen_reference="", exam_code="", exam_description=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = identifier
        self.status = status
        self.intent = intent
        self.subject_reference = subject_reference
        self.encounter_reference = encounter_reference
        self.specimen_reference = specimen_reference
        self.doctor_reference = doctor_reference
        self.organization_reference = organization_reference
        self.exam_code = exam_code  
        self.exam_description = exam_description

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["identifier"] = [
            {
                "system": "http://hospital.smarthealthit.org/placer-order-ids",
                "value": self.identifier
            }
        ]
        fhir_data["status"] = self.status
        fhir_data["intent"] = self.intent
        fhir_data["subject"] = {
            "reference": self.subject_reference
        }
        fhir_data["encounter"] = {
            "reference": self.encounter_reference
        }
        fhir_data["requester"] = {
            "reference": self.doctor_reference
        }
        fhir_data["performer"] = {
            "reference": self.organization_reference
        }
        fhir_data["specimen"] = [{
           "reference": self.specimen_reference
        }]
        fhir_data["code"] = {
                "coding": [
                    {
                        "system": "http://snomed.info/exam-code",
                        "code": self.exam_code,
                        "display": self.exam_description
                    }
                ]
        }
        fhir_data["quantityQuantity"] = {
            "value": 1
        }

        return fhir_data

class Specimen(Resource):
    def __init__(self, id="", identifier="", subject_reference="", specimen_code="", specimen_description=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = identifier
        self.subject_reference = subject_reference
        self.specimen_code = specimen_code  
        self.specimen_description = specimen_description

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["identifier"] = [
            {
                "system": "http://hospital.smarthealthit.org/placer-order-ids",
                "value": self.identifier
            }
        ]
        fhir_data["subject"] = {
            "reference": self.subject_reference
        }
        fhir_data["type"] = {
                "coding": [
                    {
                        "system": "http://snomed.info/specimen-code",
                        "code": self.specimen_code,
                        "display": self.specimen_description
                    }
                ]
        }
        fhir_data["collection"] = {
                "collectedDateTime": datetime.now().isoformat()
        }

        return fhir_data

class AllergyIntolerance(Resource):
    def __init__(self, id="", substance_code="", substance_description="", allergen_reaction="", subject_reference=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.substance_code = substance_code
        self.substance_description = substance_description
        self.allergen_reaction = allergen_reaction  
        self.subject_reference = subject_reference

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["patient"] = {
            "reference": self.subject_reference
        }
        fhir_data["reaction"] = [{
            "manifestation": [
                {
                    "text": self.allergen_reaction
                }
            ]
        }]
        fhir_data["code"] = {
            "coding": [
                {
                    "system": "http://snomed.info/allergen-code",
                    "code": self.substance_code,
                    "display": self.substance_description
                }
            ]
        }

        return fhir_data
    
class DiagnosticReport(Resource):
    def __init__(self, id="", identifier="", status="final", subject_reference="", encounter_reference="", organization_reference=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = identifier
        self.status = status
        self.subject_reference = subject_reference
        self.encounter_reference = encounter_reference
        self.performer_reference = organization_reference
        self.result = []

    def add_observation(self, reference = ""):
        self.result.append({
            "reference": reference,
        })

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["patient"] = {
            "reference": self.subject_reference
        }
        fhir_data["encounter"] = {
            "reference": self.encounter_reference
        }
        fhir_data["performer"] = {
            "reference": self.performer_reference
        }
        fhir_data["result"] = self.result
        fhir_data["status"] = self.status
        
        return fhir_data
    
class Observation(Resource):
    def __init__(self,id="",status="final",subject_reference="",performer_reference="",effectiveDateTime="",value=0.0,value_unit="",value_code="",value_display="",result_code="",result_display=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.status = status
        self.subject_reference = subject_reference
        self.performer_reference = performer_reference
        self.effectiveDateTime = effectiveDateTime
        self.value = value
        self.value_unit = value_unit
        self.value_code = value_code
        self.value_display = value_display
        self.result_code = result_code
        self.result_display = result_display

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = self.status
        fhir_data["code"] = {
            "coding": [
                {
                    "system": "http://result-code",
                    "code": self.result_code,
                    "display": self.result_display
                }
            ],
        }
        fhir_data["subject"] = {
            "reference": self.subject_reference,
        }
        fhir_data["effectiveDateTime"] = self.effectiveDateTime
        fhir_data["performer"] = [{
                "reference": self.performer_reference,
        }]
        fhir_data["valueQuantity"] = {
            "value": self.value,
            "unit": self.value_unit,
            "system": "http://snomed.info/sct", 
            "code": self.value_code,
            "display": self.value_display
        }

        return fhir_data

class Composition(Resource):
    def __init__(self,id="", identifier="", status="final",subject_reference="",doctor_reference="",date="",medication_request_reference=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.identifier = identifier
        self.subject_reference = subject_reference
        self.doctor_reference = doctor_reference
        self.date = date
        self.status = status
        self.medication_request_reference = medication_request_reference

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = self.status
        fhir_data["identifier"] = [
            {
                "system": "http://hospital.smarthealthit.org/compose-ids",
                "value": self.identifier
            }
        ]
        fhir_data["code"] = {
            "coding": [
                {
                "system" : "http://loinc.org",
                "code" : "57833-6",
                "display" : "Prescription for medication"
                },
                {
                "system" : "http://snomed.info/sct",
                "code" : "761938008",
                "display" : "Medicinal prescription record (record artifact)"
                }
            ],
        }
        fhir_data["subject"] = {
            "reference": self.subject_reference,
        }
        fhir_data["author"] = {
            "reference": self.doctor_reference,
        }
        fhir_data["date"] = self.date
        fhir_data["section"] = [
            {
                "code" : {
                    "coding" : [
                        {
                        "system" : "http://loinc.org",
                        "code" : "57828-6",
                        "display" : "Prescription list"
                        }
                    ]
                },
                "entry" : [
                    {
                        "reference" : self.medication_request_reference
                    }
                ]
            }
        ]
            
        return fhir_data

class MedicationRequest(Resource):
    def __init__(self,id="",status="active", intent="order",subject_reference="",performer_reference="",dosage_frequency=1,dosage_period=1,dosage_unit="d",dosage_method="Oral",dosage_description=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.status = status
        self.intent = intent
        self.subject_reference = subject_reference
        self.performer_reference = performer_reference
        self.medication = []
        self.dosage_frequency = dosage_frequency
        self.dosage_period = dosage_period
        self.dosage_unit = dosage_unit
        self.dosage_method = dosage_method
        self.dosage_description = dosage_description
        
    def add_medication(self, resource:Resource):
        self.medication.append(resource.to_fhir_json())

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["status"] = self.status
        fhir_data["intent"] = self.intent
        fhir_data["medication"] = self.medication
        fhir_data["subject"] = {
            "reference": self.subject_reference,
        }
        fhir_data["performer"] = [{
            "reference": self.performer_reference,
        }]
        fhir_data["dosageInstruction"] = [
            {
                "text": self.dosage_description,
                "timing": {
                    "repeat": {
                        "frequency": self.dosage_frequency,
                        "period": self.dosage_period,
                        "periodUnit": self.dosage_unit
                    }
                },
                "method": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "421661004",
                            "display": self.dosage_method
                        }
                    ]
                }
            }
        ]

        return fhir_data
    
class Medication(Resource):
    def __init__(self,id="",medication_code="",medication_description="",amount_value=0.0,amount_unit="",denominator_value=1,denominator_unit=""):
        self.resourceType = __class__.__name__
        super().__init__(id)
        self.medication_code = medication_code
        self.medication_description = medication_description
        self.amount_value = amount_value
        self.amount_unit = amount_unit
        self.denominator_value = denominator_value
        self.denominator_unit = denominator_unit

    def to_fhir_json(self):
        fhir_data = super().to_fhir_json()
        fhir_data["code"] = {
            "coding": [
                {
                    "system": "http://medication-code",
                    "code": self.medication_code,
                    "display": self.medication_description
                }
            ],
        }
        fhir_data["amount"] = {
            "numerator": {
                "value": self.amount_value,
                "unit": self.amount_unit,
                "system": "http://snomed.info/sct", 
                "code": self.medication_code,
            },
            "denominator": {
                "value": self.denominator_value,
                "unit": self.denominator_unit,
                "system": "http://snomed.info/sct", 
                "code": self.medication_code,
            }
        }

        return fhir_data