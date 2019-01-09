from yaks.encoding import *
from yaks.message import *
from papero.property import *
from yaks.runtime import *
from yaks.path import Path
from yaks.selector import Selector


class Workspace(object):
    def __init__(self, runtime, path, wsid):
        self.rt = runtime
        self.path = path
        self.wsid = wsid
        self.properties = [Property(Message.WSID, wsid)]

    def put(self, path, value, quorum=1):
        path = Path(path)
        pm = PutM(self.wsid, [(path, value)])
        reply = self.rt.post_message(pm).get()
        return check_reply_is_ok(reply, pm)

    def get(self, selector, quorum=1, encoding=Encoding.RAW, fallback=TranscodingFallback.KEEP):
        """Requests Yaks to get a list of the stored paths/values where all the paths match the selector [s].
           [s] can be absolute or relative to the workspace [w].
           The [quorum] (default value is 1) is used by Yaks to decide for each matching path the number of 
           answer from storages to wait before returning the associated value.
           The [encoding] indicates the expected encoding of the resulting values. If the original values have a different encoding, Yaks will try to transcode them into the expected encoding.
           By default, if no encoding is specified, the vaules are returned with their original encoding.
           The [fallback] indicates the action that Yakss will perform if the transcoding of a value fails. *)
        """
        s = Selector.to_selector(selector)
        gm = GetM(self.wsid, s)
        reply = self.rt.post_message(gm).get()
        if check_reply_is_values(reply, gm):
            return reply.kvs
        else:
            raise "Get received an invalid reply"
        return []

    def remove(self, path, quorum=1):
        """

        """
        path = Path.to_path(path)
        rm = DeleteM(self.wsid, path)
        reply = self.rt.post_message(rm).get()
        return check_reply_is_ok(reply, rm)

    def subscribe(self, selector, listener=None):
        s = Selector.to_selector(selector)
        sm = SubscribeM(self.wsid, s)
        reply = self.rt.post_message(sm).get()
        if check_reply_is_ok(reply, sm):
            subid = find_property(Message.SUBID, reply.properties)
            if listener is not None:
                self.rt.add_listener(subid, listener)
            return subid
        else:
            raise "Subscribe received an invalid reply"

    def unsubscribe(self, subscription_id):
        um = UnsubscribeM(self.wsid, subscription_id)
        reply = self.rt.post_message(um).get()
        if check_reply_is_ok(reply, um):
            self.rt.remove_listener(subscription_id)
            return True
        else:
            raise "Unsubscribe received an invalid reply"
