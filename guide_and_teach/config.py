import os

class Config:
    SECRET_KEY= os.environ.get('GAT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')