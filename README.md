# Welcome to habitator!

This project aims to fullfill the backend needs of any habit-tracking application.

# How to run

After cloning the repo and activating the virtual environment, run:

```
python -m app.cli --help
```

This will result in a help message appearing that will tell you everything you need.

# How to use

If you want to add a Habit for a user, simply call:

```
python -m app.cli add-habit --username username --habit-name "habitname" --habit-description "habitdescription" --habit-frequency "habitfrequencyinhours"
```

If you want to read user's Habits, call:

```
python -m app.cli read --username username
```

You want to either mark a Habit as done or failed? Be my guest:

```
python -m app.cli mark-done --username username --habit-name "habitname"
python -m app.cli mark-failed --username username --habit-name "habitname"
```

There's many other functions available; listing them here wouldn't be wise. Remember: calling `python -m app.cli --help` is your best chance of survival!

# Testing

To test, run:

```
pytest
```

To check the test coverage, run:

```
pytest --cov=app
```