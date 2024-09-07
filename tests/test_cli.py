import pytest
import os
from click.testing import CliRunner
from app.cli import cli
from app.user import User
from app.habit import Habit

test_user_file = "tests/test_user.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Create a test user file
    user = User("test_user", test_user_file)
    user.save_data_to_json()
    yield
    # Teardown: Remove the test user file
    if os.path.exists(test_user_file):
        os.remove(test_user_file)


# Test: habit-longest-streak
def test_habit_longest_streak_user_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ['habit-longest-streak', '--username', 'nonexistent_user', '--habit-name', 'test_habit'])
    assert "No habits found" in result.output

def test_habit_longest_streak_no_habits():
    runner = CliRunner()
    result = runner.invoke(cli, ['habit-longest-streak', '--username', 'test_user', '--habit-name', 'test_habit'])
    assert "No habits found for user: test_user" in result.output

def test_habit_longest_streak_habit_not_found():
    user = User("test_user", test_user_file)
    user.habits.append(Habit("other_habit", "description", 24))
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['habit-longest-streak', '--username', 'test_user', '--habit-name', 'test_habit'])
    assert "Habit 'test_habit' not found for user: test_user" in result.output

def test_habit_longest_streak_success():
    user = User("test_user", test_user_file)
    habit = Habit("test_habit", "description", 24)
    habit.fulfill()  # Simulate fulfilling the habit to create a streak
    user.habits.append(habit)
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['habit-longest-streak', '--username', 'test_user', '--habit-name', 'test_habit'])
    assert "The longest streak for habit 'test_habit' is 1 events." in result.output


# Test: add-habit
def test_add_habit_new_user():
    runner = CliRunner()
    result = runner.invoke(cli, ['add-habit', '--username', 'new_user', '--habit-name', 'exercise', '--habit-description', 'Daily exercise', '--habit-frequency', '24'])
    assert "Creating new user: new_user" in result.output
    assert "New habit created for user: new_user" in result.output
    new_user_path = "tests/new_user.json"
    assert os.path.exists(new_user_path)
    os.remove(new_user_path)


def test_add_habit_existing_user():
    user = User("test_user", test_user_file)
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['add-habit', '--username', 'test_user', '--habit-name', 'exercise', '--habit-description', 'Daily exercise', '--habit-frequency', '24'])
    assert "New habit created for user: test_user" in result.output


# Test: mark-done
def test_mark_done_habit_found():
    user = User("test_user", test_user_file)
    habit = Habit("exercise", "Daily exercise", 24)
    user.habits.append(habit)
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['mark-done', '--username', 'test_user', '--habit-name', 'exercise'])
    assert "Habit 'exercise' marked as done for user: test_user" in result.output

def test_mark_done_habit_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ['mark-done', '--username', 'test_user', '--habit-name', 'nonexistent_habit'])
    assert "Habit 'nonexistent_habit' not found for user: test_user" in result.output


# Test: mark-failed
def test_mark_failed_habit_found():
    user = User("test_user", test_user_file)
    habit = Habit("exercise", "Daily exercise", 24)
    user.habits.append(habit)
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['mark-failed', '--username', 'test_user', '--habit-name', 'exercise'])
    assert "Habit 'exercise' marked as failed for user: test_user" in result.output

def test_mark_failed_habit_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ['mark-failed', '--username', 'test_user', '--habit-name', 'nonexistent_habit'])
    assert "Habit 'nonexistent_habit' not found for user: test_user" in result.output


# Test: read
def test_read_no_habits():
    runner = CliRunner()
    result = runner.invoke(cli, ['read', '--username', 'test_user'])
    assert "No habits found for user: test_user" in result.output

def test_read_with_habits():
    user = User("test_user", test_user_file)
    user.habits.append(Habit("exercise", "Daily exercise", 24))
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['read', '--username', 'test_user'])
    assert "Habits for user: test_user" in result.output
    assert "exercise" in result.output


# Test: read-same-periodicity
def test_read_same_periodicity_no_habits():
    runner = CliRunner()
    result = runner.invoke(cli, ['read-same-periodicity', '--username', 'test_user', '--periodicity', 24])
    assert "No habits found for user: test_user" in result.output

def test_read_same_periodicity_with_habits():
    user = User("test_user", test_user_file)
    user.habits.append(Habit("exercise", "Daily exercise", 24))
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['read-same-periodicity', '--username', 'test_user', '--periodicity', 24])
    assert "Habits for user: test_user with periodicity 24 hours" in result.output
    assert "exercise" in result.output


# Test: longest-streak
def test_longest_streak_no_habits():
    runner = CliRunner()
    result = runner.invoke(cli, ['longest-streak', '--username', 'test_user'])
    assert "No habits found for user: test_user" in result.output

def test_longest_streak_success():
    user = User("test_user", test_user_file)
    habit1 = Habit("exercise", "Daily exercise", 24)
    habit2 = Habit("read", "Daily reading", 24)
    habit1.fulfill()
    habit2.fulfill()
    habit2.fulfill()
    user.habits.extend([habit1, habit2])
    user.save_data_to_json()

    runner = CliRunner()
    result = runner.invoke(cli, ['longest-streak', '--username', 'test_user'])
    assert "The habit with the longest streak is 'read' with a streak of 2 events." in result.output
