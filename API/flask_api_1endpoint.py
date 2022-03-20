from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        # Write method to fetch data from the CSV file
        data = pd.read_csv('users.csv')
        #we connot pass pands dataframe object to api so we need to convert this into dictionary
        data = data.to_dict('records')
        return {'data' : data}, 200


    def post(self):
        # Write method to write data to the CSV file
        # read the arguments from request and pass them in variables
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True) #you can add 'type' if need to data too
        parser.add_argument('age', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'name'      : [args['name']],
            'age'       : [args['age']],
            'city'      : [args['city']]
        })
        # add the newly provided values
        data = data.append(new_data, ignore_index = True)
        data.to_csv('users.csv', index=False) # save back to CSV
        return {'data' : new_data.to_dict('records')}, 201 # return data with 200 OK

    def delete(self):
        # Write method to update data in the CSV file
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        data = data[data['name'] != args['name']]

        data.to_csv('users.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200



# Add URL endpoints
# it route to in order to execute the requested operation.
api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run()