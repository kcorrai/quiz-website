from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from quiz import quizzes

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
    
correct = 0
current_question_index = 0
    
@app.route('/', methods=['GET','POST'])
def index():
    global current_question_index, correct
    value = ''
    if request.method == 'POST':
        value = request.form['value']
        quiz = quizzes[value]
        selected_answer = request.form.get('answer')
        if selected_answer and value:
            quiz = quizzes[value]
            question_keys = list(quiz.keys())
            question_key = question_keys[current_question_index]
            correct_answer = quiz[question_key]['answer']

            if selected_answer == correct_answer:
                correct += 1
            else:
                pass

        if 'next' in request.form:
        # `i` değerini artır ve soruları döndür
            current_question_index = (current_question_index + 1) % len(quiz)
        elif 'prev' in request.form:
        # `i` değerini azalt ve soruları döndür
            current_question_index = (current_question_index - 1) % len(quiz)
        elif 'finish' in request.form:
            current_question_index = 0
            return redirect(url_for('finish'))
        
        question_keys = list(quiz.keys())
        question_key = question_keys[current_question_index]
        question = quiz[question_key]

        return render_template('index.html', value=value, question=question, current_question_index=current_question_index)
            
    else:
        return render_template('index.html', value=value)
    
@app.route('/finish')
def finish():
    global correct
    return render_template('result.html', correct=correct)

@app.route('/reset')
def reset():
    global correct
    correct = 0
    return redirect(url_for('index'))

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