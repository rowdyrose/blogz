from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggin4ever@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():
    all_posts = Blog.query.all()
    
    
    blog_id = request.args.get('id')
    if blog_id:
        blog_entry = Blog.query.get(blog_id)
        return render_template('blogpost.html', post=blog_entry)
        
    return render_template('home.html', title="Build a Blog!", blogs=all_posts)

@app.route("/new_entry")
def new_entry():
    return render_template('submission_form.html')

@app.route("/blogpost", methods=['POST'])
def blogpost():
    title = request.args['title']
    content = request.args['content']
    return render_template('blogpost.html', title=title, content=content)

@app.route("/entry", methods=['POST', 'GET'])
def posted():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        title_error = ""
        content_error = ""
        if not (title):
            title_error="Title is required!"
        if not (content):
            content_error="Body is required!"

        if not title_error and not content_error:
                new_post = Blog(title, content)
                db.session.add(new_post)
                db.session.commit()
                return redirect('/?id={0}'.format(new_post.id))
    
        return render_template('submission_form.html', title="Content not posted", error1 = title_error, error2 = content_error)







if __name__ == '__main__':
    app.run()