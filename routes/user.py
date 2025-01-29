from fastapi import APIRouter
from model.user import User,User_1,BorrowBooks
from bson import ObjectId
from config.db import con
from schemas.user import userEntity,usersEntity,booksEntity

user= APIRouter()

@user.get('/')
async def find_all_members():
    return usersEntity(con.liberary_management_system.members_data.find())

@user.get('/books')
async def find_all_books():
    return booksEntity(con.liberary_management_system.books_data.find())

@user.get('/{id}')
async def find_member_by_id(id):
    return userEntity(con.liberary_management_system.members_data.find_one({"_id":ObjectId(id)}))

@user.post('/')
async def create_member(member:User):
    con.liberary_management_system.members_data.insert_one(dict(member))
    

@user.put('/{id}')
async def update_member(id,member:User):
    con.liberary_management_system.members_data.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(member)})
    return userEntity(con.liberary_management_system.members_data.find_one({"_id":ObjectId(id)}))

@user.patch('/{member_id}')
async def borrow_one_book(member_id,member:User_1):
    con.liberary_management_system.members_data.find_one_and_update({'_id':ObjectId(member_id)},{"$push":dict(member)})
    cost_1=con.liberary_management_system.books_data.find_one({"book_title":member.books_owned},{'book_price':1})
    cost_2=con.liberary_management_system.members_data.find_one({'_id':ObjectId(member_id)},{'total_price':1})
    new_cost=cost_1["book_price"]+cost_2["total_price"]
    con.liberary_management_system.members_data.update_one({'_id':ObjectId(member_id)},{'$set':{"total_price":new_cost}})
    con.liberary_management_system.members_data.update_one({'_id':ObjectId(member_id)},{"$inc": {'books_quantity': 1}})
    return userEntity(con.liberary_management_system.members_data.find_one({"_id":ObjectId(member_id)}))
# ---------------------------------------------------------------------------------------------------------------------------------
@user.put('/{_id}')
async def borrow_many_book(_id:str, members: BorrowBooks):
    books_to_borrow = members.books_owned  # Assuming this is a list of books
    con.liberary_management_system.members_data.find_one_and_update(
        {'_id': ObjectId(_id)}, 
        {"$push": {"books_owned": {"$each": books_to_borrow}}}
    )
    return userEntity(con.liberary_management_system.members_data.find_one({"_id": ObjectId(_id)}))
# -------------------------------------------------------------------------------------------------------------------------------------

@user.delete('/{id}')
async def delete_member(id,member:User):
    return userEntity(con.liberary_management_system.members_data.find_one_and_delete({"_id":ObjectId(id)}))
# ---------------------------------------------------------------------------------------------------------------------------------------
@user.patch('/{mem_id}')
async def return_books(mem_id: str,members:BorrowBooks):
    for book in members.books_owned:
        con.liberary_management_system.members_data.find_one_and_update(
            {"_id": ObjectId(mem_id)},
            {"$pull": {"books_owned": book}})
        
    con.liberary_management_system.members_data.find_one_and_update({"_id":ObjectId(mem_id)},{"$inc":{'books_quantity':-len(members.books_owned)}})

# ------------------------------------------------------------------------------------------------------------------------------------------------------
@user.get('/{_id}')
async def booking_history(_id):
    con.liberary_management_system.members_data.find_one({"_id":ObjectId(_id)},{'_id':0,'books_owned':1})
    return userEntity(con.liberary_management_system.members_data.find_one({"_id":ObjectId(id)})) ####routes