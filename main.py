from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blogpost'] 
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
    
@app.route("/blogpost", methods=['POST'])
def blogpost():
    title = "Build a Blog"

    if session:
        owner = User.query.filter_by(username = session['username']).first()

    if "id" in request.args:
        post_id = request.args.get('id')
        blog = Blog.query.filter_by(id = post_id).all()
        # username = User.query.get(owner.username)
        return render_template('blogpost.html', title = title, blog = blog, post_id = post_id)

    elif "user" in request.args:
        user_id = request.args.get('user')
        blog = Blog.query.filter_by(owner_id = user_id).all()
        return render_template('blogpost.html', title = title, blog = blog)

    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('blogpost.html', title = title, blog = blog)

@app.route("/login", methods=['POST', 'GET'])
def login():
    username = ""
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            username_error = "That user does not exist!"
            if username =="":
                username_error = "Please enter you user name!"

        if password =="":
            password_error = "Please enter yopur password"

        if user and user.password != password:
            password_error = "The password enter is incorrect!"
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/entry')
    
    return render_template('login.html', username=username, username_error=username_error, password_error=password_error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = ""
    username_error = ""
    password_error = ""
    verifypass_error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verifypass = request.form["verifypass"]

        existing_user = User.query.filter_by(username = username).first()

        if len(username) < 3 or username == "" or " " in username:
            username_error = "Please enter a valid user name at least 3 characters and no spaces"
        
        if len(password) < 3 or password == "" or " " in password:
            password_error = "Please enter a valid passwordat least 3 characters and no spaces!"
 
        if password != verifypass:
            password_error = "Passwords do not macth!"
            verifypass_error = "Passwords do not match!"

        if not username_error and not password_error and not verifypass_error:
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/new_entry')
            else:
                username_error = "That user name is already taken!"
    return render_template('signup.html', username = username, username_error = username_error, password_error = password_error, verifypass_error = verifypass_error)



@app.route("/new_entry", methods=['POST', 'GET'])
def create_post():
    title = ""
    content = ""
    title_error = ""
    content_error = ""
    owner = User.query.filter_by(username = session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title =="":
            title_error="Title is required!"
        if content =="":
            content_error="Post content is required!"

        if title_error == "" and content_error == "":
            new_post = Blog(title, content, owner)
            db.session.add(new_post)
            db.session.commit()
            

        return redirect('/blog?id={}'.format(new_post.id))

    return render_template('submission_form.html', title = title, content = content, title_error = title_error, content_error = content_error)

if __name__ == "__main__":
    app.run()


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')




if __name__ == '__main__':
    app.run()