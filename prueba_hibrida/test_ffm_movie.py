from prueba_moviepy.moviepy_testbench import MoviePyTestBench
from prueba_ffmpeg.ffmpeg_testbench import FFmpegTestBench

tester = MoviePyTestBench()
tester2 = FFmpegTestBench()

tester.cortar_video(
    "PL1PT1_PL3PT2_50M.MP4",
    "prueba_hibrida/corte_mp.mp4",
    start_sec=10,
    end_sec=25
)

tester.cortar_video(
    "PL3PT2_PL1PT1.MP4",
    "prueba_hibrida/corte_mp2.mp4",
    start_sec=10,
    end_sec=25
)

tester2.unir_videos(
    ["prueba_hibrida/corte_mp.mp4", "prueba_hibrida/corte_mp2.mp4"],
    output_path="prueba_hibrida/unido.mp4"
)

tester2.escribir_texto(
    input_path="prueba_hibrida/unido.mp4",
    output_path="prueba_hibrida/unido_texto.mp4",
    texto="Prueba FFmpeg - ProVideos 2025"
)
