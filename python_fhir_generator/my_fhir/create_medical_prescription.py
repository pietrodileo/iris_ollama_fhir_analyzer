import json
import os
from .resources import Composition, Medication, MedicationRequest, Observation, DiagnosticReport, Organization, Patient, Practitioner, Encounter, ServiceRequest, Specimen, AllergyIntolerance, Bundle, Condition, MessageHeader, Endpoint

def generate_case(case: dict, case_index: int):
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

    # MedicationRequest
    medication_request = MedicationRequest(
        id=f"medreq-{case_index}",
        subject_reference=patient.full_url,
        performer_reference=doctor.full_url,
        dosage_frequency=case["dosage_frequency"],
        dosage_period=case["dosage_period"],
        dosage_unit=case["dosage_unit"],
        dosage_method=case["dosage_method"],
        dosage_description=case["dosage_description"]
    )
    # Medication (loop through list)
    medications = []
    for j, medication_data in enumerate(case["medications"], start=1):
        med = Medication(
            id=f"med-{case_index}-{j}",
            medication_code=medication_data["medication_code"],
            medication_description=medication_data["medication_description"],
            amount_value=medication_data["amount_value"],
            amount_unit=medication_data["amount_unit"],
            denominator_value=medication_data["denominator_value"],
            denominator_unit=medication_data["denominator_unit"]
        )
        medications.append(med)

    for medication in medications:
        medication_request.add_medication(medication)

    # Composition
    composition = Composition(
        id=f"comp-{case_index}",
        identifier=f"comp-{3000+case_index}",
        status="final",
        subject_reference=patient.full_url,
        doctor_reference=doctor.full_url,
        date=case["composition_date"],
        medication_request_reference=medication_request.full_url
    )

    # MessageHeader
    message_header = MessageHeader(
        id=f"msg-{case_index}",
        source=case["source_name"],
        source_endpoint=endpoint.endpoint,
        eventCoding="medical-prescription"
    )
    message_header.add_focus(composition.full_url)
    
    # Bundle
    bundle = Bundle(id=f"bundle-{case_index}", type="message")
    entry_list = [message_header, doctor, patient, composition, medication_request]
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
        output_dir = os.path.join("output", "medical_prescription")
        output_file = os.path.join(output_dir, f"medical_prescription_{case["output_dir"]}.json")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(fhir_json)

    print("All cases generated.")

if __name__ == '__main__':
    main()
