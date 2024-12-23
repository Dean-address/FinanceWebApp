from decouple import config

from .configs import dev, prod
from django.contrib import messages

env = config("DEBUG", cast=bool)
if env == False:
    from .configs.prod import *
else:
    from .configs.dev import *

current_environment = "development" if env == True else "Production"
print(env)
print(f"Current environment: {current_environment}")
print(f"Using database: {DATABASES['default']['NAME']}")

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}
