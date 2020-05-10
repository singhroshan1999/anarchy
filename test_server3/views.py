from test_server4.settings import database
from test_server4.model import User


def hello(header):
    sesson = database.new_session()
    d = sesson.query(User).all()[0]
    print(header["params"]["name"])
    return  {"db":[d.name,d.fullname,d.email]}

def hello2(header):
    user = User(name = header['params']['name'],fullname=header['params']['fullname'],email = header['params']['email'])
    sesson = database.new_session()
    sesson.add(user)
    sesson.commit()
    print(header["params"]["name"])
    return  {"db":["roshan","singh",123456789,"gd76g5d7fg5d67g76et67346t6"]}

