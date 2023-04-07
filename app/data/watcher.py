import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class CustomFileSystemEventHandler(FileSystemEventHandler):
    
    def __init__(self, path, action):
        self.path = path
        self.action = action
        self.old = 0
        
    
    def on_modified(self, event):
        statbuf = os.stat(self.path)
        new = statbuf.st_mtime
        if (new - self.old) > 0.5:
            self.action(event)
        self.old = new
    

class Watcher:
    
    @staticmethod
    def watch(file, action):
        return Watcher(file, action)
    
    def __init__(self, file, action):
        self._event_handler = CustomFileSystemEventHandler(file, action)
        
        self._observer = Observer()
        self._observer.schedule(self._event_handler, file, recursive=False)
        self._observer.start()
                
    def stop(self):
        self._observer.stop()

