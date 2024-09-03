import pytest
from datetime import datetime, timedelta
from app.habit import Habit, HabitEvent


@pytest.fixture
def habit():
    return Habit("testName", "testDescription", 1)


def test_empty(habit: Habit):
    assert habit.name == "testName"
    assert habit.description == "testDescription"
    assert habit.frequency_in_hours == 1
    assert habit.eventList == []
    assert habit.lastMarkedDone == None


def test_fulfill(habit: Habit):
    habit.fulfill()
    assert habit.eventList == [HabitEvent.DONE]
    assert habit.lastMarkedDone != None


def test_fail(habit: Habit):
    habit.fail()
    assert habit.eventList == [HabitEvent.FAILED]
    assert habit.lastMarkedDone == None


def test_reset(habit: Habit):
    habit.fulfill()
    habit.reset()
    assert habit.eventList == []
    assert habit.lastMarkedDone == None


def test_is_streak_not_broken(habit: Habit):
    habit.fulfill()
    assert habit.is_streak_broken() == False


def test_is_streak_broken(habit: Habit):
    habit.fulfill()
    habit.lastMarkedDone = habit.lastMarkedDone - timedelta(hours=2)
    assert habit.is_streak_broken() == True


def test_is_streak_broken_on_empty(habit: Habit):
    assert habit.is_streak_broken() == True

def test_get_longest_streak_zero(habit: Habit):
    assert habit.get_longest_streak() == 0

def test_get_longest_streak_one(habit: Habit):
    habit.fulfill()
    assert habit.get_longest_streak() == 1

def test_get_longest_streak_after_fail(habit: Habit):
    habit.fulfill()
    habit.fulfill()
    habit.fail()
    habit.fulfill()
    assert habit.get_longest_streak() == 2