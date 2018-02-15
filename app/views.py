from flask import Flask, request, jsonify, render_template, session, \
    make_response
from app.models import Item, Shopping_list, User, db
from app import shop_api
from werkzeug.security import generate_password_hash, \
    check_password_hash
from app.handlers import validate, required, validate_json


@shop_api.route('/', methods=['GET'])
def index():
    """
    This endpoint will return the API documentation

    """
    return render_template('index.html')


@shop_api.route('/auth/register', methods=['POST'])
@validate_json
def register():
    """
    This endpoint will create a user account with the first name, lastname ,
     email and password
    :return: json response
    """

    data = request.json
    require = required(data, ['first_name', 'last_name', 'email', 'password'])

    if len(require) != 0:
        return make_response(jsonify({'status': 'fail',
                                      'message': require
                                      }), 400)

    invalid = validate(data)
    if invalid:
        return make_response(jsonify({'status': 'fail',
                                      'message': invalid}), 400)

    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        # create user in the database
        user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=generate_password_hash(data['password']))
        db.session.add(user)
        db.session.commit()
        return jsonify({'email': user.email,
                        'status': 'pass',
                        'message': 'user account created successfully'
                        }), 201

    return jsonify({'status': 'fail',
                    'message': 'user email already exists'
                    }), 200


@shop_api.route('/auth/login', methods=['POST'])
def login():
    """
    This endpoint will login a user with an account
    :return: json response
    """
    if not request.json:
        return jsonify({'status': 'fail',
                        'message': 'form errors'
                        }), 400
    data = request.json
    invalid = validate(data)
    if invalid:
        return make_response(jsonify({'status': 'fail',
                                      'message': invalid
                                      }), 400)
    user = User.query.filter_by(email=data['email']).first()
    # log message and authenticate user
    if user is not None:
        if check_password_hash(user.password, data['password']):
            # generate token here
            user.generate_auth_token()
            if user.token:
                # log message and return response to client
                return jsonify({'token': user.token.decode('ascii'),
                                'status': 'pass',
                                'message': 'login was successful'}), 201
        return jsonify({'status': 'fail',
                        'message': 'wrong password or email or '
                                   'may be user does\'t exist'
                        }), 200
    return jsonify({"error": "user not found. please register"}), 401


@shop_api.route('/auth/logout', methods=['POST'])
def logout():
    """
    This endpoint will logout a user
    """

    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            user = User.query.filter_by(id=user_id).first()
            user.token = None  # remove the token that was issued when user logged in
            db.session.commit()
            return jsonify({'status': 'pass',
                            'message': 'logout was successful'}), 200
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """
    This endpoint will reset a password for a given user
    logged in at the front end
    :return: json response
    """
    if not request.json:
        return jsonify({'status': 'fail',
                        'message': 'form errors'
                        }), 400
    data = request.json

    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            invalid = validate(data)
            if invalid:
                return make_response(jsonify({'status': 'fail',
                                              'message': invalid
                                              }), 400)
            # locate user and check the old password
            user = User.query.filter_by(email=data['email']).first()
            if user and check_password_hash(user.password,
                                            data['old_password']):
                user.password = generate_password_hash(data['new_password'])
                db.session.commit()
                return jsonify({'email': user.email,
                                'status': 'pass',
                                'message': 'password was changed successfully'
                                }), 201

            return jsonify({'status': 'fail',
                            'message': 'wrong email or password or '
                                       'may be user does\'t exist'
                            }), 200

        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401

    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists', methods=['POST'])
