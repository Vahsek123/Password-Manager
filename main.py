import mysql.connector as sql
from tokens import get_token
from tabulate import tabulate
import PySimpleGUI as sg


def add_password():
    layout_add = [
        [sg.Text("Password: "), sg.InputText(default_text='', key='-pass-')],
        [sg.Text("Application: "), sg.InputText(default_text='', key='-app-')],
        [sg.Text("URL: "), sg.InputText(default_text='', key='-url-')],
        [sg.Button("Confirm")]
    ]
    window_add = sg.Window("Add Password", layout_add)
    while True:
        event, values = window_add.read()
        if event == "Confirm":
            window_add.Close()
            return values


def update_table():
    cursor.execute("SELECT * FROM password_vault")
    updated_table = cursor.fetchall()
    window['vault'].Update(values=updated_table)


def main():

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Add":  # add password
            pass_entry = add_password()

            # insert encrypted password into vault
            ins = "INSERT INTO password_vault(password, app, url) " \
                  "VALUES(AES_ENCRYPT(%s,UNHEX(SHA2('passkey', 224))), %s, %s)"
            val = (pass_entry['-pass-'], pass_entry['-app-'], pass_entry['-url-'])
            cursor.execute(ins, val)
            mydb.commit()
            update_table()
        elif event == "Remove":
            pos = values['vault'][0]
            rem_id = (window['vault'].Get()[pos][0],)

            rem = "DELETE FROM password_vault WHERE pass_id = %s"
            cursor.execute(rem, rem_id)
            mydb.commit()
            update_table()
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
