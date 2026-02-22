import tempfile
import os
import sys
import pytest
from file_utils import TOOLS_PATH
from automation_mentors import run_automation, read_yml_file, WriteMode

MENTOR_2 = "Mentor2 Name"
MENTOR_3 = "Mentor3 Name"
MENTOR_4 = "Mentor4 Name"

def test_write_mentors_skip_zero_rows(monkeypatch):

    with tempfile.NamedTemporaryFile(suffix='yml', delete=False) as tmpfile:
        tmp_filename = tmpfile.name

    test_args = ['automation_mentors.py', os.path.join(TOOLS_PATH, "samples", "mentors.xlsx"), tmp_filename, "default", WriteMode.WRITE, '0']
    monkeypatch.setattr(sys, 'argv', test_args)

    run_automation()

    result = read_yml_file(tmp_filename)
    assert len(result) == 2, f"Expected to write 2 mentors but added {len(result)}"
    assert MENTOR_2 == result[0]['name'], f"Expected content to be {MENTOR_2} but got '{result[0]['name']}'"
    assert MENTOR_3 == result[1]['name'], f"Expected content to be {MENTOR_3} but got '{result[1]['name']}'"

    # Clean up the temporary file
    os.remove(tmp_filename)
