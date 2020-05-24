from dotenv import load_dotenv
load_dotenv()
import os

from application import create_app, socketio

app = create_app()

# if __name__ == "__main__" and os.getenv("LOCAL") == "True":
#     print("Running on http://localhost:5000/")
#     socketio.run(app)

if __name__ == "__main__":
    print("Running on http://localhost:5000/")
    socketio.run(app)

