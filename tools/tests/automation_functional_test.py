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
    assert len(result) == 1, f"Expected to write 1 mentor but added {len(result)}"
    assert MENTOR_ADRIANA == result[0]['name'], f"Expected content to be {MENTOR_ADRIANA} but got '{result[0]['name']}'"

    # Clean up the temporary file
    os.remove(tmp_filename)
