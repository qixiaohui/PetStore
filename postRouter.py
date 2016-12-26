import sys
from flask import Flask, jsonify, abort, request
from postModel import db, User, Posts
from flask_login import LoginManager, current_user, login_required
from postSchema import ma, post_schema, posts_schema
app = Flask(__name__)

puppies = [{"name": "1", "image":"asda"},{"name":"2","image":"fsdf"}]

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db.init_app(app)
ma.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization');
    if not api_key:
        return None
    return User.query.filter_by(api_key=api_key).first()

@app.route("/api/post/list", methods=["GET"])
def getPostList():
    posts = Posts.query.all()
    return posts_schema.jsonify(posts)

@app.route("/api/post/<int:index>", methods=["GET"])
def getPost(index):
    post = Posts.query.filter(Posts.id==index).first_or_404()
    return post_schema.jsonify(post)

@app.route("/api/post/create", methods=["POST"])
def createPost():
    post, errors = post_schema.load(request.json)
    if errors:
        res = jsonify(errors)
        res.status_code = 400
        return res
    db.session.add(post)
    db.session.commit()
    res = jsonify({"message": "created"})
    res.status_code = 201
    res.headers["location"] = post.url
    return res

@app.errorhandler(404)
def page_not_found(error):
    res = jsonify({"error": "resource not found"})
    res.status_code = 404
    return res
@app.errorhandler(401)
def unauthorized(error):
    res = jsonify({"error": "unauthorized"})
    res.status_code = 401
    return res


if __name__ == "__main__":
    if "create_db" in sys.argv:
        with app.app_context():
            db.create_all()
    else:
        app.run(debug=True)