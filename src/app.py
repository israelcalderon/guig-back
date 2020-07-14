import os
import dotenv
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from db import db
from resources import branch
from resources import commit
from resources import pull_request

dotenv.load_dotenv(verbose=True)

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_resource(branch.Branches, '/api/v1/branches', '/api/v1/branches/')

api.add_resource(branch.Branch,
                 '/api/v1/branches/<string:branch_name>',
                 '/api/v1/branches/<string:branch_name>/')

api.add_resource(commit.Commits,
                 '/api/v1/branches/<string:branch_name>/commits',
                 '/api/v1/branches/<string:branch_name>/commits/')

api.add_resource(
    commit.Commit,
    '/api/v1/branches/<string:branch_name>/commits/<string:commit_sha>',
    '/api/v1/branches/<string:branch_name>/commits/<string:commit_sha>/'
    )

api.add_resource(pull_request.PullRequest,
                 '/api/v1/pull-requests',
                 '/api/v1/pull-requests/')

api.add_resource(pull_request.MergePullRequest,
                 '/api/v1/pull-requests/<int:pull_request_id>/merge',
                 '/api/v1/pull-requests/<int:pull_request_id>/merge/')

api.add_resource(pull_request.ClosePullRequest,
                 '/api/v1/pull-requests/<int:pull_request_id>/close',
                 '/api/v1/pull-requests/<int:pull_request_id>/close/')

if __name__ == '__main__':
    db.init_app(app)
    CORS(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)
