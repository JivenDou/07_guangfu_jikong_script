from apis.api_init import *


class ApiContext:
    def set_api_object(self, object):
        self.api_object = eval(object)()

    def operation(self, request):
        return self.api_object.operation(request)
