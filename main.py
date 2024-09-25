import random
from tkinter import *
from progres_db import connect
import bcrypt
from tkinter import messagebox as msg

def generate_account_number():
        while True:
                start = random.choice([22,21])
                remaining_digit = random.randint(10000000, 99999999)
                random_num = f'{start}{remaining_digit}'
                conn=connect()
                cur = conn.cursor()
                cur.execute(
                        """
                        SELECT COUNT(*) FROM user_acct WHERE account_number = %s
                        """,(random_num,)
                )
                count =  cur.fetchone()[0]
                conn.close()
                cur.close()

                if count == 0:
                        return random_num



# register begin
def validate_numeric_input(char):
        return char.isdigit() or char == ""

def signup():
        global register_screen
        global username
        global password
        global email
        global phone_no
        global address
        global username_entry
        global password_entry
        global email_entry
        global phone_no_entry
        global address_entry

        register_screen = Toplevel(main_screen)
        register_screen.geometry("600x500")
        register_screen.title("Create an account")

        username = StringVar()
        password = StringVar()
        email = StringVar()
        phone_no = StringVar()
        address = StringVar()

        validate_cmd = register_screen.register(validate_numeric_input)

        Label(register_screen, text="")
        Label(register_screen,text="Please enter the following details", bg="red", font=("calibri", 13)).pack()
        username_label =Label(register_screen, text="Username *")
        username_label.pack()
        username_entry= Entry(register_screen, textvariable=username)
        username_entry.pack()

        password_label =Label(register_screen, text="Password *")
        password_label.pack()
        password_entry= Entry(register_screen, textvariable=password, show="*")
        password_entry.pack()

        email_label =Label(register_screen, text="Email *")
        email_label.pack()
        email_entry= Entry(register_screen, textvariable=email)
        email_entry.pack()

        phone_no_label =Label(register_screen, text="Phone Number *")
        phone_no_label.pack()
        phone_no_entry= Entry(register_screen, textvariable=phone_no, validate="key", validatecommand=(validate_cmd,"%S"))
        phone_no_entry.pack()

        address_label =Label(register_screen, text="Address *")
        address_label.pack()
        address_entry= Entry(register_screen, textvariable=address)
        address_entry.pack()

        Label(register_screen, text="")
        Button(register_screen, text="Register", bg="green", font=("calibri",13), width=13, height=1, command=register_user).pack()

def register_user():
        username_info = username.get()
        password_info = password.get()
        email_info = email.get()
        phone_no_info = phone_no.get()
        address_info = address.get()
        acct_num = generate_account_number()

        hashed_password = bcrypt.hashpw(password_info.encode('utf-8'),bcrypt.gensalt())

        conn = connect()
        cur = conn.cursor()

        cur.execute(
                """
                    INSERT INTO user_acct(username, password, email,account_number, phone_no, address)
                    VALUES(%s, %s, %s, %s, %s,%s)
                """, (username_info,hashed_password.decode('utf-8'), email_info,acct_num,phone_no_info,address_info)
        )
        conn.commit()
        conn.close()
        cur.close()

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        email_entry.delete(0, END)
        phone_no_entry.delete(0, END)
        address_entry.delete(0, END)

        Label(register_screen, text="Registration successfully", fg="green", font=("calibri",13)).pack()

# signup()
# register_user()

# register end



# login begining
def login():
          global login_screen
          global email_entry
          global password_entry
          login_screen = Toplevel(main_screen)
          login_screen.title("Login")
          login_screen.geometry("600x500")

          email = StringVar()
          password = StringVar()

          Label(login_screen, text="Please enter the following details", bg="red", font=("calibri",13)).pack()
          email_label = Label(login_screen, text = "Email *")
          email_label.pack()
          email_entry = Entry(login_screen, textvariable=email)
          email_entry.pack()

          password_label = Label(login_screen, text = "Password *")
          password_label.pack()
          password_entry = Entry(login_screen, textvariable=password, show="*")
          password_entry.pack()

          Label(login_screen, text="")
          Button(login_screen, text="Login", bg="green", font=("calibri",13), width=13, height=1, command=login_verify).pack()

