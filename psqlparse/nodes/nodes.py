import json
import six


class Node(object):

    def __iter__(self):
        # Might be better to implement this as a custom JSON encoder
        for k in self.__dict__:
            v = self.__dict__[k]

            if v in (None, [], {}):
                pass
            elif isinstance(v, Node):
                yield k, dict(v)
            elif isinstance(self.__dict__[k], list):
                l = []
                for i in v:
                    if i is None:
                        pass
                    elif isinstance(i, Node):
                        l.append(dict(i))
                    elif hasattr(i, 'val'):
                        l.append(i.val)
                    else:
                        l.append(i)
                yield k, l
            elif hasattr(v, 'val'):
                yield k, v.val
            else:
                yield k, v

    def __eq__(self, other):
        return isinstance(other, Node) and dict(self) == dict(other)

    def __hash__(self):
        return hash(json.dumps(dict(self), sort_keys=True))

    def tables(self):
        """
        Generic method that does a depth-first search on the node attributes.

        Child classes should override this method for better performance.
        """
        _tables = set()

        for attr in six.itervalues(self.__dict__):
            if isinstance(attr, list):
                for item in attr:
                    if isinstance(item, Node):
                        _tables |= item.tables()
            elif isinstance(attr, Node):
                _tables |= attr.tables()

        return _tables
