from flask import Blueprint, jsonify, request
import os

from data import db_session
from data.images import Images
from parsers import images_parser

blueprint = Blueprint('images_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/v1/images')
def get_images():
    session = db_session.create_session()
    images = session.query(Images).all()
    session.close()
    return jsonify(
        {
            'images': [item.to_dict() for item in images]
        }
    )


@blueprint.route('/api/v1/images/<int:image_id>')
def get_one_image(image_id):
    session = db_session.create_session()
    images = session.query(Images).get(image_id)
    session.close()

    if not images:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'image': images.to_dict()
        }
    )


@blueprint.route('/api/v1/images/', methods=['POST'])
def add_image():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    args = images_parser.parser.parse_args()
    session = db_session.create_session()

    image = Images(
        title=args['title'],
        about=args.get['about'],
        owner=args['owner'],
        tags=args['tags'],
        image_name=args['image_name']
    )

    session.add(image)
    session.commit()
    session.close()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/v1/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    session = db_session.create_session()
    image = session.query(Images).get(image_id)
    if not image:
        session.close()
        return jsonify({'error': 'Not found'})

    session.delete(image)
    session.commit()

    image_path = os.path.join('static', image.image_name)
    if os.path.exists(image_path):
        os.remove(image_path)

    session.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/v1/images/<int:image_id>', methods=['PUT'])
def edit_image(image_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    args = images_parser.parser.parse_args()
    session = db_session.create_session()
    image = session.query(Images).get(image_id)

    image.title = args['title']
    image.about = args.get('about')
    image.owner = args['owner']
    image.tags = args['tags']
    image.image_name = args['image_name']

    session.commit()
    session.close()
    return jsonify({'success': 'OK'})
