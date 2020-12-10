import mysql.connector as sql
from tokens import get_token
from tabulate import tabulate


def main():
    # connect to SQL database
    mydb = sql.connect(
        host='localhost',
        user='root',
        password=get_token(),
        database='password_manager'
    )
    cursor = mydb.cursor()

    while True:

        add_view = input("Do you want to add or view passwords (1/2): ")

        if add_view == '1':  # add password
            password = input("Enter password to store: ")
            app = input("Enter the application this is for: ")
            url = input("What is the url for the application: ")

            # insert encrypted password into vault
            ins = "INSERT INTO password_vault(password, app, url) " \
                  "VALUES(AES_ENCRYPT(%s,UNHEX(SHA2('passkey', 224))), %s, %s)"
            val = (password, app, url)
            cursor.execute(ins, val)
            mydb.commit()

        else:  # view current passwords
            cursor.execute("SELECT * FROM password_vault")
            result = cursor.fetchall()
            print(tabulate(result, headers=['pass_id', 'password', 'app', 'url'], tablefmt='psql'))

            # get encrypted password
            pass_id = (int(input("Which password do you want to view: ")),)
            get_val = "SELECT @val := password FROM password_vault WHERE pass_id = %s;"
            cursor.execute(get_val, pass_id)
            encrypted_pass = cursor.fetchone()

            # decrypt password and print to console
            get_pass = "SELECT AES_DECRYPT(%s, UNHEX(SHA2('passkey', 224)));"
            cursor.execute(get_pass, encrypted_pass)
            output = ''.join(cursor.fetchone())
            print(output)


main()
