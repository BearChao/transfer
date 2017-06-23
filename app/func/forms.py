#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 下午9:51
# @Author  : Bear Chao
# @Site    : http://blog.nickzy.com
# @File    : forms.py
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class NewTaskForm(FlaskForm):
    dataType = SelectField('任务类型',choices=[('file','本地文件'),('ftp','FTP'),('webDav','WebDAV'),('mysql','MySQL'),('oracle','Oracle')])
    name = StringField('描述')
    dir = StringField('地址\目录')
    port = IntegerField('端口号',validators=[NumberRange(1,65535,'请输入正确的端口号')])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), ])
    password = StringField('密码', validators=[DataRequired()])
    target = StringField('目标文件夹\数据库')
    tables = StringField('数据表')
    finger = StringField('finger')
    count = IntegerField('运行次数')
