import os
import json
from flask import Flask
from flask import request
from subprocess import call

target_repository = os.environ.get("TARGET_REPOSITORY","etcd")
external_script=os.environ.get("EXT_SCRIPT","slack-webhook.sh")

app = Flask(__name__)

@app.route("/")
def hello():
  return "I am Groot!"

@app.route('/event', methods=['POST'])
def post_event():
    event = request.get_json()["events"][0]    
    target = event["target"];
    if ("tag" not in target) and (event["action"] == "push") and (target["repository"] == target_repository):
        print ("Push image without tag "+event["id"])
    if ("tag" in target) and (event["action"] == "push") and (target["repository"] == target_repository):
        # Call external script
        if external_script != "":
            print ("Calling script: "+external_script)
            call([external_script,target["tag"]])
        else:
        	print ("Script path is empty. ")
    return ""


if __name__ == "__main__":
  app.run(port=80)

