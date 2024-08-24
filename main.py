from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(70))
    textarea = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        textarea = request.form['idea']

        contact = User(email=email, textarea=textarea)
        db.session.add(contact)
        db.session.commit()

        return redirect('/')
    
    else:
        return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)