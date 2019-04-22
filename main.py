from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-ablog:mypassword@localhost:8889/build-ablog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
     
    def __init__(self,title,body):
        self.title = title
        self.body = body
    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False
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


      
    