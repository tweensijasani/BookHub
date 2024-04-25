from flask import Flask, request, session, jsonify, render_template
from flask_session import Session
from flask_cors import CORS
from functions import validation
from functions import helper
import psycopg2
import config
import datetime

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
        host=config.DATABASE_HOST,
        database=config.DATABASE_NAME,
        user=config.DATABASE_USER,
        password=config.DATABASE_PASSWORD,
        port="5432")

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/")
def index():
    # return "Welcome!"
    return render_template("index.html"), 200


@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    return render_template("signup_admin.html"), 200


@app.route('/vendor_signup', methods=['GET', 'POST'])
def vendor_signup():
    return render_template("signup_vendor.html"), 200


@app.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    return render_template("signup_customer.html"), 200


# Sign-up admin
@app.route('/api/admin/signup', methods=['POST'])
def signup_admin():
    '''
    This function registers new admin user 
    Parameters : Username, password, email-id, phone-number, name, position
    '''
    # Validate data
    try:

        # Extract variables from the request
        _name = request.form.get("name")
        _email = request.form.get("email")
        _phone = request.form.get("phone")
        _password = request.form.get("password")
        _username = request.form.get("username")
        _position = request.form.get("position")

        # Validate data
        # response = validation.validate_data(_name, _email, _phone, _password, _username)
        # if response[1] != 200:
        #     return response
        if not _position:
            return render_template("error.html", message="Please enter position."), 500
        # if not validation.validate_admin_position(_position):
        #     return render_template("error.html", message="Invalid position."), 500

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values ({},'{}','{}','{}','{}','{}');".format(
            config.UserID, _username, _password, _email, _phone, _name)
        config.UserID += 1
        print(sql)
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = '{}' and password = '{}'".format(
            _username, _password)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        # print(results)

        _userid = results[0][0]
        sql = "INSERT into Admin(admin_id, admin_position) values ({},'{}')".format(
            _userid, _position)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
        print("executed")

    except Exception as e:
        print(e)
        return render_template("signup_admin.html", message="Error occurred in Sign-up"), 500

    return render_template("signup_admin.html", message="Successfully registered."), 200


# Sign-up vendor
@app.route('/api/vendor/signup', methods=['POST'])
def signup_vendor():
    '''
    This function registers new vendor 
    Parameters : Username, password, email-id, phone-number, name, city, company
    '''
    # Validate data
    try:
        # Extract variables from the request
        _name = request.form.get("name")
        _email = request.form.get("email")
        _phone = request.form.get("phone")
        _password = request.form.get("password")
        _username = request.form.get("username")
        _city = request.form.get("city")
        _company = request.form.get("company")

        # Validate data
        # response = validation.validate_data(_name, _email, _phone, _password, _username)
        # if response[1] != 200:
        #     return response

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values ({},'{}','{}','{}','{}','{}');".format(
            config.UserID, _username, _password, _email, _phone, _name)
        config.UserID += 1
        print(sql)
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = '{}' and password = '{}'".format(
            _username, _password)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        # print(results)

        _userid = results[0][0]
        sql = "INSERT into Vendor(vendor_id, city, company, admin_id) values ({}, '{}', '{}', NULL)".format(
            _userid, _city, _company)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
        print("executed")

    except Exception as e:
        print(e)
        return render_template("signup_vendor.html", message="Error occurred in Sign-up"), 500

    return render_template("signup_vendor.html", message="Successfully registered."), 200


# Sign-up customer
@app.route('/api/customer/signup', methods=['GET', 'POST'])
def signup_customer():
    '''
    This function registers new customer
    Parameters : Username, password, email-id, phone-number, name, bank_name, bank_acc
    '''
    # Validate data
    try:
        # Extract variables from the request
        _name = request.form.get("name")
        _email = request.form.get("email")
        _phone = request.form.get("phone")
        _password = request.form.get("password")
        _username = request.form.get("username")
        _bank = request.form.get("bank_name")
        _account = request.form.get("bank_acc")

        # Validate data
        # response = validation.validate_data(_name, _email, _phone, _password, _username)
        # if response[1] != 200:
        #     return response
        # if not validation.validate_account(_account):
        #     return render_template("error.html", message="Invalid account number."), 500

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values ({},'{}','{}','{}','{}','{}');".format(
            config.UserID, _username, _password, _email, _phone, _name)
        config.UserID += 1
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = '{}' and password = '{}'".format(
            _username, _password)
        cursor.execute(select_sql)
        results = cursor.fetchall()

        _userid = results[0][0]
        sql = "INSERT into Customer(customer_id, bank_name, bank_acc) values ({}, '{}', '{}')".format(
            _userid, _bank, _account)
        # print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("signup_customer.html", message="Error occurred in Sign-up")

    return render_template("signup_customer.html", message="Successfully registered.")


# Update customer data
@app.route('/api/customer/update', methods=['POST'])
def update_customer():
    '''
    This function updates existing customer's data
    Parameters : username, password, email-id, phone-number, name, bank_name, bank_acc
    '''
    # Validate data
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            # Extract variables from the request
            _name = request.form.get("name")
            _email = request.form.get("email")
            _phone = request.form.get("phone")
            _username = request.form.get("username")
            _bank = request.form.get("bank_name")
            _account = request.form.get("bank_acc")

            # Validate data
            # response = validation.validate_data(_name, _email, _phone, _password, _username)
            # if response[1] != 200:
            #     return response
            # if not validation.validate_account(_account):
            #     return render_template("error.html", message="Invalid account number."), 500

            cursor = conn.cursor()
            update_user_sql = "UPDATE \"User\" SET email = \'{}\', phone = \'{}\', name = \'{}\', username = \'{}\' where user_id = {} ;".format(_email, _phone, _name, _username, _userid)
            cursor.execute(update_user_sql)
            conn.commit()

            update_sql = "Update Customer set bank_name = \'{}\', bank_acc = \'{}\' where customer_id = {} ;".format(
                _bank, _account, _userid)
            # print(sql)
            cursor.execute(update_sql)
            conn.commit()

        else:
            return "Unauthenticated", 401
            # return render_template("error.html", message="Unauthenticated"), 401

    except Exception as e:
        print(e)
        return "Error occurred in updating customer data", 500
        # return render_template("error.html", message="Error occurred in updating customer data"), 500

    return "Successfully updated customer details!", 200
    # return render_template("success.html", message="Successfully updated customer details."), 200


# Update vendor data
@app.route('/api/vendor/update', methods=['POST'])
def update_vendor():
    '''
    This function updates existing vendor's data
    Parameters : username, password, email-id, phone-number, name, bank_name, bank_acc
    '''
    # Validate data
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            # Extract variables from the request
            _name = request.form.get("name")
            _email = request.form.get("email")
            _phone = request.form.get("phone")
            _password = request.form.get("password")
            _username = request.form.get("username")
            _city = request.form.get("city")
            _company = request.form.get("company")

            # Validate data
            response = validation.validate_data(_name, _email, _phone, _password, _username)
            if response[1] != 200:
                return response

            cursor = conn.cursor()
            update_user_sql = "UPDATE \"User\" SET password = \"{}\", email = \"{}\", phone = \"{}\", name = \"{}\", username = \"{}\" where user_id = {} ;".format(
                _password, _email, _phone, _name, _username, _userid)
            cursor.execute(update_user_sql)
            conn.commit()

            update_sql = "Update Vendor set city = \"{}\", company = \"{}\" where vendor_id = {} ;".format(
                _city, _company, _userid)
            # print(sql)
            cursor.execute(update_sql)
            conn.commit()

        else:
            return render_template("error.html", message="Unauthenticated"), 401

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in updating vendor data"), 500

    return render_template("success.html", message="Successfully updated vendor details."), 200


