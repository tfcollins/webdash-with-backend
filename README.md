# WebUI For Device Testing

## Setup

```bash
git clone https://github.com/tfcollins/webdash-with-backend.git
cd webdash-with-backend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
git clone https://github.com/analogdevicesinc/pyadi-iio.git
cd pyadi-iio
pip install -r requirements.txt
pip install -r requirements_dev.txt
cd ..
```

## Run the Dash App

### Create SQLite Database


```bash
sudo apt install sqlite3
sqlite3 db.sqlite3
```

### Start Celery Background Worker

```bash
celery -A tasks worker --loglevel=info
```

### Start the Dash App

```bash
python app.py
```

It will be running on http://localhost:8050/