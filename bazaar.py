from app import app, db, socketio
from app.models import User, Bid, Balance


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Bid": Bid, "Balance": Balance}


if __name__ == "__main__":
    socketio.run(app)
