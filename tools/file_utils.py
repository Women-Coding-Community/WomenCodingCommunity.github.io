import os


def _get_absolut_path():
    return os.path.abspath(os.curdir)


def get_project_path():
    path = _get_absolut_path()

    if "tools" in path:
        return path.replace("tools", "")

    return path


def get_path_in_project(path_name):
    return get_project_path() + path_name


PROJECT_PATH = get_project_path()
TOOLS_PATH = get_path_in_project("tools")
DATA_PATH = get_path_in_project("_data")
