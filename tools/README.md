## How to Run Python Scripts

There are two automation scripts:
1) `automation.py`: appends new mentors in `samples/mentors.xslx` to `_data/mentor.yml`

2) `download_image.py`: downloads image from a specified URL and saves in `assets/images/mentors`

3) `meetup_import.py`: imports new upcoming events from the WCC MeetUp page using the iCal feed: https://www.meetup.com/women-coding-community/events/ical/

4) `automation_create_mentor_spreadsheets.py`: creates spreadhseets for each longterm mentor with filenames like `WCC - Long Term - MentorName.xlsx`. All the files are saved in a folder named `Long Term Mentors`. It uses the data from `Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx` sheetname `Revised Mentees`as input.

5) `automation_prepare_adhoc_availability.py`: updates mentors data with specified availability hours in `samples/adhoc-prep.xlsx` in preparation for monthly ad-hoc mentorship.

### Dependencies

python 3.11 or above

### How to Execute on Mac

#### A) `automation.py`

```shell
sh run_automation.sh
```
**Note:** 
- Ensure to update `mentors.xslx` with the new spreadsheet containing the mentors to be added, **OR** 
- adjust the `FILE_PATH_MENTORS_XLSX` parameter in [the script](run_automation.sh) to match the file path for the new spreadsheet.


#### B) `download_image.py`

**Before running the script, make sure** to update the `IMAGE_URL` and `MENTOR_NAME` parameters in the [run_download_automation script](run_download_automation.sh) with:
- the URL you want to download the mentor's image from, **AND**
- the mentor's name as it appears in the spreadsheet e.g 'Adriana Zencke'

You can then run: 
```shell
sh run_download_automation.sh
```

#### C) `meetup_import.py`
**Before running the script, make sure** to download the most recent iCal feed using [this link](https://www.meetup.com/women-coding-community/events/ical/).

Place the downloaded `.ics` file inside the `tools/files` folder and make sure it is renamed to `meetup.ics`.

Afterwards, run the command below:
```shell
sh run_meetup_import.sh
```

**Note:** 
- New data will be appended to [`events.yml`](../_data/events.yml). Verify that all events details are formatted correctly, manually update if needed.

### How to Execute on Windows

1) [Install python](https://www.python.org/downloads/windows)

2) Navigate to the project's `\tools` directory:

    ```
    cd tools
    ```

3) Execute the desired script with the same steps as in **How to Execute on Mac**.

#### D) `automation_create_mentor_spreadsheets.py`

1) [Install python](https://www.python.org/downloads/windows)
2) Download ad save the `Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx` data file in the 'tools/samples' directory as the script file
3) Ensure sheet_name is set correctly in the script as `Revised Mentees`
4) Update `output_dir` to a `local folder path/Long Term Mentors`
5) The script creates the folder `Long Term Mentors` that will have .xlsx files for each mentor
6) Execute the script `automation_create_mentor_spreadsheets.py`
7) Each mentor will have a separate Excel file inside this folder, named: `WCC - Long Term - {Mentor Name}.xlsx`
8) Each file will contain mentee information specific to that mentor, including their reasons for selecting them

**Note:** 
  
📁 Long Term Mentors  
  │── WCC - Long Term - Nonna Shakhova.xlsx  
  │── WCC - Long Term - Rajani Rao.xlsx  
  │── WCC - Long Term - Gabriel Oliveira.xlsx   └── (more mentor files...)  

#### E) `automation_prepare_adhoc_availability.py`

```shell
sh run_adhoc_prep_automation.sh
```
**Note:** 
- If running locally, ensure to update `adhoc-prep.xslx` with the new data to be updated for the mentors. 
- If using GitHub Actions, the GHA workflow for this script uses a Google Cloud service account setup to retrieve the file from Google Drive. The service key has been configured for womencodingcommunity Google Drive account and the file to be used/updated has been shared with the service account email.
Hence, to run the GHA workflow, you only need to provide:
  - the month value (e.g 9 for September) and,
  - the file ID for the excel sheet to use

For more information on the GC service account configurations, you can read the [README](blog_automation/README.md) in the blog automation folder.
