from flask_restful import Resource
from typing import Union
from git_repo import repository
import gitdb


class Commit(Resource):
    """
    Resource for specific commit
    """

    def get(self, branch_name: str, commit_sha: str) -> Union[dict, tuple]:
        """
        Get the specific commit requested
        """
        try:
            commit = repository.commit(commit_sha)
        except gitdb.exc.BadName:
            return {'message': f'No commit found with id {commit_sha}'}, 404

        return {'commit': commit.hexsha,
                'author': commit.author.name,
                'message': commit.message,
                'email': commit.author.email,
                'files': len(commit.stats.files),
                'datetime': commit.committed_datetime.isoformat()}


class Commits(Resource):
    """
    Resource for listing many commits from branch
    """

    def get(self, branch_name: str) -> Union[list, tuple]:
        """
        TODO: implement pagination
        search for all the commits in the given branch_name
        """
        try:
            repository.heads[branch_name]
        except IndexError:
            return {'message': f'No branch found with id {branch_name}'}, 404
        # TODO: use max_count and skip for results pagination
        commits = list(repository.iter_commits(branch_name))

        result_commits = []

        for commit in commits:
            result_commits.append({
                'commit': commit.hexsha,
                'author': commit.author.name,
                'message': commit.message,
                'email': commit.author.email,
                'files': len(commit.stats.files),
                'datetime': commit.committed_datetime.isoformat()
            })

        return result_commits
