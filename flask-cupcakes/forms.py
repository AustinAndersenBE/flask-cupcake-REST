from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class CupcakeForm(FlaskForm):
    flavor = StringField("Flavor", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired()])
    image = StringField("Image")
    submit = SubmitField("Add new cupcake")