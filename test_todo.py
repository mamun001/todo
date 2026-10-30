import json

import pytest

from todo import TodoList


def test_add_a_task():
    todos = TodoList()
    task_id = todos.add("buy milk")
    assert task_id == 1
    assert todos.list()[0].text == "buy milk"


def test_list_shows_tasks():
    todos = TodoList()
    todos.add("buy milk")
    todos.add("walk dog")
    assert [t.text for t in todos.list()] == ["buy milk", "walk dog"]


def test_done_marks_one_complete():
    todos = TodoList()
    first = todos.add("buy milk")
    todos.add("walk dog")
    todos.done(first)
    assert [t.done for t in todos.list()] == [True, False]


def test_done_with_bad_id_gives_an_error():
    todos = TodoList()
    todos.add("buy milk")
    with pytest.raises(ValueError):
        todos.done(99)


@pytest.mark.skip(reason="printing belongs to the CLI, which doesn't exist yet")
def test_empty_list_prints_a_message():
    pass


def test_save_then_load_restores_tasks(tmp_path):
    path = tmp_path / "todos.json"
    todos = TodoList()
    todos.add("buy milk")
    todos.done(todos.add("walk dog"))
    todos.save(path)

    loaded = TodoList().load(path)
    assert [(t.id, t.text, t.done) for t in loaded] == [
        (1, "buy milk", False),
        (2, "walk dog", True),
    ]


def test_load_continues_ids_after_highest(tmp_path):
    path = tmp_path / "todos.json"
    todos = TodoList()
    todos.add("buy milk")
    todos.add("walk dog")
    todos.save(path)

    reloaded = TodoList()
    reloaded.load(path)
    assert reloaded.add("water plants") == 3


def test_load_missing_file_returns_empty_list(tmp_path):
    todos = TodoList()
    assert todos.load(tmp_path / "missing.json") == []
    assert todos.list() == []


def test_load_replaces_existing_tasks(tmp_path):
    path = tmp_path / "todos.json"
    saved = TodoList()
    saved.add("buy milk")
    saved.save(path)

    todos = TodoList()
    todos.add("old task")
    todos.add("another old task")
    todos.load(path)
    assert [t.text for t in todos.list()] == ["buy milk"]


def test_save_overwrites_previous_file(tmp_path):
    path = tmp_path / "todos.json"
    first = TodoList()
    first.add("buy milk")
    first.add("walk dog")
    first.save(path)

    second = TodoList()
    second.add("water plants")
    second.save(path)

    assert [t.text for t in TodoList().load(path)] == ["water plants"]


def test_save_and_load_empty_list(tmp_path):
    path = tmp_path / "todos.json"
    TodoList().save(path)
    assert TodoList().load(path) == []


def test_load_corrupt_file_raises(tmp_path):
    path = tmp_path / "todos.json"
    path.write_text("not json {")
    with pytest.raises(json.JSONDecodeError):
        TodoList().load(path)
