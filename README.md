# Starting the MongoWatson "platform"
## Create a Python3 virtual environment and install the Python backend service's required modules
```
virtualenv --python=python3 venv
. venv/bin/activate
python -m pip install -r svc/requirements.txt
python -m pip install -r svc/triage-scripts/mongosymb/requirements.txt
```

## Use keyring in order to set-up the required credentials
**Stats service secret (STATS_SVC_CREDENTIAL):**
```
keyring set MongoWatson STATS_SVC_CREDENTIAL
```

## Starting the backend service
```
python svc/mongowatson.py
```

## Starting the frontend service
```
npm install --prefix ui/
npm start --prefix ui/
```

Finally, open the browser and point it to [http://localhost:3000](http://localhost:3000).
