
import os
import pytest
import subprocess
import sys
import tempfile


_colibris_env = None


class ColibrisEnv:
    def __init__(self):
        self.venvs_tmp_dir = tempfile.TemporaryDirectory()
        self.venvs_dir = self.venvs_tmp_dir.name
        self.venv_dir = os.path.join(self.venvs_dir, 'test_venv')

        self.projects_tmp_dir = tempfile.TemporaryDirectory()
        self.projects_dir = self.projects_tmp_dir.name

        self.colibris_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # Prepare virtual env & install colibris
        self.make_virtual_env()
        dist = self.make_dist()
        self.run_cmd('pip install {}'.format(dist))

    def __del__(self):
        self.venvs_tmp_dir.cleanup()
        self.projects_tmp_dir.cleanup()

    def make_virtual_env(self):
        subprocess.check_call('pip install virtualenv', shell=True)
        subprocess.check_call('python -m virtualenv {}'.format(self.venv_dir), shell=True)

    def make_dist(self):
        prev_dir = os.getcwd()
        os.chdir(self.colibris_dir)
        subprocess.check_call('rm -rf dist build *.egg', shell=True)
        subprocess.check_call('{} setup.py sdist'.format(sys.executable), shell=True)
        os.chdir(prev_dir)

        return os.path.join(self.colibris_dir, 'dist', os.listdir(self.colibris_dir + '/dist')[0])

    def chdir_projects(self):
        os.chdir(self.projects_dir)

    def ensure_req(self, req):
        self.run_cmd('pip install {}'.format(req))

    def run_cmd(self, cmd):
        subprocess.check_call('. {}/bin/activate && {}'.format(self.venv_dir, cmd), shell=True)

    def run_popen(self, cmd, **kwargs):
        return subprocess.Popen('. {}/bin/activate && {}'.format(self.venv_dir, cmd), shell=True, **kwargs)


@pytest.fixture
def colibris_env():
    global _colibris_env

    # Reuse the same env for all tests to reduce testing time
    if _colibris_env is None:
        _colibris_env = ColibrisEnv()

    return _colibris_env


@pytest.fixture
def test_project(colibris_env):
    initial_dir = os.getcwd()
    colibris_env.chdir_projects()

    colibris_env.ensure_req('pyjwt')
    colibris_env.ensure_req('pytest')

    colibris_env.run_cmd('colibris-start-project test-project'.format(colibris_env.colibris_dir))
    os.chdir('test-project')

    yield colibris_env

    colibris_env.chdir_projects()
    colibris_env.run_cmd('rm -rf {} test-project')
    os.chdir(initial_dir)
