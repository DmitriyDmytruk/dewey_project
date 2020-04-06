from webapp import db

from .mixins import SearchableMixin


article_tags = db.Table(
    "article_tags",
    db.Column(
        "tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True
    ),
    db.Column(
        "article_id",
        db.Integer,
        db.ForeignKey("articles.id"),
        primary_key=True,
    ),
)


class TagModel(db.Model):
    """
    Tag model
    """

    __tablename__ = "tags"
    __indexable__ = "name"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Tag {}>".format(self.name)


class ArticleModel(db.Model, SearchableMixin):
    """
    Article model
    """

    __tablename__ = "articles"
    __searchable__ = [
        "id",
        "title",
        "legal_language",
        "abstract",
        "effective_date",
        "updated_date",
        "state",
        "city",
        "county",
        "zip_code",
        "tags",
    ]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    legal_language = db.Column(db.String(128))
    abstract = db.Column(db.Text)
    effective_date = db.Column(db.Date)
    updated_date = db.Column(db.Date)
    tags = db.relationship(TagModel, secondary=article_tags)

    # Location fields
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))
    county = db.Column(db.String(128))
    zip_code = db.Column(db.String(20))

    def __repr__(self):
        return "<Article {}>".format(self.title)
