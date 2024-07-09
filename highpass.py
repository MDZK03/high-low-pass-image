import numpy as np
import cv2
from tkinter import Tk, filedialog
def hpmain():
    def select_image():
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path:
            image = cv2.imread(file_path)
            return image
        else:
            return None

    # read input and convert to grayscale
    img = select_image()
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # do dft saving as complex output
    dft = np.fft.fft2(gimg, axes=(0,1))

    # apply shift of origin to center of image
    dft_shift = np.fft.fftshift(dft)

    # generate spectrum from magnitude image (for viewing only)
    mag = np.abs(dft_shift)
    spec = np.log(mag) / 20

    # create white circle mask on black background and invert so black circle on white background
    radius = 32
    mask = np.zeros_like(gimg)
    cy = mask.shape[0] // 2
    cx = mask.shape[1] // 2
    cv2.circle(mask, (cx,cy), radius, (255,255,255), -1)[0]
    mask = 255 - mask

    # blur the mask
    mask2 = cv2.GaussianBlur(mask, (19,19), 0)

    # apply mask to dft_shift
    dft_shift_masked = np.multiply(dft_shift,mask) / 255
    dft_shift_masked2 = np.multiply(dft_shift,mask2) / 255

    # shift origin from center to upper left corner
    back_ishift = np.fft.ifftshift(dft_shift)
    back_ishift_masked = np.fft.ifftshift(dft_shift_masked)
    back_ishift_masked2 = np.fft.ifftshift(dft_shift_masked2)

    # do idft saving as complex output
    gimg_back = np.fft.ifft2(back_ishift, axes=(0,1))
    gimg_filtered = np.fft.ifft2(back_ishift_masked, axes=(0,1))
    gimg_filtered2 = np.fft.ifft2(back_ishift_masked2, axes=(0,1))

    # combine complex real and imaginary components to form (the magnitude for) the original image again multiply by 3 to increase brightness
    gimg_back = np.abs(gimg_back).clip(0,255).astype(np.uint8)
    gimg_filtered = np.abs(3*gimg_filtered).clip(0,255).astype(np.uint8)
    gimg_filtered2 = np.abs(3*gimg_filtered2).clip(0,255).astype(np.uint8)

    cv2.imshow("ORIGINAL", gimg)
    cv2.imshow("FILTERED", gimg_filtered)
    cv2.waitKey(0)
    cv2.destroyAllWindows()