def add_a_list():
    """
    This endpoint will create a shopping list for a logged in user
    """
    if not request.json:
        return jsonify({'status': 'fail',
                        'message': 'form errors'
                        }), 400
    data = request.json

    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            invalid = validate(data)
            if invalid:
                return make_response(jsonify({'status': 'fail',
                                              'message': invalid
                                              }), 400)
            # create a list
            a_list = Shopping_list.query.filter_by(
                list=str(data['list']).lower(),
                user_id=user_id).first()

            if a_list is None:
                the_list = Shopping_list(
                    list=str(data['list']).lower(),
                    user_id=user_id)
                db.session.add(the_list)
                db.session.commit()
                response = jsonify({'id': the_list.id,
                                    'list': the_list.list,
                                    'status': 'pass',
                                    'message': 'list created successfully'
                                    })
                return response, 201
            return jsonify({'status': 'fail',
                            'message': 'list already exists'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists', methods=['GET'])
def view_all_lists():
    """
    This endpoint will return all the lists for a logged in user and
    if the q parameter is provided, it will implement
    a search query based on the list name. Other parameters search
    as limit and page refine the results for the user of
    the API
    """

    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            results = []
            # query parameters
            # this parameter contains the name of the list
            q = request.args.get(str('q').lower(), None)
            # limits the number of records to 50 per page
            limit = request.args.get('limit', 8,
                                     type=int)
            # page one is default,
            # but page can be passed as an argument
            page = request.args.get('page', 1,
                                    type=int)

            if q is not None:
                lists = Shopping_list.query.filter(
                    Shopping_list.list.like("%" + str(q).lower().strip() + "%")). \
                    filter_by(user_id=user_id).paginate(
                    page, limit, False)
            else:
                lists = Shopping_list.query.filter_by(
                    user_id=user_id).paginate(page, limit, False)
            for a_list in lists.items:
                result = {
                    'id': a_list.id,
                    'list': a_list.list,
                    'per_page': lists.per_page,
                    'total': lists.total
                }
                results.append(result)
            if len(results) > 0:
                return jsonify({'lists': results,
                                'count': str(len(results)),
                                'status': 'pass',
                                'message': 'lists found'
                                }), 200
            return jsonify({'count': '0',
                            'status': 'fail',
                            'message': 'no lists found'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:id>', methods=['GET'])
def get_a_list(id):
    """
    This endpoint will return a list of a given list_id
    """

    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            a_list = Shopping_list.query.filter_by(
                id=id, user_id=user_id).first()
            if a_list is not None:
                response = jsonify({'list': dict(id=a_list.id,
                                                 list=a_list.list
                                                 ),
                                    'count': '1',
                                    'status': 'pass',
                                    'message': 'list found'})
                return response, 200
            return jsonify({'count': '0',
                            'status': 'fail',
                            'message': 'list not found'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:id>', methods=['PUT'])
def update_a_list(id):
    """
    This endpoint will update a list of with a given id
    """
    if not request.json:
        return jsonify({'status': 'fail', 'message': 'form errors'}), 400
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            invalid = validate(data)
            if invalid:
                return make_response(jsonify({'status': 'fail',
                                              'message': invalid
                                              }), 400)
            the_list = Shopping_list.query.filter_by(
                id=id, user_id=user_id).first()

            if the_list is not None:
                the_list2 = Shopping_list.query.filter_by(
                    user_id=user_id, list=str(data['list']).lower()).first()
                if the_list2 is None:
                    the_list.list = str(data['list']).lower()
                    db.session.commit()
                    response = jsonify({'list': dict(id=the_list.id,
                                                     list=the_list.list
                                                     ),
                                        'status': 'pass',
                                        'message': 'list updated'})
                    return response, 201
                return jsonify({'status': 'fail', 'message': 'list exists already'})
            return jsonify({'status': 'fail',
                            'message': 'list doesnot exist'
                            }), 400
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:id>', methods=['DELETE'])
def delete_a_list(id):
    """
    This endpoint will delete a list with a given id
    """

    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            the_list = Shopping_list.query.filter_by(
                id=id,
                user_id=user_id).first()
            if the_list is not None:
                db.session.delete(the_list)
                db.session.commit()
                return jsonify({'status': 'pass',
                                'message': 'list deleted'
                                }), 200
            return jsonify({'status': 'fail',
                            'message': 'list not deleted'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


# -------------------------------------------------------------------------------------------------

@shop_api.route('/shoppinglists/<int:id>/items', methods=['POST'])
def add_items_list(id):
    """
    This endpoint will add items to a given list
    """
    # check to ensure the list exists
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            invalid = validate(data)
            if invalid:
                return make_response(jsonify({'status': 'fail',
                                              'message': invalid
                                              }), 400)
            the_list = Shopping_list.query.filter_by(
                id=id, user_id=user_id).first()
            if the_list is not None:
                # if 'name' in data and 'price' in data:
                # add an item to the list
                the_item = Item.query.filter_by(
                    name=str(data['name']).lower(), List_id=id).first()
                print(the_item)
                if the_item is None:
                    item = Item(name=str(data['name']).lower(),
                                price=data['price'],
                                List_id=id)
                    db.session.add(item)
                    db.session.commit()
                    return jsonify({'item_id': item.id,
                                    'name': item.name,
                                    'price': item.price,
                                    'status': 'pass',
                                    'message': 'item added to list'
                                    }), 201
                return jsonify({'status': 'fail',
                                'message': 'item already exists'}), 404
            return jsonify({'status': 'fail',
                            'message': 'list does not exist'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:id>/items', methods=['GET'])
def get_items_list(id):
    """
    :this returns all the items in a given list
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            results = []
            # query parameters
            # this parameter contains the name of the list
            q = request.args.get('q', None)
            # limits the number of records to 50 per page (optional)
            limit = request.args.get('limit', 8,
                                     type=int)
            # page one is default, but page can be passed as an argument (optional)
            page = request.args.get('page', 1,
                                    type=int)
            a_list = Shopping_list.query.filter_by(
                id=id, user_id=user_id).first()
            if a_list is not None:
                if q is not None:
                    items = Item.query.filter(
                        Item.name.like("%" + q.strip() + "%")). \
                        filter_by(List_id=id).paginate(
                        page, limit, False)
                else:
                    items = Item.query.filter_by(
                        List_id=id).paginate(page, limit, False)
                for a_items in items.items:
                    result = {
                        'itemid': a_items.id,
                        'name': a_items.name,
                        'price': a_items.price,
                        'per_page': items.per_page,
                        'total': items.total

                    }
                    results.append(result)

                if len(results) > 0:
                    return jsonify({'items': results,
                                    'count': str(len(results)),
                                    'status': 'pass',
                                    'message': 'items found'}), 200
                return jsonify({'count': '0',
                                'status': 'fail',
                                'message': 'no items found'
                                }), 404
            return jsonify({'status': 'fail',
                            'message': 'list not found'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:list_id>/items/<int:item_id>',
                methods=['PUT'])
def update_list_item(list_id, item_id):
    """
    This endpoint will update a given item on a given list
    """
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            the_list = Shopping_list.query.filter_by(
                id=list_id, user_id=user_id).first()
            if the_list is not None:
                the_item = Item.query.filter_by(
                    id=item_id, List_id=list_id).first()
                if the_item is not None:
                    the_item2 = Item.query.filter_by(
                        List_id=list_id, name=str(data['name']).lower()).first()
                    if the_item2 is None:
                        the_item.name = str(data['name']).lower()
                        the_item.price = data['price']
                        db.session.commit()
                        return jsonify({'item': dict(id=the_item.id,
                                                     name=the_item.name,
                                                     price=the_item.price),
                                        'status': 'pass',
                                        'message': 'item updated'
                                        }), 201
                    return jsonify({'status': 'fail', 'message': 'item exists'})
                return jsonify({'status': 'fail',
                                'message': 'item does not exist'
                                }), 400
            return jsonify({'status': 'fail',
                            'message': 'list does not exist'
                            }), 404
        return jsonify({'status': 'fail',
                        "message": "Error with your login, please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401


@shop_api.route('/shoppinglists/<int:list_id>/items/<int:item_id>',
                methods=['DELETE'])
def delete_item_from_list(list_id, item_id):
    """
    This endpoint will delete an item on given list
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user_id = User.decode_token(auth_header)
        if not isinstance(user_id, str):
            the_list = Shopping_list.query.filter_by(
                id=list_id
            ).first()
            if the_list is not None:
                the_item = Item.query.filter_by(id=item_id).first()
                if the_item is not None:
                    name = the_item.name
                    db.session.delete(the_item)
                    db.session.commit()
                    return jsonify({'status': 'pass',
                                    'message': 'item deleted'
                                    }), 200
                return jsonify({'status': 'fail',
                                'message': 'item not found'
                                }), 404
            return jsonify({'status': 'fail',
                            'message': 'list does not exist'
                            }), 404
        return jsonify({'status': 'fail', "message": "Error with your login,"
                                                     " please try again"
                        }), 401
    return jsonify({'status': 'fail',
                    "message": " cant access to login"
                    }), 401
