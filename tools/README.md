## How to Run Python Scripts

There are two automation scripts:
1) `automation.py`: appends new mentors in `samples/mentors.xslx` to `_data/mentor.yml`

2) `download_image.py`: downloads image from a specified URL and saves in `assets/images/mentors`

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