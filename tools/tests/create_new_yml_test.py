# Given XLSX_1 When no mentors Then create new Yml
# Given XLSX_1 When existent yml Then Merge Yml's
# Given XLSX_2 When existent yml Then Merge Yml
# Given XLSX_2 When All mentors are present Then no change happen

import tempfile
import os
import sys
import pytest
from file_utils import TOOLS_PATH
from automation import run_automation, read_yml_file, WriteMode

MENTOR_ADRIANA = "Adriana Zencke Zimmermann"
MENTOR_A = "Mentor A"
MENTOR_B = "Mentor B"
MENTOR_C = "Mentor C"

def test_write_mentors_skip_zero_rows(monkeypatch):

    with tempfile.NamedTemporaryFile(suffix='yml', delete=False) as tmpfile:
        tmp_filename = tmpfile.name

    test_args = ['automation.py', os.path.join(TOOLS_PATH, "samples", "mentors.xlsx"), tmp_filename, WriteMode.WRITE, '0']
    monkeypatch.setattr(sys, 'argv', test_args)

    run_automation()

    result = read_yml_file(tmp_filename)
    assert len(result) == 4, f"Expected to write 4 mentors but added {len(result)}"
    assert MENTOR_ADRIANA == result[0]['name'], f"Expected content to be {MENTOR_ADRIANA} but got '{result[0]['name']}'"
    assert MENTOR_A == result[1]['name'], f"Expected content to be {MENTOR_A} but got '{result[1]['name']}'"
    assert MENTOR_B == result[2]['name'], f"Expected content to be {MENTOR_B} but got '{result[2]['name']}'"
    assert MENTOR_C == result[3]['name'], f"Expected content to be {MENTOR_C} but got '{result[3]['name']}'"

    # Clean up the temporary file
    os.remove(tmp_filename)
