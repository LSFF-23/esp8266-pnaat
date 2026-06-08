import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

def show_images(images, titles, cmap=None, figsize=(15,5)):
    """Helper function to display images side by side"""
    plt.figure(figsize=figsize)
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, len(images), i+1)
        if len(img.shape) == 2:  # If it is grayscale
            plt.imshow(img, cmap=cmap if cmap else 'gray')
        else:  # If it is color (BGR → RGB)
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis("off")
    plt.show()

# --- Fetching Image ---
url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/baboon.jpg?"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
img = cv2.imdecode(image, cv2.IMREAD_COLOR)

# Displaying to test
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# --- Smoothing filters and edge detection ---

# 1. Mean Filter (Blur)
blur = cv2.blur(img, (5,5))

# 2. Gaussian Filter
gaussian = cv2.GaussianBlur(img, (5,5), 0)

# 3. Conversion to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4. Sobel Filter
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
sobel = cv2.magnitude(sobelx, sobely)
#sobel = np.uint8(np.clip(sobel, 0, 255)) # Scale and convert back to 8-bit

# 5. Canny Edge Detector
canny = cv2.Canny(gray, 100, 200)

show_images([blur, gaussian, sobel, canny],
            ["Mean (Blur)", "Gaussian", "Sobel", "Canny"])

# --- Image Segmentation ---

# 1.1. Simple Thresholding
ret, thresh_bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 1.2. Adaptive Thresholding
thresh_adapt = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11, 2
)

show_images(
    [gray, thresh_bin, thresh_adapt],
    ["Original (Gray)", "Binary Threshold", "Adaptive Threshold"]
)

# 2. K-means Segmentation
Z = img.reshape((-1, 3))
Z = np.float32(Z)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3  
_, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

centers = np.uint8(centers)
segmented = centers[labels.flatten()].reshape(img.shape)

show_images(
    [img, segmented],
    ["Original Image", "K-means Segmentation (K=3)"]
)

# --- Feature Extraction ---

# 1. Corner Detection (Shi-Tomasi)
corners = cv2.goodFeaturesToTrack(gray,
                                  maxCorners=100,
                                  qualityLevel=0.01,
                                  minDistance=10)
corners = np.int64(corners) # Fixed deprecated np.int0

img_corners = img.copy()
for c in corners:
    x, y = c.ravel()
    cv2.circle(img_corners, (int(x), int(y)), 4, (0, 0, 255), -1)  # Red circle (BGR format)

# 2. ORB (Oriented FAST and Rotated BRIEF)
orb = cv2.ORB_create()
kp, des = orb.detectAndCompute(gray, None)

img_orb = cv2.drawKeypoints(img, kp, None,
                            color=(0, 255, 0),   # Green
                            flags=0)

show_images([img_corners, img_orb],
            ["Corners (Shi-Tomasi)", "Keypoints (ORB)"])