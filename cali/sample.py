import cv2
import numpy as np
import os


image_path = "C:\\Users\\admin.H120\\Documents\\git\\linecar_fuji\\cali"
#print(image_path)
#print(os.path.exists(image_path))
image = cv2.imread(image_path + "\\0.jpg",cv2.IMREAD_GRAYSCALE)
#print(image)

cv2.imshow("image",image)
cv2.imwrite(image_path + "\\1.jpg", image)
cv2.waitKey()

cv2.destroyAllWindows()
#print(image.shape)