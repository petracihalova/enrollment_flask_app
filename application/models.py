from application import db, ma
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(30), unique=True)
    password = Column(String)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Model):
    course_id = Column(String(10), primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    level = Column(Integer)
    term = Column(String(25))


class Enrollment(db.Model):
    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey("user.user_id"))
    course_id = Column(String(10), db.ForeignKey("course.course_id"))


class CourseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
    
    course_id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    level = ma.auto_field()
    term = ma.auto_field()


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
