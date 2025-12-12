from ffmpeg_testbench import FFmpegTestBench

tester = FFmpegTestBench()

# 1. PRUEBA DE CORTE
tester.cortar_video(
    input_path="../PL1PT1_PL3PT2_50M.MP4",
    output_path="corte.mp4",
    start=5,
    end=35
)

tester.cortar_video(
    input_path="../PL3PT2_PL1PT1.MP4",
    output_path="corte2.mp4",
    start=5,
    end=35
)

# 2. PRUEBA DE UNION
tester.unir_videos(
    ["corte.mp4", "corte2.mp4"],
    output_path="unido.mp4"
)

# 3. PRUEBA DE TEXTO
tester.escribir_texto(
    input_path="unido.mp4",
    output_path="unido_texto.mp4",
    texto="Prueba FFmpeg - ProVideos 2025"
)
