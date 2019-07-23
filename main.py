from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggin4ever@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(2000))

    def __init__(self, name, content):
        self.name = name
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['title']
        content = request.form['content']
        new_post = Blog(post_name, content)
        db.session.add(new_post)
        db.session.commit()
    
        

    all_posts = Blog.query.all()
   # post = Blog.query.filter_by(completed=True).all()
    return render_template('home.html', title="Build a Blog!", blogs=all_posts)

@app.route("/new_entry")
def new_entry():
    return render_template('submission_form.html')

@app.route("/posted", methods=['POST', 'GET'])
def posted():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['content']

        title_error = ""
        body_error = ""
        if not (title):
            title_error="Title is required!"
        if not (body):
            body_error="Body is required!"

        if not title_error and not body_error:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return render_template('blogpost.html', title=title, body=body)
            #return render_template('posted.html', title="Content posted")
        else:
            return render_template('post.html', title="Content not posted", error1 = title_error, error2 = body_error)
    return render_template('notposted.html', title="Content not posted")



if __name__ == '__main__':
    app.run()