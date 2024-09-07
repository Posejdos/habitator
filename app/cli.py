import click
from app.user import User
from app.habit import Habit


@click.group()
def cli():
    pass


# Create a new habit for user


@click.command()
@click.option("--username", default="Steve", help="The username of the person.")
@click.option(
    "--habit-name", prompt="Enter the name of the habit", help="The name of the habit."
)
@click.option(
    "--habit-description",
    prompt="Enter the description of the habit",
    help="The description of the habit.",
)
@click.option(
    "--habit-frequency",
    prompt="Enter the frequency of the habit in hours",
    help="The frequency of the habit in hours.",
)
def add_habit(username, habit_name, habit_description, habit_frequency):
    user = User(username, f"tests/{username}.json")
    user_found = user.try_load_data_from_json()

    if not user_found:
        click.echo(f"User not found: {username}")
        click.echo(f"Creating new user: {username}")
        user.save_data_to_json()

    new_habit = Habit(habit_name, habit_description, habit_frequency)
    user.habits.append(new_habit)
    user.save_data_to_json()

    click.echo(f"New habit created for user: {username}")

    for habit in user.habits:
        click.echo(habit)


# Mark done a habit for user


@click.command()
@click.option(
    "--username",
    prompt="Enter your username",
    help="The username of the user.",
)
@click.option(
    "--habit-name",
    prompt="Enter the name of the habit to mark as done",
    help="The name of the habit to mark as done.",
)
def mark_done(username, habit_name):
    user = User(username, f"tests/{username}.json")
    user_found = user.try_load_data_from_json()

    if not user_found:
        click.echo(f"User not found: {username}")
        return

    habit_found = False
    for habit in user.habits:
        if habit.name == habit_name:
            habit.fulfill()
            habit_found = True
            break

    if habit_found:
        user.save_data_to_json()
        click.echo(f"Habit '{habit_name}' marked as done for user: {username}")
    else:
        click.echo(f"Habit '{habit_name}' not found for user: {username}")


# Mark failed a habit for user


@click.command()
@click.option(
    "--username",
    prompt="Enter your username",
    help="The username of the user.",
)
@click.option(
    "--habit-name",
    prompt="Enter the name of the habit to mark as failed",
    help="The name of the habit to mark as failed.",
)
def mark_failed(username, habit_name):
    user = User(username, f"tests/{username}.json")
    user_found = user.try_load_data_from_json()

    if not user_found:
        click.echo(f"User not found: {username}")
        return

    habit_found = False
    for habit in user.habits:
        if habit.name == habit_name:
            habit.fail()
            habit_found = True
            break

    if habit_found:
        user.save_data_to_json()
        click.echo(f"Habit '{habit_name}' marked as failed for user: {username}")
    else:
        click.echo(f"Habit '{habit_name}' not found for user: {username}")


# ANALYTICS

# Read habits of user


@click.command()
@click.option("--username", default="Steve", help="The username of the person.")
def read(username):
    user = User(username, f"tests/{username}.json")
    user.try_load_data_from_json()

    if not user.habits:
        click.echo(f"No habits found for user: {username}")
        return

    click.echo(f"Habits for user: {username} \n")
    for habit in user.habits:
        click.echo(habit)


# Read habits of user with same periodicity


@click.command()
@click.option(
    "--username",
    prompt="Enter your username",
    help="The username of the user.",
)
@click.option(
    "--periodicity",
    prompt="Enter the periodicity in hours",
    type=int,
    help="The periodicity in hours to filter habits.",
)
def read_same_periodicity(username, periodicity):
    user = User(username, f"tests/{username}.json")
    user.try_load_data_from_json()

    if not user.habits:
        click.echo(f"No habits found for user: {username}")
        return

    filtered_habits = [
        habit for habit in user.habits if habit.frequency_in_hours == periodicity
    ]

    if not filtered_habits:
        click.echo(
            f"No habits found with periodicity {periodicity} hours for user: {username}"
        )
        return

    click.echo(f"Habits for user: {username} with periodicity {periodicity} hours\n")
    for habit in filtered_habits:
        click.echo(habit)


# Read the habit with the longest streak
@click.command()
@click.option(
    "--username",
    prompt="Enter your username",
    help="The username of the user.",
)
def longest_streak(username):
    user = User(username, f"tests/{username}.json")
    user.try_load_data_from_json()

    if not user.habits:
        click.echo(f"No habits found for user: {username}")
        return

    longest_streak_habit = None
    longest_streak_length = 0

    for habit in user.habits:
        streak = habit.get_longest_streak()
        if streak > longest_streak_length:
            longest_streak_length = streak
            longest_streak_habit = habit

    if longest_streak_habit:
        click.echo(
            f"The habit with the longest streak is '{longest_streak_habit.name}' with a streak of {longest_streak_length} events."
        )
    else:
        click.echo(f"No streaks found for user: {username}")


# Read a habits longest streak


@click.command()
@click.option(
    "--username",
    prompt="Enter your username",
    help="The username of the user.",
)
@click.option(
    "--habit-name",
    prompt="Enter the name of the habit",
    help="The name of the habit to get the longest streak for.",
)
def habit_longest_streak(username, habit_name):
    user = User(username, f"tests/{username}.json")
    user.try_load_data_from_json()

    if not user.habits:
        click.echo(f"No habits found for user: {username}")
        return

    habit_found = False
    for habit in user.habits:
        if habit.name == habit_name:
            longest_streak = habit.get_longest_streak()
            habit_found = True
            break

    if habit_found:
        click.echo(
            f"The longest streak for habit '{habit_name}' is {longest_streak} events."
        )
    else:
        click.echo(f"Habit '{habit_name}' not found for user: {username}")


cli.add_command(habit_longest_streak)
cli.add_command(longest_streak)
cli.add_command(read_same_periodicity)
cli.add_command(mark_failed)
cli.add_command(mark_done)
cli.add_command(add_habit)
cli.add_command(read)
if __name__ == "__main__":
    cli()
