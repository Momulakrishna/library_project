def userEntity(item) -> dict:
    return{
        'id':str(item["_id"]),
        'member_id':item['member_id'],
        'member_name':item["member_name"],
        'books_quantity':item['books_quantity'],
        'books_owned':item['books_owned'],
        'total_price':item['total_price']
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]


def bookEntity(item) -> dict:
    return{
        'id':str(item["_id"]),
        'book_id':item['book_id'],
        'book_title':item["book_title"],
        'book_author':item['book_author'],
        'book_avalibility':item['book_avalibility'],
        'book_price':item['book_price']
    }

def booksEntity(entity) -> list:
    return [bookEntity(item) for item in entity]####schemas