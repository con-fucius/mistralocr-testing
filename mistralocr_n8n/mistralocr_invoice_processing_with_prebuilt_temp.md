# Invoice Processing with Mistral OCR

To replicate this workflow you will need following:

- [Mistral API](https://console.mistral.ai/home)
- [Google Drive and Google Sheets API](https://console.cloud.google.com/)
- [n8n](https://app.n8n.cloud/register)


### 1. Create Mistral API

1. Go to [Mistral console](https://console.mistral.ai/home) and create an account
2. Create new API key and save it for later use in n8n

### 2. Create Google Cloud API (for accessing Google Sheets and Google Drive)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one.
3. Go to APIs & Services
4. Search for “Google Drive API” and enable it for your project. Do the same for “Google Sheets API”
5. Go to APIs & Services > Credentials. Click on + CREATE CREDENTIALS and select OAuth client ID
6. Select Web application and copy this URL to the Authorized redirect URIs - https://oauth.n8n.cloud/oauth2/callback
7. Save Client ID and Client secret for later use in n8n
8. Go to Audience menu and publish the app

### 3. Create [n8n account](https://app.n8n.cloud/register)

1. Go to n8n and create an account(https://app.n8n.cloud/register)
2. Select Credentials tab and create new credentials
3. Create credential for Google Drive and copy the client id and client secret that you got from Google Cloud API. Then Sign in Google.
4. You will get this popup. Click on the Advanced and go to n8n.cloud. Select all items and confirm.
5. Create new credential for Google Sheets as well
6. Set Mistral credential and copy the API key


### 4. Setting up the workflow

We are using the template 'invoice_automation_template.json' to set up the workflow

1. Go to n8n and create new workflow
2. Import the workflow from file and select the template file
3. Configure workflow with your credentials
4. Select the folder you want to test with