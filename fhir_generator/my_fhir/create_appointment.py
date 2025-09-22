import json
import os
from .resources import Appointment, Organization, Patient, Practitioner, Slot, Location, Bundle, Schedule, MessageHeader, Endpoint

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

    # Location
    location = Location(
        id=f"location-{case_index}",
        name=case["location_name"],
        telecom=case["location_phone"],
        email=case["location_email"],
        address=case["location_address"],
        state=case["location_state"],
        city=case["location_city"],
        postalCode=case["location_postalcode"]
    )
    location.add_organization(organization.full_url)

    # Schedule
    schedule = Schedule(
        id=f"schedule-{case_index}",
        description=case["schedule_description"],
        start=start_time,
        end=end_time
    )
    schedule.add_actor(doctor.full_url, f"Dr. {doctor.given_name} {doctor.family_name}")
    schedule.add_actor(location.full_url, location.name)

    # Slot
    slot = Slot(
        id=f"slot-{case_index}",
        start=start_time,
        end=end_time,
        specialty=case["slot_specialty"],
        schedule=schedule.full_url
    )

    # Appointment
    appointment = Appointment(
        id=f"appointment-{case_index}",
        type=case["appointment_type"],
        type_desc=case["appointment_type_desc"],
        description=case["appointment_description"],
        slot_reference=slot.full_url
    )
    appointment.add_actor(doctor.full_url, f"Dr. {doctor.given_name} {doctor.family_name}")
    appointment.add_actor(patient.full_url, f"{patient.given_name} {patient.family_name}")
    appointment.add_actor(location.full_url, location.name)

    # MessageHeader
    message_header = MessageHeader(
        id=f"msg-{case_index}",
        source=case["source_name"],
        source_endpoint=endpoint.endpoint,
        eventCoding="appointment-booked"
    )
    message_header.add_focus(appointment.full_url)

    # Bundle
    bundle = Bundle(id=f"bundle-{case_index}", type="message")
    entry_list = [message_header, appointment, slot, schedule, location, organization, doctor, patient, endpoint]
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
        output_dir = os.path.join("output", "appointment")
        output_file = os.path.join(output_dir, f"appointment_{case["output_dir"]}.json")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(fhir_json)

    print("All cases generated.")

if __name__ == '__main__':
    main()
