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

### 1. Enable the Drive and Sheets APIs
1. In the left menu, go to **APIs & Services → Library**.
2. Search for **Google Drive API** and click **Enable**.
3. Search for **Google Sheets API** and click **Enable** (needed to read the submissions spreadsheet).

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
6. Repeat the **Share** step for the **blog submissions spreadsheet** (the Google Form responses sheet), giving the service account **Editor** access. Editor (not just Viewer) is required because the pipeline writes `isPublished = TRUE` back to a row after exporting it.

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

## Export a single blog manually (for testing)
1. Activate virtual environment: `source venv/bin/activate`
2. Export one Google Doc into a post:
   `python blog_exporter.py --doc_id <DOC_ID> --author_name "Jane Doe" --image_link "<DRIVE_IMAGE_LINK>"`

This is handy to check a Doc renders correctly. The full pipeline below reads all
of this metadata from the spreadsheet automatically.

## Tests

Run `pytest test_blog_exporter.py`

## CI/CD pipeline: publish a blog when you mark it reviewed

The Google Sheet is the **single source of truth** — there is no local CSV. The
GitHub Action [`.github/workflows/run_blog_exporter.yml`](../../.github/workflows/run_blog_exporter.yml)
turns a reviewed blog into a draft pull request automatically.

### How to publish a blog (the editor's workflow)
1. In the submissions spreadsheet (the **Form Responses 1** sheet), set the row's
   **`isReviewedandApproved`** cell to **`TRUE`** once the draft is reviewed.
   Leave **`isPublished`** blank/`FALSE`.
2. On the next weekly run (Mondays, or immediately via **Actions → Publish
   reviewed blogs → Run workflow**) the action exports the blog, sets that row's
   **`isPublished`** to `TRUE` in the sheet, and opens a PR
   (`Automated import of reviewed blog posts`) with the new post and cover image.
3. **Review the rendered post and merge.**

### What runs
`publish_reviewed_blogs.py` reads the sheet and exports every row where
`isReviewedandApproved` is `TRUE` and `isPublished` is not `TRUE`. Because the
`isPublished` flag is written straight back to the sheet, a blog is never exported
twice — and the existing backlog (already `isPublished = TRUE`) is left alone.

> The draft must be a **native Google Doc** (Drive can only export those to
> Markdown). If a submitter uploaded a `.docx`/`.pdf`, open it and do
> **File → Save as Google Docs** first, otherwise that row is skipped with an error.

### One-time repo setup
- **Service account needs Editor access to the spreadsheet** (see setup step 4) so
  the pipeline can write back `isPublished`.
- **Secret `BLOG_AUTOMATION_SERVICE_ACCOUNT`** — paste the full contents of
  `service_account_key.json` into a repository secret with this name
  (Settings → Secrets and variables → Actions). The workflow writes it to disk at
  runtime and deletes it afterwards; the key is never committed.
- **Secret `GHA_ACTIONS_ALLOW_TOKEN`** — already used by the other automations; it
  lets the action open the pull request.



