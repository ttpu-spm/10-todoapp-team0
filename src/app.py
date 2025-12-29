from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# File storage
DATA_FILE = 'todos.json'

def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(todos, f, indent=4)
    except IOError as e:
        print(f"Error saving todos: {e}")

# Load todos on startup
todos = load_todos()

def get_next_id():
    if not todos:
        return 1
    return max(t['id'] for t in todos) + 1

@app.route('/')
def index():
    # Reload todos to ensure we have the latest state (optional, but good for consistency if multiple processes)
    # global todos
    # todos = load_todos() 
    
    filter_status = request.args.get('filter', 'all')
    
    if filter_status == 'active':
        filtered_todos = [t for t in todos if not t['completed']]
    elif filter_status == 'completed':
        filtered_todos = [t for t in todos if t['completed']]
    else:
        filtered_todos = todos
        
    return render_template('index.html', todos=filtered_todos, filter=filter_status)

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form.get('content')
    if content:
        new_todo = {'id': get_next_id(), 'content': content, 'completed': False}
        todos.append(new_todo)
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            save_todos(todos)
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    content = request.form.get('content')
    if content:
        for todo in todos:
            if todo['id'] == todo_id:
                todo['content'] = content
                save_todos(todos)
                break
    return redirect(url_for('index'))

if __name__ == "__main__":
    # For development only
    app.run(debug=True, host='0.0.0.0', port=3310)
