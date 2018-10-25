import os
class Config(object):
	SECRET_KEY = 'ContraseNia'

class DevelopmentConfig(Config):
	DEBUG = True
