from pos_detect import data
from sym_detect import symbol
import cv2

cut, pos = data('board.png')[3]
cv2.imwrite('cut.png', cut)
print(symbol(cut), pos)
