import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'\x8e\xa3\x1f\xa6\xdbti\x1b\x91s\x95\xd3\xa3\x00^\x1e'

    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "enrollments.db")

    