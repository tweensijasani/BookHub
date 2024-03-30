from flask import Flask, request, session, jsonify
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
def main():
    return "Welcome!"


# Sign-up admin
@app.route('/api/admin/signup', methods=['POST'])
def signup_admin():
    '''
    This function registers new admin user 
    Parameters : Username, password, email-id, phone-number, name, position
    '''
    # Validate data
    try:
        response = validation.validate_data(request.json["name"],
                                            request.json["email"],
                                            request.json["phone"],
                                            request.json["password"],
                                            request.json["username"])
        if response[1] != 200:
            return response
        if not request.json["position"]:
            return jsonify({"Message": "Please enter position."}), 500
        if not validation.validate_admin_position(request.json["position"]):
            return jsonify({"Message": "Invalid position."}), 500

        # Read the input from signup page and register a new user
        _name = request.json["name"]
        _email = request.json["email"]
        _phone = request.json["phone"]
        _password = request.json["password"]
        _username = request.json["username"]
        _position = request.json["position"]

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values (0,\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
            _username, _password, _email, _phone, _name)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        # print(results)

        _userid = results[0][0]
        sql = "INSERT into Admin(admin_id, admin_position) values (\"{}\",\"{}\")".format(
            _userid, _position)
        # print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in Sign-up"}), 500

    return jsonify({"Message": "Successfully registered."}), 200


# Sign-up vendor
@app.route('/api/vendor/signup', methods=['POST'])
def signup_vendor():
    '''
    This function registers new vendor 
    Parameters : Username, password, email-id, phone-number, name, city, company
    '''
    # Validate data
    try:
        response = validation.validate_data(request.json["name"],
                                            request.json["email"],
                                            request.json["phone"],
                                            request.json["password"],
                                            request.json["username"])
        if response[1] != 200:
            return response

        # read the input from signup page and register a new user
        _name = request.json["name"]
        _email = request.json["email"]
        _phone = request.json["phone"]
        _password = request.json["password"]
        _username = request.json["username"]
        _city = request.json["city"]
        _company = request.json["company"]

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values (0,\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
            _username, _password, _email, _phone, _name)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        # print(results)

        _userid = results[0][0]
        sql = "INSERT into Vendor(vendor_id, city, company, admin_id) values (\"{}\", \"{}\", \"{}\", NULL)".format(
            _userid, _city, _company)
        # print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in Sign-up"}), 500

    return jsonify({"Message": "Successfully registered."}), 200


