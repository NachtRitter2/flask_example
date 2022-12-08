from app import app, db, cli
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'main.user':User, 'Post':Post}
