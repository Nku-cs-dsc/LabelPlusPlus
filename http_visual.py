# -*- coding: utf-8 -*-
"""
#####################################################################
    > File Name: http_visual.py
    > Author: dongshichao.
    > Email: dongshichao1996@gmail.com
    > Created Time: 2023/05/25 15:36:12
#####################################################################
"""
import os
import json
import socket
from functools import lru_cache
from flask import Flask
from flask_paginate import get_page_parameter, Pagination
from flask import render_template, request
from flask import redirect, url_for

app = Flask(__name__)

ImageSet = list()
AnnotationList = set()
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
# default post ID is 8009
ImageURL = f'http://{ip}:8009'

Page = 1
HyperParameters = {'labelID': '', 'bottomScore': '', 'topScore': '',}


@lru_cache(maxsize=1)
def get_imageset(labelID, bottomScore, topScore):
    """get badcase from scorefile."""
    imageSet = [[os.path.join(ImageURL, 'images/testdata_229.jpg'), f'VisulDemo{i}', f'TestImg{i}.png'] for i in range(500)]
    return imageSet


@app.route("/resetLabel",methods=["POST", "GET"])
def annotation():
    global ImageSet, HyperParameters
    placeholder1 = '请输入LabelID'
    placeholder2 = '请输入CaseBottomScore'
    placeholder3 = '请输入CaseTopScore'
    per_page = 80
    Page = request.args.get(get_page_parameter(), type=int, default=1)
    # split total dataset into multi-pages.
    paginate = Pagination(page=Page, per_page=per_page, total=len(ImageSet), css_framework='bootstrap4')

    start = (Page - 1) * per_page
    end = start + per_page
    imageset = ImageSet[start:end]

    if request.method == "POST":
        annotation_list = request.form.getlist('checkedList[]')
        if len(annotation_list):
            print(annotation_list)

    return render_template('index.html', **locals())


@app.route("/",methods=["POST", "GET"])
def index():
    global ImageSet, HyperParameters, Page
    placeholder1 = '请输入LabelID'
    placeholder2 = '请输入CaseBottomScore'
    placeholder3 = '请输入CaseTopScore'
    
    per_page = 80
    Page = request.args.get(get_page_parameter(), type=int, default=1)

    if request.method == "GET":
        pass

    if request.method == "POST":
        visual_info = request.values.to_dict()
        for k in HyperParameters.keys():
            ret = visual_info.get(k)
            if ret != "":
                Page = 1
                HyperParameters[k] = ret
            
        ImageSet = get_imageset(**HyperParameters)
        
    # split total dataset into multi-pages.
    paginate = Pagination(page=Page, per_page=per_page, total=len(ImageSet), css_framework='bootstrap4')

    start = (Page - 1) * per_page
    end = start + per_page
    imageset = ImageSet[start:end]

    return render_template('index.html', **locals())


if __name__ == "__main__":
    app.run(debug=True, port=8801)

