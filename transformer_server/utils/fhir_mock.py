import uuid
import datetime

class MockFHIR():
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.op_id = str(uuid.uuid4())
        self.mh_id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    def create_response(self, data: dict) -> dict:
        response_id = data.get("id")
        
        operation_outcome = {
            "resourceType": "OperationOutcome",
            "id": f"oo-{self.op_id}",
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

        message_header = {
            "resourceType": "MessageHeader",
            "id": f"mh-{self.mh_id}",
            "eventCoding": {
                "system": "http://hl7.org/fhir/message-events",
                "code": "operation-complete",
                "display": "FHIR Operation Completed"
            },
            "source": {
                "name": "FHIR Mock API",
                "endpoint": "http://localhost:5000"
            },
            "focus": [
                {
                    "reference": f"OperationOutcome/oo-{self.op_id}"
                }
            ],
            "response": {
                "identifier": response_id,
                "code": "ok"
            }
        }

        return {
            "resourceType": "Bundle",
            "id": self.id,
            "type": "message",
            "timestamp": self.timestamp,
            "entry": [
                {
                    "fullUrl": f"MessageHeader/mh-{self.mh_id}",
                    "resource": message_header
                },
                {
                    "fullUrl": f"OperationOutcome/oo-{self.op_id}",
                    "resource": operation_outcome
                }
            ]
        }

