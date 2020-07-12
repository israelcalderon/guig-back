from __future__ import annotations
from db import db
from datetime import datetime
from typing import Union


class PullRequest(db.Model):

    __tablename__ = 'pull_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(255))
    status = db.Column(db.String(10))
    author = db.Column(db.String(150))
    source_branch = db.Column(db.String(200))
    destiny_branch = db.Column(db.String(200))
    commit = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    # status
    OPEN = 'open'
    CLOSED = 'closed'
    MERGED = 'merged'

    def __repr__(self):
        return f'<PullRequest( {self.id}, {self.title}, {self.status})>'

    def create_or_update(self):
        """
        Store current object in db
        """
        db.session.add(self)
        db.session.commit()

    def as_dict(self) -> dict:
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'status': self.status,
                'author': self.author,
                'source_branch': self.source_branch,
                'destiny_branch': self.destiny_branch,
                'commit': self.commit,
                'created_at': self.created_at.isoformat()}

    @classmethod
    def get(cls) -> list:
        """
        TODO: implement pagination
        TODO: implement filters
        Return a collection of pull requests from db
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, pull_request_id: int) -> Union[PullRequest, None]:
        """
        Retrieve pull request or None if id not found
        """
        return cls.query.filter_by(id=pull_request_id).first()
