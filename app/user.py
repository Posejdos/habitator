from json_file import JSONFile
from habit import Habit

class User:
    def __init__(self, name = None, jsonPath = None):
        self.name = name
        self.jsonFile = JSONFile(jsonPath)
        self.habits = []

    def load_data_from_json(self):
        data = self.jsonFile.read()
        if data is not None:
            for habitData in data:
                habitName = habitData["name"]
                habitDescription = habitData["description"]
                habitFrequency = habitData["frequency"]

                # Load stats if they exist
                if "stats" in habitData:
                    habitStats = HabitStats(
                        habitData["stats"]["eventList"],
                        habitData["stats"]["lastMarkedDone"],
                    )
                else:
                    habitStats = None

                habit = Habit(habitName, habitDescription, habitFrequency, habitStats)
                self.habits.append(habit)

    def greet(self):
        return f"Hello {self.name}!"
