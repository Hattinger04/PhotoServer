import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.sql.expression import func

from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# UPLOAD_FOLDER = r'PATH\PhotoServer\static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(
    r'sqlite:///C:\Users\s8gre\Documents\Schule\4BHWII\UC\PhotoServer\photos.sqlite3')  # Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()


class Photo(Base):
    __tablename__ = 'Photos'

    ID = Column(Integer, primary_key=True)
    TITLE = Column(Text, nullable=False)
    DEVICE = Column(Text, nullable=False)
    UPLOADDATE = Column(DateTime, default=func.now())
    PICTURE = Column(Text, nullable=False)
    EXTENSION = Column(Text, nullable=False)
    DESCRIPTION = Column(Text)

    def serialize(self):
        return {
            "ID": str(self.ID),
            "TITLE": self.TITLE,
            "DEVICE": self.DEVICE,
            "UPLOADDATE": str(self.UPLOADDATE),
            "PICTURE": self.PICTURE,
            "EXTENSION": self.EXTENSION,
            "DESCRIPTION": self.DESCRIPTION
        }


def allowed_file(filename):
    '''
    :param filename:
    :return: true if filename has any of the supported extensions
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class File(Resource):
    def get(self, id):
        photo = Photo.query.get(id)
        if not photo:
            return jsonify({"message": "does not exist"})
        return photo.serialize()

    def put(self, id):
        if request.form["EXTENSION"] not in ALLOWED_EXTENSIONS:
            return jsonify({"message": "wrong extension"})
        # creating file and store in static
        # with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as fp:
        #    fp.write(request.data)

        picture = Photo(TITLE=request.form["TITLE"], DEVICE=request.form["DEVICE"],
                        UPLOADDATE=datetime.datetime.strptime(request.form["UPLOADDATE"], '%Y-%m-%d %H:%M:%S.%f'), \
                        PICTURE=request.form["PICTURE"], EXTENSION=request.form["EXTENSION"],
                        DESCRIPTION=request.form["DESCRIPTION"])
        db_session.add(picture)
        db_session.flush()
        return jsonify({'message': 'file stored'})

    def delete(self, id):
        photo = Photo.query.get(id)
        if not photo:
            return jsonify({'message': 'File does not exist: %s' % id})
        db_session.delete(photo)
        db_session.flush()
        return jsonify({'message': '%s deleted' % id})


api.add_resource(File, '/file/<string:id>')


def createDb():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    createDb()
    app.run(debug=True, host="0.0.0.0")
