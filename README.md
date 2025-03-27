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


**Run the frontend**
In frontend dir
```
npm run start
```


**Seed backend with data**

```
$env:SEED_DATA="True" 
>> python -m backend.app
```