def login_verify():
        email_info = email_entry.get()
        password_info = password_entry.get()


        conn = connect()
        cur = conn.cursor()
        cur.execute(
                """
                    SELECT password FROM user_acct WHERE email = %s
                """,(email_info,)
        )
        result = cur.fetchone()
        conn.close()

        if result:
                store_hashed_password = result[0].encode('utf-8')
                if bcrypt.checkpw(password_info.encode('utf-8'), store_hashed_password):
                    login_success()
                else: 
                    password_invalid()
        else:
                user_not_found()

def login_success():
        
        global login_success_screen
        login_success_screen = Toplevel(login_screen)
        login_success_screen.title("Successful")
        login_success_screen.geometry('150x100')

        Label(login_success_screen, text="Login Successful", fg="green", font=("calibri",13)).pack()
        Button(login_success_screen, text="OK", bg="red", font=("calibri",13), width=13, height=1, command=menu).pack()

def user_not_found():
        global user_not_found_screen
        user_not_found_screen = Toplevel(login_screen)
        user_not_found_screen.title("Failed")
        user_not_found_screen.geometry("150x100")

        Label(user_not_found_screen, text="user not found", fg="red", font=("calibri",13)).pack()
        Button(user_not_found_screen, text="OK", bg="green", font=("calibri",13), width=13, height=1, command=delete_user_not_found).pack()

def delete_user_not_found():
        user_not_found_screen.destroy()

def password_invalid():
        global password_invalid_screen
        password_invalid_screen = Toplevel(login_screen)
        password_invalid_screen.title("password is invalid")
        password_invalid_screen.geometry("150x100")
        Label(password_invalid_screen, text="password is invalid", fg="red", font=("calibri",13)).pack()
        Button(password_invalid_screen, text="OK", bg="red", font=("calibri",13), width=13, height=1, command=delete_password_invalid).pack()

def delete_password_invalid():
        password_invalid_screen.destroy()

# login end



# deposit begin
def deposit():
          
          global deposit_screen
          global name_entry
          global account_number_entry
          global amount_entry
          global name_label
          global account_number_label
          global amount_label
          global name
          global account_number
          global amount

          name = StringVar()
          account_number = StringVar()
          amount  = StringVar()

          deposit_screen = Toplevel(menu_screen)
          deposit_screen.title("Deposit Screen")
          deposit_screen.geometry("600x500")

          Label(deposit_screen, text="")
          Label(deposit_screen, text="Fill your details", bg="red", fg='black', width="30",height="2",font=("Arial Bold",13)).pack()

          name_label =Label(deposit_screen, text="Name",font=("Calibri",13))
          name_label.pack()
          name_entry =Entry(deposit_screen, textvariable=name)
          name_entry.pack()


          account_number_label= Label(deposit_screen, text="Account Number", font=("calibri",13))
          account_number_label.pack()
          account_number_entry = Entry(deposit_screen, textvariable=account_number)
          account_number_entry.pack()


          amount_label = Label(deposit_screen, text="Amount", font=("calibri",13))
          amount_label.pack()
          amount_entry = Entry(deposit_screen, textvariable=amount)
          amount_entry.pack()

          Button(deposit_screen, text="Deposit",bg="green", font=("calibri",13),width=13, height=1,command=deposit_verify).pack()

def deposit_verify():
        conn = connect()
        cur = conn.cursor()

        name_info = name.get()
        account_number_info = account_number.get()
        amount_info = amount.get()
        email_info = email_entry.get()

        cur.execute(
                """
                SELECT id FROM user_acct WHERE email = %s
                """,(email_info,)
        )

        user= cur.fetchone()
        if user is None:
                msg.showerror('Error', 'User not found')

        user_id = user[0]

        cur.execute(
                """
                INSERT INTO transaction(name, account_number, amount, user_id)
                VALUES(%s, %s, %s, %s)
                """,(name_info, account_number_info, amount_info, user_id)
        )
        cur.execute(
                """
                UPDATE user_acct SET balance = %s WHERE email = %s
                """, (amount_info, email_info)
        )

        conn.commit()
        conn.close()
        cur.close()
        msg.showinfo('Saved',f'Amount of ${amount_info} deposited successfully')
        
# deposit end

# withdraw begin

