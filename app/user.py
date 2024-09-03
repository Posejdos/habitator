from datetime import datetime
from json_file import JSONFile
from habit import Habit, HabitEvent


class User:
    def __init__(self, name=None, jsonPath=None):
        self.name = name
        self.jsonFile: JSONFile = JSONFile(jsonPath)
        self.habits: list[Habit] = []

    def get_event_from_string(self, event):
        if event == "DONE":
            return HabitEvent.DONE
        elif event == "FAILED":
            return HabitEvent.FAILED
        else:
            return None

    def get_string_from_event(self, event):
        if event == HabitEvent.DONE:
            return "DONE"
        elif event == HabitEvent.FAILED:
            return "FAILED"
        else:
            return "ERROR"

    def parse_event_list(self, eventList):
        result = []
        for event in eventList:
            e = self.get_event_from_string(event)
            if e is not None:
                result.append(e)

        return result

    def parse_habit(self, jsonHabit):
        habitName = jsonHabit["name"]
        habitDescription = jsonHabit["description"]
        habitFrequency = jsonHabit["frequency"]
        habitEventList = jsonHabit["eventList"]
        habitLastMarkedDone = jsonHabit["lastMarkedDone"]

        newHabit = Habit(habitName, habitDescription, habitFrequency)
        newHabit.eventList = self.parse_event_list(habitEventList)

        if habitLastMarkedDone != "":
            newHabit.lastMarkedDone = datetime.strptime(
                habitLastMarkedDone, "%Y-%m-%dT%H:%M:%S"
            )

        self.habits.append(newHabit)

    def try_load_data_from_json(self):
        data = self.jsonFile.read()
        if data is None:
            return False

        self.name = data["name"]
        for habit in data["habits"]:
            self.parse_habit(habit)

        return True

    def save_data_to_json(self):
        data = {"name": self.name, "habits": []}
        for habit in self.habits:
            if habit.lastMarkedDone is None:
                data["habits"].append(
                    {
                        "name": habit.name,
                        "description": habit.description,
                        "frequency": habit.frequency_in_hours,
                        "eventList": [
                            self.get_string_from_event(event)
                            for event in habit.eventList
                        ],
                        "lastMarkedDone": "",
                    }
                )
            else:
                data["habits"].append(
                    {
                        "name": habit.name,
                        "description": habit.description,
                        "frequency": habit.frequency_in_hours,
                        "eventList": [
                            self.get_string_from_event(event)
                            for event in habit.eventList
                        ],
                        "lastMarkedDone": habit.lastMarkedDone.strftime(
                            "%Y-%m-%dT%H:%M:%S"
                        ),
                    }
                )

        self.jsonFile.write(data)
