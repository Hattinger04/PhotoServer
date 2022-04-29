import datetime
import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.sql.expression import func

from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
import base64

# UPLOAD_FOLDER = r'PATH\PhotoServer\static'
import keysServer

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata
engine = create_engine(
    r'sqlite:///C:\Users\s8gre\Documents\Schule\4BHWII\UC\PhotoServer\photos.sqlite3')  # Welche Datenbank wird verwendet
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()

ex_01_subscription_key = keysServer.ex_01_subscription_key
ex_02_subscription_key = keysServer.ex_02_subscription_key
ex_04_subscription_key = keysServer.ex_04_subscription_key
ex_04_endpoint = keysServer.ex_04_endpoint


class Photo(Base):
    __tablename__ = 'Photos'

    ID = Column(Integer, primary_key=True)
    TITLE = Column(Text, nullable=False)
    DEVICE = Column(Text, nullable=False)
    UPLOADDATE = Column(DateTime, default=func.now())
    PICTURE = Column(Text, nullable=False)
    EXTENSION = Column(Text, nullable=False)
    DESCRIPTION = Column(Text)
    ANALYSIS = Column(Text)
    RECOGNITION = Column(Text)

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


def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)


class AzureServices():
    # TODO: make json better
    def analyseImage(self, name):
        endpoint = "germanywestcentral"
        credentials = CognitiveServicesCredentials(ex_02_subscription_key)
        client = ComputerVisionClient(endpoint="https://" + endpoint + ".api.cognitive.microsoft.com/",
                                      credentials=credentials)
        image_analysis = client.analyze_image_in_stream(open(name, "rb"), visual_features=[VisualFeatureTypes.tags])
        info = []
        for tag in image_analysis.tags:
            info.append(str(tag))
        analysis = client.describe_image_in_stream(open(name, "rb"), 3, "en")
        for caption in analysis.captions:
            info.append(caption.confidence)
        return json.dumps(info)

    def recognizeImage(self, image):
        return ""


class File(Resource):
    def get(self, id):
        photo = Photo.query.get(id)
        if not photo:
            return jsonify({"message": "does not exist"})
        return photo.serialize()

    def put(self, id):
        services = AzureServices()
        if request.form["EXTENSION"] not in ALLOWED_EXTENSIONS:
            return jsonify({"message": "wrong extension"})
        analysis = ""
        recognition = ""
        path = "img/%s.%s" % (str(id), request.form["EXTENSION"])
        if request.form["SERVICE"] == "analysis":
            decode_Base64(path, request.form["PICTURE"])
            analysis = json.dumps(services.analyseImage(path))
        elif request.form["SERVICE"] == "recognition":
            recognition = services.recognizeImage(request.form["PICTURE"])
        else:
            response = "no/unknown service!"
        picture = Photo(TITLE=request.form["TITLE"], DEVICE=request.form["DEVICE"],
                        UPLOADDATE=datetime.datetime.strptime(request.form["UPLOADDATE"], '%Y-%m-%d %H:%M:%S.%f'), \
                        PICTURE=request.form["PICTURE"], EXTENSION=request.form["EXTENSION"],
                        DESCRIPTION=request.form["DESCRIPTION"], ANALYSIS=analysis, RECOGNITION=recognition)

        db_session.add(picture)
        db_session.flush()
        return jsonify({'message': 'file stored', "analysis": analysis, "recognition": recognition })

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
