import cv2
import imutils  # to resize out image

import pytesseract

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def identify_plate(path):
    print(path)
    image = cv2.imread(path)
    image = imutils.resize(image, width=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # now we will reduce  from noise from our image and make  i8t smooth
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    edged = cv2.Canny(gray, 170, 200)

    # Convert to Grayscale Image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny Edge Detection
    canny_edge = cv2.Canny(gray_image, 170, 200)

    # Find contours based on Edges
    contours, new = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    # cv2.imshow("License Plate Detection", image)
    # cv2.waitKey(0)

    # Initialize license Plate contour and x,y,w,h coordinates
    contour_with_license_plate = None
    license_plate = None
    x = None
    y = None
    w = None
    h = None

    # Find the contour with 4 potential corners and create ROI around it
    for contour in contours:
        # Find Perimeter of contour and it should be a closed contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        if len(approx) == 4:  # see whether it is a Rect
            contour_with_license_plate = approx
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = gray_image[y:y + h, x:x + w]
            break
    (thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow("plate", license_plate)
    # cv2.waitKey(0)

    try:
        # Removing Noise from the detected image, before sending to Tesseract
        license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
        (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)
    except:
        pass

    # Text Recognition
    text = pytesseract.image_to_string(license_plate)
    text = text.replace(" ", "")

    # Draw License Plate and write the Text
    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
    image = cv2.putText(image, text, (x - 100, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # cv2.imshow("License Plate Detection", image)
    # cv2.waitKey(0)
    print("License Plate : ", text)

    return text
