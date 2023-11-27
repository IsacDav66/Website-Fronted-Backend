# src/controllers/indexController.py
from flask import render_template, session
from src.controllers.baseController import BaseController
from flask import Blueprint, render_template, session
from flask import current_app as app

class IndexController(BaseController):
    def __init__(self, app):
        prefix = '/index'
        super().__init__(app, 'index')
        
        self.blueprint.route('/', methods=['GET'])(self.index)

    def index(self):
        # tu lógica aquí
        username = session.get('username', None)
        return render_template('index.html', username=username)
