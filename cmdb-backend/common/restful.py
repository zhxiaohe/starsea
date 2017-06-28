#!/usr/bin/env python
#coding=utf-8
from flask import Flask, request, render_template, redirect, url_for, session, g, abort, flash,jsonify


class Serialization(object):
    def json_message(self,data):
        return  jsonify(
                      data
                  )

    def json_message_200(self,data,info=''):
        return  jsonify( {
                      "status":"200",
                      "message":"OK",
                      "result":data,
                      "info":info
                  })

    def json_message_201(self,data,info=''):
        return  jsonify( {
                      "status":"200",
                      "message":"CREATED",
                      "result":data,
                      "info":info
                  })

    def json_message_401(self,mes="Unauthorized!"):
        return  jsonify( {
                      "status": "401",
                      "message": mes
                  })

    def json_message_403(self,mes="Forbidden!"):
        return  jsonify( {
                      "status": "403",
                      "message": mes
                  })

    def json_message_404(self,mes="NOT FOUND!"):
        return  jsonify( {
                      "status": "404",
                       "message": mes
                  })

    def json_message_406(self,mes="Not Acceptable!"):
        return  jsonify( {
                      "status": "406",
                       "message": mes
                  })

    def json_message_422(self,mes="Unprocesable entity!"):
        return  jsonify( {
                      "status": "422",
                       "message": mes
                  })

    def json_message_500(self,mes="INTERNAL SERVER ERROR!"):
        return  jsonify( {
                      "status": "500",
                       "message": mes
                  })