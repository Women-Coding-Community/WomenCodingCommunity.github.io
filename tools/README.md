## How to Run Python Scripts

### On your machine install Python (version 3.11.3 or above).

- Windows: https://www.python.org/downloads/windows/
- Linux: $ sudo apt install python3.11

### Set up for Visual Studio Code

- Open project in VS Code:

  1. Git Bash terminal window
  2. Go to the location of the project
  3. Type: code .

- Create virtual environment
  1. Open Command Palette (View->Command Palette)
  2. Select Python: Create Environment
  3. Select Venv (Creates a .venv virtual envir.)
  4. Select the Python version
  5. Select /tools/requirements.txt to install the libraries

### Set up for PyCharm

TBD

### Execute on Windows

1. Run CMD
2. Go to project's \tools folder
3. Enter run_mentors_automation.bat
4. Enter the parameters: FILE_PATH_MENTORS_XLSX FILE_PATH_MENTORS_YML MODE

- Example: mentors.xlsx mentors.yml a
- MODE "a" for APPEND new mentors from the xlsx table to the existing mentors.yml
- WIP-> MODE "w" for WRITE all mentors from the xlsx table to mentors.yml (write does not preserve existing mentors' indexes - this is to be done)
