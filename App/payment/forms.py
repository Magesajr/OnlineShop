from wtforms import (
TelField,BooleanField,FloatField,SelectField,TextAreaField,
StringField,SubmitField,FileField,EmailField,)
from wtforms.validators import (
    DataRequired,Length,Email,EqualTo,ValidationError,Optional
)
from flask_wtf import FlaskForm

choices='USD TZS KES'.split()


class LipaInitForm(FlaskForm):
    phone=StringField('phonenumber',validators=[DataRequired('phonenumber needed'),Length(max=12,min=12)],default='255')
    provider=SelectField('Network',choices='AIRTEL VODACOM YAS HALOTEL'.split())
    description=TextAreaField('Description',validators=[Optional()],description='After press pay button confirm payment on your Phone within 30s')
    submit=SubmitField('Pay')

    def validate_phone(self,phone):
        if not phone.data.startswith('255'):
            raise ValidationError('phonumber must starts with 255!')



class LipaWithdrawForm(FlaskForm):
    amount=StringField('amount',validators=[DataRequired()])
    phone=StringField('phonenumber',validators=[DataRequired('phonenumber needed'),Length(max=12,min=12)],default='255')
    provider=SelectField('Network',choices='AIRTEL VODACOM YAS HALOTEL'.split())
    description=TextAreaField('Description',validators=[Optional()])
    submit=SubmitField('Withdraw')


    def validate_phone(self,phone):
        if not phone.data.startswith('255'):
            raise ValidationError('phonumber must starts with 255!')




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




