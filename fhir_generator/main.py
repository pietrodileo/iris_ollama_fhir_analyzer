import requests
import json
import os
from dotenv import load_dotenv

class FHIRClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def post(self, payload):
        """
        Post a FHIR request to the server.

        :param payload: The FHIR request as a JSON object
        :return: The response from the server as a JSON object, or an error dictionary with keys "error" and "raw"
        """
        try:
            response = requests.post(self.api_url, json=payload, headers={"Content-Type": "application/fhir+json"})
            
            if response.status_code in (200, 201):  # 201 Created is common for FHIR
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"error": "Unable to parse JSON response", "raw": response.text}
            else:
                return {"error": f"{response.status_code} - {response.text}"}
        except Exception as e:
            return {"error": str(e)}

def send_all_requests_in_folder(folder_path, client: FHIRClient):
    # loop through all the folders in the given folder
    """
    Recursively sends all FHIR requests in the given folder and its subfolders.
    :param folder_path: The path to the folder containing the FHIR requests.
    :param client: The FHIRClient to use for sending the requests.
    """

    print(f"Processing folder: {folder_path}")
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            print(f"Processing subfolder: {dir_path}")
            send_requests_in_folder(dir_path, client)
            
def send_requests_in_folder(folder_path, client: FHIRClient):
    """
    Sends all FHIR requests in the given folder to the server.

    :param folder_path: The path to the folder containing the FHIR requests.
    :param client: The FHIRClient to use for sending the requests.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Sending {file_name} ...")
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    payload = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Skipping {file_name}, invalid JSON: {e}")
                    continue

            response = client.post(payload)
            print(f"Response for {file_name}: {response}\n")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Access API URL from .env
    API_URL = os.getenv("API_URL")
    if not API_URL:
        raise ValueError("API_URL is not defined in .env")

    # Define API Client
    client = FHIRClient(API_URL)

    # Folder containing JSON files
    folder = "output"

    # Send all JSON requests in the folder
    send_all_requests_in_folder(folder, client)
