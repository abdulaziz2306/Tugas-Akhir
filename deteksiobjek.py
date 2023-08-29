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
camera = videoSource("/dev/video0")

# Inisialisasi video output untuk tampilan
display = videoOutput("display://0")

# Daftarkan fungsi on_key_release() sebagai callback saat tombol ditekan
keyboard.on_release(on_key_release)

stop_program = False
count_human = 0

try:
    while display.IsStreaming() and not stop_program:
        # Ambil frame dari kamera
        img = camera.Capture()

        if img is None: # Timeout pengambilan frame
            continue

        # Deteksi objek pada frame menggunakan model
        detections = net.Detect(img)


	#loop hitung objek manusia
	for detection in detections:
		if detecion.ClassID == net.GetClassDesc("person"):
		   count_human += 1 #menambahkan jumlah manusia

        # Render frame dengan bounding box dan label objek
        display.Render(img)

        # Set status dengan jumlah frame per detik (FPS) model
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

finally:
    # Tutup program dengan membersihkan sumber daya
    display.Close()
    camera.Close()
    keyboard.unhook_all()

