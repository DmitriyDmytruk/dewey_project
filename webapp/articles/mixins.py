from webapp import db

from .search import add_to_index, remove_from_index


class SearchableMixin:
    """Updates indexes"""

    @classmethod
    def before_commit(cls, session) -> None:
        """Adds ``_changes`` dict to session object"""
        session._changes = {  # pylint: disable=protected-access
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session) -> None:
        """Updates indexes"""
        # fmt: off
        for obj in session._changes["add"]:  # pylint: disable=protected-access
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:  # pylint: disable=protected-access
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:  # pylint: disable=protected-access
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None  # pylint: disable=protected-access
        # fmt: on

    @classmethod
    def reindex(cls) -> None:
        """Reindex"""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
