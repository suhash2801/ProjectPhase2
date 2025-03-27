**Activate virtual environment**

```
blockchain-env/Scripts/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

***Run the tests***
Activate the virtual environment
```
python -m pytest backend/tests
```

***Run Application and API***
Activate virtual environment
```
python3 -m backend.app
```


**Run a peer instance**
Activate virtual environment
```
$env:PEER = "True"
python -m backend.app

```