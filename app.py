#! usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_cors import CORS
from ext import db
from schema import schema
from flask_graphql_auth import (
    GraphQLAuth,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    auth = GraphQLAuth(app)
    app.secret_key = app.config['SECRET_KEY']
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                     schema=schema, graphiql=True, context={'session': db.session}))
    app.url_map.strict_slashes = False
    db.init_app(app)
    @app.route('/')
    def hello_world():
        return 'Go to /graphql'

    return app


app = create_app()
CORS(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
