from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import time

#coba lagi
# Inisialisasi detektor objek dengan model SSD MobileNetV2
net = detectNet("ssd-mobilenet-v2", threshold=0.5)

# Inisialisasi video source dari kamera CSI
camera = videoSource("/dev/video0")

# Inisialisasi video output untuk tampilan
display = videoOutput("display://0")

try:
    # Membuka file untuk menulis data
    with open("data.txt", "w") as file:
        for _ in range(10):  # Loop selama 10 detik
            start_time = time.time()  # Catat waktu awal detik

            # Ambil frame dari kamera
            img = camera.Capture()

            if img is None: # Timeout pengambilan frame
                continue

            # Deteksi objek pada frame menggunakan model
            detections = net.Detect(img)

            # Filter deteksi hanya untuk manusia (classID 1)
            human_detections = [detection for detection in detections if detection.ClassID == 1]

            # Simpan data dalam file
            file.write("Waktu Pengambilan Data: {}\n".format(start_time))
            file.write("Jumlah Manusia Terdeteksi: {}\n".format(len(human_detections)))
            file.write("FPS pada waktu itu: {:.2f}\n".format(net.GetNetworkFPS()))
            file.write("\n")

            # Render frame dengan bounding box dan label objek manusia
            for detection in human_detections:
                net.PrintProfilerTimes() # print the detection profiling info
                display.Render(img)
                display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

            # Tunggu hingga akhir detik
            while time.time() - start_time < 1.0:
                pass

finally:
    # Tutup program dengan membersihkan sumber daya
    display.Close()
    camera.Close()

