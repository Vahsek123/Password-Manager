import mysql.connector as sql
from tokens import get_token


mydb = sql.connect(
    host='localhost',
    user='root',
    password=get_token(),
    database='password_manager'
)

mycursor = mydb.cursor()

ins = "INSERT INTO password_vault(password, app, url) " \
      "VALUES(AES_ENCRYPT(%s,UNHEX(SHA2('passkey', 224))), %s, %s)"

input_pass = input("Enter password to store: ")
val = (input_pass, 'Tester', 'https://tester.com')


mycursor.execute(ins, val)
mydb.commit()

