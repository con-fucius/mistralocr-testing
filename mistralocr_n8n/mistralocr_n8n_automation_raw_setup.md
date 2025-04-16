---

### **1. Core Components**  
#### **n8n**  
- **Purpose**: Visual workflow automation (nodes for apps/APIs).  
- **Key Features**:  
  - Drag-and-drop interface.  
  - Pre-built integrations (databases, APIs, cloud storage).  
  - Self-hosted or cloud deployment.  
  - Custom nodes (JavaScript/Python).  

#### **Mistral AI OCR**  
- **Purpose**: High-accuracy text extraction via API.  
- **Key Features**:  
  - Async processing (upload → job ID → poll results).  
  - Structured output (text by page, bounding boxes).  
  - Cloud-based, scalable.  

**Why Mistral?**  
n8n’s built-in OCR lacks advanced layout handling; Mistral excels for complex documents.  

---

### **2. n8n Workflow Setup**  
#### **Prerequisites**  
- Running n8n instance.  
- Mistral API key (from [console.mistral.ai](https://console.mistral.ai)).  

#### **Steps**  
1. **Trigger**: `On Form Submission` node.  
   - Configure:  
     - Form title: `Invoice OCR Upload`.  
     - Field: `invoice_file` (type: File).  

2. **Upload to Mistral**: `HTTP Request` node (POST).  
   - URL: `https://ocr.mistral.ai/v1/ocr/upload` (verify endpoint).  
   - Auth: `Bearer YOUR_MISTRAL_API_KEY`.  
   - Body: Form-data, binary field `file` = `invoice_file`.  

3. **Get Signed URL**: `HTTP Request` node (GET).  
   - URL: `https://ocr.mistral.ai/v1/ocr/signed-url/{{ $json.id }}`.  
   - Use expression for `job_id` from prior step.  

4. **Retrieve Results**: `HTTP Request` node (GET).  
   - URL: `https://ocr.mistral.ai/v1/ocr/retrieve/{{ $node["Upload..."].json.id }}`.  
   - Body (JSON): `{"url": "{{ $node["Get Signed..."].json.signed_url }}"` (verify if query param is preferred).  

---

### **3. Python Implementation**  
#### **Requirements**  
- Install: `pip install requests`.  
- Set env var: `MISTRAL_API_KEY`.  

#### **Key Functions**  
1. **Upload Document**:  
   ```python  
   def upload_document(file_path):  
       with open(file_path, 'rb') as f:  
           response = requests.post(UPLOAD_ENDPOINT, headers=headers, files={'file': f})  
           return response.json().get('id')  # job_id  
   ```  

2. **Get Results**:  
   ```python  
   def get_ocr_results(job_id, signed_url):  
       response = requests.get(RETRIEVE_ENDPOINT, headers=headers, params={'url': signed_url})  
       return response.json()  
   ```  

**Notes**:  
- Replace placeholder endpoints with Mistral’s latest docs.  
- Use polling (not `time.sleep`) in production.  

---

### **4. Extensions**  
#### **Post-Processing**  
- **n8n**: Use `Edit Fields` or code nodes for regex/LLM parsing.  
- **Python**: `re` module or Mistral’s chat API for structured data.  

#### **Storage/Integrations**  
- Databases: n8n nodes or libraries like `psycopg2` (PostgreSQL).  
- Notifications: Slack/Email via n8n nodes or `smtplib`.  

#### **Error Handling**  
- **n8n**: Enable error routes in node settings.  
- **Python**: Wrap calls in `try/except`, log with `logging`.  

#### **File Formats**  
- Add logic (n8n `IF` node or Python `if/else`) to handle PDF/PNG/JPG.  

--- 

### **Execution**  
- **n8n**: Deploy workflow → test with form submissions.  
- **Python**: Run script with `python mistral_ocr_demo.py`.  

--- 