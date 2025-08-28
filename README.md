Have python installed. 
Have git installed.

git clone https://github.com/Kookierhondje/qt-img-sorter.git
cd qt-img-sorter
python -m venv venv 
pip install -r requirements.txt
python main.py source_dir target_dir skim_dir


The app will only copy files, never delete. 
Takes image files and removes duplicates while giving the user the option to rename each image file. 
Also, allows one to "skim" image files off to a second directory for further sorting. 

Simple, easy, safe, as this QT app only calls shutils.copy2
