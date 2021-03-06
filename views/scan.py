#!/usr/bin/env python
__author__ = 'XeanYu'
from flask.blueprints import Blueprint

scan = Blueprint('scan',__name__,url_prefix='/scan')

@scan.route('/',method=['GET','POST'])
def pscan():
    def scan(ip, ports):
        opport = []
        for port in ports:
            try:
                setdefaulttimeout(0.5)
                tcpsock = socket(AF_INET, SOCK_STREAM)
                tcpsock.connect((str(ip), int(port)))
                opport.append(port)
            except:
                pass

        return opport

    if request.method == 'POST':
        session['ip'] = request.form.get('ip') # 接受扫描地址
        session['ports'] = request.form.get('ports') # 接受扫描端口

        # 扫描端口
        if session.get('ip') and session.get('ports'):

            # 对格式错误的端口号进行简单修补
            if session.get('ports')[-1] != ',':
                session['ports'] = session['ports'] + ','

            # 开始正式扫描
            try:
                ports = eval(str(session.get('ports')))
                g.ret = scan(str(session.get('ip')), ports)
                return render_template('scan.html', show=True, ports=g.ret, ip=session.get('ip'))

            # 如果端口填写有误，则返回Flush
            except:
                flash('IP/端口填写错误!')
                return render_template('scan.html', show=False)

        # 信息填写不完整 返回 Flush
        else:
            flash('请传入完整信息')
            return render_template('scan.html', show=False)


    elif request.method == 'GET':
        return render_template('scan.html',show=False)

    else:
        return redirect(url_for('scanhtml'))