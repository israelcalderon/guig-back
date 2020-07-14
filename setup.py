from setuptools import setup
from setuptools import find_packages

setup(name='Guig',
      description='Graphical User Interface for Git Backend API',
      version='0.0',
      author='Israel Calderón',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      install_requires=[
        'pytest',
        'flask',
        'gitpython',
        'flask-restful',
        'Flask-SQLAlchemy',
        'python-dotenv',
        'requests',
        'Flask-CORS'])