# Admin login
@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    '''
    This function is for admin login 
    Parameters : Username, password
    '''
    try:
        _username = request.form.get("username")
        _password = request.form.get("password")
        cursor = conn.cursor()
        select_sql = "Select password, user_id from \"User\" join Admin on user_id = admin_id where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return render_template("index.html", message="User does not exist"), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            return render_template("home_admin.html", message="Login successful"), 200
        else:
            return render_template("index.html", message="Invalid password"), 500
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in login"), 500


# Vendor login
@app.route('/api/vendor/login', methods=['POST'])
def login_vendor():
    '''
    This function is for vendor login 
    Parameters : Username, password
    '''
    try:
        _username = request.form.get("username")
        _password = request.form.get("password")
        cursor = conn.cursor()
        select_sql = "Select password, user_id, admin_id from \"User\" join Vendor on user_id = vendor_id where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            return render_template("index.html", message="User does not exist"), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            msg = "Login succesful"
            if results[0][2] == None:
                print("Vendor is not approved")
                msg += ", vendor not approved"
            return render_template("home_vendor.html", message=msg), 200
        else:
            return render_template("index.html", message="Invalid password"), 500
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in login"), 500


# Customer login
@app.route('/api/customer/login', methods=['POST'])
def login_customer():
    '''
    This function is for customer login 
    Parameters : Username, password
    '''
    try:
        _username = request.form.get("username")
        _password = request.form.get("password")
        print(_username)
        print(_password)
        cursor = conn.cursor()
        select_sql = "Select password, user_id from \"User\" join Customer on user_id = customer_id where username = \'{}\'".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return render_template("index.html", message="User does not exist"), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            return view_all_books()
            # return render_template("home_customer.html", message="Login successful"), 200
        else:
            return render_template("index.html", message="Invalid password"), 500
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in login"), 500


# Logout
@app.route('/api/user/logout', methods=['GET', 'POST'])
def logout():
    '''
    This function logs user out of current session 
    '''
    try:
        if session.get("user_id"):
            session["user_id"] = None
            return render_template("index.html", message="Successfully Logged out!"), 200
        else:
            return render_template("index.html", message="Error occurred in logout"), 500
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in logout"), 500


# View vendor profile
@app.route('/api/vendor/viewprofile', methods=['GET'])
def view_vendor_profile():
    '''
    This function gets vendor profile information 
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select name, email, phone, company, city from \"User\" join Vendor on user_id = vendor_id where user_id = \"{}\";".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="User does not exist"), 404

            vendor_profile = {
                "name": results[0][0],
                "email": results[0][1],
                "phone": results[0][2],
                "company": results[0][3],
                "city": results[0][4]
            }
            return render_template("vendor_profile.html", vendor=vendor_profile), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view vendor profile"), 500


# View customer profile
@app.route('/api/customer/viewprofile', methods=['GET'])
def view_customer_profile():
    '''
    This function gets customer profile information 
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select Name, username, email, phone, bank_name, bank_acc, user_id from \"User\" join Customer C on user_id = customer_id where user_id = {};".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("index.html", message="User does not exist"), 404

            customer_profile = {
                "name": results[0][0],
                "username": results[0][1],
                "email": results[0][2],
                "phone": results[0][3],
                "bank_name": results[0][4],
                "bank_acc": results[0][5],
                "user_id": results[0][6]
            }

            select_sql = "Select addr_id, street, apt, city, pin from Address where customer_id = {};".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()
            address = []
            for row in results:
                addr = {
                    "addr_id": row[0],
                    "street": row[1],
                    "apt": row[2],
                    "city": row[3],
                    "pin": row[4]
                }
                address.append(addr)

            return render_template("profile_customer.html", customer=customer_profile, addresses=address), 200
        else:
            return render_template("index.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in view customer profile"), 500


