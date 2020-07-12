from git import Repo
import os


repository = Repo(os.environ.get('REPO_PATH'))
