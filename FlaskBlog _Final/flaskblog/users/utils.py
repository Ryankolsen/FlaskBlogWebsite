import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)      #random the name to make sure it does not collide with any other existing file. pass in 8 bytes
    _, f_ext = os.path.splitext(form_picture.filename) #split filename to get ext, get rid of name
    picture_fn = random_hex + f_ext     #create new filename
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #gives full path all the way to package directory

    output_size = (125, 125)    #resize picture so it doesnt waste space
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)     #save picture to the file system, save as i

    return picture_fn

#requires flask mail (installed w/pip)
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
            sender='RyanTest9981@gmail',#important, change this email so not to spoof user and end up in junkmail
            recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made
'''

    mail.send(msg)
