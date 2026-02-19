import cv2

# Membaca gambar
image = cv2.imread("foto1.jpg")

if image is not None:
    resized = cv2.resize(image, (300, 200))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    cv2.imwrite("opencv_gray.jpg", gray)
    cv2.imwrite("opencv_edges.jpg", edges)
else:
    print("Gambar tidak ditemukan")

import cv2

cap = cv2.VideoCapture("Jadoo.mp4")

if not cap.isOpened():
    print("Video tidak bisa dibuka")
    exit()

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(
    "opencv_result.avi",
    fourcc,
    fps if fps > 0 else 20,
    (width, height),
    False
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 👉 TAMPILKAN VIDEO
    cv2.imshow("OpenCV Video - Grayscale", gray)

    # 👉 SIMPAN VIDEO
    out.write(gray)

    # Tekan Q untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
