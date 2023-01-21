import cv2
import datetime
import numpy as np
import pytesseract
from difflib import SequenceMatcher

video_file = '../shortVideo.mp4'
video_capture = cv2.VideoCapture(video_file)
success, image = video_capture.read()

count = 0
frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
fps = video_capture.get(cv2.CAP_PROP_FPS)

# calculate duration of the video
seconds = round(frames / fps)
video_time = datetime.timedelta(seconds=seconds)
print(f"duration in seconds: {seconds}")
print(f"video time: {video_time}")


def extract_text(image):
    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file

    text_extracted = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Cropping the text block for giving input to OCR
        cropped = image[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        text_extracted.append(text)

    return text_extracted


def is_similar(image1, image2):
    return image1.shape == image2.shape and not (np.bitwise_xor(image1, image2).any())

def get_similarity(arr1, arr2):
    similarity_average = 0
    min_len = min(len(arr1), len(arr2))

    for i in min_len:
        similarity_average += SequenceMatcher(None, arr1[i], arr2[i]).ratio()

    return similarity_average / min_len

slides = {}

while video_capture.isOpened():
    ret, frame = video_capture.read()

    if ret:
        # get a frame every 10 seconds
        image_name = 'frame{:d}.jpg'.format(count)
        cv2.imwrite(image_name, frame)
        seconds = fps * count
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, seconds)
        count += 10

        # extract image and add it to slides
        extracted_text = extract_text(cv2.imread(image_name))
        print(extracted_text)
        if len(extracted_text) > 0:
            if len(slides) == 0:
                slides[image_name] = extracted_text
            else:
                print(slides)


    else:
        video_capture.release()
        break
