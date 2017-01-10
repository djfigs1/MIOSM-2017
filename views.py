from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound
import os, shutil, uuid, json

@view_defaults(route_name='home')
class MusicViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='hello', renderer='views/main.pt')
    def hello_world(self):
        return {}


    @view_config(request_method='POST', route_name='hello', request_param='photo.save')
    def savePhoto(self):
        input_file = self.request.POST['photo'].file
        caption = self.request.POST['caption']
        filenameExtension = os.path.splitext(self.request.POST['photo'].filename)[1][1:]
        UUID = uuid.uuid4()
        file_path = os.path.join('C:\\Users\\djfig\\Pictures\\Test\\', '%s.' % UUID + filenameExtension)
        jsonFile = os.path.join('C:\\Users\\djfig\\Pictures\\Test\\', 'photoCaptions.json')
        input_file.seek(0)
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        print (caption)
        return HTTPFound(self.request.url)