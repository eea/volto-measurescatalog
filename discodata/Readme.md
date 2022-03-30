  Execute shell in wise-test-marine-frontend-1:
  $ cd /opt/frontend/src/addons/volto-measurescatalog/discodata
  $ apt-get update || : && apt-get install python -y
  $ apt-get install -y virtualenv
  $ rm -rf .venv
  $ apt-get install python3-pip
  $ rm -rf .venv
  $ virtualenv -p /usr/bin/python3 .venv
  $ .venv/bin/pip install -r requirements.txt
  $ apt install vim
  $ vim importer.py - set host = '10.50.4.135'
  $ .venv/bin/python3 importer.py
