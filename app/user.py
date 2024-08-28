from datetime import datetime
from json_file import JSONFile
from habit import Habit, HabitEvent


class User:
    def __init__(self, name=None, jsonPath=None):
        self.name = name
        self.jsonFile = JSONFile(jsonPath)
        self.habits = []

    def parse_event_list(self, eventList):
        result = []
        for event in eventList:
            if event == "DONE":
                result.append(HabitEvent.DONE)
            elif event == "FAILED":
                result.append(HabitEvent.FAILED)

        return result

    def parse_habit(self, jsonHabit):
        habitName = jsonHabit["name"]
        habitDescription = jsonHabit["description"]
        habitFrequency = jsonHabit["frequency"]
        habitEventList = jsonHabit["eventList"]
        habitLastMarkedDone = jsonHabit["lastMarkedDone"]

        newHabit = Habit(habitName, habitDescription, habitFrequency)
        newHabit.eventList = self.parse_event_list(habitEventList)
        newHabit.lastMarkedDone = datetime.strptime(
            habitLastMarkedDone, "%Y-%m-%dT%H:%M:%S"
        )

        self.habits.append(newHabit)

    def try_load_data_from_json(self):
        data = self.jsonFile.read()
        if data is None:
            return

        self.name = data["name"]
        for habit in data["habits"]:
            self.parse_habit(habit)