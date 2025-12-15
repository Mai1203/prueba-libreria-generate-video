from moviepy_testbench import MoviePyTestBench

tester = MoviePyTestBench()

# 1. Prueba corte
tester.cortar_video(
    "../PL1PT1_PL3PT2_50M.MP4",
    "corte_mp.mp4",
    start_sec=10,
    end_sec=25
)

tester.cortar_video(
    "../PL3PT2_PL1PT1.MP4",
    "corte_mp2.mp4",
    start_sec=10,
    end_sec=25
)

# 2. Prueba unión
tester.unir_videos(
    ["corte_mp.mp4", "corte_mp2.mp4"],
    "unido_mp.mp4"
)

# 3. Prueba texto
tester.escribir_texto(
    "unido_mp.mp4",
    "texto_mp.mp4",
    "Prueba OpenCV - ProVideos 2025"
)
