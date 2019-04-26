from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz2:mypassword@localhost:8889/blogz2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner
    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def is_valid(self):
        if self.username and self.password:
            return True
        else:
            return False
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')
@app.route('/register', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

   

@app.route("/")

def index():
    return redirect("/blog")

    

@app.route("/blog")
def display_blog():   
    entry_id = request.args.get('id')  

    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('newblog.html',title="Build a Blog",entry=entry)
    else:  
        entry='' 
        all_entries = Blog.query.all()   
        return render_template('blog.html' ,title="Build a Blog",entry=entry,all_entries=all_entries)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    title_error=''
    new_body_error=''

    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_entry = Blog(new_title, new_body)

        
        if (new_title.strip()==""): 
            title_error="please fill the title"
        if (new_body.strip()==""):
            new_body_error="please fill the body"  
        return render_template('newpost.html',title="Create new blog entry",
                new_title=new_title,new_body=new_body, title_error=title_error,new_body_error=new_body_error)

        if ((not title_error) or (not new_body_error)):
             db.session.add(new_entry)
             db.session.commit()
             url = "/blog?id=" + str(new_entry.id)
             return redirect(url)
    return render_template('newpost.html',title="Create new blog entry",
                title_error=title_error,new_body_error=new_body_error)

if __name__ == '__main__':

    app.run()


      
    