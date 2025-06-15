from flask_restful import reqparse


parser = reqparse.RequestParser()

parser.add_argument('title', required=True, type=str)
parser.add_argument('about', required=False, type=str)
parser.add_argument('owner', required=True, type=int)
parser.add_argument('tags', required=True, type=str)
parser.add_argument('image_name', required=True, type=str)
