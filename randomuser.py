import requests
import os
import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "My first security key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"
    pk = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(64))
    name_title = db.Column(db.String(64))
    name_first = db.Column(db.String(64))
    name_last = db.Column(db.String(64))
    location_street = db.Column(db.String(64))
    location_city = db.Column(db.String(64))
    location_state = db.Column(db.String(64))
    location_postcode = db.Column(db.String(64))
    location_coordinates_latitude = db.Column(db.String(64))
    location_coordinates_longitude = db.Column(db.String(64))
    location_timezone_offset = db.Column(db.String(64))
    location_timezone_description = db.Column(db.String(64))
    email = db.Column(db.String(64))
    login_uuid = db.Column(db.String(64))
    login_username = db.Column(db.String(64))
    login_password = db.Column(db.String(64))
    login_salt = db.Column(db.String(64))
    login_md5 = db.Column(db.String(64))
    login_sha1 = db.Column(db.String(64))
    login_sha256 = db.Column(db.String(64))
    registered_date = db.Column(db.String(64))
    registered_age = db.Column(db.String(64))
    dob_date = db.Column(db.String(64))
    dob_age = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    cell = db.Column(db.String(64))
    id_name = db.Column(db.String(64))
    id_value = db.Column(db.String(64))
    picture_large = db.Column(db.String(64))
    picture_medium = db.Column(db.String(64))
    picture_thumbnail = db.Column(db.String(64))
    nat = db.Column(db.String(64))


class Form(FlaskForm):
    get = SubmitField("Get random users and save to local database")
    list = SubmitField("List random users from local database")


class Filter(FlaskForm):
    first_filter = StringField()
    first = SubmitField("First Name Filter")
    last_filter = StringField()
    last = SubmitField("Last Name Filter")
    email_filter = StringField()
    email = SubmitField("E-Mail Filter")


@app.route("/", methods=["GET", "POST"])
def index():
    form = Form()
    filter = Filter()
    if form.validate_on_submit() and form.get.data:
        result = get_randomusers(100)
        return render_template("index.html", result=result, form=form)
    elif form.validate_on_submit() and form.list.data:
        users = list_randomusers()
        return render_template("list.html", users=users, filter=filter)
    elif filter.validate_on_submit() and filter.first.data:
        users = list_randomusers_filtered_first(filter.first_filter.data)
        return render_template("list.html", users=users, filter=filter)
    elif filter.validate_on_submit() and filter.last.data:
        users = list_randomusers_filtered_last(filter.last_filter.data)
        return render_template("list.html", users=users, filter=filter)
    elif filter.validate_on_submit() and filter.email.data:
        users = list_randomusers_filtered_email(filter.email_filter.data)
        return render_template("list.html", users=users, filter=filter)
    else:
        return render_template("index.html", form=form)


def get_randomusers(count):
    """Get users from https://randomuser.me/ in JSON and save to local database"""
    url = "https://randomuser.me/api/?results=" + str(count)
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as err:
        return "Something Else: " + str(err)
    except requests.exceptions.HTTPError as errh:
        return "Http Error: " + str(errh)
    except requests.exceptions.ConnectionError as errc:
        return "Error Connecting: " + str(errc)
    except requests.exceptions.Timeout as errt:
        return "Timeout Error: " + str(errt)

    users = r.json()
    db.drop_all()
    db.create_all()
    for user in users["results"]:
        record = Users(gender = user["gender"],
                       name_title = user["name"]["title"],
                       name_first = user["name"]["first"],
                       name_last = user["name"]["last"],
                       location_street = user["location"]["street"],
                       location_city = user["location"]["city"],
                       location_state = user["location"]["state"],
                       location_postcode = user["location"]["postcode"],
                       location_coordinates_latitude = user["location"]["coordinates"]["latitude"],
                       location_coordinates_longitude = user["location"]["coordinates"]["longitude"],
                       location_timezone_offset = user["location"]["timezone"]["offset"],
                       location_timezone_description = user["location"]["timezone"]["description"],
                       email = user["email"],
                       login_uuid = user["login"]["uuid"],
                       login_username = user["login"]["username"],
                       login_password = user["login"]["password"],
                       login_salt = user["login"]["salt"],
                       login_md5 = user["login"]["md5"],
                       login_sha1 = user["login"]["sha1"],
                       login_sha256 = user["login"]["sha256"],
                       registered_date = user["registered"]["date"],
                       registered_age=user["registered"]["age"],
                       dob_date = user["dob"]["date"],
                       dob_age = user["dob"]["age"],
                       phone = user["phone"],
                       cell = user["cell"],
                       id_name = user["id"]["name"],
                       id_value = user["id"]["value"],
                       picture_large = user["picture"]["large"],
                       picture_medium = user["picture"]["medium"],
                       picture_thumbnail = user["picture"]["thumbnail"],
                       nat = user["nat"],
                       )
        db.session.add(record)
    db.session.commit()
    return "Random's users has been loaded to local database"


def list_randomusers():
    """List all users from local database"""
    users = Users.query.all()
    return users


def list_randomusers_filtered_first(first):
    """List users from local database. Filtered by First"""
    users = Users.query.filter(Users.name_first.ilike("%" + first + "%"))
    return users


def list_randomusers_filtered_last(last):
    """List all users from local database. Filtered by Last"""
    users = Users.query.filter(Users.name_last.ilike("%" + last + "%"))
    return users


def list_randomusers_filtered_email(email):
    """List all users from local database. Filtered by Email"""
    users = Users.query.filter(Users.email.ilike("%" + email + "%"))
    return users


if __name__ == "__main__":
    app.run(debug=True)
