#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response(
            {"message": "Welcome to the Newsletter RESTful API"},
            200
        )

api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        return make_response(newsletters, 200)

    def post(self):
        data = request.get_json()  # Use JSON data

        new_record = Newsletter(
            title=data.get('title'),
            body=data.get('body')
        )

        db.session.add(new_record)
        db.session.commit()

        return make_response(new_record.to_dict(), 201)

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.get(id)

        if not newsletter:
            return make_response({"error": "Newsletter not found"}, 404)

        return make_response(newsletter.to_dict(), 200)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
