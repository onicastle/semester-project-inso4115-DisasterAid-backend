from flask import jsonify
from dao.user import User


class BaseHandler:
    @staticmethod
    def verify_params(params, required_params):
        """
        Verify the validity of submitted parameter.
        :param params: submitted params
        :param required_params: list of required parameters
        :return: params, otherwise none
        """
        for param, value in params.items():
            if param in required_params and value is None:
                return None
        return params


class UserHandler(BaseHandler):

    @staticmethod
    def get_all_users():
        try:
            users = User.get_all_users()
            result_list = []
            for user in users:
                result_list.append(user.to_dict())
            result = {
                "message": "Success!",
                "users": result_list,
            }
            return jsonify(result), 200
        except:
            return jsonify(message="Server error!"), 500

    @staticmethod
    def get_user_by_id(uid, relationship=None):
        if uid:
            try:
                user = User.get_user_by_id(uid)
                if not user:
                    return jsonify(Error="User Not Found"), 404
                else:
                    result = {"message": "Success!"}
                    if relationship:
                        result[relationship] = user.get_all_user_relationship_values(relationship)
                    else:
                        result['user'] = user.to_dict()
                    return jsonify(result), 200
            except:
                return jsonify(message="Server Error!"), 500
        else:
            return jsonify(message="Bad request!"), 400

    @staticmethod
    def create_user(json):
        valid_params = UserHandler.verify_params(json, User.USER_REQUIRED_PARAMETERS)
        if valid_params:
            try:
                new_user = User(**valid_params)
                created_user = new_user.create()
                result = {
                    "message": "Success!",
                    "user": created_user.to_dict(),
                }
                return jsonify(result), 201
            except:
                return jsonify(message="Server error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400

    @staticmethod
    def update_user(uid, json):
        if uid:
            try:
                user_to_update = User.get_user_by_id(uid)
                if user_to_update:
                    valid_params = UserHandler.verify_params(json, User.USER_REQUIRED_PARAMETERS)
                    for key, value in valid_params.items():
                        if key == "password":
                            user_to_update.update_password(value)
                        else:
                            setattr(user_to_update, key, value)
                    user_to_update.update()
                    result = {
                        "message": "Success!",
                        "user": user_to_update.to_dict(),
                    }
                    return jsonify(result), 200
                else:
                    return jsonify(message="Not Found!"), 404
            except:
                return jsonify(message="Server Error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400

    @staticmethod
    def delete_user(uid):
        if uid:
            try:
                user_to_delete = User.get_user_by_id(uid)
                if user_to_delete:
                    user_to_delete.delete()
                    return jsonify(message="Success!"), 200
                else:
                    return jsonify(message="Not Found!"), 404
            except:
                return jsonify(message="Server Error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400
