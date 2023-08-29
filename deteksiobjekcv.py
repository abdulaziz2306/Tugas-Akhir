from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import keyboard

# Fungsi untuk menutup program ketika tombol "q" ditekan
def on_key_release(key):
    if key.name == 'q':
        global stop_program
        stop_program = True

# Inisialisasi detektor objek dengan model SSD MobileNetV2
net = detectNet("ssd-mobilenet-v2", threshold=0.5)

# Inisialisasi video source dari kamera CSI
camera = videoSource("/dev/192.168.1.8/stream")

# Inisialisasi video output untuk tampilan
display = videoOutput("display://0")

# Daftarkan fungsi on_key_release() sebagai callback saat tombol ditekan
keyboard.on_release(on_key_release)

stop_program = False
count_blue_line = 0  # Jumlah objek manusia yang melintasi garis biru
count_red_line = 0  # Jumlah objek manusia yang melintasi garis merah

# Tentukan posisi garis biru dan merah
blue_line_position = int(camera.GetHeight() / 2), 50  # Koordinat garis biru (y, x)
red_line_position = int(camera.GetHeight() / 2), camera.GetWidth() - 50  # Koordinat garis merah (y, x)

try:
    while display.IsStreaming() and not stop_program:
        # Ambil frame dari kamera
        img = camera.Capture()

        if img is None:  # Timeout pengambilan frame
            continue

        # Deteksi objek pada frame menggunakan model
        detections = net.Detect(img)

        # Reset jumlah objek manusia yang melintasi garis menjadi 0
        count_blue_line = 0
        count_red_line = 0

        # Loop melalui setiap deteksi objek
        for detection in detections:
            # Periksa jika objek yang terdeteksi adalah manusia
            if net.GetClassDesc(detection.ClassID) == "person":
                if detection.Center[1] < blue_line_position[1]:  # Melewati garis biru
                    count_blue_line += 1
                elif detection.Center[1] > red_line_position[1]:  # Melewati garis merah
                    count_red_line += 1

            # Render bounding box dan label objek
            detection.RenderOverlay(img)

        # Render frame dengan bounding box dan label objek
        display.Render(img)

        # Tampilkan jumlah objek yang melintasi garis biru dan merah pada tampilan
        display.SetStatus("Object Detection | Network {:.0f} FPS | Blue Line: {} | Red Line: {}".format(
            net.GetNetworkFPS(), count_blue_line, count_red_line))

finally:
    # Tutup program dengan membersihkan sumber daya
    display.Close()
    camera.Close()
    keyboard.unhook_all()

