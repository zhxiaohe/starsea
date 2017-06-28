#!/usr/bin/env python
#coding=utf-8
from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash
from app import db, app


def abort_if_id_doesnt_exist(object, **kwargs):
    obj = object.query.filter_by(**kwargs).first()
    if obj is None:
        return None
    else:
        return obj

def dbdel(models, **kwargs):
    '''
        Detele data from Database
    '''
    for value in kwargs.values():
        if not value:
            return None

    db.session.query(models).filter_by(**kwargs).delete()
    dbcommit()
    return True


def dbupdate(model, Id, args):
    '''
        Update db
    '''
    model.query.filter_by(Id=Id).update(args)
    dbcommit()
    return True


def dbcommit():
    '''
        commit db connect
    '''
    db.session.commit()
    return True
