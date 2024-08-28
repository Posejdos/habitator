from datetime import datetime, timedelta
from enum import Enum


class HabitEvent(Enum):
    DONE = 1
    FAILED = 2


class Habit:
    def __init__(self, name, description, frequency_in_hours):
        self.name = name
        self.description = description
        self.frequency_in_hours = frequency_in_hours
        self.eventList = []
        self.lastMarkedDone = None

    def fulfill(self):
        self.eventList.append(HabitEvent.DONE)
        self.lastMarkedDone = datetime.now()

    def fail(self):
        self.eventList.append(HabitEvent.FAILED)

    def reset(self):
        self.eventList = []
        self.lastMarkedDone = None

    def is_streak_broken(self):
        if self.lastMarkedDone is None:
            return True

        now = datetime.now()
        timeSinceDone = now - self.lastMarkedDone
        maxWait = timedelta(hours=self.frequency_in_hours)
        return timeSinceDone > maxWait

    def __str__(self):
        return (
            f"Habit(name='{self.name}', description='{self.description}', "
            f"frequency_in_hours={self.frequency_in_hours}, "
            f"doneCnt={self.stats.doneCnt}, failedCnt={self.stats.failedCnt}, "
            f"currentStreak={self.stats.currentStreak}, longestStreak={self.stats.longestStreak})"
        )
