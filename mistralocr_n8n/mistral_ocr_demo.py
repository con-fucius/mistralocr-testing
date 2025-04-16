import requests
import os
import time
import json

# Configuration
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

# Verify your endpoints with official Mistral documentation
BASE_URL = "https://ocr.mistral.ai/v1/ocr" # Example Base URL
UPLOAD_ENDPOINT = f"{BASE_URL}/upload"
SIGNED_URL_ENDPOINT_TEMPLATE = f"{BASE_URL}/signed-url/{{job_id}}" # Template expecting job_id
RETRIEVE_ENDPOINT_TEMPLATE = f"{BASE_URL}/retrieve/{{job_id}}"   # Template expecting job_id

# Standard headers for authentication
if MISTRAL_API_KEY:
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Accept": "application/json", # Generally good practice
    }
else:
    print("Warning: MISTRAL_API_KEY environment variable not set.")
    headers = {} # Avoid error later, but calls will fail auth

# Function definitions

def upload_document(file_path):
    """Uploads a document file to the Mistral OCR API."""
    if not MISTRAL_API_KEY: return None # Skip if no key
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    print(f"Attempting to upload '{os.path.basename(file_path)}'...")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(UPLOAD_ENDPOINT, headers=headers, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            job_id = result.get('id') # Verify key name 'id'

            if job_id:
                print(f"Upload successful. Job ID: {job_id}")
                return job_id
            else:
                print(f"Upload succeeded but no Job ID found: {result}")
                return None
    # (Include detailed exception handling as in the previous Python-only response)
    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
    return None

def get_signed_url(job_id):
    """Retrieves the signed URL for accessing OCR results."""
    if not MISTRAL_API_KEY: return None
    print(f"Attempting to get signed URL for Job ID: {job_id}...")
    signed_url_endpoint = SIGNED_URL_ENDPOINT_TEMPLATE.format(job_id=job_id)
    try:
        response = requests.get(signed_url_endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        signed_url = result.get('url') # Verify key name 'url'

        if signed_url:
            print("Successfully retrieved signed URL.")
            return signed_url
        else:
            print(f"Signed URL request succeeded but no URL found: {result}")
            print("Job might still be processing. Consider polling.")
            return None
    # (Include detailed exception handling)
    except requests.exceptions.RequestException as e:
         print(f"Error getting signed URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred getting signed URL: {e}")
    return None

def get_ocr_results(job_id, signed_url):
    """Retrieves the final OCR results."""
    if not MISTRAL_API_KEY: return None
    print(f"Attempting to retrieve OCR results for Job ID: {job_id}...")
    retrieve_url = RETRIEVE_ENDPOINT_TEMPLATE.format(job_id=job_id)

    # Approach 1: Pass signed_url in body (UNCONVENTIONAL for GET) ---
    body_payload = {"url": signed_url} # Verify expected key 'url'
    request_headers = headers.copy()
    request_headers['Content-Type'] = 'application/json'
    try:
        response = requests.get(retrieve_url, headers=request_headers, data=json.dumps(body_payload), timeout=60)

    # Approach 2: Pass signed_url as query parameter (More standard) ---
    # Uncomment and use if API expects this; check param name (e.g., 'signed_url')
    # try:
    #     params = {'signed_url': signed_url}
    #     response = requests.get(retrieve_url, headers=headers, params=params, timeout=60)

        response.raise_for_status()
        results = response.json()
        print("Successfully retrieved OCR results.")
        return results
    # (Include detailed exception handling)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving OCR results: {e}")
    except Exception as e:
        print(f"An unexpected error occurred getting OCR results: {e}")
    return None

# Main Execution logic example
if __name__ == "__main__":
    if not MISTRAL_API_KEY:
        print("Fatal Error: MISTRAL_API_KEY environment variable is not set.")
        exit(1)

    # Specify the path to your document
    document_path = "path/to/your/document.pdf" # Change to reflect your actual path to document

    if not os.path.exists(document_path):
        print(f"Error: Input file not found at {document_path}")
        exit(1)

    print("-" * 30)
    print("Starting Mistral OCR Workflow Simulation (Python)")
    print("-" * 30)

    job_id = upload_document(document_path)
    if job_id:
        print("\nWaiting for potential processing...")
        time.sleep(10) # Basic delay; implement polling in production
        signed_url = get_signed_url(job_id)
        if signed_url:
            print("\nWaiting before fetching results...")
            time.sleep(5) # Basic delay
            ocr_results = get_ocr_results(job_id, signed_url)
            if ocr_results:
                print("\n--- Final OCR Results ---")
                print(json.dumps(ocr_results, indent=2))
                print("-------------------------")
            else: print("\nFailed to retrieve OCR results.")
        else: print("\nFailed to get Signed URL.")
    else: print("\nUpload failed.")

    print("\nWorkflow simulation finished.")
    print("-" * 30)