# View admin profile
@app.route('/api/admin/viewprofile', methods=['GET'])
def view_admin_profile():
    '''
    This function gets customer profile information 
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select Name, email, phone, admin_position from \"User\" join Admin on user_id = admin_id where user_id = \"{}\";".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="User does not exist"), 404
                # Form a dictionary from query results
            admin_profile = {
                "name": results[0][0],
                "email": results[0][1],
                "phone": results[0][2],
                "admin_position": results[0][3]
            }
            return render_template("admin_profile.html", admin=admin_profile), 200

        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view admin profile"), 500


# Change customer password
@app.route('/api/change_password', methods=['POST'])
def change_password():
    '''
    This function changes customer password
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            _oldpassword = request.form.get("old-password")
            _newpassword = request.form.get("new-password")
            cursor = conn.cursor()
            select_sql = "Select password from \"User\" where user_id = {};".format(_userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()
            if len(results) == 0:
                return "Something went wrong", 404
                # return render_template("profile_customer.html", message="Something went wrong"), 404
            if results[0][0] == _oldpassword:
                select_sql = "Update \"User\" set password = \'{}\' where user_id = {};".format(_newpassword, _userid)
                cursor.execute(select_sql)
                conn.commit()
                return "Password Changed Successfully!", 200
                # return render_template("profile_customer.html", message="Password Changed Successfully!"), 200
            else:
                return "Invalid password", 500
                # return render_template("profile_customer.html", message="Invalid password"), 500
    except Exception as e:
        print(e)
        return "Error occurred in changing password", 500
        # return render_template("index.html", message="Error occurred in login"), 500


# View all books
@app.route('/api/view/allbooks', methods=['GET'])
def view_all_books():
    '''
    This function gets details of all available books  
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                         "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("index.html", message="No books available"), 404
            # Form a list of dictionaries for query results
            books = []
            for row in results:
                book = {
                    "Cover_image": row[3],
                    "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
                }
                books.append(book)
            return render_template("home_customer.html", books=books), 200
        else:
            return render_template("index.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in view all books"), 500


# View sale books
@app.route('/api/view/salebooks', methods=['GET'])
def view_all_sale_books():
    '''
    This function gets details of all available sale books  
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, Fixed_Discount, Name "\
                         "from Books_for_Sale natural join book_author BA join author A on BA.author_id = A.author_id;"
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No sale books available"), 404
            # Form a list of dictionaries for query results
            sale_books = []
            for row in results:
                sale_book = {
                    "ISBN": row[0],
                    "Title": row[1],
                    "Price": row[2],
                    "Cover_image": row[3],
                    "Description": row[4],
                    "Page_count": row[5],
                    "Avg_rating": row[6],
                    "Fixed_Discount": row[7],
                    "Author": row[8]
                }
                sale_books.append(sale_book)
            return render_template("sale_books.html", sale_books=sale_books), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view all sale books"), 500


# View rent books
@app.route('/api/view/rentbooks', methods=['GET'])
def view_all_rent_books():
    '''
    This function gets details of all available rent books  
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, Deposit, ROUND(Price*0.3, 2) as rental_fee, Name "\
                         "from Books_for_Rent natural join book_author BA join author A on BA.author_id = A.author_id;"
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No rent books available"), 404
            # Form a list of dictionaries for query results
            rent_books = []
            for row in results:
                rent_book = {
                    "ISBN": row[0],
                    "Title": row[1],
                    "Price": row[2],
                    "Cover_image": row[3],
                    "Description": row[4],
                    "Page_count": row[5],
                    "Avg_rating": row[6],
                    "Deposit": row[7],
                    "Rental_fee": row[8],
                    "Author": row[9]
                }
                rent_books.append(rent_book)
            return render_template("rent_books.html", rent_books=rent_books), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view all rent books"), 500


# View books by category - Academics, Children, Fiction
@app.route('/api/view/category', methods=['GET'])
def view_books_by_category():
    '''
    This function gets details of books according to category - Academics, Children, Fiction  
    Parameter : Category
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            _category = request.form.get('category')
            if _category.lower() == "fiction":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, genre, intro, Name " \
                             "from fiction natural join book_with_rating natural join book_author natural join author;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books available in fiction category"), 404

                books = []
                for row in results:
                    book = {
                        "ISBN": row[0],
                        "Title": row[1],
                        "Price": row[2],
                        "Cover_image": row[3],
                        "Description": row[4],
                        "Page_count": row[5],
                        "Avg_rating": row[6],
                        "Genre": row[7],
                        "Intro": row[8],
                        "Author": row[9]
                    }
                    books.append(book)
                return render_template("category_books.html", books=books, category=_category), 200

            elif _category.lower() == "children":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, age_group, main_character, Name " \
                             "from children natural join book_with_rating natural join book_author BA natural join author A;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books available in children category"), 404

                books = []
                for row in results:
                    book = {
                        "ISBN": row[0],
                        "Title": row[1],
                        "Price": row[2],
                        "Cover_image": row[3],
                        "Description": row[4],
                        "Page_count": row[5],
                        "Avg_rating": row[6],
                        "Age_group": row[7],
                        "Main_character": row[8],
                        "Author": row[9]
                    }
                    books.append(book)
                return render_template("category_books.html", books=books, category=_category), 200

            elif _category.lower() == "academics":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, course, level, Name "\
                    "from Academics natural join book_with_rating natural join book_author BA natural join author A;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books available in academics category"), 404

                books = []
                for row in results:
                    book = {
                        "ISBN": row[0],
                        "Title": row[1],
                        "Price": row[2],
                        "Cover_image": row[3],
                        "Description": row[4],
                        "Page_count": row[5],
                        "Avg_rating": row[6],
                        "Course": row[7],
                        "Level": row[8],
                        "Author": row[9]
                    }
                    books.append(book)
                return render_template("category_books.html", books=books, category=_category), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view books by category"), 500


# View sale books by vendor
@app.route('/api/vendor/view/salebooks', methods=['GET'])
def view_sale_book_vendor():
    '''
    This function gets details of all the sale books uploaded by the vendor
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select Book.ISBN, title, price, cover_image, description, page_count, fixed_discount, avail_qty from Book join Sale_Book on Book.ISBN = Sale_Book.ISBN where Book.vendor_id = {};".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No sale books uploaded"), 404

            sale_books = []
            for row in results:
                sale_book = {
                    "ISBN": row[0],
                    "Title": row[1],
                    "Price": row[2],
                    "Cover_image": row[3],
                    "Description": row[4],
                    "Page_count": row[5],
                    "Fixed_discount": row[6],
                    "Available_quantity": row[7]
                }
                sale_books.append(sale_book)
            return render_template("sale_books.html", sale_books=sale_books), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view sale books uploaded by vendor"), 500


# View rent books by vendor
@app.route('/api/vendor/view/rentbooks', methods=['GET'])
def view_rent_book_vendor():
    '''
    This function gets details of all the rent books uploaded by the vendor
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select Book.ISBN, title, price, cover_image, description, page_count, deposit, rental_fee, qty from Book join Rent_Book on Book.ISBN = Rent_Book.ISBN where Book.vendor_id = {};".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No rent books uploaded"), 404

            rent_books = []
            for row in results:
                rent_book = {
                    "ISBN": row[0],
                    "Title": row[1],
                    "Price": row[2],
                    "Cover_image": row[3],
                    "Description": row[4],
                    "Page_count": row[5],
                    "Deposit": row[6],
                    "Rental_fee": row[7],
                    "Quantity": row[8]
                }
                rent_books.append(rent_book)
            return render_template("rent_books.html", rent_books=rent_books), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print("Exception")
        print(e)
        return render_template("error.html", message="Error occurred in view rent books uploaded by vendor"), 500


# View customer purchase history
@app.route('/api/view/history/purchase', methods=['GET', 'POST'])
def view_purchase_history():
    '''
    This function gets purchase history for a customer
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            _order_id = request.form.get("order_id")
            print(_order_id)
            cursor = conn.cursor()
            select_sql = "Select title, cover_image, qty, S.price, S.ISBN " \
                         "from Sale_Order S join Book B on S.ISBN = B.ISBN natural join Orders " \
                         "where order_id = {};".format(_order_id)

            print(select_sql)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            # if len(results) == 0:
            #     return render_template("error.html", message="No purchases made"), 404

            purchases = []
            for row in results:
                purchase = {
                    "Title": row[0],
                    "Cover_image": row[1],
                    "Quantity": row[2],
                    "Price": row[3],
                    "ISBN": row[4]
                }
                purchases.append(purchase)
            return purchases, 200
            # return render_template("purchase_history.html", purchases=purchases), 200
        else:
            return "Unauthenticated", 401
            # return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return "Error occurred in view purchase history", 500
        # return render_template("error.html", message="Error occurred in view purchase history"), 500


# View customer rent history
@app.route('/api/view/history/rent', methods=['GET'])
def view_rental_history():
    '''
    This function gets rental history for a customer
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select title, cover_image, qty, ROUND(price*0.3, 2) as rent_fee " \
                         "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                         "where order_id IN ( Select order_id from Orders Ord where Ord.customer_id = {})" \
                         "order by date desc;".format(_userid)

            print(select_sql)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No books rented"), 404

            rentals = []
            for row in results:
                rental = {
                    "Title": row[0],
                    "Cover_image": row[1],
                    "Quantity": row[2],
                    "Rental_fee": row[3]
                }
                rentals.append(rental)
            return render_template("rental_history.html", rentals=rentals), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view rental history"), 500


