from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField,SubmitField,DateField,PasswordField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from ..models import User 

class RegisterForm(FlaskForm):
    username=StringField('username',
                         validators=[DataRequired('Enter username'),
                                     Length(min=6,max=10,message='username is not less than 6 characters but not more than 10 characters')])
    email=StringField('email',validators=[Email()])
    address=StringField('address',validators=[DataRequired()])
    phonenumber=StringField('phonenumber',validators=[DataRequired(),Length(min=10,max=15)])
    submit=SubmitField('register')

    def validate_phonenumber(self,phonenumber):
        if not str(phonenumber.data).startswith('+255') and not str(phonenumber.data).startswith('0'):
            raise ValidationError('Invalid phonenumber')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email existed')

class LoginForm(FlaskForm):    
    email=StringField('email',validators=[Email()])
    token=PasswordField('Token',
                         validators=[DataRequired('insert token sent from email'),
                                     Length(min=6,max=6)])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid Email')
        
class TokenForm(FlaskForm):
    email=StringField('email',validators=[DataRequired()],description='enter your email')
    submit=SubmitField('send token')
    
    # def validate_email(self,email):
    #     user=User.query.filter_by(email=email.data).first()
    #     if not user:
    #         raise ValidationError('Invalid Email')
        
        