import json
import os
from .resources import Organization, Patient, Practitioner, Encounter, ServiceRequest, Specimen, AllergyIntolerance, Bundle, Condition, MessageHeader, Endpoint

def generate_case(case: dict, case_index: int):
    # Extract common values
    start_time = case["slot_start_time"]
    end_time = case["slot_end_time"]
    endpoint_url = "https://acme.example.org/fhir"

    # Create Patient
    patient = Patient(
        id=f"patient-{case_index}",
        identifier=f"pat-{1000+case_index}",
        family_name=case["patient_family_name"],
        given_name=case["patient_name"],
        gender=case["patient_gender"],
        state=case["patient_state"],
        city=case["patient_city"],
        postalCode=case["patient_postalcode"],
        address=case["patient_address"],
        telecom=case["patient_phone"],
        birthDate=case["patient_birthdate"]
    )

    # Create Practitioner
    doctor = Practitioner(
        id=f"doctor-{case_index}",
        identifier=f"doc-{2000+case_index}",
        family_name=case["doctor_family_name"],
        given_name=case["doctor_name"],
        gender=case["doctor_gender"],
        state=case["doctor_state"],
        city=case["doctor_city"],
        postalCode=case["doctor_postalcode"],
        address=case["doctor_address"],
        telecom=case["doctor_phone"]
    )

    # Endpoint
    endpoint = Endpoint(id=f"endpoint-{case_index}", endpoint=endpoint_url)

    # Organization
    organization = Organization(
        id=f"hospital-{case_index}",
        name=case["organization_name"],
        endpoint=endpoint.full_url
    )

    # Specimen
    specimen = Specimen(
        id=f"specimen-{case_index}",
        identifier=case["specimen_identifier"],
        specimen_code=case["specimen_code"],
        specimen_description=case["specimen_description"],
        subject_reference=patient.full_url
    )

    # Condition
    condition = Condition(
        id=f"condition-{case_index}",
        identifier=case["condition_identifier"],
        subject_reference=patient.full_url,
        pathology=case["pathology"]
    )

    # AllergyIntolerance
    allergy = AllergyIntolerance(
        id=f"allergy-{case_index}",
        subject_reference=patient.full_url,
        substance_description=case["substance_description"],
        substance_code=case["substance_code"],
        allergen_reaction=case["allergen_reaction"]
    )
    
    # Encounter
    encounter = Encounter(
        id=f"encounter-{case_index}",
        subject_reference=patient.full_url,
        condition_reference=condition.full_url,
        status="planned"
    )
    
    # ServiceRequest
    service_request = ServiceRequest(
        id=f"sr-{case_index}",
        identifier=case["service_request_identifier"],
        subject_reference=patient.full_url,
        encounter_reference=encounter.full_url,
        specimen_reference=specimen.full_url,
        doctor_reference=doctor.full_url,
        organization_reference=organization.full_url,
        exam_code=case["exam_code"],
        exam_description=case["exam_description"]
    )
    
    encounter.add_basedOn(service_request.full_url)
    
    # MessageHeader
    message_header = MessageHeader(
        id=f"msg-{case_index}",
        source=case["source_name"],
        source_endpoint=endpoint.endpoint,
        eventCoding="exam-request"
    )
    message_header.add_focus(encounter.full_url)
    message_header.add_focus(allergy.full_url)
    
    # Bundle
    bundle = Bundle(id=f"bundle-{case_index}", type="message")
    entry_list = [message_header, encounter, allergy, service_request, condition, specimen, organization, doctor, patient, endpoint]
    bundle.add_entry(entry_list)

    return bundle

def main():
    with open(os.path.join("config", "config.json"), "r") as f:
        config = json.load(f)

    if not isinstance(config, list):
        print("Error: config.json must contain a JSON array.")
        return

    if not config:
        print("Error: config.json array is empty.")
        return

    for i, case in enumerate(config, start=1):
        print(f"Processing Case {i}: {case.get('patient_name', 'Unnamed')} {case.get('patient_family_name','')}")
        bundle = generate_case(case, i)

        # Serialize
        fhir_json = bundle.to_fhir_json()
        fhir_json = json.dumps(fhir_json, indent=4)

        # Write to per-case output_dir
        output_dir = os.path.join("output", "exam_request")
        output_file = os.path.join(output_dir, f"exam_request_{case["output_dir"]}.json")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(fhir_json)

    print("All cases generated.")

if __name__ == '__main__':
    main()
