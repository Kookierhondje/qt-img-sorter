from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
)
import os
import shutil
import hashlib
import sys
    # We want this program to:
    # Take a directory, toll through the directory for images, for each image show the image, and then save the image to the target dir.
    # images should not be saved if they already exist in the target dir
    # images should be skipped if they are the same as an image in the directory. 
    # Each image is shown and then renamed as the user directs. 
def scrape_images_from_dir(fdir):
    exts = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff', '.webp'}
    return [os.path.join(fdir, f) for f in os.listdir(fdir) if os.path.isfile(os.path.join(fdir, f)) and os.path.splitext(f)[1].lower() in exts]

def _fry_hash(file):
    frier = hashlib.sha256()
    with open(file, 'rb') as grill:
        for potato in iter(lambda: grill.read(4096), b''):
            frier.update(potato)
    return frier.hexdigest()

def is_same_file(f1, f2)->bool:
    if _fry_hash(f1) == _fry_hash(f2):
        return True
    else:return False

def is_imagefile_in_list(image, targetlist):
    for f in targetlist:
        if is_same_file(image, f):
            return True
    else:return False
# Example usage:
sourcedir = ""
targetdir = ""
skimdir = ""
class BasicImageApp(QWidget):
    def __init__(self, srcdir, targdir, skimdir, mode=None):
        #Before we even start some QT
        self.sourcedir = srcdir
        self.targdir = targdir
        self.skimdir =skimdir
        self.targs  = scrape_images_from_dir(targdir)
        self.source = [i for i in scrape_images_from_dir(srcdir) if not is_imagefile_in_list(i, self.targs)]
        self.dealt = []
        self.ss = 0
        super().__init__()
        self.setWindowTitle("Image Sorter")
        # Image display
        self.image_label = QLabel()
#        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(800, 800)
        # Load a placeholder image (you can replace this path)
#        pixmap.fill(Qt.lightGray)
        # Text field
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text here...")
        # Buttons (no functionality)
        skim_button = QPushButton("Skim")
        save_button = QPushButton("Save")
#        button3 = QPushButton("Button 3")
        # Layout setup
        button_layout = QHBoxLayout()
        button_layout.addWidget(skim_button)
        button_layout.addWidget(save_button)
#        button_layout.addWidget(button3)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.text_input)
        main_layout.addLayout(button_layout)
        save_button.clicked.connect(self.save_button)
        skim_button.clicked.connect(self.save_to_skim_bin)
        self.setLayout(main_layout)
        self.loadimg()
    
    def current_img(self):
        return self.source[self.ss]
    def loadimg(self):
        self.image_label.clear()
        self.text_input.clear()
        imgpath = self.current_img()
        # Check if we've already dealt with the image, if we have, skip it.
        if _fry_hash(imgpath) in self.dealt:
            print(imgpath + " is a copy")
            self.ss = self.ss + 1
            self.loadimg()
        pixmap = QPixmap(imgpath)
        self.image_label.setPixmap(pixmap.scaled(
        self.image_label.width(),
        self.image_label.height(),
        Qt.AspectRatioMode.KeepAspectRatio))
        self.text_input.setPlaceholderText(imgpath.replace(self.sourcedir, ""))
        self.ext = imgpath.split('.')[1]

    def save_button(self):
        if not self.text_input.text():
            print("Default needed!")
            final = self.text_input.placeholderText()
            print(f"Chose: {final}")
        else:
            final = f'{self.text_input.text()}.{self.ext}'
        shutil.copy2(self.current_img(), os.path.join(self.targdir, final))
        self.dealt.append(_fry_hash(self.current_img()))
        self.ss = self.ss + 1
        self.loadimg()

    def save_to_skim_bin(self):
        print("skim milk")
        if not self.text_input.text():
            final = self.text_input.placeholderText()
        final = f'{self.text_input.text()}.{self.ext}'
        shutil.copy2(self.current_img(), os.path.join(self.skimdir, final))
        self.ss = self.ss + 1
        self.loadimg()
# Launch the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicImageApp(sourcedir, targetdir, skimdir)
    window.show()
    sys.exit(app.exec_())
