"""

5. Activity Planner

The following information is stored in a personal activity planner:

    Person: person_id, name, phone_number
    Activity: activity_id, person_id - list, date, time, description

Create an application to:

1.    Manage persons and activities. The user can add, remove, update, and list both persons and activities.
2.    Add/remove activities. Each activity can be performed together with one or several other persons, who are already in the user’s planner. Activities must not overlap (user cannot have more than one activity at any given time).
3.    Search for persons or activities. Persons can be searched for using name or phone number. Activities can be searched for using date/time or description. The search must work using case-insensitive, partial string matching, and must return all matching items.
4.    Create statistics:
      -  Activities for a given date. List the activities for a given date, in the order of their start time.
      -  Busiest days. This will provide the list of upcoming dates with activities, sorted in descending order of the free time in that day (all intervals with no activities).
      -  Activities with a given person. List all upcoming activities to which a given person will participate.
5.    Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying).


"""
from repository import binary_repo
from repository import text_repo
from repository import inmemory_repo
from ui.GUI import GUI
from ui.console import UI

if __name__ == '__main__':
    print('   Hello!\n')

    separator = " = "
    keys = {}
    with open('settings.properties') as f:

        for line in f:
            if separator in line:
                name, value = line.split(separator, 1)
                keys[name.strip()] = value.strip()
    f.close()

    if keys['repository'] == 'binary_repo':
        repo = binary_repo.Repository()
    elif keys['repository'] == 'text_repo':
        repo = text_repo.Repository()
    elif keys['repository'] == 'inmemory_repo':
        repo = inmemory_repo.Repository()
    else:
        raise ValueError('Unknown repository!')

    if keys['ui'] == 'UI':
        ui = UI()
    elif keys['ui'] == 'GUI':
        ui = GUI(repo)
    else:
        raise ValueError('Unknown ui!')
    ui.start()
