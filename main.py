from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
)
import argparse
import os
import shutil
import hashlib
import sys
def scrape_images_from_dir(fdir):
    exts = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff', '.webp'}
    return [os.path.join(fdir, f) for f in os.listdir(fdir) if os.path.isfile(os.path.join(fdir, f)) and os.path.splitext(f)[1].lower() in exts]
# hashlib is weird and I'm a bit hungry
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
class ImageSorter(QWidget):
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
        self.image_label = QLabel()
        self.image_label.setFixedSize(800, 800)
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text here...")
        skim_button = QPushButton("Skim")
        save_button = QPushButton("Save")
        button_layout = QHBoxLayout()
        button_layout.addWidget(skim_button)
        button_layout.addWidget(save_button)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.text_input)
        main_layout.addLayout(button_layout)
        save_button.clicked.connect(self.save_button)
        skim_button.clicked.connect(self.save_to_skim_bin)
        self.setLayout(main_layout)
        self.loadimg()
    def current_img(self):
        # honestly I'm not typing this again
        # I could wrap this in a try loop that that catches the index error and exit gracefully
        # But it's funnier that it errors to kill itself
        return self.source[self.ss]
    def loadimg(self):
        self.image_label.clear()
        self.text_input.clear()
        imgpath = self.current_img()
        if _fry_hash(imgpath) in self.dealt:
            print(imgpath + " is a copy")
            self.ss = self.ss + 1
            self.loadimg()
        pixmap = QPixmap(imgpath) # Yeah, pixmap will eat whatever we give it.
        # The fat fuck
        self.image_label.setPixmap(pixmap.scaled(
        self.image_label.width(),
        self.image_label.height(),
        Qt.AspectRatioMode.KeepAspectRatio))
        # Look at him just munch
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
        #print("skim milk")
        if not self.text_input.text():
            final = self.text_input.placeholderText()
        final = f'{self.text_input.text()}.{self.ext}'
        shutil.copy2(self.current_img(), os.path.join(self.skimdir, final))
        self.ss = self.ss + 1
        self.loadimg()

if __name__ == "__main__":
    app = QApplication(sys.argv) # I don't care to look up what QT is doing with my args. I'll handle it myself.
    parser = argparse.ArgumentParser(description="Sync image files to a target folder, usage: main.py source target skim; All directories must exist!!")
    parser.add_argument('source', help="Path to source directory")
    parser.add_argument('target', help="Path to target directory")
    parser.add_argument('skim', help="Path to skim directory")
    args = parser.parse_args()
    window = ImageSorter(args.source, args.target, args.skim)
    window.show()
    sys.exit(app.exec_())
