import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser=reqparse.RequestParser() #initialise a new object which we can use to parse the request 
    parser.add_argument("price",type=float,required=True,help="This field cannot be left blank ")
    @jwt_required()
    def get(self,name):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="SELECT * FROM items where name=?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        connection.close()

        if row:
            return {"item":{"name":row[0],"price":row[1]}}
        
        return {"message":"Item "}


    def post(self,name):
        if next(filter(lambda x:x["name"]==name,items),None) is not None:
            return {"message":"An item with name {} already exists.".format(name)},400
        data=Item.parser.parse_args()
        item={"name":name,"price":data["price"]}
        items.append(item)
        return item,201
    
    def delete(self,name):
        global items
        items=list(filter(lambda x:x["name"]!=name,items))
        return {"Message": "Item deleted"}
    
    def put(self,name):

        data=Item.parser.parse_args()
        print(data["another"])
        item=next(filter(lambda x:x["name"]==name,items),None)
        if item is None:
            item={"name":name,"price":data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item 
 
class ItemList(Resource):
    # def get(self):
    #     return {"items":items}
    pass