import json

# Base event class
class EventBase:
    def serialize(self):
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, body):
        # Call child class constructor, passing JSON keys as keyword args
        return cls.__call__(**json.loads(body))

class EventModel(EventBase):
    def __init__(
            self, 
            specversion, 
            type, 
            source,
            subject,
            id,
            datacontenttype = None,
            data = None):
        self.specversion = specversion
        self.type = type
        self.source = source
        self.subject = subject
        self.id = id
        self.datacontenttype = datacontenttype
        self.data = data
