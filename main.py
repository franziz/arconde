from lib.factories.listener      import ListenerFactory
from falcon_multipart.middleware import MultipartMiddleware
import falcon


api           = falcon.API(middleware=[MultipartMiddleware()])
deploy        = ListenerFactory.get_listener(ListenerFactory.DEPLOY)

api.add_route("/deploy", deploy)