import pytest
from datetime import datetime, timedelta
from app.habit import Habit, HabitEvent

@pytest.fixture
def habit():
    return Habit("testName", "testDescription", 1)

def test_empty(habit):
    assert habit.name == "testName"
    assert habit.description == "testDescription"
    assert habit.frequency_in_hours == 1
    assert habit.eventList == []
    assert habit.lastMarkedDone == None


def test_fulfill(habit):
    habit.fulfill()
    assert habit.eventList == [HabitEvent.DONE]
    assert habit.lastMarkedDone != None


def test_fail(habit):
    habit.fail()
    assert habit.eventList == [HabitEvent.FAILED]
    assert habit.lastMarkedDone == None


def test_reset(habit):
    habit.fulfill()
    habit.reset()
    assert habit.eventList == []
    assert habit.lastMarkedDone == None


def test_is_streak_not_broken(habit):
    habit.fulfill()
    assert habit.is_streak_broken() == False


def test_is_streak_broken(habit):
    habit.fulfill()
    habit.lastMarkedDone = habit.lastMarkedDone - timedelta(hours=2)
    assert habit.is_streak_broken() == True


def test_is_streak_broken_on_empty(habit):
    assert habit.is_streak_broken() == True
