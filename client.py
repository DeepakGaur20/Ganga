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
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    client = Client("opc.tcp://0.0.0.0:4840/sinewave/server")
    client.set_security_string(
        "Basic256Sha256,"
        "SignAndEncrypt,"
        "certificate.pem,"
        "key.pem")

    client.set_user("sinewaveuser")
    client.set_password("passw0rd")

    try:
        client.connect()
        client.load_type_definitions() 

        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # gettting our namespace idx
        uri = "http://sinewave.myopc.com"
        idx = client.get_namespace_index(uri)

        # Now getting a variable node using its browse path
        sinevar = root.get_child(["0:Objects", "{}:SineObj".format(idx), "{}:SineWave".format(idx)])
        freqnode = root.get_child(["0:Objects", "{}:SineObj".format(idx), "{}:Frequnecy".format(idx)])
        obj = root.get_child(["0:Objects", "{}:SineObj".format(idx)])
        print("myvar is: ", freqnode)

        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(sinevar)
        time.sleep(0.1)

        # we can also subscribe to events from server
        sub.subscribe_events()
        # calling a method on server
        res = obj.call_method("{}:changefrequency".format(idx),freqnode.nodeid, 1)
        embed()
    finally:
        client.disconnect()

