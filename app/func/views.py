from flask import render_template

from . import func

# 主页
@func.route('/home', methods=['GET'])
#@login_required
def home():
    return render_template('func/home.html')