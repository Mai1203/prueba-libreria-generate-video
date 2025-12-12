import subprocess
import time
import os
from pathlib import Path


class FFmpegTestBench:

    def __init__(self):
        self.ffmpeg_cmd = "ffmpeg"

    # -----------------------------------------------------------
    # UTILIDAD: Ejecutar FFmpeg y medir tiempo
    # -----------------------------------------------------------
    def run_ffmpeg(self, args, output_path: str):
        inicio = time.time()

        # ==== EJECUTAR FFmpeg Y MOSTRAR LOGS EN TIEMPO REAL ====
        process = subprocess.Popen(
            [self.ffmpeg_cmd] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        process.wait()

        fin = time.time()
        duracion = fin - inicio

        size_mb = self.get_file_size_mb(output_path)

        print("\n============== RESULTADO ==============")
        print(f"Archivo generado: {output_path}")
        print(f"Duración proceso: {duracion:.2f} segundos")
        print(f"Tamaño final: {size_mb:.2f} MB")
        print("========================================\n")

        return {
            "time": duracion,
            "size_mb": size_mb
        }


    # -----------------------------------------------------------
    def get_file_size_mb(self, path):
        if not os.path.exists(path):
            return 0
        return os.path.getsize(path) / (1024 * 1024)

    # -----------------------------------------------------------
    # 1. RECORTAR VIDEO
    # -----------------------------------------------------------
    def cortar_video(self, input_path: str, output_path: str, start: float, end: float):
        print(">>> Cortando video...\n")
        args = [
            "-y",
            "-ss", str(start),              # SEEK RÁPIDO (ANTES DEL -i)
            "-i", input_path,
            "-t", str(end - start),         # DURACIÓN, no tiempo absoluto
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            output_path
        ]

        return self.run_ffmpeg(args, output_path)

    # -----------------------------------------------------------
    # 2. UNIR VIDEOS
    # -----------------------------------------------------------
    def unir_videos(self, lista_videos, output_path: str):
        print(">>> Uniendo videos...\n")

        # Crear archivo lista temporal
        list_file = "videos_to_concat.txt"
        with open(list_file, "w") as f:
            for v in lista_videos:
                f.write(f"file '{Path(v).as_posix()}'\n")

        args = [
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path
        ]

        result = self.run_ffmpeg(args, output_path)
        os.remove(list_file)
        return result

    # -----------------------------------------------------------
    # 3. ESCRIBIR TEXTO
    # -----------------------------------------------------------
    def escribir_texto(self, input_path: str, output_path: str, texto: str):
        print(">>> Escribiendo texto en el video...\n")

        args = [
            "-y",
            "-i", input_path,
            "-vf",
            f"drawtext=text='{texto}':fontcolor=white:fontsize=48:x=50:y=50:shadowcolor=black:shadowx=2:shadowy=2",
            "-c:a", "copy",
            output_path
        ]

        return self.run_ffmpeg(args, output_path)
