# from .model import
from flask import request, render_template
import numpy as np
from app import app


@app.route('/api/test', methods=['POST'])
def test():

    response = {
        'message' : 'alls fine'
                }

    return response
