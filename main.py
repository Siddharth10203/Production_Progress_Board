import jinja2.exceptions
import sqlalchemy.exc
from flask import Flask, render_template, redirect, url_for, flash, request, current_app, abort
from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from forms import ProjectEntryForm
from sqlalchemy.orm import relationship
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production_projects.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database setup
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Project_code = db.Column(db.Integer,unique=True, nullable=False)
    Status = db.Column(db.Text, nullable=False)
    Description = db.Column(db.Text, nullable=False)

db.create_all()

# MAIN WEB BROWSER HANDLING CODE
@app.route('/')
def main_page():
    lprojects = Project.query.all()
    return render_template("index.html",all_proj=lprojects)

@app.route('/add', methods=['GET','POST'])
def addproject():
    addform = ProjectEntryForm()
    if request.method == 'POST':
        data = request.form.to_dict()

        # IDENTIFY IF THE PROJECT ALREADY EXISTS
        try:
            proj_exists = Project.query.filter_by(Project_code=data['proj']).first()
            if proj_exists.Project_code == data['proj']:
                flash("Project Already exists")
                return render_template("add-project.html", form=addform)
        except AttributeError:
            pass

        # ADD NEW PROJECT ONLY IF IT DOEN'T EXIST
        try:
            newitem = Project(Project_code=data['proj'],
                              Status=data['status'].upper(),
                              Description=data['desc'].upper())
            db.session.add(newitem)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("There was an error with your request.")
            return render_template("add-project.html", form=addform)
        return redirect(url_for('main_page'))
    else:
        return render_template("add-project.html", form=addform)

@app.route('/remove/<int:pcode>', methods=['GET'])
def removeproject(pcode):
    try:
        proj_to_remove = Project.query.filter_by(Project_code=pcode).first()
        db.session.delete(proj_to_remove)
        db.session.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        flash(f"Entry {proj_to_remove}, cannot be deleted!")

    return redirect(url_for('main_page'))

@app.route('/update/<int:pcode>/<string:status>', methods=['GET'])
def updateproject(pcode,status):
    try:
        proj_to_update = Project.query.filter_by(Project_code=pcode).first()
        proj_to_update.Status = status
        db.session.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        flash(f"Entry {proj_to_update}, cannot be updated!")

    return redirect(url_for('main_page'))

if __name__ == "__main__":
    app.run(debug=True)