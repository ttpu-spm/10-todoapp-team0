from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# In-memory storage for todos
todos = []
next_id = 1

@app.route('/')
def index():
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
    global next_id
    content = request.form.get('content')
    if content:
        todos.append({'id': next_id, 'content': content, 'completed': False})
        next_id += 1
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    content = request.form.get('content')
    if content:
        for todo in todos:
            if todo['id'] == todo_id:
                todo['content'] = content
                break
    return redirect(url_for('index'))

if __name__ == "__main__":
    # For development only
    app.run(debug=True, host='0.0.0.0', port=3310)
