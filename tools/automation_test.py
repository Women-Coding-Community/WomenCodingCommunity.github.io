from automation import run_automation


def test_automation_default_params():
    try:
        run_automation()
        assert True

    except Exception as e:
        assert False, f"An error occurred: {e}"
