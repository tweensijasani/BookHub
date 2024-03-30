import re
from flask import jsonify


def validate_name(name):
    # Check if name contains only letters and spaces
    if re.match("^[a-zA-Z ]+$", name):
        return True
    else:
        return False


def validate_username(username):
    # Check if username contains only alphanumeric characters and underscores
    if re.match("^[a-zA-Z0-9_]+$", username):
        return True
    else:
        return False


def validate_admin_position(pos):
    # Check if username contains only alphanumeric characters and underscores
    if re.match("junior", pos) or re.match("senior", pos) or re.match("super", pos) or re.match("entry", pos):
        return True
    else:
        return False


def validate_email(email):
    # Check if email is valid
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False


def validate_password(password):
    # Check if password is at least 5 characters long
    if len(password) >= 5:
        return True
    else:
        return False


def validate_account(acc):
    pattern = r'^\d+$'
    # Check if password is at least 5 characters long
    if len(acc) == 16 and  bool(re.match(pattern, acc)):
        return True
    else:
        return False


def validate_phone_number(phone_number):
    # Check if phone number is valid
    if re.match("^(\d{3}|\d{3}-)?(\d{3}|\d{3}-)?(\d{4})$", phone_number):
        return True
    else:
        return False


def validate_data(name, email, phone, password, username):
    if not name :
        return jsonify({"Message": "Please enter name."}), 500
    if not validate_name(name):
        return jsonify({"Message": "Invalid name."}), 500

    if not email :
        return jsonify({"Message": "Please enter email-id."}), 500
    if not validate_email(email):
        return jsonify({"Message": "Invalid email-id."}), 500

    if not phone :
        return jsonify({"Message": "Please enter phone number."}), 500
    if not validate_phone_number(phone):
        return jsonify({"Message": "Invalid phone number."}), 500

    if not password :
        return jsonify({"Message": "Please enter password."}), 500
    if not validate_password(password):
        return jsonify({"Message": "Invalid password."}), 500

    if not username :
        return jsonify({"Message": "Please enter username."}), 500
    if not validate_username(username):
        return jsonify({"Message": "Invalid username."}), 500
    
    return jsonify({"Message": "Validated"}), 200