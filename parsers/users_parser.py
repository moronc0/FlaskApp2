from email_validator import validate_email, EmailNotValidError
from flask_restful import reqparse


def validate_email_arg(email):
    try:
        validate_email(email)
        return email
    except EmailNotValidError:
        raise ValueError('Error in email format')


parser = reqparse.RequestParser()

parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('nickname', required=True, type=str)
parser.add_argument('age', required=True, type=int)
parser.add_argument('country', required=False, type=str)
parser.add_argument('email', required=True, type=validate_email_arg)
parser.add_argument('password', required=True, type=str)
parser.add_argument('user_photo', required=False, type=str)
