from flask import jsonify

from dao.donation import Donation
from handler.user import BaseHandler


class DonationHandler(BaseHandler):
    @staticmethod
    def get_all_donations(available=None):
        try:
            print("Estoy aqui")
            donations = Donation.get_all_donations() if not available else Donation.get_available_donations()
            donation_list = [donation.to_dict() for donation in donations]
            result = {
                "message": "Success!",
                "donations": donation_list,
            }
            return jsonify(result), 200
        except:
            return jsonify(message="Server error!"), 500

    @staticmethod
    def get_donation_by_id(did, relationship=None):
        if did:
            try:
                donation = Donation.get_donation_by_id(donation_id=did)
                if not donation:
                    return jsonify(message="Not Found!"), 404
                else:
                    result = {"message": "Success!"}
                    if relationship:
                        result['requsts'] = donation.get_all_donation_requests()
                    else:
                        result['donation'] = donation.to_dict()
                    return jsonify(result), 200
            except:
                return jsonify(message="Server Error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400

    @staticmethod
    def create_donation(json):
        valid_params = DonationHandler.verify_params(json, Donation.DONATION_REQUIRED_PARAMS)
        if valid_params:
            try:
                new_donation = Donation(**valid_params)
                created_donation = new_donation.create()
                result = {
                    "message": "Success!",
                    "donation": created_donation.to_dict(),
                }
                return jsonify(result), 201
            except:
                return jsonify(message="Server error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400

    @staticmethod
    def update_donation(did, json):
        if did:
            try:
                donation_to_update = Donation.get_donation_by_id(did)
                if donation_to_update:
                    valid_params = DonationHandler.verify_params(json, Donation.DONATION_REQUIRED_PARAMS)
                    print(valid_params)
                    for key, value in valid_params.items():
                        setattr(donation_to_update, key, value)
                    donation_to_update.update()
                    result = {
                        "message": "Success!",
                        "donation": donation_to_update.to_dict(),
                    }
                    return jsonify(result), 200
                else:
                    return jsonify(message="Not Found!"), 404
            except:
                return jsonify(message="Server Error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400

    @staticmethod
    def delete_donation(did):
        if did:
            try:
                donation_to_delete = Donation.get_donation_by_id(did)
                if donation_to_delete:
                    donation_to_delete.delete()
                    return jsonify(message="Success!"), 200
                else:
                    return jsonify(message="Not Found!"), 404
            except:
                return jsonify(message="Sever Error!"), 500
        else:
            return jsonify(message="Bad Request!"), 400
