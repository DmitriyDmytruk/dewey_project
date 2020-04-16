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


article_categories = db.Table(
    "article_categories",
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True,
    ),
    db.Column(
        "article_id",
        db.Integer,
        db.ForeignKey("articles.id"),
        primary_key=True,
    ),
)


class CategoryModel(db.Model):
    """
    Category model
    """

    __tablename__ = "categories"
    __indexable__ = "name"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Category {}>".format(self.name)


class ArticleModel(db.Model, SearchableMixin):
    """
    Article model
    """

    __tablename__ = "articles"
    __searchable__ = [
        "id",
        "title",
        "legal_language",
        "citation",
        "cfr40_part280",
        "local_regulation",
        "abstract",
        "categories",
        "effective_date",
        "updated_date",
        "state",
        "city",
        "county",
        "tags",
    ]

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(30), nullable=False, unique=True)
    title = db.Column(db.String(500), nullable=False)
    legal_language = db.Column(db.Text, nullable=False)
    citation = db.Column(db.String(255), nullable=False)
    cfr40_part280 = db.Column(db.Text, nullable=False)
    local_regulation = db.Column(db.Text)
    abstract = db.Column(db.Text)
    categories = db.relationship(CategoryModel, secondary=article_categories)
    effective_date = db.Column(db.Date)
    updated_date = db.Column(db.Date)
    tags = db.relationship(TagModel, secondary=article_tags)

    # Location fields
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))
    county = db.Column(db.String(128))

    def __repr__(self):
        return "<Article {}>".format(self.title)
