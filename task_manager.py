from email.policy import default
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])

def index():
    if (request.method == 'POST'):
        task_content = request.form['content']
        new_task = Task(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error: Couldn't add task"
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('home.html', tasks = tasks)

if __name__ == "__main__":
    app.run(debug = True)