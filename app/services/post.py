from app.models import PostModel


def list_post():
    posts = PostModel.query.order_by(PostModel.date_created.desc()).all()
    return [p.to_json() for p in posts]


def create_post(data):
    new_post = PostModel(**data)
    new_post.save()
    return new_post.to_json()


def get_post(post_id):
    post = PostModel.find_by_id(post_id)
    return post.to_json()