# Sign-up customer
@app.route('/api/customer/signup', methods=['POST'])
def signup_customer():
    '''
    This function registers new customer
    Parameters : Username, password, email-id, phone-number, name, bank_name, bank_acc
    '''
    # Validate data
    try:
        response = validation.validate_data(request.json["name"],
                                            request.json["email"],
                                            request.json["phone"],
                                            request.json["password"],
                                            request.json["username"])
        if response[1] != 200:
            return response
        if not validation.validate_account(request.json["account"]):
            return jsonify({"Message": "Invalid account number."}), 500

        # read the input from signup page and register a new user
        _name = request.json["name"]
        _email = request.json["email"]
        _phone = request.json["phone"]
        _password = request.json["password"]
        _username = request.json["username"]
        _bank = request.json["bank"]
        _account = request.json["account"]

        cursor = conn.cursor()
        sql = "INSERT into \"User\"(user_id, username, password, email, phone, Name) values (0,\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
            _username, _password, _email, _phone, _name)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        select_sql = "Select user_id from \"User\" where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()

        _userid = results[0][0]
        sql = "INSERT into Customer(customer_id, bank_name, bank_acc) values (\"{}\", \"{}\", \"{}\")".format(
            _userid, _bank, _account)
        # print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in Sign-up"}), 500

    return jsonify({"Message": "Successfully registered."}), 200


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
            response = validation.validate_data(request.json["name"],
                                                request.json["email"],
                                                request.json["phone"],
                                                request.json["password"],
                                                request.json["username"])
            if response[1] != 200:
                return response
            if not validation.validate_account(request.json["account"]):
                return jsonify({"Message": "Invalid account number."}), 500

            # read the input from signup page and register a new user
            _name = request.json["name"]
            _email = request.json["email"]
            _phone = request.json["phone"]
            _password = request.json["password"]
            _bank = request.json["bank"]
            _account = request.json["account"]

            cursor = conn.cursor()
            update_user_sql = "UPDATE \"User\" SET password = \"{}\", email = \"{}\", phone = \"{}\", name = \"{}\" where user_id = {} ;".format(
                _password, _email, _phone, _name, _userid)
            cursor.execute(update_user_sql)
            conn.commit()

            update_sql = "Update Customer set bank_name = \"{}\", bank_acc = \"{}\" where customer_id = {} ;".format(
                _bank, _account, _userid)
            # print(sql)
            cursor.execute(update_sql)
            conn.commit()

        else:
            return jsonify({"Message": "Unauthenticated"}), 401

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in updating customer data"}), 500

    return jsonify({"Message": "Successfully updated customer details."}), 200


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
            response = validation.validate_data(request.json["name"],
                                                request.json["email"],
                                                request.json["phone"],
                                                request.json["password"],
                                                request.json["username"])
            if response[1] != 200:
                return response

            # read the input from signup page and register a new user
            _name = request.json["name"]
            _email = request.json["email"]
            _phone = request.json["phone"]
            _password = request.json["password"]
            _city = request.json["city"]
            _company = request.json["company"]

            cursor = conn.cursor()
            update_user_sql = "UPDATE \"User\" SET password = \"{}\", email = \"{}\", phone = \"{}\", name = \"{}\" where user_id = {} ;".format(
                _password, _email, _phone, _name, _userid)
            cursor.execute(update_user_sql)
            conn.commit()

            update_sql = "Update Vendor set city = \"{}\", company = \"{}\" where vendor_id = {} ;".format(
                _city, _company, _userid)
            # print(sql)
            cursor.execute(update_sql)
            conn.commit()

        else:
            return jsonify({"Message": "Unauthenticated"}), 401

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in updating vendor data"}), 500

    return jsonify({"Message": "Successfully updated vendor details."}), 200


# Admin login
@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    '''
    This function is for admin login 
    Parameters : Username, password
    '''
    try:
        _username = request.json["username"]
        _password = request.json["password"]
        cursor = conn.cursor()
        select_sql = "Select password, user_id from \"User\" join Admin on user_id = admin_id where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return jsonify({"Message": "User does not exist"}), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            return jsonify({"Message": "Login successful"}), 200
        else:
            return jsonify({"Message": "Invalid password"}), 500
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in login"}), 500


# Vendor login
@app.route('/api/vendor/login', methods=['POST'])
def login_vendor():
    '''
    This function is for vendor login 
    Parameters : Username, password
    '''
    try:
        _username = request.json["username"]
        _password = request.json["password"]
        cursor = conn.cursor()
        select_sql = "Select password, user_id, admin_id from \"User\" join Vendor on user_id = vendor_id where username = \"{}\"".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            return jsonify({"Message": "User does not exist"}), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            msg = "Login succesful"
            if results[0][2] == None:
                print("Vendor is not approved")
                msg += ", vendor not approved"
            return jsonify({"Message": msg}), 200
        else:
            return jsonify({"Message": "Invalid password"}), 500
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in login"}), 500


# Customer login
@app.route('/api/customer/login', methods=['POST'])
def login_customer():
    '''
    This function is for customer login 
    Parameters : Username, password
    '''
    try:
        _username = request.json["username"]
        _password = request.json["password"]
        print(_username)
        print(_password)
        cursor = conn.cursor()
        select_sql = "Select password, user_id from \"User\" join Customer on user_id = customer_id where username = \'{}\'".format(
            _username)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return jsonify({"Message": "User does not exist"}), 404
        if results[0][0] == _password:
            print("Login successful")
            session["user_id"] = results[0][1]
            return jsonify({"Message": "Login successful"}), 200
        else:
            return jsonify({"Message": "Invalid password"}), 500
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in login"}), 500


