# Age Archiver

---
 This app is made to help with the clutter by scanning a folder you designate for
 files older than a time range you designate. It then places the files in a zipped folder to save on space.
---
#### Installation and setup:
Clone
```commandline
git clone https://github.com/drachelehre/agearchiver
```

Set up and start a virtual environment:

For Linux/MacOS
```commandline
python3 -m venv venv
```
```commandline
source venv/bin/activate 
```

For Windows:
```commandline
python -m venv venv
.venv\Scripts\activate.bat
```

Once the virtual environment is active, install PyQt6:

```commandline
pip install PyQt6
```

Once everything is installed run the script:
```commandline
python main.py
```