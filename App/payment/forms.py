from wtforms import (
TelField,DateField,BooleanField,
SelectMultipleField,FloatField,SelectField,
StringField,SubmitField,FileField,EmailField,PasswordField,ColorField)
from wtforms.validators import (
    DataRequired,Length,Email,EqualTo,ValidationError,Optional
)
from flask_wtf import FlaskForm

choices='USD TZS KES'.split()


class BillFillForm(FlaskForm):
    name=StringField('Customer Name',validators=[DataRequired()]) 
    email=EmailField('Email',validators=[Optional(),Email('invalid email')]) 
    phonenumber=StringField('phonenumber',validators=[Optional()]) 
    Amount=FloatField('Amount',validators=[DataRequired()]) 
    city=StringField('city',validators=[Optional()])
    currency=SelectField('choose currency',choices=choices) 
    description=StringField('discription',validators=[Optional()])
    shipped=BooleanField('Need a deliverly?',validators=[Optional()])
    submit=SubmitField('Pay')
    
class RefundForm(FlaskForm):
    name=StringField('Customer Name',validators=[DataRequired()]) 
    email=EmailField('Email',validators=[DataRequired(),Email('invalid email')]) 
    confirm_code=StringField('confirmation Code',validators=[DataRequired()]) 
    Amount=FloatField('Amount',validators=[DataRequired()])  
    remarks=StringField('discription',validators=[Optional()])
    #submit=SubmitField('Request')
