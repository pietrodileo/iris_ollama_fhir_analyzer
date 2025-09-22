from my_fhir import create_appointment, create_exam_request, create_exam_result, create_medical_prescription

print("Generating Appointment Bundles...")
create_appointment.main()
print("Generating Exam Request Bundles...")
create_exam_request.main()
print("Generating Exam Result Bundles...")
create_exam_result.main()
print("Generating Medical Prescription Bundles...")
create_medical_prescription.main()