##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.mongoengine import MongoEngine
from MongoEngine import Document, StringField, FileField, ImageField, ListField

class Image(Document):
    '''Image database model. Fields:
    - title : the title given to image
    - fimg  : the file system location of the picture
    - url   : the url where the image was uploaded from
    '''
    title = StringField(required=true)
    fimg = FileField()
    #url = StringField()

    # Contain all image categories in the image database
    meta = {"db_alias" : "pic"}

class User(Document):
    '''User database model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - img_array : array of img ids
    '''
    uname = StringField(required=true)
    fname = StringField(required=true)
    lname = StringField(required=true)
    email = StringField(required=true)
    pwd = StringField(required=true)
    img_array = ListField()
    
    # Contain all user categories in the user database
    meta = {"db_alias" : "test"}


def createUser(uname, fname, lname, email, pwd, img_array = []):
    '''Creates a new user using the user model. This also checks for any duplicate usernames and reports some error if there is
    @param uname - user name, this is checked for uniquieness [required]
    @param fname - first name [required]
    @param lname - last name [required]
    @param email - email address [required]
    @param pwd - password [required]
    @param img_array - array of image object ids [not required]
    @return A new user if the user does not already exist. Otherwise an error is given
    '''
    usr = User(uname=uname, fname=fname, lname=lname, email=email,pwd=pwd, img_array=img_array)
    return usr

def writeFileFieldData(FF, ext="png"):
    '''Writes the FileField data allowing for metadata to be stored in the same call
    @param FF - file field [required]
    @param ext - extension of image file [not required] [default value = "png"]
    '''
    imgDoc.fimg.put(imgDoc_fimg, content_type="image/%s" % ext)
    imgDoc.save()
