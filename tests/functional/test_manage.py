
import json
import os
import requests
import sqlite3
import time


def test_manage_make_migrations(test_project):
    test_project.run_cmd('testproject/manage.py db create .models')

    assert '0001_create_table_user.py' in os.listdir('testproject/migrations')


def test_manage_migrate(test_project):
    test_project.run_cmd('testproject/manage.py db create .models')
    test_project.run_cmd('testproject/manage.py db upgrade')

    conn = sqlite3.connect('testproject.db')
    cursor = conn.cursor()
    count_res = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='user'; ").fetchall()

    assert int(count_res[0][0]) == 1


def test_manage_runserver(test_project):
    test_project.run_cmd('testproject/manage.py db create .models')
    test_project.run_cmd('testproject/manage.py db upgrade')

    process = test_project.run_popen('testproject/manage.py runserver')
    time.sleep(2)  # Wait for the server to start

    response = requests.get('http://localhost:8888/health')

    try:
        assert response.status_code == 200
        assert json.loads(response.text) == 'healthy'

    finally:
        process.kill()
        time.sleep(2)  # Wait for the server to stop
