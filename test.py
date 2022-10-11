import cv2 as cv
import keyboard
import pyautogui
import numpy as np
import tensorflow as tf
from keras.models import load_model

model = load_model('ownmodel.h5')

def predict_num(img):
    # reshape for model compatibility
    img = img.reshape(1,28,28,3)
    #predicting the class
    img = tf.expand_dims(img[0], 0) # Create a batch
    predictions = model.predict(img)
    score = tf.nn.softmax(predictions[0])

    print(
    "You draw number {} with a {:.2f} percent confidence."
    .format(np.argmax(score), 100 * np.max(score))
    )


def find_minmax(pic):
    # find the min,max of x,y
    colored = np.where(pic != [0,0,0])
    freespace = 10
    min_y = np.amin(colored[0]) - freespace
    max_y = np.amax(colored[0]) + freespace
    min_x = np.amin(colored[1]) - freespace
    max_x = np.amax(colored[1]) + freespace
    
    return min_y,max_y,min_x,max_x
 
def main():
    screenWidth, screenHeight = pyautogui.size()
    prevmouseX = prevmouseY = 0
    firstrun = True
    dim=(28,28)

    # create np array with a size of max windows resolution
    y = np.zeros([screenHeight,screenWidth,3],dtype=np.uint8)
    # make array image black
    pic = np.full_like(y,[0,0,0])
    
    while not keyboard.is_pressed('esc'):
        if firstrun:
            print("Draw your number now and confirm with ESC")
            firstrun=False

        # get mouse position
        mouseX, mouseY = pyautogui.position()
        # make the drawing lines bigger
        for i in range(-5,5):
            pic[mouseY ,mouseX + i] = [255,255,255]
            pic[mouseY + i, mouseX] = [255,255,255]

    cv.imwrite('./original.png',pic)

    # find number and reduce picturesize to a minimum
    min_y,max_y,min_x,max_x = find_minmax(pic)
    picresized = pic[min_y:max_y,min_x:max_x]
    cv.imwrite('./originalcut.png',picresized)

    # resize image to (28,28)
    picresized = cv.resize(picresized,dim)
    cv.imwrite('./resized.png',picresized)

    #predict
    predict_num(picresized)

if __name__ == '__main__':
    main()