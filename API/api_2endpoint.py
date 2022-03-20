from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('./data/users.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe obj to dict to send api
        return {'data': data}, 200  # return data and 200 OK
    
    def post(self):
        parser = reqparse.RequestParser()  # initialize required parameters
        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('./data/users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': [args['userId']],
                'name': [args['name']],
                'city': [args['city']],
                'locations': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('./data/users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK
   
    #put can be used here to add a cafe to a user. 
    #we can’t use POST as this returns a 401 Unauthorized code
    def put(self):
        parser = reqparse.RequestParser()
        parser = add_argument('userId', required=True)
        parser = add_argument('location', required=True)
        args = parser.parse_args()# parse arguments to dictionary

        data = pd.read_csv('./data/users.csv')

        if args['userId'] in list(data['userId']):
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])
            
            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)  # add userId arg
        args = parser.parse_args()
        
        # read our CSV
        data = pd.read_csv('./data/users.csv')
        
        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]
            # save back to CSV
            data.to_csv('./data/users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404


class Locations(Resource):
    def get(self):
        data = pd.read_csv('./data/locations.csv')
        data = data.to_dict()
        return {'data': data}, 200
    
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', required=True)
        parser.add_argument('rating', required=True)
        args = parser.parse_args() 

        data = pd.read_csv('./data/locations.csv')
    
        # check if location already exists
        if args['locationId'] in list(data['locationId']):
            # if locationId already exists, return 401 unauthorized
        #     return {
        #         'message': f"'{args['locationId']}' already exists."
        #     }, 409
        # else:
        #     # otherwise, we can add the new location record
        #     # create new dataframe containing new values
            new_data = pd.DataFrame({
                'locationId': [args['locationId']],
                'name': [args['name']],
                'rating': [args['rating']]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('locations.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required=True, type=int)
        #Whether the arguments default value should be stored if the argument is missing from the request.
        #if name is missing from request not store orginal value
        parser.add_argument('name', store_missing=False)
        parser.add_argument('rating', store_missing=False)
        args = parser.parse_args() # parse arguments to dictionary

        data = pd.read_csv('./data/locations.csv')

        # check that the location exists
        if args['locationId'] in list(data['locationId']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['locationId'] == args['locationId']]
            
            # if name has been provided, we update name
            if 'name' in args:
                user_data['name'] = args['name']
            # if rating has been provided, we update rating
            if 'rating' in args:
                user_data['rating'] = args['rating']
            
            # update data
            data[data['locationId'] == args['locationId']] = user_data
            data.to_csv('locations.csv', index=False)
            return {'data': data.to_dict()}, 200
        
        else:
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('locationId', required=True, type=int)
        args = parser.parse_args()

        data = pd.read_csv('locations.csv')
        

        if args['locationId'] in list(data['locationId']):
            data = data[data['locationId'] != args['locationId']]
            data.to_csv('locations.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }

   
api.add_resource(Users, '/users')  # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations

if __name__ == '__main__':
    app.run(debug=True)