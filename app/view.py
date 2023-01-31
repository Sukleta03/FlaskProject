from flask import Blueprint, render_template, request
import json

pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.route('/')
def homepage():
    return {"hellow": "new student"}

