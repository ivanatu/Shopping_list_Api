import re
from functools import wraps
from flask import request, jsonify, request
from werkzeug.exceptions import BadRequest

from app import shop_api

def required(*values_required):
    """"""
    message = []
    for value in values_required[1]:
        if value not in values_required[0]:
            message.append("{} is required".format(value))

    return message

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest as e:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper

def validate(*values):
    """
    :rtype: object
    """
    # Helper function to validate all the data supplied from the user

    min_length = 8
    message = []

    # Value is value that needs to be validated
    for value in values:

        for value_key in value.keys():
            # Check the value is not empty
            if value[value_key] is None:
                message.append(value_key.title() + " is required")
                return message


            if not isinstance(value[value_key], str) :
                message.append("Your " + value_key + " is not string")
                return message

            if len(value[value_key].strip()) == 0:
                message.append("Your " + value_key + " is empty")


            # Check the value can not be numbers only
            if value[value_key].isdigit() and value_key != "price":
                message.append(value_key.title() + " can't be numbers only")

           # Check the price is numbers only
            if value_key == "price":
                if re.search("[^0-9.]", value[value_key]):
                    message.append(value_key.title() + " has to be numbers only")

            # Use regex to validate email
            if value_key == "email":
                email_regex = re.compile(
                    r"(^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]+$)")
                if not email_regex.match(value[value_key]):
                    message.append("Your " +
                                   value_key +
                                   " is not valid. "
                                     "Example: shopping@gmail.com")

            # Use regex to validate question
            if value_key == "first_name" or value_key == "last_name":
                # Check the value is not empty
                if len(value[value_key].strip()) < 2:
                    message.append("Your " + value_key +
                                   " should be more than 2 characters")


                # Check special characters are being rejectedat
                elif not re.match("^[-a-zA-Z0-9_\\s]*$", value[value_key]):
                    message.append(
                        "Your " + value_key +
                        " has special characters that are not allowed"
                    )

            if value_key == "password":
                if len(value_key) is None:
                    message.append(value_key.title() + " is required")
                    return message
                if len(value[value_key]) < min_length:
                    message.append("Your " + value_key +
                                   " is too weak, minimum "
                                   "length is 8 characters")
                pass_word = re.compile(r"^[a-z]+$")
                if pass_word.match(value[value_key]):
                    # message.append("Your " + value_key +
                    # 			   " is too weak, must contain capitals")
                    pass_word = re.compile(r"(^[A-Z]+[0-9]+$)")
                    if pass_word.match(value[value_key]):
                        message.append("STRONG PASSWORD")
                    message.append("Your " + value_key +
                                   " is too weak, must contain "
                                   "capitals OR numbers")

    # Return an array that contains all the error messages else false
    if message == []:
        return False
    return message
