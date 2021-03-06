from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class CfgNotifyForm(FlaskForm):
    check_order = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_name = StringField('通知人姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_number = StringField('通知号码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')

class UserForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='不能为空')])
    fullname = StringField('真实姓名',validators=[DataRequired(message='不能为空')])
    password = PasswordField('密码',validators=[DataRequired(message='不能为空')])
    email = StringField('电子邮箱')
    phone = StringField('电话号码')
    role = SelectField('操作权限', choices=[(1,'管理员'), (2,'查看日志')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')