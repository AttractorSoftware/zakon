from settings import *

INSTALLED_APPS = INSTALLED_APPS + (
    'tests.document',
    'lettuce.django'
)

LETTUCE_AVOID_APPS = (
    'document',
    'reference',
)
