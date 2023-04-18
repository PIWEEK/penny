# Installation


```
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/ShoneGK/ChatterPy
python3 -m spacy download en_core_web_sm
pip install chatterbot-corpus flask flask-socketio
pip install --upgrade PyYaml
```


# Train

```
python penny.py train
```


# Run

```
python penny.py
```

The web interface will be at http://127.0.0.1:5000/

