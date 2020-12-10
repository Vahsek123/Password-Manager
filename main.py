import mysql.connector as sql
from tokens import get_token
from tabulate import tabulate
import PySimpleGUI as sg


def main():

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Add":  # add password
            password = input("Enter password to store: ")
            application = input("Enter the application this is for: ")
            url = input("What is the url for the application: ")

            # insert encrypted password into vault
            ins = "INSERT INTO password_vault(password, app, url) " \
                  "VALUES(AES_ENCRYPT(%s,UNHEX(SHA2('passkey', 224))), %s, %s)"
            val = (password, application, url)
            cursor.execute(ins, val)
            mydb.commit()
            cursor.execute("SELECT * FROM password_vault")
            updated_table = cursor.fetchall()
            window.FindElement('vault').Update(values=updated_table)
        #
        # else:  # view current passwords
        #     cursor.execute("SELECT * FROM password_vault")
        #     result = cursor.fetchall()
        #     print(tabulate(result, headers=['pass_id', 'password', 'app', 'url'], tablefmt='psql'))
        #
        #     # get encrypted password
        #     pass_id = (int(input("Which password do you want to view: ")),)
        #     get_val = "SELECT @val := password FROM password_vault WHERE pass_id = %s;"
        #     cursor.execute(get_val, pass_id)
        #     encrypted_pass = cursor.fetchone()
        #
        #     # decrypt password and print to console
        #     get_pass = "SELECT AES_DECRYPT(%s, UNHEX(SHA2('passkey', 224)));"
        #     cursor.execute(get_pass, encrypted_pass)
        #     output = ''.join(cursor.fetchone())
        #     print(output)


if __name__ == "__main__":
    mydb = sql.connect(
        host='localhost',
        user='root',
        password=get_token(),
        database='password_manager'
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM password_vault")
    result = cursor.fetchall()

    sg.theme('Dark')
    app = [
        [sg.Text("Password Manager", justification='center')],
        [sg.Table(
            values=result,
            headings=['pass_id', 'password', 'app', 'url'],
            justification='center',
            col_widths=[50, 20, 20, 20],
            num_rows=10,
            key='vault'
        )],
        [sg.Button("Add"), sg.Button("Remove")],
    ]
    window = sg.Window("Password Manager",
                       layout=app,
                       size=(600, 400),
                       element_justification='c')

    main()
