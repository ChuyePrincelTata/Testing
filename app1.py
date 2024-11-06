from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        # Validate input
        if not title or not content:
            flash('Title and content are required!', 'danger')
            return render_template('create_post.html', title='New Post')
            
        if len(title) > 100:
            flash('Title must be less than 100 characters!', 'danger')
            return render_template('create_post.html', title='New Post')

        post = Post(title=title, content=content)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your post.', 'danger')
            return render_template('create_post.html', title='New Post')

    return render_template('create_post.html', title='New Post')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)