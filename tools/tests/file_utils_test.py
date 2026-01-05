from file_utils import *


def test_get_project_path_is_correct():
    path = get_project_path()

    assert path.endswith("WomenCodingCommunity.github.io") or path.endswith("WomenCodingCommunity.github.io\\") or path.endswith("WomenCodingCommunity.github.io/")


def test_get_project_path():
    path = get_project_path()

    assert "/tools" not in path


def test_get_path_in_project():
    assert get_path_in_project("_data").endswith(os.path.join("WomenCodingCommunity.github.io", "_data"))
    assert get_path_in_project("tools").endswith(os.path.join("WomenCodingCommunity.github.io", "tools"))
    assert get_path_in_project("tools/").endswith(os.path.join("WomenCodingCommunity.github.io", "tools/"))


def test_data_folder():
    assert DATA_PATH.endswith(os.path.join("WomenCodingCommunity.github.io", "_data"))
