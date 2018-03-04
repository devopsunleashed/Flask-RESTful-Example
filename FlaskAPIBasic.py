from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


# Callback function to get password
@auth.get_password
def get_password(username):
    if username == 'devopsunleasheduser':
        return 'devopsunleashedpassword'
    return None


# Callback to send an authentication error back to the client
@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

# Sample data for testing
SampleList = {
    '1': {'task': 'Entry 1'}
}
 
# Argument parser - must add all arguments explicitly here
parser = reqparse.RequestParser()
parser.add_argument('task_item')
parser.add_argument('id')


# Check if item exists and error if it doesn't
def error_if_item_doesnt_exist(id):
    if id not in SampleList:
        abort(404, message="SampleList {} doesn't exist".format(id))


# Check if item exists and error if it does
def error_if_item_does_exist(id):
    if id in SampleList:
        abort(404, message="SampleList {} exist".format(id))


# Define get, delete, and put method class
# Put = Update\Replace
# Get = Read
# Delete = Delete
class APISampleItem(Resource):

    decorators = [auth.login_required]

    def get(self, id):
        error_if_item_doesnt_exist(id)
        return SampleList[id]

    def delete(self, id):
        error_if_item_doesnt_exist(id)
        del SampleList[id]
        return '', 204

    def put(self, id):
        args = parser.parse_args()
        SampleList[id] = {'task': args['task_item']}
        return SampleList[id], 201


# Define get and post method class
# Post = Create
# Get = Read list
class APISampleList(Resource):
    decorators = [auth.login_required]

    def get(self):
        return SampleList

    def post(self):
        args = parser.parse_args()
        error_if_item_does_exist(args['id'])
        SampleList[args['id']] = {'task': args['task_item']}
        return SampleList[args['id']], 201


# Setup Api Resourceful Routing to classes here
api.add_resource(APISampleItem, '/listitems/<id>')
api.add_resource(APISampleList, '/listitems')


# If program is executed itself, then run
if __name__ == '__main__':
    app.run(debug=True)


