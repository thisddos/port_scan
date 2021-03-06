from flask import Flask,request,flash,session,render_template,g,redirect,url_for
from socket import *
import threading
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HARD'

@app.route('/scan/',methods=['GET','POST'])
def pscan():

    def scan(ip, ports):

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

        # 检验参数是否为空
        if session.get('ip') and session.get('ports'):

            # 禁止IP扫描,并且写入扫描者IP地址
            if '127.0' in session.get('ip') or '0.0.' in session.get('ip') or session.get('ip') == 'localhost':
                session['ip'] = 0

                req_ip = request.remote_addr # 获取扫描者IP

                # 准备写入扫描者IP
                with open('./notscanip.log','a') as f:

                    # 写入IP
                    f.write(str(req_ip) + str(datetime.datetime.now()))

                # 返回flush消息
                flash('此 地址 禁止扫描，已留下禁止扫描记录')

                # 返回页面
                return render_template('scan.html', show=False)


            # 对格式错误的端口号进行简单修补
            if session.get('ports')[-1] != ',':
                session['ports'] = session['ports'] + ','

            # 开始正式扫描
            try:

                opport = [] # 打开端口数量
                t_list = [] # 线程列表

                # 转换为列表，方便进行切片
                ports = list(eval(str(session.get('ports'))))

                # 进行切片，并且每2个端口号添加一个线程
                for run in range(int(len(ports)/2)+1):
                    port = ports[:2] # 进行切片
                    del ports[:2] # 删除之前的值
                    Thread = threading.Thread(target=scan,args=(session.get('ip'),port)) # 创建线程
                    t_list.append(Thread) # 添加线程到列表

                # 运行线程
                for thread in t_list:
                    thread.start()

                # 等待线程结束
                for thread in t_list:
                    thread.join()

                # 获取线程结果，并且去重复
                g.ret = sorted(set(opport),key=opport.index)

                # 返回结果
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
        return redirect(url_for('scanhtml'),show=False)

@app.errorhandler(404)
def error_404(e):
    return """
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" />
    <div class='container'>
    <div class="jumbotron">
      <h1>404, 您访问的页面不存在.</h1>
      <p>...</p>
      <p><a class="btn btn-primary btn-lg" href="/" role="button">返回首页</a></p>
    </div>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)
