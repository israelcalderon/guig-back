from flask_restful import Resource
from typing import Union

from git_repo import repository


class Branch(Resource):
    """
    Resource for one branch
    """

    def get(self, branch_name) -> Union[dict, tuple]:
        """
        Search the requested branch in repository
        """
        try:
            branch = repository.heads[branch_name]
        except IndexError:
            return {'message': f'No branch found with id {branch_name}'}, 404
        else:
            return {'name': branch.name,
                    'commit': branch.commit.hexsha,
                    'datetime': branch.commit.committed_datetime.isoformat()}


class Branches(Resource):
    """
    Resource for list of Branch
    """

    def get(self) -> list:
        """
        Returns a list of branches
        """
        branches = []

        for branch in repository.heads:
            branches.append({
                'name': branch.name,
                'commit': branch.commit.hexsha,
                'datetime': branch.commit.committed_datetime.isoformat()
            })

        return branches
