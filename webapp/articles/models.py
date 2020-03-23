from webapp import db


class LocationModel(db.Model):
    """
    Location model
    """

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))
    county = db.Column(db.String(128))
    zip_code = db.Column(db.String(20))

    def __repr__(self):
        return "<Location {}, {}>".format(self.city, self.zip_code)


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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Tag {}>".format(self.name)


class ArticleModel(db.Model):
    """
    Article model
    """

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    legal_language = db.Column(db.String(128))
    abstract = db.Column(db.Text)
    effective_date = db.Column(db.Date)
    updated_date = db.Column(db.Date)
    tags = db.relationship(TagModel, secondary=article_tags)

    def __repr__(self):
        return "<Article {}>".format(self.title)