def withdraw():
        global withdraw_screen
        global withdraw_name_entry
        global withdraw_account_number_entry
        global withdraw_amount_entry
        global withdraw_name
        global withdraw_account_number
        global withdraw_amount

        withdraw_screen = Toplevel(menu_screen)
        withdraw_screen.title("withdraw Screen")
        withdraw_screen.geometry("600x500")

        withdraw_name = StringVar()
        withdraw_account_number = StringVar()
        withdraw_amount = StringVar()

        Label(withdraw_screen, text="")
        Label(withdraw_screen, text="Fill your details", bg="red", fg='black', width="30",height="2",font=("Arial Bold",13)).pack()

        Label(withdraw_screen, text="Name",font=("Calibri",13)).pack()
        withdraw_name_entry =Entry(withdraw_screen, textvariable=withdraw_name).pack()


        Label(withdraw_screen, text="Account Number", font=("calibri",13)).pack()
        withdraw_account_number_entry = Entry(withdraw_screen, textvariable=withdraw_account_number).pack()


        Label(withdraw_screen, text="Amount", font=("calibri",13)).pack()
        withdraw_amount_entry = Entry(withdraw_screen, textvariable=withdraw_amount).pack()

        Button(withdraw_screen, text="Withdraw",bg="green", font=("calibri",13),width=13, height=1,command=withdraw_verify).pack()

def withdraw_verify():
        conn = connect()
        cur = conn.cursor()

        withdraw_name_info = withdraw_name.get()
        withdraw_account_number_info = withdraw_account_number.get()
        withdraw_amount_info = withdraw_amount.get()
        withdraw_email_info = email_entry.get()

        cur.execute(
                """
                SELECT id FROM user_acct WHERE email = %s
                """,(withdraw_email_info,)
        )

        user = cur.fetchone()
        if user is None:
                msg.showerror(("Error","User Not Found"))
        
        
        user_id = user[0]
        
        cur.execute(
                """
                SELECT id , balance FROM user_acct  WHERE email = %s
                """,(withdraw_email_info,)
        )
        trans_amount = cur.fetchone()
        current_balance = float(trans_amount[1])
        if float(withdraw_amount_info)>current_balance:
                msg.showerror('Error', 'insufficient Funds')
                return
        
        new_balance = current_balance - float(withdraw_amount_info)
        
        cur.execute(
                """
                UPDATE user_acct SET balance =%s WHERE id = %s
                """,(new_balance,user_id)
        )

        cur.execute(
                """
                INSERT INTO transaction(name, account_number, amount, transaction_type,user_id)
                VALUES (%s, %s,%s,'withdraw',%s)
                """,(withdraw_name_info, withdraw_account_number_info,withdraw_amount_info,user_id)
        )
        

        conn.commit()
        conn.close()
        cur.close()

        msg.showinfo('Saved', f'Amount of ${withdraw_amount_info} withdrawed successful')

# withdraw end

# balance function
def balance():
    conn = connect()
    cur = conn.cursor()

    email_info = email_entry.get()

    cur.execute(
        """
        SELECT balance FROM user_acct WHERE email = %s
        """, (email_info,)
    )
    main_balance = cur.fetchone()[0]
    
    if main_balance is None:
        msg.showerror('Error', 'User not found')
        return

    conn.close()
    cur.close()

    msg.showinfo('Balance', f'Your current balance is ${main_balance}')
# balance end

# transfer begin
def transfer_fund():
        global transfer_screen
        global sender_account_entry
        global recipient_account_entry
        global transfer_amount_entry
        global sender_account
        global recipient_account
        global transfer_amount

        transfer_screen = Toplevel(menu_screen)
        transfer_screen.title("transfer Screen")
        transfer_screen.geometry("600x500")

        
        sender_account = StringVar()
        recipient_account = StringVar()
        transfer_amount = StringVar()

        Label(transfer_screen, text="")
        Label(transfer_screen, text="Fill your details", bg="red", fg='black', width="30",height="2",font=("Arial Bold",13)).pack()

        Label(transfer_screen, text="Sender Acount Number",font=("Calibri",13)).pack()
        sender_account_entry =Entry(transfer_screen, textvariable=sender_account).pack()


        Label(transfer_screen, text="Recipient Account Number", font=("calibri",13)).pack()
        recipient_account_entry = Entry(transfer_screen, textvariable=recipient_account).pack()


        Label(transfer_screen, text="Amount", font=("calibri",13)).pack()
        transfer_amount_entry = Entry(transfer_screen, textvariable=transfer_amount).pack()

        Button(transfer_screen, text="Transfer",bg="green", font=("calibri",13),width=13, height=1,command=transfer_verify).pack()


