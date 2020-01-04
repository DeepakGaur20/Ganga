from threading import Thread
import copy
import logging
import time
import numpy as np
import sys
sys.path.insert(0, "..")

try:
    from IPython import embed

except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


from opcua import ua, uamethod, Server
from opcua.server.user_manager import UserManager
credentials =  {
                'sinewaveuser': 'passw0rd',
            }

def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in credentials and password == credentials[username]


@uamethod
def changefrequency(parent,freqnode,freq):
    server.set_attribute_value(freqnode,ua.DataValue(freq))
    return freq


class SineWaveGenerator(Thread):
    def __init__(self, var,f):
        Thread.__init__(self)
        self._stopev = False
        self.var = var
        self.f = f

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            logging.info("frequency value is  : %s",self.f.get_value())
            t = np.linspace(0,  self.f.get_value()* np.pi, 1024)
            a = np.sin(t)
            self.var.set_value(a.tolist())
            time.sleep(8)



if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/sinewave/server")
    server.set_server_name("SINE WAVE OPC SERVER")
    # set all possible endpoint policies for clients to connect through
    server.load_certificate("certificate.pem")
    server.load_private_key("key.pem")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    policyIDs = ["Username"]
    server.set_security_IDs(policyIDs)
    server.user_manager.set_user_manager(user_manager)
    uri = "http://sinewave.myopc.com"
    idx = server.register_namespace(uri)

    sineobj = server.nodes.objects.add_object(idx, "SineObj")
    freq = sineobj.add_variable(idx,"Frequnecy",2)
    freq.set_writable()
    sinewave = sineobj.add_variable(idx, "SineWave", [0.0])
    amplitude = sineobj.add_variable(idx, "Amplitude", [0.0])
    amplitude.set_writable()
    frequency_node = sineobj.add_method(idx, "changefrequency", changefrequency, [ua.VariantType.Int64,ua.VariantType.Int64], [ua.VariantType.Int64])

    # import some nodes from xml
    #server.import_xml("custom_nodes.xml")

    sineevent = server.get_event_generator()
    sineevent.event.Severity = 300
    generator = SineWaveGenerator(amplitude,freq)
    generator.start()
    logging.info("frequency node id :%s" ,freq.nodeid)
    server.start()
    try:
        while True:
            sineevent.trigger(message="New sine wave generated")
            server.set_attribute_value(sinewave.nodeid, ua.DataValue(amplitude.get_value()))  # Server side write method which is a but faster than using set_value
            time.sleep(10)
        embed()
    finally:
        generator.stop()
        server.stop()

