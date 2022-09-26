from importlib.resources import Resource
import sqlite3
import string
from typing_extensions import Required
from flask_restful import Resource,reqparse

class User():
    def __init__(self,_id,username,password) -> None:
        self.id=_id
        self.username=username
        self.password=password 
    @classmethod
    def find_by_username(cls,username):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE username=?"

        result=cursor.execute(query,(username,))  #
        #Get the first row 
        row=result.fetchone()

        if row :
            user=cls(*row)
        else:
            user=None
        connection.close()

        return user
    @classmethod
    def find_by_id(cls,_id):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE id=?"

        result=cursor.execute(query,(_id,))  #
        #Get the first row 
        row=result.fetchone()

        if row :
            user=cls(*row)
        else:
            user=None
        connection.close()

        return user

class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="You have to add the username")
    parser.add_argument("password",type=str,required=True,help="You have to add the password")
    def post(self):
        data=UserRegister.parser.parse_args()
        if not User.find_by_username(data["username"]):

            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()
            query="INSERT INTO users VALUES (NULL,?,?)"

            cursor.execute(query, (data["username"],data["password"]))

            connection.commit()

            connection.close()

            return {"message":"User created successfuly"},201
        return {"message": "User exists already"},400


