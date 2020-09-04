import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = b'G\xd1\xe6\xe3m\xd4\xc5p\xc1\xe5\xd8\xb7M\x15d\xbf\x9bj\x14\x05\x93\xfa\x0f\xa9'
    ADMIN_ACCESS = False
    S3_BUCKET                 = 'outerspace'
    S3_KEY                    = 'AKIAIZB5XLHWQLPOR3JA'
    S3_SECRET                 = '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'
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    S3_REGION                 = 'us-east-1'
    S3_SIGNATURE_VERSION      = 's3v4'


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

