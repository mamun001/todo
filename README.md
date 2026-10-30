# todo

A small command-line todo list written in Python. Tasks are stored in a JSON file.

## Requirements

Python 3. No third-party packages are needed to run it; [pytest](https://pytest.org) is needed to run the tests.

## Usage

```
$ python3 todo.py add buy milk
Added task 1
$ python3 todo.py add walk dog
Added task 2
$ python3 todo.py done 1
Completed task 1
$ python3 todo.py list
[x] 1: buy milk
[ ] 2: walk dog
```

| Command | What it does |
|---|---|
| `add TEXT` | Adds a task and prints its ID. Quotes around the text are optional. |
| `list` | Lists all tasks; `[x]` marks completed ones. Prints `No tasks.` when there are none. |
| `done ID` | Marks a task complete. Exits with status 1 if there is no task with that ID. |

Tasks are saved to `todo.json` in the current directory. Use `--file` to choose another file:

```
python3 todo.py --file ~/work-todos.json list
```

## Using it from Python

```python
from todo import TodoList

todos = TodoList()
todos.load("todo.json")   # returns [] if the file doesn't exist
task_id = todos.add("buy milk")
todos.done(task_id)       # raises ValueError for an unknown ID
print(todos.list())
todos.save("todo.json")
```

## Running the tests

```
python3 -m pytest
```
