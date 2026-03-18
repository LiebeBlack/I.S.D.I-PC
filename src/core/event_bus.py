import collections

class EventBus:
    def __init__(self):
        self._listeners = collections.defaultdict(list)

    def subscribe(self, event_type: str, callback):
        self._listeners[event_type].append(callback)

    def emit(self, event_type: str, data=None):
        for callback in self._listeners[event_type]:
            callback(data)

# Global Instance
bus = EventBus()
