from factory import ListenerFactory
import falcon


api           = falcon.API()
engine_source = ListenerFactory.get_listener(ListenerFactory.ENGINE_SOURCE)

api.add_route("/engine_source", engine_source)