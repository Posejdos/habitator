import pytest
import os

from app.json_file import JSONFile

emptyFilePath = "tests/json_file_class_test_file_empty.json"
bullshitFilePath = "tests/json_file_class_test_file_bullshit.json"
goodFilePath = "tests/json_file_class_test_file_good.json"


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    open(emptyFilePath, "w").close()
    open(bullshitFilePath, "w").write("bullshit")
    open(goodFilePath, "w").write('{"key": "value"}')

    yield  # this is where the testing happens

    os.remove(emptyFilePath)
    os.remove(bullshitFilePath)
    os.remove(goodFilePath)


def test_read_none():
    jsonFile = JSONFile("tests/notExistingFile.json")
    assert jsonFile.read() == None


def test_write_no_file():
    jsonFile = JSONFile(emptyFilePath)
    assert jsonFile.write(None) == False


def test_read_empty_file():
    jsonFile = JSONFile(emptyFilePath)
    assert jsonFile.read() == None


def test_read_bullshit_file():
    jsonFile = JSONFile(bullshitFilePath)
    assert jsonFile.read() == None


def test_read_good_file():
    jsonFile = JSONFile(goodFilePath)
    assert jsonFile.read() == {"key": "value"}
