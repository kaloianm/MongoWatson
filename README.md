# Starting the MongoWatson "platform"
## Create a Python3 virtual environment and install the Python backend service's required modules
```
virtualenv --python=python3 venv
. venv/bin/activate
python -m pip install -r svc/requirements.txt
python -m pip install -r svc/triage-scripts/mongosymb/requirements.txt
```

## Starting the backend service
```
python svc/mongowatson.py
```

## Starting the frontend service
```
cd ui/
npm install
npm start
```

Then open the browser and point it to [http://localhost:3000](http://localhost:3000).
