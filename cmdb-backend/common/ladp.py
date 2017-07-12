#!/usr/bin/env python
#coding=utf-8
import ldap
from config import LDAP_URL, LDAP_BASE_DN, LDAP_USER, LDAP_PASSWD

ldappath = LDAP_URL
baseDN =   LDAP_BASE_DN
ldapuser = LDAP_USER
ldappass = LDAP_PASSWD

def _validateLDAPUser(user):
    try:
        l = ldap.initialize(ldappath)
        l.protocol_version = ldap.VERSION3
        l.simple_bind(ldapuser, ldappass)

        searchScope = ldap.SCOPE_SUBTREE
        searchFiltername = "sAMAccountName"
        retrieveAttributes = None
        searchFilter = '(' + searchFiltername + "=" + user +')'

        ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
        result_type, result_data = l.result(ldap_result_id,1)
        # print result_data
        if ( not len(result_data) == 0 ):
          r_a, r_b = result_data[0]
          # print r_b["distinguishedName"]
          return 1, r_b["distinguishedName"][0]
        else:
          return 0, ''
    except ldap.LDAPError, e:
        return 0, ''
    finally:
        l.unbind()
        del l

def GetDn(user, trynum = 10):
    i = 0
    isfound = 0
    foundResult = ""
    while (i < trynum):
        isfound, foundResult = _validateLDAPUser(user)
        if ( isfound ):
          break
        i += 1
    return foundResult

def LDAPLogin(userName, Password):
    try:
        if ( Password=="" ):
            return "PassWord empty"

        dn = GetDn(userName, 10)
        if ( dn=='' ):
            return "Not Exist User"

        my_ldap = ldap.initialize(ldappath)
        if my_ldap.simple_bind_s(dn, Password):
            #print "Login Ok"
            return True
        else:
            return False
    except Exception, e:
        # print "Login Fail"
        return False

if __name__ == '__main__':
    print(LDAPLogin('zhangtx', 'Qianbao'))
    pass