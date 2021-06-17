from flask import Flask, abort
from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
api_app = Api(app, version='1.0', title='Student Listings', description='Hello World! This is a test API.')

name_space = api_app.namespace('student', description='API for basic CRUD ops')

students = {
    1:{'name':'John','age':14,'gender':'male'},
    2:{'name':'Doe','age':16,'gender':'female'},
    3:{'name':'Will','age':15,'gender':'male'}
}

args = reqparse.RequestParser()
args.add_argument('name',type=str,help="student_name",required=True)
args.add_argument('age',type=int,help="student_age",required=True)
args.add_argument('gender',type=str,help="student_gender",required=True)

@name_space.route('/<int:student_id>')
class MainClass(Resource):
    @api_app.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, student_id):
        if student_id in students:
            return students[student_id],200
        else:
            return {'data':'Not Found'},404

    @api_app.doc(responses={201: 'Created', 409: 'Already Exists'},params={'name': 'student_name','age':'student_age','gender':'student_gender' })
    def post(self, student_id):
        x = args.parse_args()
        if student_id in students:
            abort(409, "Video ID already exists.")
        students[student_id]=x
        return students[student_id], 201

    @api_app.doc(responses={200: 'Deleted', 404: 'Not Found'})
    def delete(self, student_id):
        if student_id not in students:
            return {'data': 'Not Found'}, 404
        else:
            del students[student_id]
            return {'data':'Deleted'},200


if __name__=='__main__':
    app.run(debug=True)

