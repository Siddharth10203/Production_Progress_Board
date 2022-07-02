from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, Email
#from flask_ckeditor import CKEditorField

##WTForm
class ProjectEntryForm(FlaskForm):
    proj = IntegerField("Project Code:", validators=[DataRequired()])
    status = StringField("Status:", validators=[DataRequired()])
    desc = StringField("Description:", validators=[DataRequired()])
    #desc = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Register Project")