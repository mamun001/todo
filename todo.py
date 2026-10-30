from dataclasses import dataclass


@dataclass
class Task:
    id: int
    text: str
    done: bool = False


class TodoList:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def add(self, text):
        task = Task(self._next_id, text)
        self._tasks[task.id] = task
        self._next_id += 1
        return task.id

    def list(self):
        return list(self._tasks.values())
        

    def done(self, id):
        if id not in self._tasks:
            raise ValueError(f"no task with id {id}")
        self._tasks[id].done = True
