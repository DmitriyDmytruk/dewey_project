from .. import db


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
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))
    county = db.Column(db.String(128))
    zip_code = db.Column(db.String(20))

    def __repr__(self):
        return "<Article {}>".format(self.title)
