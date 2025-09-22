import json
import os
from .resources import Observation, DiagnosticReport, Organization, Patient, Practitioner, Encounter, ServiceRequest, Specimen, AllergyIntolerance, Bundle, Condition, MessageHeader, Endpoint

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

    # Encounter
    encounter = Encounter(
        id=f"encounter-{case_index}",
        subject_reference=patient.full_url,
        status="planned"
    )
    
    # ServiceRequest
    service_request = ServiceRequest(
        id=f"sr-{case_index}",
        identifier=case["service_request_identifier"],
        subject_reference=patient.full_url,
        encounter_reference=encounter.full_url,
        doctor_reference=doctor.full_url,
        organization_reference=organization.full_url,
        exam_code=case["exam_code"],
        exam_description=case["exam_description"]
    )
    
    encounter.add_basedOn(service_request.full_url)
    
    # Observations (loop through list)
    observations = []
    for j, obs_data in enumerate(case["observations"], start=1):
        obs = Observation(
            id=f"obs-{case_index}-{j}",
            subject_reference=patient.full_url,
            performer_reference=organization.full_url,
            status="final",
            effectiveDateTime=obs_data["effectiveDateTime"],
            value=obs_data["value"],
            value_unit=obs_data["unit"],
            value_code=obs_data["code"],
            value_display=obs_data["display"],
            result_display=obs_data["result_display"],
            result_code=obs_data["result_code"]
        )
        observations.append(obs)

    # DiagnosticReport (add all observations)
    diagnostic_report = DiagnosticReport(
        id=f"dr-{case_index}",
        subject_reference=patient.full_url,
        encounter_reference=encounter.full_url,
        organization_reference=organization.full_url,
        status="final",
        identifier=case["diagnostic_report_identifier"]
    )
    for obs in observations:
        diagnostic_report.add_observation(obs.full_url)
    
    # MessageHeader
    message_header = MessageHeader(
        id=f"msg-{case_index}",
        source=case["source_name"],
        source_endpoint=endpoint.endpoint,
        eventCoding="exam-result"
    )
    message_header.add_focus(diagnostic_report.full_url)
    
    # Bundle
    bundle = Bundle(id=f"bundle-{case_index}", type="message")
    entry_list = [message_header, encounter, service_request, organization, doctor, patient, endpoint, diagnostic_report] + observations
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
        output_dir = os.path.join("output", "exam_result")
        output_file = os.path.join(output_dir, f"exam_result_{case["output_dir"]}.json")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(fhir_json)

    print("All cases generated.")

if __name__ == '__main__':
    main()
