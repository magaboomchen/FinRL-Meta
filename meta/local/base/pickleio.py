'''
compatibility
https://rebeccabilbro.github.io/convert-py2-pickles-to-py3/
'''

import base64
import sys

if sys.version > '3':
    import _pickle as cPickle
else:
    import cPickle


class PickleIO(object):
    def __init__(self):
        self.default_protocol = 2

    def readfile(self, filepath):
        df = open(filepath, 'rb')
        if sys.version > '3':
            obj = cPickle.load(df, encoding="latin1")
        else:
            obj = cPickle.load(df)
        df.close()
        # self.logger.debug("obj:{0}".format(obj))
        return obj

    def writefile(self, filepath, obj):
        df = open(filepath, 'wb')
        cPickle.dump(obj, df, protocol=self.default_protocol)
        df.close()

    def obj2pickle(self, obj):
        return base64.b64encode(cPickle.dumps(obj,
                                    protocol=self.default_protocol
                                ))

    def pickle2obj(self, pickle_instance):
        if sys.version > '3':
            return cPickle.loads(base64.b64decode(pickle_instance), encoding="latin1")
        else:
            return cPickle.loads(base64.b64decode(pickle_instance))
