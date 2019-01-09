from yaks.encoding import *

class Workspace(object):
    def __init__(self, runtime, path, wsid):
        self.runtime = runtime
        self.path = path
        self.wsid = wsid

    def put(self, path, value, quorum=1):
        return True
        
    def get(self,selector, quorum=1, encoding=Encoding.RAW, fallback=TranscodingFallback.KEEP):
        """Requests Yaks to get a list of the stored paths/values where all the paths match the selector [s].
           [s] can be absolute or relative to the workspace [w].
           The [quorum] (default value is 1) is used by Yaks to decide for each matching path the number of 
           answer from storages to wait before returning the associated value.
           The [encoding] indicates the expected encoding of the resulting values. If the original values have a different encoding, Yaks will try to transcode them into the expected encoding.
           By default, if no encoding is specified, the vaules are returned with their original encoding.
           The [fallback] indicates the action that Yakss will perform if the transcoding of a value fails. *)
        """
        return []