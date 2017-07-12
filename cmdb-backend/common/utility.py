#!/usr/bin/env python
#coding=utf-8
from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash, jsonify
import hashlib
from common.token_manage import  Token_Manager
from functools import wraps


def hashpass(src):
    passwd=hashlib.md5()
    passwd.update(src)
    return passwd.hexdigest()




def login_required(func):
    @wraps(func)
    def dec(*args,**kwargs):
        if not  session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return dec


def login_required_forapi(func):
    @wraps(func)
    def dec(*args,**kwargs):
        if not  session.get('logged_in'):
            return jsonify({'status': 'error','data': 'please login '})
        return func(*args,**kwargs)
    return dec


def auth_login_required(func):
    @wraps(func)
    def auth(*args,**kwargs):
        if not request.headers.get('Authorization'):
            return  'Authorization Unauthorized',401
        t = request.headers.get('Authorization')
        au = Token_Manager().verify_auth_token(token=t)
        if 401 == au:
            return  'Authorization1 Unauthorized',401
        else:
            pass
        return func(*args,**kwargs)
    return auth


