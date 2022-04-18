MOODS = [
    {
        "id": 1,
        "label": "Happy"
    },
    {
        "id": 2,
        "label": "Sad"
    },
    {
        "id": 3,
        "label": "Angry"
    },
    {
        "id": 4,
        "label": "Ok"
    }
]

def get_all_moods():
    return MOODS

def get_single_mood(id):
    # Variable to hold the found mood, if it exists
    requested_mood = None

    # Iterate the MOODS list above
    for mood in MOODS:
        if mood["id"] == id:
            requested_mood = mood

    return requested_mood

def create_mood(mood):
    # Get the id value of the last mood in the list
    max_id = MOODS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the mood dictionary
    mood["id"] = new_id

    # Add the mood dictionary to the list
    MOODS.append(mood)

    # Return the dictionary with `id` property added
    return mood