from file_utils import *


def test_get_project_path_is_correct():
    path = get_project_path()
    print(path)

    assert path.endswith("WomenCodingCommunity.github.io/")


def test_get_project_path():
    path = get_project_path()

    assert "/tools" not in path


def test_get_path_in_project():
    assert get_path_in_project("_data").endswith("WomenCodingCommunity.github.io/_data")
    assert get_path_in_project("tools").endswith("WomenCodingCommunity.github.io/tools")
    assert get_path_in_project("tools/").endswith("WomenCodingCommunity.github.io/tools/")


def test_data_folder():
    assert DATA_PATH.endswith("WomenCodingCommunity.github.io/_data")
