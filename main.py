import json
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QFileDialog, QVBoxLayout
from PIL import Image
import pytesseract
import numpy as np
import cv2
from json import JSONEncoder


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        
        self.text = QLabel("Freelancer Job Bid Extractor")
        self.button = QPushButton("Upload Images!")
        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.upload_images)
        
        
    def dump_to_json(self, data):
        

        # print(type(data))
        
        dict_data = { "data": data}
        
        json_string = json.dumps(dict_data, indent=2)
        
        # print(json_string)
        # print(type(json_string))
        

        with open("image_text.json", 'a') as f:
            f.write(json_string)
        
    @QtCore.Slot()
    def upload_images(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open File", "Image Files (*.png *.jpg *.jpeg)")
        
        
        for path in paths:
            og_img = cv2.imread(path)
            
            gray = cv2.cvtColor(og_img, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5,5), 1.5)

            thresh, img_bw = cv2.threshold(blur, 150, 200, cv2.THRESH_BINARY)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

            dilate = cv2.dilate(img_bw, kernel, iterations=1)

            contours, hierarchy = cv2.findContours(dilate, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

            # Extract text from each contourf
            for cnt in filtered_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(og_img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw bounding box

                text = pytesseract.image_to_string(og_img)
                                
                self.dump_to_json(text) 
                
        # # Display the image
        # for i in path:
        #     img = cv2.imread(i)

        #     cv2.imshow('Image', img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
                
                
if __name__=="__main__":
    
    app = QApplication([])
    
    widget = MyApp()
    
    widget.resize(800, 600)
    widget.show()
    
    
    sys.exit(app.exec())
    
    
    
    
# upload to json
# Then learn what to do
