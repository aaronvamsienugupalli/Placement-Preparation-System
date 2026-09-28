import json
import os


def load_json(filename):
    """Load data from a JSON file."""

    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    """Save data to a JSON file."""

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_data(filename, new_data):
    """Add new data to an existing JSON file."""

    data = load_json(filename)

    data.append(new_data)

    save_json(filename, data)