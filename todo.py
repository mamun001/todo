import json
from dataclasses import asdict, dataclass


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

    def save(self, path):
        with open(path, "w") as f:
            json.dump([asdict(t) for t in self._tasks.values()], f, indent=2)

    def load(self, path):
        try:
            with open(path) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        self._tasks = {d["id"]: Task(**d) for d in data}
        self._next_id = max(self._tasks, default=0) + 1
        return self.list()
