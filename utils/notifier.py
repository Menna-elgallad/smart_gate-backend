import requests
from models.user_model import User
from models.camera_model import Camera
from models.gate_model import Gate
from flask import current_app
from models.notification_model import Notification

fcm_url = "https://fcm.googleapis.com/fcm/send"
headers = {
    "Content-Type": "application/json",
    "Authorization": "key=AAAA29oZ54c:APA91bFPAS7uu7dZ7kr5JZFiMqIGhZJBnkSpbJfsENdnKXvzVnZ6AvOr-efF5vPffbzYnt78JdC82c8zaSq-bmXu3uepnz-ae24Y7tq3ska3BPSNB8HTJJ39Z76I5iK3ZHGT7Qv2uiaQ"
}
data = {
    "notification": {
        "icon": "http://localhost:3000/images/logo.png"
    },
}


def send_notification(gate_id, plate, message=None, title=None):
    gate = Gate.query.filter_by(id=gate_id).first()

    users = User.get_all()
    Notification.create(
        body=message or f"Unknown Car Trying access \n plate : {plate} at gate : {gate.name} ", title=title or "Car Access")
    if users is None or len(users) == 0:
        return "User not found"
    url = "http://localhost:3000/camera"

    for user in users:
        print(user)
        if user.fcm_tokens != None and len(user.fcm_tokens) > 0:
            for token in user.fcm_tokens:
                print(token)
                data['to'] = token
                data['notification'][
                    'body'] = message or f"Unknown Car Trying access  \n plate : {plate} at gate : {gate.name} "
                data['notification']['title'] = title or "Car Access"
                data['notification']['click_action'] = url
                print(data)
                requests.post(fcm_url, headers=headers, json=data)
    return True
