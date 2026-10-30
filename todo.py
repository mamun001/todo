import argparse
import json
import sys
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


def main(argv=None):
    parser = argparse.ArgumentParser(description="A simple todo list.")
    parser.add_argument("--file", default="todo.json", help="JSON file to store tasks in")
    commands = parser.add_subparsers(dest="command", required=True)

    add_cmd = commands.add_parser("add", help="add a task")
    add_cmd.add_argument("text", nargs="+", help="task text")
    commands.add_parser("list", help="list tasks")
    done_cmd = commands.add_parser("done", help="mark a task complete")
    done_cmd.add_argument("id", type=int, help="task ID")

    args = parser.parse_args(argv)
    todos = TodoList()
    todos.load(args.file)

    if args.command == "add":
        task_id = todos.add(" ".join(args.text))
        todos.save(args.file)
        print(f"Added task {task_id}")
    elif args.command == "list":
        tasks = todos.list()
        if not tasks:
            print("No tasks.")
        for task in tasks:
            mark = "x" if task.done else " "
            print(f"[{mark}] {task.id}: {task.text}")
    elif args.command == "done":
        try:
            todos.done(args.id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        todos.save(args.file)
        print(f"Completed task {args.id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
