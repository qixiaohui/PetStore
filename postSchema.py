from flask_marshmallow import Marshmallow
from postModel import Posts

ma = Marshmallow()

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Posts

post_schema = PostSchema()
posts_schema = PostSchema(many=True)