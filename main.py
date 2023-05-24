from website import create_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

