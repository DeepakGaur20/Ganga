import sys
sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event.EventId)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #Create client
    client = Client("opc.tcp://localhost:4840/sinewave/server")
    #set certificate path
    client.set_security_string(
        "Basic256Sha256,"
        "SignAndEncrypt,"
        "certificate.pem,"
        "key.pem")

    #set authentication
    client.set_user("sinewaveuser")
    client.set_password("passw0rd")

    try:
        #connect to server
        client.connect()
        client.load_type_definitions() 

        root = client.get_root_node()
        print("Root node is: ", root)
        #get server object nodes
        objects = client.get_objects_node()

        # gettting our namespace idx
        uri = "http://sinewave.myopc.com"
        idx = client.get_namespace_index(uri)

        # get sine variable node using its browse path
        sinevar = root.get_child(["0:Objects", "{}:SineObj".format(idx), "{}:SineWave".format(idx)])
        freqnode = root.get_child(["0:Objects", "{}:SineObj".format(idx), "{}:Frequnecy".format(idx)])
        obj = root.get_child(["0:Objects", "{}:SineObj".format(idx)])
        print("myvar is: ", freqnode)

        # subscribing to a sinewave node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(sinevar)
        time.sleep(0.1)

        # we can also subscribe to events from server
        sub.subscribe_events()
        # calling server UA methos to change frequency
        res = obj.call_method("{}:changefrequency".format(idx),freqnode.nodeid, 6)
        embed()
    finally:
        client.disconnect()


