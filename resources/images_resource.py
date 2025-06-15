import os

from flask import jsonify
from flask_restful import Resource, abort


from data import db_session
from data.images import Images
from parsers import images_parser


def abort_if_image_not_found(image_id):
    session = db_session.create_session()
    images = session.query(Images).get(image_id)
    session.close()

    if not images:
        abort(404, message=f"Image {image_id} not found")


class ImageResource(Resource):
    def get(self, image_id):
        abort_if_image_not_found(image_id)
        session = db_session.create_session()
        image = session.query(Images).get(image_id)

        session.close()

        return jsonify(
            {
                'image': image.to_dict()
            }
        )

    def delete(self, image_id):
        abort_if_image_not_found(image_id)
        session = db_session.create_session()
        image = session.query(Images).get(image_id)

        session.delete(image)
        session.commit()

        image_path = os.path.join('static', image.image_name)
        if os.path.exists(image_path):
            os.remove(image_path)

        session.close()

        return jsonify({'success': 'OK'})


class ImageListResource(Resource):
    def get(self):
        session = db_session.create_session()
        images = session.query(Images).all()
        session.close()

        return jsonify(
            {
                'images': [item.to_dict() for item in images]
            }
        )

    def post(self):
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
