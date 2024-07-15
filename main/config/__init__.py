import os
import sys
from .settings import DevConfig, ProductionConfig, TestConfig

# Determine the appropriate configuration class
APP_ENV = os.environ.get('APP_ENV', 'Dev')
APP_ENV = "Production"
print(APP_ENV)
if APP_ENV == 'Production':
    ConfigClass = ProductionConfig
elif APP_ENV == 'Test':
    ConfigClass = TestConfig
else:
    ConfigClass = DevConfig

# Create an instance of the config class
_current = ConfigClass()

# Copy attributes to the module for convenience
for attr in [a for a in dir(_current) if not a.startswith('__')]:
    val = os.environ.get(attr, getattr(_current, attr))
    setattr(sys.modules[__name__], attr, val)

def as_dict():
    return {attr: getattr(sys.modules[__name__], attr) for attr in dir(sys.modules[__name__]) if not attr.startswith('__')}
