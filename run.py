from flask import Flask

app = Flask(__name__)





@app.route('/')
def hello_world():
    return 'hello world~by zx!!这是一个自动化部署的程序！'


if __name__ == '__main__':
    app.run()
