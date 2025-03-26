## How to Run Python Scripts

There are two automation scripts:
1) `automation.py`: appends new mentors in `samples/mentors.xslx` to `_data/mentor.yml`

2) `download_image.py`: downloads image from a specified URL and saves in `assets/images/mentors`

3) `automation_create_mentor_spreadsheets.py`: creates spreadhseets for each longterm mentor with filenames like `WCC - Long Term - MentorName.xlsx`. All the files are saved in a folder named `Long Term Mentors`. It uses the data from `Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx` sheetname `Revised Mentees`as input.

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
```shell
sh run_meetup_import.sh
```

**Note:** 
- New data will be imported to [`imported_events.yml`](../_data/imported_events.yml)
- Ensure to copy the generated data to [`events.yml`](../_data/events.yml) and clear the file.


### How to Execute on Windows

1) [Install python](https://www.python.org/downloads/windows)

2) Navigate to the project's `\tools` directory:

    ```
    cd tools
    ```

3) Execute the desired script with the same steps as in **How to Execute on Mac**.

#### D) `automation_create_mentor_spreadsheets.py`

1) [Install python](https://www.python.org/downloads/windows)
2) Download ad save the `Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx` data file in the same directory as the script file
3) Execute the script `automation_create_mentor_spreadsheets.py`
4) The script creates the folder `Long Term Mentors` that will have .xlsx files for each mentor
5) Each mentor will have a separate Excel file inside this folder, named: `WCC - Long Term - {Mentor Name}.xlsx`
6) Each file will contain mentee information specific to that mentor, including their reasons for selecting them

**Note:** 
📂 File Structure Example
Your Folder  
│── automation_generate_mentor_files.py  # The script  
│── Mentorship Programme long-term Registration Form for Mentees (Responses).xlsx  # Input data  
│── 📁 Mentor_Files  
│   │── WCC - Long Term - Nonna Shakhova.xlsx  
│   │── WCC - Long Term - Rajani Rao.xlsx  
│   │── WCC - Long Term - Gabriel Oliveira.xlsx  
│   └── (more mentor files...)  