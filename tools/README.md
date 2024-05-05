## How to Run Python Scripts

### Dependencies

python 3.11 or above

### Execute on Mac

Execute mentor's automation to re-create mentors yml file
  
```shell
sh run_automation.sh 
```

to change default values [go to](run_automation.sh) and adjust the necessary params.

### Setup and Execute on Windows

* [Install python](https://www.python.org/downloads/windows)

1. Navigate to the project's \tools directory:

   cd tools

2. Setup .venv:

- Execute setup_venv_template.bat
  ```
  setup_python_venv.bat
  ```

3. Update mentors.yml

- Execute run_mentors_automation.bat

  ```
  run_mentors_automation.bat
  ```

  - Enter the parameters: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML MODE
  - Example: mentors.xlsx mentors.yml a
  - mode "a" for APPEND new mentors from the xlsx table to the existing mentors.yml
  - WIP-> mode "w" for WRITE all mentors from the xlsx table to mentors.yml (write does not preserve existing mentors' indexes - this is to be done)
