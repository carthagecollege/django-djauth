#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""OneLogin LDAP authentication."""

import argparse

import django
import sys


django.setup()

from django.conf import settings
from djauth.managers import LDAPManager

# set up command-line options
desc = """
    Maquette for OneLogin
"""

parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '--username',
    dest='username',
    required=True,
    help="Person's username.",
)
parser.add_argument(
    '--password',
    dest='password',
    required=False,
    help="Person's password.",
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Authenticate against OneLogin LDAP."""
    ldap_groups = settings.LDAP_GROUPS
    ldap_group_attr = settings.LDAP_GROUP_ATTR
    eldap = None
    try:
        eldap = LDAPManager()
    except Exception as error:
        raise Exception(error)

    if eldap:
        print("El Dap init")
        result_data = eldap.search(find=username, field='cn')
        print(result_data)
        if result_data:
            cid = result_data[0][1][settings.LDAP_ID_ATTR][0]
            print('cid = {0}'.format(cid))
            if password:
                print("attempting to bind...")
                try:
                    bind = eldap.bind(result_data[0][0], password)
                except Exception as auth_fail:
                    bind = auth_fail
                print(bind)
            print('groups:\n\n')
            groups = []
            for role in result_data[0][1][ldap_group_attr]:
                if isinstance(role, bytes):
                    role = role.decode(encoding='utf-8')
                group = ldap_groups.get(role.split(',')[0].split(' ')[0][3:])
                if group and group not in groups:
                    groups.append(group)
            print(groups)
            # testing for djbeca
            luser = result_data[0][1]
            print('username={0}'.format(luser['cn'][0]))
            print('email={0}'.format(luser['mail'][0]))
            print('first_name={0}'.format(luser['givenName'][0]))
            print('last_name={0}'.format(luser['sn'][0]))
    else:
        print("El Dap fail")


if __name__ == '__main__':

    args = parser.parse_args()
    username = args.username
    password = args.password
    test = args.test
    sys.exit(main())
