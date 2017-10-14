from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import *
from datetime import timedelta
from pyramid.renderers import render
from pyramid.security import (remember, forget)
import os, shutil, uuid, json, time, pyramid.request, pyramid.response

version = "b0.1"
photoDir = os.path.join(os.path.dirname(__file__), "data/photos")
photoJSONDir = os.path.join(os.path.dirname(__file__), "data/photos/users.json")
cookieName = "_musicID"

acceptedLogins = {"admin": "hcmstrimmiosm2017"}
acceptedExtensions = ['jpg', 'jpeg', 'png', 'JPG']


@view_defaults(route_name='home')
class MusicViews(object):
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home', renderer='views/main.pt')
    def home(self):
        loginText = ""
        loginLink = ""
        galleryText = ""
        if (self.request.authenticated_userid != None):
            loginText = "Logout"
            loginLink = "/logout"
            galleryText = "Gallery"
        else:
            loginText = "Login"
            loginLink = "/login"
        return {'version': version, 'user_text': loginText, 'user_link': loginLink, 'gallery_link': '/gallery', 'gallery_text': galleryText}

    @view_config(route_name='json', renderer='json')
    def json(self):
        if (self.logged_in != None):
            jsonFile = os.path.join(os.path.dirname(__file__), photoJSONDir)
            j = None
            with open(jsonFile, 'r') as f:
                j = json.load(f)
                f.close()
            return j
        return HTTPForbidden()

    @view_config(route_name='points')
    def points(self):
        if (self.request.authenticated_userid != None):
            user = self.request.matchdict['id']
            points = self.request.matchdict['amount']
            jsonFile = os.path.join(os.path.dirname(__file__), photoJSONDir)
            j = None
            with open(jsonFile, 'r') as f:
                j = json.load(f)
                f.close()

            j['users'][user]['points'] += int(points)

            with open(jsonFile, 'w') as f:
                json.dump(j,f)
                f.close()
            return HTTPOk()
        else:
            return HTTPForbidden()

    @view_config(route_name='user', renderer='views/user.pt')
    def user(self):
        if (self.request.authenticated_userid != None):
            user = self.request.matchdict['id']
            jsonFile = os.path.join(os.path.dirname(__file__), photoJSONDir)
            j = None
            with open(jsonFile, 'r') as f:
                j = json.load(f)
                f.close()
            loginText = ""
            loginLink = ""
            if (self.request.authenticated_userid != None):
                loginText = "Logout"
                loginLink = "/logout"
            else:
                loginText = "Login"
                loginLink = "/login"

            points = 0
            if not j == None:
                points = j['users'][user]['points']
            return {'user_text': loginText, 'user_link': loginLink, 'points': str(points)}
        else:
            return HTTPForbidden()

    @view_config(route_name='photo')
    def photo(self):
        if (self.logged_in != None):
            photoId = self.request.matchdict['id']
            j = None
            with open(photoJSONDir, 'r') as f:
                j = json.load(f)
                f.close()

            for user in j['users']:
                for photo in j['users'][user]['photos']:
                    if photoId == photo:
                        return pyramid.response.FileResponse(os.path.join(photoDir, photoId + "." + j['users'][user]['photos'][photo]['extension']))
            return HTTPBadRequest()
        return HTTPForbidden()

    @view_config(route_name='rate')
    def rate(self):
        if (self.logged_in != None):
            photoId = self.request.matchdict['id']
            rate = self.request.matchdict['rate']
            jsonFile = os.path.join(os.path.dirname(__file__), photoJSONDir)
            j = None
            with open(photoJSONDir, 'r') as f:
                j = json.load(f)
                f.close()

            if not j == None:
                find = False
                for user in j['users']:
                    for photo in j['users'][user]['photos']:
                        if photoId == photo:
                            j['users'][user]['photos'][photoId]['approved'] = rate
                            find = True
                            break
                    if find:
                        break

                with open(jsonFile, 'w') as f:
                    json.dump(j, f)
                    f.close()
                return HTTPOk()
        else:
            return HTTPForbidden()


    @view_config(route_name='leaderboard', renderer='views/leaderboard.pt')
    def leaderboard(self):
        return {}

    @view_config(route_name='upload', renderer='views/upload.pt')
    def upload(self):
        # Submissions are done!
        return HTTPFound('/')

        j = None
        with open(photoJSONDir, 'r') as f:
            j = json.load(f)
            f.close()
        cookies = self.request.cookies

        try:
            user_uuid = cookies[cookieName]
        except KeyError:
            user_uuid = ""

        name = ""
        if not user_uuid == "":
            try:
                name = j['users'][user_uuid]['names'][-1]
            except KeyError:
                name = ""

        return {'errorMsg': '', 'name': name}

    @view_config(route_name='login', renderer='views/login.pt')
    def login(self):
        if ('form.submitted' in self.request.params):
            login = (self.request.params['login'])
            password = (self.request.params['password'])
            if (login in acceptedLogins.keys()):
                if (password == acceptedLogins[login]):
                    headers = remember(self.request, login)
                    return HTTPFound('/', headers=headers)
            return {'error': 'Invaild login. Either your username or password is incorrect.'}
        return {'error': ''}

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        return HTTPFound('/', headers=headers)

    @view_config(route_name='gallery', renderer='views/gallery.pt')
    def gallery(self):
        if (self.logged_in != None):
            return {}
        return HTTPForbidden()

    @view_config(request_method='POST', route_name='upload', request_param='photo.save', renderer='views/upload.pt')
    def photoPOST(self):
        # Submissions are done!
        return HTTPForbidden()

        caption = self.request.POST['caption']
        name = self.request.POST['name']

        # Check if file was submitted
        try:
            input_file = self.request.POST['photo'].file
        except AttributeError:
            return {'errorMsg': 'No photo was uploaded.', 'name': name}

        # Check if both name and caption was submitted

        if caption == "":
            return {'errorMsg': 'You must specify a caption.', 'name': name}
        elif name == "":
            return {'errorMsg': 'You must specify a name.', 'name': name}

        # Check if filename extension is supported
        filenameExtension = os.path.splitext(self.request.POST['photo'].filename)[1][1:]
        if not filenameExtension in acceptedExtensions:
            return {'errorMsg': 'That file isn\'t a valid file type.', 'name': name}

        UUID = uuid.uuid4()
        cookies = self.request.cookies
        file_path = os.path.join(photoDir, '%s.' % UUID + filenameExtension)
        jsonFile = os.path.join(os.path.dirname(__file__), photoJSONDir)
        input_file.seek(0)

        r = pyramid.response.Response()
        user_uuid = ""

        # Get the user UUID, if none exists, create one.
        try:
            user_uuid = cookies[cookieName]
        except KeyError:
            user_uuid = str(uuid.uuid4())
            r.set_cookie(cookieName, user_uuid, expires=timedelta(days=365))

        # Save the image
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
            output_file.close()

        j = None
        if (not os.path.isfile(jsonFile)):
            open(jsonFile, 'w+')

        # Get JSON file
        with open(jsonFile, 'r') as file:
            try:
                j = json.load(file)
            except:
                j = {'users': {}}
            file.close()

        # Write details to JSON file.
        with open(jsonFile, 'w') as file:
            photoDict = {}
            photoDict['extension'] = filenameExtension
            photoDict['approved'] = 0
            photoDict['caption'] = caption
            photoDict['time'] = time.time() * 1000

            try:
                j['users'][str(user_uuid)]['photos'][str(UUID)] = photoDict
                j['users'][str(user_uuid)]['lastUploadTime'] = time.time() * 1000
                if not name in j['users'][str(user_uuid)]['names']:
                    j['users'][str(user_uuid)]['names'].append(name)
            except:
                j['users'][str(user_uuid)] = {}
                j['users'][str(user_uuid)]['lastUploadTime'] = time.time() * 1000
                j['users'][str(user_uuid)]['names'] = []
                j['users'][str(user_uuid)]['names'].append(name)
                j['users'][str(user_uuid)]['points'] = 0
                try:
                    j['users'][str(user_uuid)]['photos'][str(UUID)] = photoDict
                except:
                    j['users'][str(user_uuid)]['photos'] = {}
                    j['users'][str(user_uuid)]['photos'][str(UUID)] = photoDict
            json.dump(j, file)
            file.close()

        return HTTPFound(location=self.request.url, headers=r.headers)