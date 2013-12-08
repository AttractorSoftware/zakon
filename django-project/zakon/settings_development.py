from settings import *

INSTALLED_APPS = INSTALLED_APPS + (
    'tests.document',
    'lettuce.django',
    'discover_jenkins',
)

TEST_RUNNER = 'discover_jenkins.runner.DiscoverCIRunner'

LETTUCE_AVOID_APPS = (
    'document',
    'reference',
    'discover_jenkins',

)

TEST_PROJECT_APPS = (
    'tests',
)
