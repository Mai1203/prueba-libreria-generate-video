import time
import os
from moviepy import (
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip
)


class MoviePyTestBench:

    # -----------------------------------------------------------
    # UTILIDAD: Obtener tamaño de archivo
    # -----------------------------------------------------------
    def get_file_size_mb(self, path):
        if not os.path.exists(path):
            return 0
        return os.path.getsize(path) / (1024 * 1024)

    # -----------------------------------------------------------
    # UTILIDAD: Mostrar resultados
    # -----------------------------------------------------------
    def show_results(self, output_path, start_time):
        end = time.time()
        duracion = end - start_time
        size_mb = self.get_file_size_mb(output_path)

        print("\n============== RESULTADO (MoviePy) ==============")
        print(f"Archivo generado: {output_path}")
        print(f"Duración del proceso: {duracion:.2f} segundos")
        print(f"Tamaño final: {size_mb:.2f} MB")
        print("===============================================\n")

        return {
            "time": duracion,
            "size_mb": size_mb
        }

    # -----------------------------------------------------------
    # 1. CORTAR VIDEO
    # -----------------------------------------------------------
    def cortar_video(self, input_path, output_path, start_sec, end_sec):
        print(">>> MoviePy: Cortando video...\n")
        start_time = time.time()

        clip = VideoFileClip(input_path)[start_sec:end_sec]
        
        assert clip is not None
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=os.cpu_count(),
            logger=None
        )

        clip.close()

        return self.show_results(output_path, start_time)

    # -----------------------------------------------------------
    # 2. UNIR VIDEOS
    # -----------------------------------------------------------
    def unir_videos(self, lista_videos, output_path):
        print(">>> MoviePy: Uniendo videos...\n")
        start_time = time.time()

        clips = [VideoFileClip(v) for v in lista_videos]

        final_clip = concatenate_videoclips(
            clips,
            method="compose"
        )

        final_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=os.cpu_count(),
            logger=None
        )

        for c in clips:
            c.close()
        final_clip.close()

        return self.show_results(output_path, start_time)

    # -----------------------------------------------------------
    # 3. ESCRIBIR TEXTO SOBRE EL VIDEO
    # -----------------------------------------------------------
    def escribir_texto(self, input_path, output_path, texto):
        print(">>> MoviePy: Escribiendo texto en el video...\n")
        start_time = time.time()

        video = VideoFileClip(input_path)

        txt = TextClip(
            text=texto,          # 👈 CLAVE
            font_size=60,
            color="white",
            method="caption",
            size=video.size
        )

        txt = txt.with_position((50, 50))
        txt = txt.with_duration(video.duration)

        final = CompositeVideoClip([video, txt])
        assert final is not None

        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=os.cpu_count(),
            logger=None
        )

        video.close()
        final.close()

        return self.show_results(output_path, start_time)
