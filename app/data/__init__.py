 
from threading import Lock
from app.data.watcher import Watcher

import logging

FILE_PATH = "authorized_keys.txt"
LOGGER = logging.getLogger("uvicorn")

class AuthorizedkeysRepo:
    
    def __init__(self):
        self._lock = Lock()
        self._keys = self._read_keys_file()
        self._watcher = Watcher.watch(file=FILE_PATH, action=lambda event: self._update_keys(event))
    
    def _read_keys_file(self):
        with self._lock:
            with open(FILE_PATH, "r") as f:
                keys = set(f.readlines())
            
        return [key.strip() for key in keys]
   
    def _update_keys(self, event):
        if event.src_path == FILE_PATH:
            self._keys = self._read_keys_file()
            LOGGER.info("Updated authorized keys")

    def authorized(self, key):
        with self._lock:
            return key in self._keys
