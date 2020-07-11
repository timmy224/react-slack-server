from flask import request
from .. import main

@main.route("/challenge2-form/", methods=["POST"])
def challenge2_form():
    print('running')
    if request.method == "POST":
        data = request.json
        output = {
            data.get("name"): {
                "username": data.get("username"),
                "email": data.get("email")
            }
        }
        
        print(output)
        return output
        
    return "Something that's not POST"