# Logout
@app.route('/api/user/logout', methods=['POST'])
def logout():
    '''
    This function logs user out of current session 
    '''
    try:
        if session.get("user_id"):
            session["user_id"] = None
            return jsonify({"Message": "Logged out"}), 200
        else:
            return jsonify({"Message": "Error occured in logout"}), 500
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in logout"}), 500


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
                return jsonify({"Message": "User does not exist"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view vendor profile"}), 500


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
            select_sql = "Select Name, email, phone, bank_name, bank_acc, street, apt, city, pin from (\"User\" join Customer C on user_id = customer_id) join Address A on C.customer_id = A.customer_id where user_id = \"{}\";".format(
                _userid)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return jsonify({"Message": "User does not exist"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view customer profile"}), 500


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
                return jsonify({"Message": "User does not exist"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200

        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view admin profile"}), 500


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
            select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, Name "\
                         "from Book_with_rating natural join book_author BA join author A on BA.author_id = A.author_id;"
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return jsonify({"Message": "No books available"}), 404
            # Form json response for query results
            book_authors = helper.get_book_authors(results)

            select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating from Book_with_rating;"
            cursor.execute(select_sql)
            results = cursor.fetchall()
            json_result = helper.get_book_with_authors(
                book_authors, cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view all books"}), 500


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
                return jsonify({"Message": "No sale books available"}), 404
            # Form json response for query results
            book_authors = helper.get_book_authors(results)

            select_sql = " Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, Fixed_Discount from Books_for_Sale"
            cursor.execute(select_sql)
            results = cursor.fetchall()
            json_result = helper.get_book_with_authors(
                book_authors, cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view all sale books"}), 500


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
                return jsonify({"Message": "No rent books available"}), 404
            # Form json response for query results
            book_authors = helper.get_book_authors(results)

            select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, Deposit, ROUND(Price*0.3, 2) as rental_fee from Books_for_Rent;"
            cursor.execute(select_sql)
            results = cursor.fetchall()
            json_result = helper.get_book_with_authors(
                book_authors, cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)

        return jsonify({"Message": "Error occured in view all rent books"}), 500


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
            _category = request.json["category"]
            if _category.lower() == "fiction":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, genre, intro, Name " \
                             "from fiction natural join book_with_rating natural join book_author natural join author;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books available in fiction category"}), 404

                book_authors = helper.get_book_authors(results)
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, genre, intro " \
                             "from fiction natural join book_with_rating;"
                cursor.execute(select_sql)
                results = cursor.fetchall()
                json_result = helper.get_book_with_authors(
                    book_authors, cursor.description, results)
                return jsonify(json_result), 200

            elif _category.lower() == "children":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, age_group, main_character, Name " \
                             "from children natural join book_with_rating natural join book_author BA natural join author A;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books available in children category"}), 404

                book_authors = helper.get_book_authors(results)
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating,age_group, main_character "\
                    "from children natural join book_with_rating;"
                cursor.execute(select_sql)
                results = cursor.fetchall()
                json_result = helper.get_book_with_authors(
                    book_authors, cursor.description, results)
                return jsonify(json_result), 200

            elif _category.lower() == "academics":
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating, course, level, Name "\
                    "from Academics natural join book_with_rating natural join book_author BA natural join author A;"
                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books available in academics category"}), 404

                book_authors = helper.get_book_authors(results)
                select_sql = "Select ISBN, Title, Price, Cover_image, Description, Page_count, Avg_rating,course, level "\
                             "from Academics natural join book_with_rating;"
                cursor.execute(select_sql)
                results = cursor.fetchall()
                json_result = helper.get_book_with_authors(
                    book_authors, cursor.description, results)
                return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view books by category"}), 500


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
                return jsonify({"Message": "No sale books uploaded"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view sale books uploaded by vendor"}), 500


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
                return jsonify({"Message": "No rent books uploaded"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view rent books uploaded by vendor"}), 500


# View customer purchase history
@app.route('/api/view/history/purchase', methods=['GET'])
def view_purchase_history():
    '''
    This function gets purchase history for a customer
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()
            select_sql = "Select title, cover_image, qty, S.price " \
                         "from Sale_Order S join Book B on S.ISBN = B.ISBN natural join Orders " \
                         "where order_id IN ( Select order_id from Orders Ord where Ord.customer_id = {}) " \
                         "order by date desc;".format(_userid)

            print(select_sql)
            cursor.execute(select_sql)
            results = cursor.fetchall()

            if len(results) == 0:
                return jsonify({"Message": "No purchases made"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view purchase history"}), 500


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
                return jsonify({"Message": "No books rented"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view rental history"}), 500


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
                return jsonify({"Message": "No out of stock books found"}), 404
            # Form json response for query results
            json_result = helper.get_json_response(cursor.description, results)
            return jsonify(json_result), 200
        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view out of stock books"}), 500


# Admin views customer rent orders
@app.route('/api/view/orders/rent', methods=['GET'])
def view_order_history():
    '''
    This function gets customer rent orders based on date, customer_username or both
    Parameters : customer username, date
    '''
    try:
        if session.get("user_id"):
            _username = request.json["customer_username"]
            _date = request.json["date"]
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
                    return jsonify({"Message": "No books rented by customer"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200
            elif _date != "":
                select_sql = "Select title, cover_image, qty, R.rent_fee " \
                    "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where date = \"{}\" "\
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books rented on given date"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200
            else:
                select_sql = "Select title, cover_image, qty, R.rent_fee " \
                    "from Rent_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books rented yet"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200

        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view rental history"}), 500


# Admin views customer sale orders
@app.route('/api/view/orders/sale', methods=['GET'])
def view_sale_order_history():
    '''
    This function gets customer sale orders based on date, customer_username or both
    Parameters : customer username, date
    '''
    try:
        if session.get("user_id"):
            _username = request.json["customer_username"]
            _date = request.json["date"]
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
                    return jsonify({"Message": "No books bought by customer"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200
            elif _date != "":
                select_sql = "Select title, cover_image, qty, R.price " \
                    "from Sale_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "where date = \"{}\" "\
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books bought on given date"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200
            else:
                select_sql = "Select title, cover_image, qty, R.price " \
                    "from Sale_Order R join Book B on R.ISBN = B.ISBN natural join Orders " \
                    "order by date desc;".format(_date)

                cursor.execute(select_sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    return jsonify({"Message": "No books bought yet"}), 404
                # Form json response for query results
                json_result = helper.get_json_response(
                    cursor.description, results)
                return jsonify(json_result), 200

        else:
            return jsonify({"Message": "Unauthenticated"}), 401
    except Exception as e:
        print("Exception")
        print(e)
        return jsonify({"Message": "Error occured in view sale history"}), 500


@app.route('/api/search/category', methods=['GET'])
def search_book_category():
    '''
    This function search the book by the category
    '''
    try:
        _category = request.json['category']
        cursor = conn.cursor()
        if _category == 'Academics':
            select_sql = "SELECT * FROM book B JOIN Academics A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN JOIN Book_Author BA ON B.ISBN=BA.ISBN JOIN Author ON BA.author_id=Author.author_id;"
        elif _category == 'Fiction':
            select_sql = "SELECT * FROM book B JOIN Fiction A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN JOIN Book_Author BA ON B.ISBN=BA.ISBN JOIN Author ON BA.author_id=Author.author_id;;"
        elif _category == 'Children':
            select_sql = "SELECT * FROM book B JOIN Children A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN JOIN Book_Author BA ON B.ISBN=BA.ISBN JOIN Author ON BA.author_id=Author.author_id;;"
        else:
            return jsonify({"Message": "Invalid search"}), 404
        cursor.execute(select_sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "Invalid search"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)
        return jsonify(json_result), 20
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view vendor profile"}), 500


@app.route('/api/search/genre', methods=['GET'])
def search_book_genre():
    '''
    This function search the book by the category
    '''
    try:
        _category = request.json['category']
        cursor = conn.cursor()
        if _category == 'Fantasy':
            select_sql = "SELECT * FROM book B JOIN Fiction A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN where A.genre='Fantasy';"
        elif _category == 'Thriller':
            select_sql = "SELECT * FROM book B JOIN Fiction A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN where A.genre='Thriller';"
        elif _category == 'ScienceFiction':
            select_sql = "SELECT * FROM book B JOIN Fiction A ON B.ISBN = A.ISBN JOIN Book_with_rating R ON B.ISBN = R.ISBN where A.genre='ScienceFiction';"
        else:
            return jsonify({"Message": "Invalid search"}), 404
        cursor.execute(select_sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "Invalid search"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)
        return jsonify(json_result), 20
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in view vendor profile"}), 500


@app.route('/api/sort/price', methods=['GET'])
def sort_based_price():
    '''
    This function sort the book by the price
    '''
    try:
        _min_price = request.json['min_price']
        _max_price = request.json['max_price']
        print("Here")
        cursor = conn.cursor()
        select_sql = "SELECT * FROM Book_with_rating WHERE Price >= %s AND Price <= %s ORDER BY Price"
        cursor.execute(select_sql, (_min_price, _max_price))
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "Invalid search"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)
        return jsonify(json_result), 20
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in price profile"}), 500


@app.route('/api/sort/ratings', methods=['GET'])
def sort_based_rating():
    '''
    This function sort the book by the ratings
    '''
    try:
        cursor = conn.cursor()
        select_sql = "SELECT * FROM Book_with_rating ORDER BY Avg_rating"
        cursor.execute(select_sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "Invalid search"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)
        return jsonify(json_result), 20
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in sort ratings"}), 500


@app.route('/api/display/address', methods=['GET'])
def display_address():
    try:
        _userid = request.json['user_id']
        cursor = conn.cursor()
        select_sql = "select street, apt, city, pin from Address where customer_id={}".format(
            _userid)
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return jsonify({"Message": "Invalid search"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)
        return jsonify(json_result), 20
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occured in display address"}), 500


@app.route('/api/add/address', methods=['POST'])
def add_address():
    try:
        _userid = session.get("user_id")
        print(_userid)
        data = request.get_json()
        cursor = conn.cursor()
        select_sql = "select max(addr_id) from Address"
        cursor.execute(select_sql)
        results = cursor.fetchall()
        print("\n\n\n")
        print("Executed")
        print("\n\n")
        val = helper.get_json_response(cursor.description, results)[
            'Results'][0]['max(addr_id)']
        print(val)
        print("\n\n")
        insert_sql = "insert into Address (customer_id, addr_id, street, apt, city, pin) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            _userid, val+1, data['street'], data['apt'], data['city'], data['pin'])
        cursor.execute(insert_sql)
        conn.commit()
        return jsonify({"Message": "Address added successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred while adding address"}), 500


@app.route('/api/delete/address', methods=['GET'])
def delete_address():
    try:
        _userid = session.get("user_id")
        data = request.get_json()
        cursor = conn.cursor()
        delete_sql = "delete from Address where customer_id ={} and addr_id = {}".format(
            5, data['address_id'])
        cursor.execute(delete_sql)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Invalid address id"}), 404
        conn.commit()
        return jsonify({"Message": "Address deleted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred while deleting address"}), 500


# Add to cart
@app.route('/api/customer/add_to_cart', methods=['POST'])
def add_to_cart():
    '''
    This function adds book to cart for a particular customer
    Parameters: isbn, for_rent, for_sale, qty
    '''
    try:
        if session.get("user_id"):
            _userid = session.get("user_id")
            cursor = conn.cursor()

        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _for_rent = request.json["for_rent"]
        _for_sale = request.json["for_sale"]
        _qty = request.json["qty"]

        if (bool(_for_sale) and bool(_for_rent)) or _for_rent == _for_sale or not bool(_qty):
            return jsonify({"Message": "False Inputs!"}), 400

        if bool(_for_sale):
            _available_qty = "SELECT avail_qty from sale_book where ISBN = \"{}\";".format(_isbn)
            if cursor.execute(_available_qty) < _qty:
                return jsonify({"Message": "Exceeds Available Quantity!"}), 400

        else:
            _available_qty = "SELECT qty from rent_book where ISBN = \"{}\";".format(_isbn)
            if cursor.execute(_available_qty) < _qty:
                return jsonify({"Message": "Exceeds Available Quantity!"}), 400

        sql = "INSERT into Cart(customer_id, isbn, for_rent, for_sale, qty) values (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
            _userid, _isbn, _for_rent, _for_sale, _qty)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Add-to-cart"}), 500

    return jsonify({"Message": "Successfully added to cart!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _for_rent = request.json["for_rent"]
        _for_sale = request.json["for_sale"]
        _qty = request.json["qty"]

        if not bool(_qty):
            return jsonify({"Message": "False Inputs!"}), 400

        if bool(_for_sale):
            _available_qty = "SELECT avail_qty from sale_book where ISBN = \"{}\";".format(_isbn)
            if cursor.execute(_available_qty) < _qty:
                return jsonify({"Message": "Exceeds Available Quantity!"}), 400

        else:
            _available_qty = "SELECT qty from rent_book where ISBN = \"{}\";".format(_isbn)
            if bool(cursor.execute(_available_qty)) and cursor.fetchone()[0] < _qty:
                return jsonify({"Message": "Exceeds Available Quantity!"}), 400

        sql = "UPDATE Cart SET qty = \"{}\" where customer_id = \"{}\" and isbn = \"{}\" and for_rent = \"{}\" and for_sale = \"{}\";".format(
            _qty, _userid, _isbn, _for_rent, _for_sale)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in updating quantity"}), 500

    return jsonify({"Message": "Successfully updated quantity!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _for_rent = request.json["for_rent"]
        _for_sale = request.json["for_sale"]

        sql = "DELETE from Cart where customer_id = \"{}\" and ISBN = \"{}\" and for_rent = \"{}\" and for_sale = \"{}\";".format(
            _userid, _isbn, _for_rent, _for_sale)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Remove-from-cart"}), 500

    return jsonify({"Message": "Successfully removed from cart!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _sale_books = "Select ISBN, title, cover_image, for_rent, for_sale, qty, price*qty*((100-fixed_discount)/100) as amount from ((cart natural join book) natural join sale_book) where customer_id = \"{}\" and for_rent = 0".format(_userid)
        _rent_books = "Select ISBN, title, cover_image, for_rent, for_sale, qty, ((price*0.30)+deposit)*qty as amount from ((cart natural join book) natural join rent_book) where customer_id = \"{}\" and for_sale = 0;".format(_userid)
        sql = "{} union {}".format(_sale_books, _rent_books)
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "No item in cart"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in View-cart"}), 500

    return jsonify(json_result), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]

        sql = "INSERT into Wishlist(customer_id, isbn) values (\"{}\",\"{}\");".format(_userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Add-to-wishlist"}), 500

    return jsonify({"Message": "Successfully added to wishlist!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]

        sql = "DELETE from Wishlist where customer_id = \"{}\" and ISBN = \"{}\";".format(_userid, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Remove-from-wishlist"}), 500

    return jsonify({"Message": "Successfully removed from wishlist!"}), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _visibility = request.json["visibility"]

        sql = "UPDATE book SET visibility = \"{}\" where ISBN = \"{}\";".format(_visibility, _isbn)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in toggling visibility-of-book"}), 500

    return jsonify({"Message": "Successfully toggled visibility of book!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _rating = request.json["rating"]
        _sale_order = "SELECT customer_id, ISBN from (Sale_order natural join Orders) where customer_id = \"{}\" and ISBN = \"{}\"".format(_userid, _isbn)
        _rent_order = "SELECT customer_id, ISBN from (Rent_order natural join Orders) where customer_id = \"{}\" and ISBN = \"{}\";".format(_userid, _isbn)
        ordered = cursor.execute("{} union {};".format(_sale_order, _rent_order))
        if not bool(ordered):
            return jsonify({"Message": "Permission denied"}), 403

        sql = "INSERT into Feedback(customer_id, ISBN, rating) values(\"{}\", \"{}\", \"{}\");".format(_userid, _isbn, _rating)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Rate-a-book"}), 500

    return jsonify({"Message": "Successfully rated a book!"}), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _title = request.json["title"]
        _price = request.json["price"]
        _cover_image = request.json["cover_image"]
        _page_count = request.json["page_count"]
        _description = request.json["description"]
        _publisher = request.json["publisher"]
        _published_date = request.json["published_date"]
        _authors = request.json["authors"]

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

        _is_salebook = request.json["is_salebook"]
        _is_rentbook = request.json["is_rentbook"]
        _is_fiction = request.json["is_fiction"]
        _is_children = request.json["is_children"]
        _is_academics = request.json["is_academics"]

        if bool(_is_salebook):
            _fixed_discount = request.json["fixed_discount"]
            _avail_qty = request.json["avail_qty"]
            sale_book = "INSERT into sale_book(isbn,fixed_discount,avail_qty) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _fixed_discount, _avail_qty)
            cursor.execute(sale_book)

        if bool(_is_rentbook):
            _deposit = request.json["deposit"]
            _qty = request.json["qty"]
            _rental_fee = request.json["rental_fee"]
            rent_book = "INSERT into rent_book(isbn,deposit,qty,rental_fee) values(\"{}\",\"{}\",\"{}\",\"{}\")".format(_isbn, _deposit, _qty, _rental_fee)
            cursor.execute(rent_book)

        if bool(_is_fiction):
            _genre = request.json["genre"]
            _intro = request.json["intro"]
            fiction = "INSERT into fiction(isbn,genre,intro) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _genre, _intro)
            cursor.execute(fiction)

        if bool(_is_children):
            _age_group = request.json["age_group"]
            _main_character = request.json["main_character"]
            children = "INSERT into children(isbn,age_group,main_character) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _age_group, _main_character)
            cursor.execute(children)

        if bool(_is_academics):
            _course = request.json["course"]
            _level = request.json["level"]
            academics = "INSERT into academics(isbn,course,level) values(\"{}\",\"{}\",\"{}\")".format(_isbn, _course, _level)
            cursor.execute(academics)

        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Add-a-book"}), 500

    return jsonify({"Message": "Successfully added a book!"}), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        book = "SELECT vendor_id, isbn from book where vendor_id = \"{}\" and isbn = \"{}\";".format(_userid, _isbn)
        cursor.execute(book)
        if not bool(book):
            return jsonify({"Message": "Permission denied"}), 403

        sql = "DELETE from sale_book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        sql = "DELETE from rent_book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        sql = "DELETE from book where ISBN = \"{}\";".format(_isbn)
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Remove-a-book"}), 500

    return jsonify({"Message": "Successfully removed a book!"}), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _price = request.json["price"]
        _is_sale = request.json["is_sale"]
        _is_rent = request.json["is_rent"]

        book = "SELECT vendor_id, isbn from book where vendor_id = \"{}\" and isbn = \"{}\";".format(_userid, _isbn)
        cursor.execute(book)
        if not bool(book):
            return jsonify({"Message": "Permission denied"}), 403
        update_book = "UPDATE book SET price = \"{}\" where ISBN = \"{}\";".format(_price, _isbn)
        cursor.execute(update_book)

        if bool(_is_sale):
            _fixed_discount = request.json["fixed_discount"]
            _avail_qty = request.json["avail_qty"]
            sale_book = cursor.execute("SELECT * from sale_book where ISBN = \"{}\";".format(_isbn))
            if bool(sale_book):
                cursor.execute("UPDATE sale_book SET fixed_discount = \"{}\", avail_qty = \"{}\" where ISBN = \"{}\";".format(_fixed_discount, _avail_qty, _isbn))
            else:
                cursor.execute("INSERT into sale_book(ISBN,fixed_discount,avail_qty) values(\"{}\",\"{}\",\"{}\");".format(_isbn, _fixed_discount, _avail_qty))
        else:
            cursor.execute("DELETE from sale_book where ISBN = \"{}\";".format(_isbn))

        if bool(_is_rent):
            _deposit = request.json["deposit"]
            _rental_fee = request.json["rental_fee"]
            _qty = request.json["qty"]
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
        return jsonify({"Message": "Error occurred in Update-book-data"}), 500

    return jsonify({"Message": "Successfully updated book data!"}), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        sql = "SELECT * from Vendor_to_Approve;"
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results) == 0:
            return jsonify({"Message": "No vendor in waitlist for approval"}), 404
        # Form json response for query results
        json_result = helper.get_json_response(cursor.description, results)

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Vendors-to-approve"}), 500

    return jsonify(json_result), 200


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
                return jsonify({"Message": "Permission denied"}), 403
        else:
            return jsonify({"Message": "Unauthenticated"}), 401

        _username = request.json["username"]
        _is_approve = request.json["is_approve"]
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
        return jsonify({"Message": "Error occurred in approving a vendor"}), 500

    return jsonify({"Message": "Successfully approved/disapproved a vendor!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _address_id = request.json["address_id"]
        _date = datetime.date.today()
        print(_date)

        create_order = "INSERT into orders(customer_id,date,status,address_id) values(\"{}\",\"{}\",\"Ordered\",\"{}\");".format(
            _userid, _date, _address_id)
        cursor.execute(create_order)
        cursor.execute("SELECT LAST_INSERT_ID();")
        _order_id = cursor.fetchone()[0]

        cursor.execute("SELECT cart.ISBN, cart.qty, ((price*0.30)+deposit)*cart.qty, rent_book.qty from ((cart join rent_book on cart.ISBN = rent_book.ISBN) join book on cart.ISBN = book.ISBN) where customer_id = \"{}\" and for_sale = 0;".format(_userid))
        _rent_books = cursor.fetchall()
        print(_rent_books)

        _due_date = _date + datetime.timedelta(days=14)
        for item in _rent_books:
            cursor.execute("INSERT into rent_order(order_id,ISBN,issue_date,due_date,qty,rent_fee) values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(
                _order_id, item[0], _date, _due_date, item[1], item[2]))
            cursor.execute("UPDATE rent_book SET qty = \"{}\" where ISBN = \"{}\";".format(item[3]-item[1], item[0]))

        cursor.execute("SELECT ISBN, qty, price*qty*((100-fixed_discount)/100), avail_qty from ((cart natural join book) natural join sale_book)  where customer_id = \"{}\" and for_rent = 0;".format(_userid))
        _sale_books = cursor.fetchall()
        print(_sale_books)

        for item in _sale_books:
            cursor.execute("INSERT into sale_order(order_id,ISBN,qty,price) values(\"{}\",\"{}\",\"{}\",\"{}\");".format(
                _order_id, item[0], item[1], item[2]))
            cursor.execute("UPDATE sale_book SET avail_qty = \"{}\" where ISBN = \"{}\";".format(item[3]-item[1], item[0]))

        cursor.execute("DELETE from cart where customer_id = \"{}\";".format(_userid))

        cursor.execute("SELECT sum(rent_fee) from rent_order where order_id = \"{}\" group by order_id;".format(_order_id))
        _total_rent_fee = cursor.fetchone()[0]
        cursor.execute("SELECT sum(price) from sale_order where order_id = \"{}\" group by order_id;".format(_order_id))
        _total_price = cursor.fetchone()[0]
        _invoice_ammount = _total_rent_fee + _total_price
        cursor.execute("UPDATE orders SET invoice_amount = \"{}\" where order_id = \"{}\";".format(_invoice_ammount,_order_id))
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Add-to-cart"}), 500

    return jsonify({"Message": "Successfully added to cart!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _isbn = request.json["isbn"]
        _order_id = request.json["order_id"]
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
        return jsonify({"Message": "Error occurred in Return-book"}), 500

    return jsonify({"Message": "Successfully returned book!"}), 200


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
            return jsonify({"Message": "Unauthenticated"}), 401

        _order_id = request.json["order_id"]
        _time = datetime.datetime.now()
        print(_time)

        sql = "INSERT into transaction(order_id, payment_status, time) value(\"{}\",\"Paid\",\"{}\")".format(_order_id, _time)
        print(sql)
        cursor.execute(sql)
        cursor.execute("UPDATE orders SET status=\"Completed\" where order_id = \"{}\";".format(_order_id))
        conn.commit()

    except Exception as e:
        print(e)
        return jsonify({"Message": "Error occurred in Make-payment"}), 500

    return jsonify({"Message": "Successfully paid!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
