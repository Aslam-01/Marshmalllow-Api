from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqllite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def hello():
    return 'hello world'

class NoteModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable= False)
    content = db.Column(db.String(200),nullable=False)

# with app.app_context():
#     db.create_all()

# create marshmallow schema  from model
class Note_Schema(ma.Schema):
    class Meta:
        model = NoteModel
        fields = ['id','title','content']
noteschema=Note_Schema()
noteschema=Note_Schema(many=True)


@app.route('/note/',methods = ['GET'])
def note_list():
    all_notes = NoteModel.query.all()
    return jsonify(noteschema.dump(all_notes))
    return jsonify({"msg":"data retrieved"})


@app.route('/note/',methods=['POST'])
def create_note():
    title = request.json.get('title')
    content = request.json.get('content')
    note = NoteModel(title=title,content=content)
    print(note.content)
    db.session.add(note)
    db.session.commit()
    # return Note_Schema().jsonify(note)
    return jsonify({"message":"Create success ..."})

@app.route('/note/<int:note_id>/',methods=['GET'])
def note_detail(note_id):
    title=request.json.get('title','')
    content = request.json.get('content','')
    note = NoteModel.query.get(note_id)
    # return Note_Schema().jsonify(note)
    return jsonify({"message":"Retrieve success .."})

@app.route('/note/<int:note_id>/',methods=['PATCH'])
def update_note(note_id):
    title= request.json.get('title','')
    content=request.json.get('content','')
    note = NoteModel.query.get(note_id)

    note.title=title
    note.content=content
    db.session.add(note)
    db.session.commit()
    # return Note_Schema().jsonify(note)
    return jsonify({"message" : "Partially updated"})

@app.route('/note/<int:note_id>/',methods=['DELETE'])
def delete_note(note_id):
    note=NoteModel.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    # return Note_Schema().jsonify(note)
    return jsonify({"message" : "Delete..."})

if __name__ == '__main__':
    app.run(debug=True)
    # class List(list):
        # def f1(self):
            # pass