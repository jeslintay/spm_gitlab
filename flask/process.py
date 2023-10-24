from flask import Flask
import multiprocessing
import login
import roles

def run_login_app():
    login.app.run(debug=True, host='0.0.0.0', port=6000)

def run_roles_app():
    roles.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=run_login_app)
    process2 = multiprocessing.Process(target=run_roles_app)

    process1.start()
    process2.start()