def transfer_verify():
        conn = connect()
        cur =conn.cursor()

        sender_account_info = sender_account.get()
        recipient_account_info = recipient_account.get()
        transfer_amount_info = transfer_amount.get()
        # transfer_email_info = email_entry.get()

        cur.execute(
                """
                SELECT u.id,u.balance
                FROM user_acct u
                JOIN transaction t ON u.id = t.user_id
                WHERE t.account_number = %s
                """,(sender_account_info,)
        )
        sender = cur.fetchone()
        if sender is None:
                msg.showerror('Error', 'sender account not found')
        sender_id = sender[0]
        sender_balance = float(sender[1])

        if float(transfer_amount_info)>sender_balance:
                msg.showerror('Error',f'Insufficient fund, your balance is ${sender_balance}')
                return
        cur.execute(
                """
                SELECT u.id,u.balance
                FROM user_acct u
                JOIN transaction t ON u.id = t.user_id
                WHERE t.account_number = %s
                """,(recipient_account_info,)
        )

        recipient = cur.fetchone()
        if recipient is None:
                msg.showerror('Error', 'recipient account not found')
        recipient_id = recipient[0]
        recipient_balance = float(recipient[1])

        new_sender_balance = sender_balance - float(transfer_amount_info)
        new_recipient_balance = recipient_balance + float(transfer_amount_info)

        cur.execute(
                """
                UPDATE user_acct SET balance = %s WHERE id= %s
                """,(new_sender_balance,sender_id)
        )

        cur.execute(
                """
                UPDATE user_acct SET balance = %s WHERE id= %s
                """,(new_recipient_balance,recipient_id)
        )
        cur.execute(
                """
                INSERT INTO transaction (name, account_number, amount, transaction_type, user_id)
                VALUES (%s,%s,%s,'transfer_sent',%s)
                """,(
                        'Sender',
                        sender_account_info,
                        transfer_amount_info,
                        sender_id
                )
        )
        cur.execute(
                """
                INSERT INTO transaction (name, account_number, amount, transaction_type, user_id)
                VALUES (%s,%s,%s,'transfer_received',%s)
                """,(
                        'Recipient',
                        recipient_account_info,
                        transfer_amount_info,
                        recipient_id
                )
        )

        conn.commit()
        conn.close()
        cur.close()
        msg.showinfo('Saved', f'Amount of ${transfer_amount_info} tranfer successfully to {recipient_account_info}')
        

# transfer end

def menu():
        global menu_screen
        menu_screen =Toplevel(main_screen)
        menu_screen.title('MENU')
        menu_screen.geometry('300x200')

        Button(menu_screen, text="Deposit", bg="violet", fg='black', width="30",height="2",font=("Arial Bold",10), command=deposit).pack()
        Button(menu_screen, text="Withdraw", bg="red", fg='black', width="30",height="2",font=("Arial Bold",10), command=withdraw).pack()
        Button(menu_screen, text="Balance", bg="red", fg='black', width="30",height="2",font=("Arial Bold",10),command=balance).pack()
        Button(menu_screen, text="Transfer fund", bg="red", fg='black', width="30",height="2",font=("Arial Bold",10), command=transfer_fund).pack()
        Label(menu_screen, text="").pack(side=LEFT)

def main_action_screen():
        global main_screen
        main_screen = Tk()
        main_screen.geometry("3000x2500")
        main_screen.title("User Account Login/Register")

        Label(text="select your choice",bg="green",width="300",height="1",font=("calibri",13)).pack()
        
        Button(text="Register", bg="red", width="30",height="2",font=("Arial Bold",10),command=signup).pack()
        Button(text="Login", bg="green", width="30",height="2",font=("Arial Bold",10),command=login).pack()

        main_screen.mainloop()
main_action_screen()