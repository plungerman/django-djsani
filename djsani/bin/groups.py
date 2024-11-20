# -*- coding: utf-8 -*-

import django
import os
import sys

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

django.setup()

from django.conf import settings
from django.contrib.auth.models import User


def main():
    users = User.objects.filter(groups__isnull=True)
    for user in users:
        if hasattr(user, 'student'):
            print(user, user.last_login)


if __name__ == '__main__':
    sys.exit(main())