# Get out of stock books
@app.route('/api/view/outofstock', methods=['GET'])
def view_outofstock():
    '''
    This function gets out of stock books and their vendor
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select ISBN, title, cover_image, description, publisher, published_date, price, Name as vendor_name from Out_of_Stock;"

            print(select_sql)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("error.html", message="No out of stock books found"), 404

            out_of_stock_books = []
            for row in results:
                book = {
                    "ISBN": row[0],
                    "Title": row[1],
                    "Cover_image": row[2],
                    "Description": row[3],
                    "Publisher": row[4],
                    "Published_date": row[5],
                    "Price": row[6],
                    "Vendor_name": row[7]
                }
                out_of_stock_books.append(book)
            return render_template("out_of_stock.html", out_of_stock_books=out_of_stock_books), 200
        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view out of stock books"), 500


# Admin views customer rent orders
@app.route('/api/view/orders/rent', methods=['GET'])
def view_rent_order_history():
    '''
    This function gets customer rent orders based on date, customer_username or both
    Parameters : customer username, date
    '''
    try:
        if session.get("user_id"):
            _username = request.form.get("customer_username")
            _date = request.form.get("date")
            cursor = conn.cursor()

            if _username != "":
                getcustomer_sql = "Select user_id from \"User\" where username = \"{}\"".format(
                    _username)
                cursor.execute(getcustomer_sql)
                results = cursor.fetchall()
                _custid = results[0][0]

                select_sql = "Select title, cover_image, qty, R.rent_fee " \
                    "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where order_id IN ( Select order_id from Orders Ord where Ord.customer_id = {})" \
                    "order by date desc;".format(_custid)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books rented by the customer"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Rent Fee": row[3]
                    })
                return render_template("order_history.html", variables=variables), 200
            elif _date != "":
                select_sql = "Select title, cover_image, qty, R.rent_fee " \
                    "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where date = \"{}\" "\
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books rented by the customer"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Rent Fee": row[3]
                    })
                return render_template("order_history.html", variables=variables), 200
            else:
                select_sql = "Select title, cover_image, qty, R.rent_fee " \
                    "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books rented by the customer"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Rent Fee": row[3]
                    })
                return render_template("order_history.html", variables=variables), 200

        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view rental history"), 500


# Admin views customer sale orders
@app.route('/api/view/orders/sale', methods=['GET'])
def view_sale_order_history():
    '''
    This function gets customer sale orders based on date, customer_username or both
    Parameters : customer username, date
    '''
    try:
        if session.get("user_id"):
            _username = request.form.get("customer_username")
            _date = request.form.get("date")
            cursor = conn.cursor()

            if _username != "":
                getcustomer_sql = "Select user_id from \"User\" where username = \"{}\"".format(
                    _username)
                cursor.execute(getcustomer_sql)
                results = cursor.fetchall()
                _custid = results[0][0]

                select_sql = "Select title, cover_image, qty, R.price " \
                    "from Sale_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where order_id IN ( Select order_id from Orders Ord where Ord.customer_id = {})" \
                    "order by date desc;".format(_custid)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books bought by the customer"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Price": row[3]
                    })
                return render_template("sale_order_history.html", variables=variables), 200
            elif _date != "":
                select_sql = "Select title, cover_image, qty, R.price " \
                    "from Sale_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where date = \"{}\" "\
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books bought on given date"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Price": row[3]
                    })
                return render_template("sale_order_history.html", variables=variables), 200
            else:
                select_sql = "Select title, cover_image, qty, R.price " \
                    "from Sale_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return render_template("error.html", message="No books bought yet"), 404

                variables = []
                for row in results:
                    variables.append({
                        "Title": row[0],
                        "Cover Image": row[1],
                        "Quantity": row[2],
                        "Price": row[3]
                    })
                return render_template("sale_order_history.html", variables=variables), 200

        else:
            return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in view rental history"), 500


@app.route('/api/search/category', methods=['GET'])
def search_book_category():
    '''
    This function search the book by the category
    '''
    try:
        # _category = request.form.get('category')
        cursor = conn.cursor()
        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Academics AC ON B.ISBN = AC.ISBN " \
                     "group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        academics = []
        for row in results:
            academics.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(academics)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        fiction = []
        for row in results:
            fiction.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(fiction)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Children C ON B.ISBN = C.ISBN " \
                     "group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        children = []
        for row in results:
            children.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(children)

        return render_template("search_by_category.html", academics=academics, fiction=fiction, children=children), 200

    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in view vendor profile"), 500


@app.route('/api/search/title', methods=['GET', 'POST'])
def search_by_title():
    return render_template("search_by_title.html"), 200


@app.route('/api/search/book/title', methods=['GET', 'POST'])
def search_book_title():
    '''
    This function search the book by the title
    '''
    try:
        _text = request.form.get('searchedbook').lower().strip()
        _location = request.form.get('searchBy')
        print(_text)
        print(_location)
        cursor = conn.cursor()
        if _location == 'title':
            select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                         "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id "\
                         "where position('{}' in LOWER(title)) > 0 group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;".format(_text)
            cursor.execute(select_sql)
            results = cursor.fetchall()
            print(results)
            if len(results) == 0:
                return "No Books Found!", 200

            books = []
            for row in results:
                book = {
                    "Cover_image": row[3],
                    "ISBN": f"{row[0]}",
                    "Title": f"{row[1]}",
                    "Price": f"${row[2]}",
                    "Description": f"{row[4]}",
                    "QTY": row[6] if bool(row[6]) else 0,
                    "Author": f"{row[8]}"
                }
                books.append(book)
            print(books)
            return books, 200

        elif _location == 'description':
            select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                         "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id " \
                         "where LOWER(description) LIKE '%{}%' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;".format(_text)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return "No Books Found!", 200

            books = []
            for row in results:
                book = {
                    "Cover_image": row[3],
                    "ISBN": f"{row[0]}",
                    "Title": f"{row[1]}",
                    "Price": f"${row[2]}",
                    "Description": f"{row[4]}",
                    "QTY": row[6] if bool(row[6]) else 0,
                    "Author": f"{row[8]}"
                }
                books.append(book)
            return books, 200

        else:
            return "Invalid Search", 404

    except Exception as e:
        print(e)
        return "Error occurred in search book", 500


@app.route('/api/search/genre', methods=['GET'])
def search_book_genre():
    '''
    This function search the book by the genre
    '''
    try:
        # _category = request.json['category']
        cursor = conn.cursor()

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Fantasy' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"

        cursor.execute(select_sql)
        results = cursor.fetchall()

        fantasy = []
        for row in results:
            fantasy.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(fantasy)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Thriller' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        thriller = []
        for row in results:
            thriller.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(thriller)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors "\
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Science Fiction' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        science = []
        for row in results:
            science.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(science)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Mystery' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        mystery = []
        for row in results:
            mystery.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(mystery)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Dystopian' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        dystopian = []
        for row in results:
            dystopian.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(dystopian)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Humor' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        humor = []
        for row in results:
            humor.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(humor)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Historical Fiction' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        historical = []
        for row in results:
            historical.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(historical)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Romance' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        romance = []
        for row in results:
            romance.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(romance)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Horror' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        horror = []
        for row in results:
            horror.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(horror)

        select_sql = "Select B.ISBN, Title, Price, Cover_image, Description, Page_count, avail_qty, Avg_rating, STRING_AGG(A.Name, ', ') AS authors " \
                     "from Book_with_rating B natural join book_author BA left join sale_book SB on B.ISBN = SB.ISBN join author A on BA.author_id = A.author_id JOIN Fiction F ON B.ISBN = F.ISBN " \
                     "where F.genre='Paranormal' group by B.ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, avail_qty;"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        paranormal = []
        for row in results:
            paranormal.append({
                "Cover_image": row[3],
                "book_data": f'{{"ISBN": "{row[0]}", "Title": "{row[1]}", "Price": "${row[2]}", "Cover_image": "{row[3]}", "Description": "{row[4]}", "Page_count": "{row[5]}", "QTY": "{row[6] if bool(row[6]) else 0}", "Avg_rating": "{row[7]}", "Author": "{row[8]}"}}'
            })
        print(paranormal)

        return render_template("search_by_genre.html", science=science, thriller=thriller, fantasy=fantasy, mystery=mystery, dystopian=dystopian, humor=humor, historical=historical, romance=romance, horror=horror, paranormal=paranormal), 200

    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in search by genre"), 500


@app.route('/api/sort/price', methods=['GET'])
def sort_based_price():
    '''
    This function sort the book by the price
    '''
    try:
        _min_price = request.form.get("min_price")
        _max_price = request.form.get("max_price")
        cursor = conn.cursor()
        select_sql = "SELECT ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating FROM Book_with_rating WHERE Price >= %s AND Price <= %s ORDER BY Price"
        cursor.execute(select_sql, (_min_price, _max_price))
        results = cursor.fetchall()

        if len(results) == 0:
            return render_template("error.html", message="Invalid search"), 404

        variables = []
        for row in results:
            variables.append({
                "ISBN": row[0],
                "Title": row[1],
                "Price": row[2],
                "Cover Image": row[3],
                "Description": row[4],
                "Page Count": row[5],
                "Avg Rating": row[6]
            })
        return render_template("sort_based_price.html", variables=variables), 200

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in price profile"), 500


@app.route('/api/sort/ratings', methods=['GET'])
def sort_based_rating():
    '''
    This function sort the book by the ratings
    '''
    try:
        cursor = conn.cursor()
        select_sql = "SELECT ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating FROM Book_with_rating ORDER BY Avg_rating"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return render_template("error.html", message="Invalid search"), 404

        variables = []
        for row in results:
            variables.append({
                "ISBN": row[0],
                "Title": row[1],
                "Price": row[2],
                "Cover Image": row[3],
                "Description": row[4],
                "Page Count": row[5],
                "Avg Rating": row[6]
            })
        return render_template("sort_based_rating.html", variables=variables), 200

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in sort ratings"), 500


@app.route('/api/display/address', methods=['GET'])
def display_address():
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "select addr_id, street, apt, city, pin from Address where customer_id={}".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()
            if len(results) == 0:
                return "No address Found", 404
            print(results)
            variables = []
            for row in results:
                variables.append({
                    "address_id": row[0],
                    "Street": row[1],
                    "Apartment": row[2],
                    "City": row[3],
                    "Pin": row[4]
                })

            return variables, 200
        # return render_template("display_address.html", variables=variables), 200
        else:
            return "Unauthenticated", 401

    except Exception as e:
        print(e)
        return "Error occurred in display address", 500
        # return render_template("error.html", message="Error occurred in display address"), 500


@app.route('/api/add/address', methods=['POST'])
def add_address():
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            _street = request.form.get("street")
            _apt = request.form.get("apt")
            _city = request.form.get("city")
            _pin = request.form.get("pin")
            cursor = conn.cursor()
            select_sql = "select max(addr_id) from Address where customer_id = {}".format(_userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()
            if bool(results[0][0]):
            # val = helper.get_json_response(cursor.description, results)[
            #     'Results'][0]['max(addr_id)']
                insert_sql = "insert into Address (customer_id, addr_id, street, apt, city, pin) values ({}, {}, '{}', '{}', '{}', '{}')".format(
                    _userid, results[0][0]+1, _street, _apt, _city, _pin)
            else:
                insert_sql = "insert into Address (customer_id, addr_id, street, apt, city, pin) values ({}, {}, '{}', '{}', '{}', '{}')".format(
                    _userid, 1, _street, _apt, _city, _pin)
            cursor.execute(insert_sql)
            conn.commit()
            return "Address added successfully", 200
            # return render_template("success.html", message="Address added successfully"), 200
        else:
            return "Unauthenticated", 401
            # return render_template("error.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return "Error occurred while adding address", 500
        # return render_template("error.html", message="Error occurred while adding address"), 500


@app.route('/api/delete/address', methods=['GET', 'POST'])
def delete_address():
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            _address_id = request.form.get("address_id")
            cursor = conn.cursor()
            delete_sql = "delete from Address where customer_id = {} and addr_id = {}".format(
                _userid, _address_id)
            cursor.execute(delete_sql)
            if cursor.rowcount == 0:
                return "Invalid address id", 404
                # return render_template("error.html", message="Invalid address id"), 404
            conn.commit()
            return "Address deleted successfully", 200
            # return render_template("success.html", message="Address deleted successfully"), 200
        else:
            return "Unauthenticated", 401

    except Exception as e:
        print(e)
        return "Error occurred while deleting address", 500
        # return render_template("error.html", message="Error occurred while deleting address"), 500


# Add to cart
@app.route('/api/customer/add_to_cart', methods=['POST'])
def add_to_cart():
    '''
    This function adds book to cart for a particular customer
    Parameters: isbn, for_rent, for_sale, qty
    '''
    try:
        print("Inside method")
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return render_template("index.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _isbn = _isbn.replace("ISBN: ", "")
        # _for_rent = request.form.get("for_rent")
        # _for_sale = request.form.get("for_sale")
        _qty = request.form.get("qty")

        # if (bool(_for_sale) and bool(_for_rent)) or _for_rent == _for_sale or not bool(_qty) or not bool(_isbn):
        #     return render_template("error.html", message="False Inputs!"), 400

        # if bool(_for_sale):
        #     _available_qty = "SELECT avail_qty from sale_book where ISBN = \"{}\";".format(_isbn)
        #     if cursor.execute(_available_qty) < _qty:
        #         return render_template("error.html", message="Exceeds Available Quantity!"), 400
        #
        # else:
        #     _available_qty = "SELECT qty from rent_book where ISBN = \"{}\";".format(_isbn)
        #     if cursor.execute(_available_qty) < _qty:
        #         return render_template("error.html", message="Exceeds Available Quantity!"), 400

        sql = "Select * from cart where ISBN = '{}' and customer_id = {} and for_sale = 'true' and for_rent = 'false';".format(
            _isbn, _userid)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(sql)

        if len(results) != 0:
            return "Item Already in Cart", 404

        sql = "INSERT into Cart(customer_id, isbn, for_rent, for_sale, qty) values ({},'{}','false','true',{});".format(
            _userid, _isbn, _qty)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return "Error occurred in Add-to-cart", 500
        # return render_template("home_customer.html", message="Error occurred in Add-to-cart"), 500

    return "Successfully added to cart!", 200
    # return render_template("success.html", message="Successfully added to cart!"), 200


# Update qty in cart
@app.route('/api/customer/update_qty_in_cart', methods=['POST'])
def update_qty_in_cart():
    '''
    This function updates qty of books in cart for a particular customer
    Parameters: isbn, for_rent, for_sale, qty
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return "Unauthenticated", 401
            # return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        # _for_rent = request.form.get("for_rent")
        # _for_sale = request.form.get("for_sale")
        _qty = request.form.get("qty")

        # if not bool(_qty) or not bool(_isbn):
        #     return render_template("error.html", message="False Inputs!"), 400

        # if bool(_for_sale):
        #     _available_qty = "SELECT avail_qty from sale_book where ISBN = \"{}\";".format(_isbn)
        #     if cursor.execute(_available_qty) < _qty:
        #         return render_template("error.html", message="Exceeds Available Quantity!"), 400

        # else:
        #     _available_qty = "SELECT qty from rent_book where ISBN = \"{}\";".format(_isbn)
        #     if bool(cursor.execute(_available_qty)) and cursor.fetchone()[0] < _qty:
        #         return render_template("error.html", message="Exceeds Available Quantity!"), 400

        sql = "UPDATE Cart SET qty = {} where customer_id = {} and isbn = '{}' and for_rent = 'false' and for_sale = 'true';".format(
            _qty, _userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return "Error occurred in updating quantity", 500
        # return render_template("error.html", message="Error occurred in updating quantity"), 500

    return "Successfully updated quantity!", 200
    # return render_template("success.html", message="Successfully updated quantity!"), 200


# Remove from cart
@app.route('/api/customer/remove_from_cart', methods=['POST'])
def remove_from_cart():
    '''
    This function removes book from cart for a particular customer
    Parameters: isbn, for_rent, for_sale
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return "Unauthenticated", 401
            # return render_template("cart.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        # _for_rent = request.form.get("for_rent")
        # _for_sale = request.form.get("for_sale")

        sql = "DELETE from Cart where customer_id = {} and ISBN = '{}' and for_rent = 'false' and for_sale = 'true';".format(
            _userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return "Error occurred in Remove-from-cart", 500
        # return render_template("cart.html", message="Error occurred in Remove-from-cart"), 500

    return "Successfully removed from cart!", 200
    # return render_template("cart.html", message="Successfully removed from cart!"), 200


@app.route('/api/cart', methods=['GET', 'POST'])
def cart():
    return render_template("cart.html"), 200


# View cart
@app.route('/api/customer/view_cart', methods=['GET'])
def view_cart():
    '''
    This function lists items in cart
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
        else:
            return render_template("index.html", message="Unauthenticated"), 401

        _sale_books = "Select ISBN, title, cover_image, price, qty, price*qty, avail_qty as amount from ((cart natural join book) natural join sale_book) where customer_id = {} and for_rent = false".format(_userid)
        # _rent_books = "Select ISBN, title, cover_image, for_rent, for_sale, qty, ((price*0.30)+deposit)*qty as amount from ((cart natural join book) natural join rent_book) where customer_id = \"{}\" and for_sale = 0;".format(_userid)
        # sql = "{} union {}".format(_sale_books, _rent_books)
        print(_sale_books)
        cursor.execute(_sale_books)
        results = cursor.fetchall()

        if len(results) == 0:
            return render_template("cart.html", message="No item in cart"), 200

        variables = []
        for row in results:
            variables.append({
                "ISBN": row[0],
                "Title": row[1],
                "Cover Image": row[2],
                "Price": row[3],
                "QTY": row[4],
                "Amount": row[5],
                "Available": row[6]
            })

    except Exception as e:
        print(e)
        return render_template("cart.html", message="Error occurred in View-cart"), 500

    return render_template("cart.html", variables=variables), 200


# Add to wishlist
@app.route('/api/customer/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    '''
    This function adds book to wishlist for a particular customer
    Parameters: isbn
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")

        sql = "INSERT into Wishlist(customer_id, isbn) values (\"{}\",\"{}\");".format(_userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Add-to-wishlist"), 500

    return render_template("success.html", message="Successfully added to wishlist!"), 200


# Remove from wishlist
@app.route('/api/customer/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    '''
    This function removes book from wishlist for a particular customer
    Parameters: isbn
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")

        sql = "DELETE from Wishlist where customer_id = \"{}\" and ISBN = \"{}\";".format(_userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Remove-from-wishlist"), 500

    return render_template("success.html", message="Successfully removed from wishlist!"), 200


# Admin toggles visibility of a book
@app.route('/api/admin/toggle_visibility_of_book', methods=['POST'])
def toggle_visibility_of_book():
    '''
    This function helps admin toggle visibility of a book
    Parameters: ISBN, visibility
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            admin = cursor.execute("Select * from admin where admin_id = \"{}\";".format(_userid))
            if not bool(admin):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _visibility = request.form.get("visibility")

        sql = "UPDATE book SET visibility = \"{}\" where ISBN = \"{}\";".format(_visibility, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in toggling visibility-of-book"), 500

    return render_template("success.html", message="Successfully toggled visibility of book!"), 200


# Rate a book
@app.route('/api/customer/rate_a_book', methods=['POST'])
def rate_a_book():
    '''
    This function allows customer to rate a book
    Parameters: ISBN, rating
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _rating = request.form.get("rating")
        _sale_order = "SELECT customer_id, ISBN from (Sale_order natural join Orders) where customer_id = \"{}\" and ISBN = \"{}\"".format(_userid, _isbn)
        _rent_order = "SELECT customer_id, ISBN from (Rent_order natural join Orders) where customer_id = \"{}\" and ISBN = \"{}\";".format(_userid, _isbn)
        ordered = cursor.execute("{} union {};".format(_sale_order, _rent_order))
        if not bool(ordered):
            return render_template("error.html", message="Permission denied"), 403

        sql = "INSERT into Feedback(customer_id, ISBN, rating) values(\"{}\", \"{}\", \"{}\");".format(_userid, _isbn, _rating)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Rate-a-book"), 500

    return render_template("success.html", message="Successfully rated a book!"), 200


# Add a book
@app.route('/api/vendor/add_a_book', methods=['POST'])
def add_a_book():
    '''
    This function allows vendor to add a book
    Parameters: isbn, title, price, cover_image, page_count, description, publisher, published_date, authors
                is_salebook: fixed_discount, avail_qty
                is_rentbook: deposit, qty, rental_fee
                is_fiction: genre, intro
                is_children: age_group, main_character
                is_academics: course, level
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            vendor = cursor.execute("Select * from vendor where vendor_id = \"{}\";".format(_userid))
            if not bool(vendor):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _title = request.form.get("title")
        _price = request.form.get("price")
        _cover_image = request.form.get("cover_image")
        _page_count = request.form.get("page_count")
        _description = request.form.get("description")
        _publisher = request.form.get("publisher")
        _published_date = request.form.get("published_date")
        _authors = request.form.get("authors")

        add_book = "INSERT into book(ISBN,title,price,cover_image,page_count,description,publisher,published_date, vendor_id) values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\", \"{}\");".format(
            _isbn, _title, _price, _cover_image, _page_count, _description, _publisher, _published_date, _userid)
        cursor.execute(add_book)

        for item in _authors:
            author = cursor.execute("SELECT author_id from author where name = \"{}\";".format(item.strip()))
            if bool(author):
                index = cursor.fetchone()[0]
                book_author = "INSERT into book_author(ISBN,author_id) values(\"{}\",\"{}\");".format(_isbn, index)
                cursor.execute(book_author)
            else:
                cursor.execute("Select max(author_id) from author;")
                index = cursor.fetchone()[0]
                add_author = "INSERT into author(author_id,name) values(\"{}\",\"{}\");".format(index+1, item.strip())
                cursor.execute(add_author)
                book_author = "INSERT into book_author(ISBN,author_id) values(\"{}\",\"{}\");".format(_isbn, index+1)
                cursor.execute(book_author)

        _is_salebook = request.form.get("is_salebook")
        _is_rentbook = request.form.get("is_rentbook")
        _is_fiction = request.form.get("is_fiction")
        _is_children = request.form.get("is_children")
        _is_academics = request.form.get("is_academics")

        if bool(_is_salebook):
            _fixed_discount = request.form.get("fixed_discount")
            _avail_qty = request.form.get("avail_qty")
            sale_book = "INSERT into sale_book(isbn,fixed_discount,avail_qty) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _fixed_discount, _avail_qty)
            cursor.execute(sale_book)

        if bool(_is_rentbook):
            _deposit = request.form.get("deposit")
            _qty = request.form.get("qty")
            _rental_fee = request.form.get("rental_fee")
            rent_book = "INSERT into rent_book(isbn,deposit,qty,rental_fee) values(\"{}\",\"{}\",\"{}\",\"{}\")".format(_isbn, _deposit, _qty, _rental_fee)
            cursor.execute(rent_book)

        if bool(_is_fiction):
            _genre = request.form.get("genre")
            _intro = request.form.get("intro")
            fiction = "INSERT into fiction(isbn,genre,intro) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _genre, _intro)
            cursor.execute(fiction)

        if bool(_is_children):
            _age_group = request.form.get("age_group")
            _main_character = request.form.get("main_character")
            children = "INSERT into children(isbn,age_group,main_character) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _age_group, _main_character)
            cursor.execute(children)

        if bool(_is_academics):
            _course = request.form.get("course")
            _level = request.form.get("level")
            academics = "INSERT into academics(isbn,course,level) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _course, _level)
            cursor.execute(academics)

        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Add-a-book"), 500

    return render_template("success.html", message="Successfully added a book!"), 200


# Remove a book
@app.route('/api/vendor/remove_a_book', methods=['POST'])
def remove_a_book():
    '''
    This function allows vendor to remove a book
    Parameters: isbn
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            vendor = cursor.execute("Select * from vendor where vendor_id = \"{}\";".format(_userid))
            if not bool(vendor):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        book = "SELECT vendor_id, isbn from book where vendor_id = \"{}\" and isbn = \"{}\";".format(_userid, _isbn)
        cursor.execute(book)
        if not bool(book):
            return render_template("error.html", message="Permission denied"), 403

        sql = "DELETE from sale_book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        sql = "DELETE from rent_book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        sql = "DELETE from book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Remove-a-book"), 500

    return render_template("success.html", message="Successfully removed a book!"), 200


# Update book data
@app.route('/api/vendor/update_book_data', methods=['POST'])
def update_book_data():
    '''
    This function allows vendor to update book data
    Parameters: isbn, price, is_sale, is_rent
                If is_sale : avail_qty, fixed_discount
                If is_rent : deposit, rental_fee, qty
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            vendor = cursor.execute("Select * from vendor where vendor_id = \"{}\";".format(_userid))
            if not bool(vendor):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _price = request.form.get("price")
        _is_sale = request.form.get("is_sale")
        _is_rent = request.form.get("is_rent")

        book = "SELECT vendor_id, isbn from book where vendor_id = \"{}\" and isbn = \"{}\";".format(_userid, _isbn)
        cursor.execute(book)
        if not bool(book):
            return render_template("error.html", message="Permission denied"), 403
        update_book = "UPDATE book SET price = \"{}\" where ISBN = \"{}\";".format(_price, _isbn)
        cursor.execute(update_book)

        if bool(_is_sale):
            _fixed_discount = request.form.get("fixed_discount")
            _avail_qty = request.form.get("avail_qty")
            sale_book = cursor.execute("SELECT * from sale_book where ISBN = \"{}\";".format(_isbn))
            if bool(sale_book):
                cursor.execute("UPDATE sale_book SET fixed_discount = \"{}\", avail_qty = \"{}\" where ISBN = \"{}\";".format(_fixed_discount, _avail_qty, _isbn))
            else:
                cursor.execute("INSERT into sale_book(ISBN,fixed_discount,avail_qty) values(\"{}\",\"{}\",\"{}\");".format(_isbn, _fixed_discount, _avail_qty))
        else:
            cursor.execute("DELETE from sale_book where ISBN = \"{}\";".format(_isbn))

        if bool(_is_rent):
            _deposit = request.form.get("deposit")
            _rental_fee = request.form.get("rental_fee")
            _qty = request.form.get("qty")
            rent_book = cursor.execute("SELECT * from rent_book where ISBN = \"{}\";".format(_isbn))
            if bool(rent_book):
                cursor.execute("UPDATE rent_book SET deposit = \"{}\",qty = \"{}\",rental_fee = \"{}\" where ISBN = \"{}\";".format(
                        _deposit, _qty, _rental_fee, _isbn))
            else:
                cursor.execute("INSERT into rent_book(ISBN,deposit,qty,rental_fee) values(\"{}\",\"{}\",\"{}\",\"{}\");".format(
                        _isbn, _deposit, _qty, _rental_fee))
        else:
            cursor.execute("DELETE from rent_book where ISBN = \"{}\";".format(_isbn))

        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Update-book-data"), 500

    return render_template("success.html", message="Successfully updated book data!"), 200


# Vendors to approve
@app.route('/api/admin/vendors_to_approve', methods=['GET'])
def vendors_to_approve():
    '''
    This function lists vendors waiting for approval from the Admin
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            admin = cursor.execute("Select * from admin where admin_id = \"{}\";".format(_userid))
            if not bool(admin):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        sql = "SELECT Name, email, phone, city, company from Vendor_to_Approve;"
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return render_template("error.html", message="No vendor in waitlist for approval"), 404

        variables = []
        for row in results:
            variables.append({
                "Name": row[0],
                "email": row[1],
                "phone": row[2],
                "city": row[3],
                "company": row[4]
            })

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Vendors-to-approve"), 500

    return render_template("vendors_to_approve.html", variables=variables), 200


# Approve vendor
@app.route('/api/admin/approve_vendor', methods=['POST'])
def approve_vendor():
    '''
    This function helps admin approve vendor
    Parameters: username, is_approve
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            admin = cursor.execute("Select * from admin where admin_id = \"{}\";".format(_userid))
            if not bool(admin):
                return render_template("error.html", message="Permission denied"), 403
        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _username = request.form.get("username")
        _is_approve = request.form.get("is_approve")
        cursor.execute("SELECT vendor_id from vendor where username = \"{}\";".format(_username))
        _vendor_id = cursor.fetchone()[0]

        if bool(_is_approve):
            sql = "UPDATE vendor SET admin = \"{}\" where vendor_id = \"{}\";".format(_userid, _vendor_id)
            print(sql)
            cursor.execute(sql)
        else:
            sql = "DELETE from vendor where vendor_id = \"{}\";".format(_vendor_id)
            cursor.execute(sql)
            sql = "DELETE from user where user_id = \"{}\";".format(_vendor_id)
            cursor.execute(sql)

        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in approving a vendor"), 500

    return render_template("success.html", message="Successfully approved/disapproved a vendor!"), 200


# Place an order
@app.route('/api/customer/place_an_order', methods=['POST'])
def place_an_order():
    '''
    This function places an order for the customer
    Parameters: address_id
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return "Unauthenticated", 401
            # return render_template("error.html", message="Unauthenticated"), 401

        _address_id = request.form.get("address_id")
        _total = request.form.get("total")
        print(_total)
        _date = datetime.date.today()
        print(_date)

        create_order = "INSERT into orders(customer_id,date,status,invoice_amount,address_id) values({},'{}','Ordered',{},{});".format(
            _userid, _date, _total, _address_id)
        cursor.execute(create_order)
        print(create_order)
        cursor.execute("SELECT max(order_id) from orders;")
        _order_id = cursor.fetchone()[0]
        print(_order_id)

        # cursor.execute("SELECT cart.ISBN, cart.qty, ((price*0.30)+deposit)*cart.qty, rent_book.qty from ((cart join rent_book on cart.ISBN = rent_book.ISBN) join book on cart.ISBN = book.ISBN) where customer_id = \"{}\" and for_sale = 0;".format(_userid))
        # _rent_books = cursor.fetchall()
        # print(_rent_books)

        # _due_date = _date + datetime.timedelta(days=14)
        # for item in _rent_books:
        #     cursor.execute("INSERT into rent_order(order_id,ISBN,issue_date,due_date,qty,rent_fee) values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(
        #         _order_id, item[0], _date, _due_date, item[1], item[2]))
        #     cursor.execute("UPDATE rent_book SET qty = \"{}\" where ISBN = \"{}\";".format(item[3]-item[1], item[0]))

        cursor.execute("SELECT ISBN, qty, price*qty, avail_qty from ((cart natural join book) natural join sale_book)  where customer_id = {} and for_rent = 'false' and for_sale = 'true';".format(_userid))
        _sale_books = cursor.fetchall()
        print(_sale_books)

        for item in _sale_books:
            cursor.execute("INSERT into sale_order(order_id,ISBN,qty,price) values({},'{}',{},{});".format(
                _order_id, item[0], item[1], item[2]))
            cursor.execute("UPDATE sale_book SET avail_qty = {} where ISBN = '{}';".format(item[3]-item[1], item[0]))

        cursor.execute("DELETE from cart where customer_id = {};".format(_userid))

        # cursor.execute("SELECT sum(rent_fee) from rent_order where order_id = \"{}\" group by order_id;".format(_order_id))
        # _total_rent_fee = cursor.fetchone()[0]
        # cursor.execute("SELECT sum(price) from sale_order where order_id = \"{}\" group by order_id;".format(_order_id))
        # _total_price = cursor.fetchone()[0]
        # _invoice_ammount = _total_rent_fee + _total_price
        # cursor.execute("UPDATE orders SET invoice_amount = \"{}\" where order_id = \"{}\";".format(_invoice_ammount,_order_id))
        conn.commit()

    except Exception as e:
        print(e)
        return "Error occurred in Add-to-cart", 500
        # return render_template("error.html", message="Error occurred in Add-to-cart"), 500

    return "Successfully added to cart!", 200
    # return render_template("success.html", message="Successfully added to cart!"), 200


# Customer Order History
@app.route('/api/customer/order_history', methods=['GET', 'POST'])
def order_history():
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select order_id, date, status, invoice_amount, street, apt, city, pin " \
                         "from orders O join address A on O.customer_id = A.customer_id and A.addr_id = O.address_id " \
                         "where O.customer_id={} " \
                         "order by date desc;".format(_userid)

            print(select_sql)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return render_template("order_history.html", orders=[]), 200

            orders = []
            for row in results:
                order = {
                    "order_id": row[0],
                    "date": row[1],
                    "status": row[2],
                    "invoice_amount": row[3],
                    "address": f"{row[5]} - {row[4]}, {row[6]}, {row[7]}"
                }
                orders.append(order)
            return render_template("order_history.html", orders=orders), 200
        else:
            return render_template("index.html", message="Unauthenticated"), 401
    except Exception as e:
        print(e)
        return render_template("index.html", message="Error occurred in view order history"), 500


# Return Book
@app.route('/api/customer/return_book', methods=['POST'])
def return_book():
    '''
    This function allows customer to return books
    Parameters: order_id, ISBN
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _isbn = request.form.get("isbn")
        _order_id = request.form.get("order_id")
        _date = datetime.date.today()
        print(_date)

        _return = "UPDATE rent_order SET return_date = \"{}\" where order_id = \"{}\" and ISBN = \"{}\";".format(_date, _order_id, _isbn)
        print(_return)
        cursor.execute(_return)
        cursor.execute("SELECT qty from rent_order where order_id = \"{}\" and ISBN = \"{}\";".format(_order_id, _isbn))
        _qty = cursor.fetchone()[0]
        print(_qty)
        _update_qty = "UPDATE rent_book SET qty = qty + \"{}\" where ISBN = \"{}\";".format(_qty, _isbn)
        print(_update_qty)
        cursor.execute(_update_qty)
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Return-book"), 500

    return render_template("success.html", message="Successfully returned book!"), 200


# Make payment
@app.route('/api/customer/make_payment', methods=['POST'])
def make_payment():
    '''
    This function allows customer to complete transaction
    Parameters: order_id
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return render_template("error.html", message="Unauthenticated"), 401

        _order_id = request.form.get("order_id")
        _time = datetime.datetime.now()
        print(_time)

        sql = "INSERT into transaction(order_id, payment_status, time) value(\"{}\",\"Paid\",\"{}\")".format(_order_id, _time)
        print(sql)
        cursor.execute(sql)
        cursor.execute("UPDATE orders SET status=\"Completed\" where order_id = \"{}\";".format(_order_id))
        conn.commit()

    except Exception as e:
        print(e)
        return render_template("error.html", message="Error occurred in Make-payment"), 500

    return render_template("success.html", message="Successfully paid!"), 200


if __name__ == "__main__":
    app.run(debug=True)
