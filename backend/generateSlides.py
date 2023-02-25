from PIL import Image
from collections import namedtuple, OrderedDict
import cv2
import datetime
import numpy as np
import pytesseract
from difflib import SequenceMatcher


def generate_slides(video_file):
    #video_file = '../Chen.mp4'
    text_from_slides_file = './uploads/textFromSlides.txt'
    video_capture = cv2.VideoCapture(video_file)

    count = 0
    frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f"duration in seconds: {seconds}")
    print(f"video time: {video_time}")


    def extract_text(image):
        #https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
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

        if len(text_extracted) == 0 or (len(text_extracted) == 1 and text_extracted[0] == ''):
            return []
        return text_extracted


    # get Mean Squared Error between two images' pixel values
    def is_image_similar(image1_name, image2_name):
        img1 = cv2.imread(image1_name)
        img2 = cv2.imread(image2_name)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff ** 2)
        mse = err / (float(h * w))

        # initial 2.5
        return mse < 2.5


    def is_text_similar(arr1, arr2):
        similarity_average = 0
        min_len = min(len(arr1), len(arr2))

        for i in range(min_len):
            similarity_average += SequenceMatcher(None, arr1[i], arr2[i]).ratio()

        # initial 0.5
        return similarity_average / min_len > 0.5


    # slides: {nameOfFile: Pair([arr of extracted texts], [startTime, endTime])]}
    slides = OrderedDict()
    Pair = namedtuple("Pair", ["text", "time"])
    # slides: stack of nameOfFiles to keep track of lastly added text
    slides_stack = []

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if ret:
            # get a frame every 10 seconds
            image_name = 'frame{:d}.jpg'.format(count)
            cv2.imwrite(image_name, frame)
            seconds = fps * count
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, seconds)

            # extract image and add it to slides
            extracted_text = extract_text(cv2.imread(image_name))

            if len(extracted_text) > 0:
                if len(slides_stack) == 0:
                    slides[count] = Pair(extracted_text, [0, count])
                    slides_stack.append(count)
                else:
                    last_slide_added = slides_stack.pop(-1)
                    last_image_name = 'frame{:d}.jpg'.format(last_slide_added)
                    if is_image_similar(last_image_name, image_name) or is_text_similar(extracted_text, slides[last_slide_added].text):
                        slides_stack.append(count)
                        slides[count] = Pair(extracted_text, [slides[last_slide_added].time[0], count])
                        slides.pop(last_slide_added)
                    else:
                        slides[count] = Pair(extracted_text, [slides[last_slide_added].time[1], count])
                        slides_stack.append(count)

            count += 30
        else:
            video_capture.release()
            break

    # iterate through the slides and create a pdf file of slides
    images = [
        Image.open('frame{:d}.jpg'.format(id))
        for id in slides
    ]

    pdf_path = "uploads/slides.pdf"
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )

    # print text extracted from slides
    open(text_from_slides_file, 'w').close()
    with open(text_from_slides_file, 'a') as f:
        for id in slides:
            start_min, start_sec = divmod(slides[id].time[0], 60)
            start_hour, start_min = divmod(start_min, 60)

            end_min, end_sec = divmod(slides[id].time[1], 60)
            end_hour, end_min = divmod(end_min, 60)

            f.write('Time Stamp: {:d}:{:02d}:{:02d}-'.format(start_hour, start_min, start_sec))
            f.write('{:d}:{:02d}:{:02d}\n'.format(end_hour, end_min, end_sec))
            for slide in slides[id].text:
                f.write(slide)
            f.write("\n\n")

