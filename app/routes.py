from flask import render_template
from app import app

@app.route("/")
@app.route("/index")

def index():
    user = {'username':'Mikel'}
    posts = [
            {
                'author':{'username':'John'},
                'body':'Beautiful day in Portland!'
            },
            {
                'author':{'username':'Susan'},
                'body':'The Avengers movie was awful!'
            }
            ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/page1")
def page1():

    user = {'username':'Todd'}
    posts = [
            {
                'author':{'username':'Jeff'},
                'body':'Rainy day in Sacramento!'
            },
            {
                'author':{'username':'Sherri'},
                'body':'The art gallery visit was Enchanting!'
            }
            ]
    return render_template('index.html', title='Page1', user=user, posts=posts)



if __name__ == "__main__":
    app.run()
