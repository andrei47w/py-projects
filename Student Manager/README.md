# Students Manager
## Requirements

- You will be given one of the problems below to solve using feature-driven development
- The program must provide a menu-driven console user interface.
- Use classes to represent the following:
    - The domain entity (`complex`,  `expense`,  `student`, `book`)
    - A services class that implements the required functionalities
    - The ui class which implements the user interface
- Have 10 programmatically generated entries in the application at start-up.
- Unit tests and specifications for non-UI functions related to the first functionality.

1. You must implement two additional repository sets: one using text files for storage, and one using binary files (e.g. using object serialization with [Pickle](https://docs.python.org/3.8/library/pickle.html)).
2. The program must work the same way using in-memory repositories, text-file repositories and binary file repositories.
3. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file. An example is below:

    a. `settings.properties` for loading from memory (input files are not required):
    ```
    repository = inmemory
    cars = “”
    clients = “”
    rentals = “”
    ```
    b. `settings.properties` for loading from binary files, for someone who also created a GUI:
    ```
    repository = binaryfiles
    cars = “cars.pickle”
    clients = “clients.pickle”
    rentals = “rentals.pickle”
    ui = “GUI”
    ```
- Implement an iterable data structure. Study the [`__setItem__`](https://docs.python.org/3/reference/datamodel.html#object),`__getitem__`, `__delItem__`, `__next__` and `__iter__` Python methods.
- Implement a sorting algorithm that was not studied during the lecture or seminar (no bubble sort, cocktail sort, merge sort, insert sort, quicksort). You can use one of shell sort, comb sort, bingo sort, gnome sort, or other sorting method. Prove that you understand the sorting method implemented. The sort function will accept two parameters: the list to be sorted as well as a comparison function used to determine the order between two elements.
- Implement a filter function that can be used to filter the elements from a list. The function will use 2 parameters: the list to be filtered, and an acceptance function that decided whether a given value passes the filter.

## Problem Statement
---
###  Students
Manage a list of students. Each student has an `id` (integer, unique), a `name` (string) and a `group` (positive integer). Provide the following features:
1. Add a student. Student data is read from the console.
2. Display the list of students.
3. Filter the list so that students in a given group (read from the console) are deleted from the list.
4. Undo the last operation that modified program data. This step can be repeated.

