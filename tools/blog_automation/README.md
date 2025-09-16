# Goals of this Automation

# Setup
## 🔑 Setting up Google Service Account Credentials

To allow our scripts to access Google Drive and export documents, you need to create a **Google Cloud Project**, a **service account**, and download its credentials as a JSON key file.

*Alternatively, you can ask Silke for the service_account_key.json (in which case, you can skip steps 0-3).*

### 0. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Open the project selector (top bar) and click **New Project**.
3. Name the project **`blog-automation`**.
4. Click **Create**.
5. Make sure the new project is selected in the top bar.

👉 **Note:** You need the **Project Editor** or **Owner** role on this project to create service accounts and keys.  
If you’re the one who created the project, you already have these permissions.

### 1. Enable the Drive API
1. In the left menu, go to **APIs & Services → Library**.
2. Search for **Google Drive API**.
3. Click **Enable**.

### 2. Create a Service Account
1. In the left menu, go to **IAM & Admin → Service Accounts**.
2. Click **Create Service Account**.
3. Name it **`blog-exporter`** and add a short description (e.g. *Exports blog content from Google Docs*).
4. Click **Create and Continue**.  
   - You do **not** need to assign project-wide roles to this service account.
   - Just click **Done** once the account is created.

### 3. Generate and Download the JSON Key
1. Click on the service account you just created.
2. Go to the **Keys** tab.
3. Click **Add Key → Create new key**.
4. Choose **JSON** and click **Create**.
5. A file will be downloaded (e.g. `blog-exporter-123abc.json`).  
   - Rename it to **`service_account_key.json`**.  
   - Move this file into the **`blog_automation`** folder of this repo (the same folder where this README lives).  
   - **Do not commit this file to Git!** It should already be listed in `.gitignore`.

### 4. Share the Google Drive Folder or Document
1. In Google Drive, right-click the folder (e.g. `blog_automation`) or a specific Google Doc.
2. Click **Share**.
3. Enter the service account’s email (looks like `blog-exporter@blog-automation.iam.gserviceaccount.com`).
4. Give it at least **Viewer** access.
5. Save changes.  
   - Now the service account can read/export files in that folder or doc.

---

✅ At this point you should have:
- A **Google Cloud Project** called `blog-automation` with the **Drive API enabled**.
- A **service account** called `blog-exporter`.
- A local **`service_account_key.json`** file inside your `blog_automation` folder (same place as this README, ignored by git).
- The service account email added as a **Viewer** to your Google Drive folder or doc.


## Set up Virtual Environment & Install Required Package
- Set up venv `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

# Automation Script

## Find Document ID
Each Google Doc has a unique ID in its URL.  
For example, if the URL is:
https://docs.google.com/document/d/1ABCDEFghijklmnopQRS_tUVWXyz1234567890/edit

Then the **Document ID** is:

1ABCDEFghijklmnopQRS_tUVWXyz1234567890

Use this ID in your scripts when exporting the document.

## Run Automation
1. Activate virtual environment: `source venv/bin/activate`
2. Run the script: `python doc_to_html_conversion.py <DOC_ID>`


