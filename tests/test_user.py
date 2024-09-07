import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.user import User
from app.habit import Habit, HabitEvent


@pytest.fixture
def user():
    user = User(name="Test User", jsonPath="test.json")
    user.jsonFile = MagicMock()
    return user


def test_initialization(user):
    assert user.name == "Test User"
    assert isinstance(user.jsonFile, MagicMock)
    assert user.habits == []


def test_get_event_from_string(user):
    assert user.get_event_from_string("DONE") == HabitEvent.DONE
    assert user.get_event_from_string("FAILED") == HabitEvent.FAILED
    assert user.get_event_from_string("UNKNOWN") == None


def test_get_string_from_event(user):
    assert user.get_string_from_event(HabitEvent.DONE) == "DONE"
    assert user.get_string_from_event(HabitEvent.FAILED) == "FAILED"
    assert user.get_string_from_event(None) == "ERROR"


def test_parse_event_list(user):
    event_list = ["DONE", "FAILED", "UNKNOWN"]
    parsed_list = user.parse_event_list(event_list)
    assert parsed_list == [HabitEvent.DONE, HabitEvent.FAILED]


def test_parse_habit(user):
    json_habit = {
        "name": "Test Habit",
        "description": "Test Description",
        "frequency": 24,
        "eventList": ["DONE", "FAILED"],
        "lastMarkedDone": "2023-01-01T00:00:00",
    }
    user.parse_habit(json_habit)
    assert len(user.habits) == 1
    habit = user.habits[0]
    assert habit.name == "Test Habit"
    assert habit.description == "Test Description"
    assert habit.frequency_in_hours == 24
    assert habit.eventList == [HabitEvent.DONE, HabitEvent.FAILED]
    assert habit.lastMarkedDone == datetime.strptime(
        "2023-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"
    )


def test_try_load_data_from_json(user):
    user.jsonFile.read.return_value = {
        "name": "Loaded User",
        "habits": [
            {
                "name": "Loaded Habit",
                "description": "Loaded Description",
                "frequency": 24,
                "eventList": ["DONE"],
                "lastMarkedDone": "2023-01-01T00:00:00",
            }
        ],
    }
    assert user.try_load_data_from_json() == True
    assert user.name == "Loaded User"
    assert len(user.habits) == 1
    habit = user.habits[0]
    assert habit.name == "Loaded Habit"


def test_save_data_to_json(user):
    habit = Habit("Test Habit", "Test Description", 24)
    habit.eventList = [HabitEvent.DONE]
    habit.lastMarkedDone = datetime.strptime("2023-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
    user.habits.append(habit)
    user.save_data_to_json()
    user.jsonFile.write.assert_called_once_with(
        {
            "name": "Test User",
            "habits": [
                {
                    "name": "Test Habit",
                    "description": "Test Description",
                    "frequency": 24,
                    "eventList": ["DONE"],
                    "lastMarkedDone": "2023-01-01T00:00:00",
                }
            ],
        }
    )
