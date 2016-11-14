class DeployConfig(object):
    def __init__(self, env=None, config=None):
        self._config = config
        self._env = env
    
    def get(self, key=None):
        return self._config[self._env].get(key)
    
    def exists(self, key=None):
        return key in self._config[self._env]

