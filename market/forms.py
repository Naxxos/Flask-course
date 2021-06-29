from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    # Flaskform reconnait les fonction qui commence par validate et le nom du champ 'username'
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Ce nom d'utilisateur existe déjà, choisissez un autre nom d'utilisateur")

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError(
                "Cette adresse mail est déjà utilisée, choisissez une autre adresse mail")

    username = StringField(label='User name : ', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(
        label='Email address : ', validators=[Email(), DataRequired()])
    password1 = PasswordField(
        label='Password : ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(
        label='Confirm password : ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    username = StringField(label='User name : ', validators=[DataRequired()])
    password = PasswordField(
        label='Password : ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
