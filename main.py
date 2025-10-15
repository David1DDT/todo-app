from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=True)


@app.route("/")
def index():
    # show all todos
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_todo():
    # Logic to add a new todo item
    new_task = request.form.get("task")
    if new_task:
        new_todo = Todo()
        new_todo.task = new_task
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo added successfully!", "success")
    return redirect(url_for("index"))


@app.route('/delete', methods=['POST'])
def delete_todo():
    todo_id = request.form.get('id')
    if todo_id:
        todo = Todo.query.get(todo_id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            flash('Todo deleted', 'info')
    return redirect(url_for('index'))



if __name__ == "__main__":
    # ensure tables exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)