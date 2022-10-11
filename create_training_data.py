import cv2 as cv
import pyautogui
import numpy as np
import keyboard
import string
import random
from time import sleep


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
    dim=(28,28)

    for n in range(0,10,1):
        for d in range(0,1,1):
            print(f'Zahl: {n} \nAnzahl: {d}')
            # create np array with a size of max windows resolution
            y = np.zeros([screenHeight,screenWidth,3],dtype=np.uint8)
            # make array image black
            pic = np.full_like(y,[0,0,0])
            while not keyboard.is_pressed('esc'):
                # get mouse position
                mouseX, mouseY = pyautogui.position()
                #print(mouseX,mouseY)
                # make the drawing lines bigger
                for i in range(-5,5):
                    pic[mouseY ,mouseX + i] = [255,255,255]
                    pic[mouseY + i, mouseX] = [255,255,255]
                      
            sleep(0.1)
            # find min and max of each axis(x,y)
            min_y,max_y,min_x,max_x = find_minmax(pic)
            picresized = pic[min_y:max_y,min_x:max_x]
            picresized = cv.resize(picresized,dim)
            randomstring = ''.join(random.choices(string.ascii_lowercase,k=8))
            #print(f"create file {n}/{d}{randomstring}.png")
            #cv.imwrite(f'./{n}/{d}{randomstring}.png',picresized)
            print(f"create file Test/{d}{randomstring}.png")
            cv.imwrite(f'./Test/{d}{randomstring}.png',picresized)
        


if __name__ == '__main__':
    main()