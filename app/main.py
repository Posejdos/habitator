import click
from user import User
from habit import Habit


@click.group()
def cli():
    pass


# Read Habits of user


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


cli.add_command(read)
if __name__ == "__main__":
    cli()
