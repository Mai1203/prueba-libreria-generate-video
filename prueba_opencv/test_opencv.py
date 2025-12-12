from opencv_testbench import OpenCVTestBench

tester = OpenCVTestBench()

# 1. Prueba corte
tester.cortar_video(
    "../PL1PT1_PL3PT2_50M.MP4",
    "corte_cv.mp4",
    start_sec=10,
    end_sec=25
)

tester.cortar_video(
    "../PL3PT2_PL1PT1.MP4",
    "corte_cv2.mp4",
    start_sec=10,
    end_sec=25
)

# 2. Prueba unión
tester.unir_videos(
    ["corte_cv.mp4", "corte_cv2.mp4"],
    "unido_cv.mp4"
)

# 3. Prueba texto
tester.escribir_texto(
    "unido_cv.mp4",
    "texto_cv.mp4",
    "Prueba OpenCV - ProVideos 2025"
)
