import git
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = '06c2e0da2228af49ebeae9b1ceadde75'

@app.route("/")
def hello_world():
    return render_template('home.html', subtitle='Home Page', text='This is Dar\'s Dash!')
    
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='About me!', text='Here are some interesting facts about me.')
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        username = form.username.data
        return redirect(url_for('third_page', username=username)) # if so - send to secret third page
    return render_template('register.html', title='Register', form=form)

@app.route("/secret_gallery/<username>")
def third_page(username):
  return render_template('third_page.html', subtitle='Secret Gallery??', text='These are some of my fav pictures! Just so you can get to know me a little more.', username=username)


@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/CHANGE_TO_PYTHON_ANYWHERE_USERNAME/CHANGE_TO_GITHUB_REPO_NAME')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
