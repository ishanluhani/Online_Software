from tkinter.filedialog import askopenfilename
import cv2
import zxingcpp

img = cv2.imread(askopenfilename())
results = zxingcpp.read_barcodes(img)
for result in results:
	print("Found barcode:\n Text:    '{}'\n Format:   {}\n Position: {}"
		.format(result.text, result.format, result.position))
if len(results) == 0:
	print("Could not find any barcode.")