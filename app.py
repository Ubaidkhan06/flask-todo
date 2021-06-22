from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mysupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Creating models


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f'{self.title} {self.description}')


# Creating Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    if (request.method == 'POST'):
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)
