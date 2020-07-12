from flask_restful import Resource, reqparse
from git_repo import repository
from typing import Union
from models import models
import git


class PullRequest(Resource):
    """
    Resource for pull requests handling
    """

    parser = reqparse.RequestParser()

    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    parser.add_argument('description',
                        type=str,
                        required=False)

    parser.add_argument('source_branch',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    parser.add_argument('destiny_branch',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self) -> Union[dict, tuple]:
        """
        Create a new pull request
        """
        data = PullRequest.parser.parse_args()

        try:
            for branch in ('source_branch', 'destiny_branch'):
                repository.heads[data[branch]]
        except IndexError:
            return {'message': f'Invalid {branch} {data[branch]}'}, 400

        git_config = repository.config_reader()

        pull_request = models.PullRequest(**data)
        pull_request.status = pull_request.OPEN
        pull_request.author = git_config.get_value('user', 'email')
        pull_request.create_or_update()

        return pull_request.as_dict(), 201

    def get(self) -> list:
        """
        TODO: implement pagination
        TODO: implement filters
        Retrieve a list of pull requests
        """
        pull_requests = models.PullRequest.get()

        if not pull_requests:
            return []

        return [pr.as_dict() for pr in pull_requests]


class MergePullRequest(Resource):
    """
    Merge open pull requests
    """

    def post(self, pull_request_id: int) -> Union[dict, tuple]:
        """
        Merge pull request for id provided
        """
        pull_request = models.PullRequest.get_by_id(pull_request_id)

        if not pull_request:
            error = {
                'message': f'No pull request found with id {pull_request_id}'
            }
            return error, 404

        if pull_request.status != models.PullRequest.OPEN:
            error = {
                'message': f'Cannot merge a pull request with status {pull_request.status}'
            }
            return error, 400

        repository.git.checkout(pull_request.destiny_branch)

        try:
            result = repository.git.merge(pull_request.source_branch)
        except git.exc.GitCommandError as err:
            error = err.stdout

            if error and 'conflict' in error.lower():
                repository.git.merge('--abort')
                error = f'Merge was aborted because of server response: {error}'

            return {'message': error}, 400
        except Exception as ex:
            return {'message': str(ex)}, 500
        else:
            pull_request.status = models.PullRequest.MERGED
            pull_request.commit = repository.head.commit.hexsha
            pull_request.create_or_update()
            return {'message': result or 'suceess'}


class ClosePullRequest(Resource):
    """
    Close open pull request
    """

    def post(self, pull_request_id: int) -> Union[dict, tuple]:
        """
        Merge pull request for id provided
        """
        pull_request = models.PullRequest.get_by_id(pull_request_id)

        if not pull_request:
            error = {
                'message': f'No pull request found with id {pull_request_id}'
            }
            return error, 404

        if pull_request.status != models.PullRequest.OPEN:
            error = {
                'message': f'Cannot close a pull request with status {pull_request.status}'
            }
            return error, 400

        pull_request.status = models.PullRequest.CLOSED
        pull_request.create_or_update()
        return {'message': 'suceess'}
