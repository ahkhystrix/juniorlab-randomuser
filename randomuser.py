import requests
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import SubmitField
app = Flask(__name__)
app.config["SECRET_KEY"] = "My first security key"


class GetRandomUsersForm(Form):
    submit = SubmitField("Get random users")


@app.route("/", methods=["GET", "POST"])
def index():
    form = GetRandomUsersForm()
    if form.validate_on_submit():
        users = get_randomuser(10)
        return render_template("list.html", users=users)
    return render_template("index.html", form=form)


def get_randomuser(count):
    """Get users from https://randomuser.me/ in JSON"""
    url = "https://randomuser.me/api/?results=" + str(count)
    r = requests.get(url)
    users = r.json()
    return users


if __name__ == "__main__":
    app.run(debug=True)
