from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    pub_date = db.Column(db.DateTime)

    def __init__(self,title,body,owner,pub_date=None):
        self.title = title
        self.body = body
        self.owner = owner
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
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
    
@app.before_request
def require_login():
    allowed_routes = ['login', 'display_blog','index','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/', methods=['GET', 'POST'])
def index():
    
    users=User.query.all()
    return render_template('index.html',users=users)


@app.route("/blog", methods=['GET'])
def display_blog():   
    
    entry_id = request.args.get('id')
    user_id=request.args.get('userid')
    posts = Blog.query.order_by(Blog.pub_date.desc())
    if (entry_id):
        post = Blog.query.filter_by(id=entry_id).first()
        return render_template('newblog.html',title=post.title,post=post, posts=posts,pub_date=post.pub_date, user_id=post.owner_id,username=post.owner.username)
    if (user_id):
        entries=Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html',posts=posts,entries=entries)
    else:
        users=User.query.all()
        entries=Blog.query.all()
        print(entries) 
       

        return render_template('blog.html',entries=entries,users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/newpost')
        if not user:
            flash("Not a valid user")
            return redirect('/signup')
            
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    title_error=''
    new_body_error=''
    owner = User.query.filter_by(username=session['username']).first()


    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']

        new_entry = Blog(new_title, new_body,owner)

        
        if (new_title.strip()=="") and(new_body.strip()==""):
            title_error="please fill the title"
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


      
    