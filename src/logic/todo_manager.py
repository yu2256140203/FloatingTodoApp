import json
import os
import uuid
from datetime import datetime

class TodoManager:
    def __init__(self, filepath="todos.json"):
        self.filepath = filepath
        self.todos = []
        self.load_todos()

    def load_todos(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
            except:
                self.todos = []
        else:
            self.todos = []
        return self.todos

    def save_todos(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, indent=4)

    def add_todo(self, text):
        new_todo = {
            'id': str(uuid.uuid4()),
            'text': text,
            'done': False,
            'created_at': datetime.now().isoformat()
        }
        self.todos.append(new_todo)
        self.save_todos()
        return new_todo

    def remove_todo(self, todo_id):
        self.todos = [t for t in self.todos if t['id'] != todo_id]
        self.save_todos()

    def update_todo(self, todo_id, is_done):
        for t in self.todos:
            if t['id'] == todo_id:
                t['done'] = is_done
                break
        self.save_todos()

    def get_pending_count(self):
        return sum(1 for t in self.todos if not t['done'])
