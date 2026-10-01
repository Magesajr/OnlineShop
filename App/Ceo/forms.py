from wtforms import (
TelField,DateField,TextAreaField,
SelectMultipleField,FloatField,SelectField,
StringField,SubmitField,FileField,ColorField)
from wtforms.validators import (
    DataRequired,Length,Email,EqualTo,ValidationError,Optional
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed


class ProductForm(FlaskForm):
    name=StringField('Product\'s name',validators=[DataRequired()])
    price=StringField('Price',validators=[DataRequired()])
    specs=TextAreaField('specifications',validators=[DataRequired()])
    img=FileField('Add product image',validators=[FileAllowed('jpeg png jpg'.split(),'only png jpeg jpg are allowed')])
    submit=SubmitField('add')


class UpdateForm(FlaskForm):
    name=StringField('Product\'s name',validators=[DataRequired()])
    price=StringField('Price',validators=[DataRequired()])
    specs=TextAreaField('specifications',validators=[DataRequired()])
    img=FileField('Choose a file',validators=[DataRequired()])
    submit=SubmitField('Update')

    