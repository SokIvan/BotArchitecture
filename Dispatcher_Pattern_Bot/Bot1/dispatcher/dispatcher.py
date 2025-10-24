from Handlers.handlers import Handler

class Dispatcher:
    def __init__(self):
        self._handlers: list[Handler] = []
        
    def add_handlers(self,*handlers: Handler):
        for handler in handlers:
            self._handlers.append(handler)
            
    def dispatch(self,update):
        for handler in self._handlers:
            if handler.can_handle(update):
                signal = handler.handle(update)
                if not signal:
                    break