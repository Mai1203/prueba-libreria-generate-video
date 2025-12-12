import cv2
import time
import os


class OpenCVTestBench:

    def __init__(self):
        pass

    # -----------------------------------------------------------
    # UTILIDAD: Obtener tamaño de archivo
    # -----------------------------------------------------------
    def get_file_size_mb(self, path):
        if not os.path.exists(path):
            return 0
        return os.path.getsize(path) / (1024 * 1024)

    # -----------------------------------------------------------
    # UTILIDAD: Escribir info del resultado
    # -----------------------------------------------------------
    def show_results(self, output_path, start_time):
        end = time.time()
        duracion = end - start_time
        size_mb = self.get_file_size_mb(output_path)

        print("\n============== RESULTADO (OpenCV) ==============")
        print(f"Archivo generado: {output_path}")
        print(f"Duración del proceso: {duracion:.2f} segundos")
        print(f"Tamaño final: {size_mb:.2f} MB")
        print("==============================================\n")

        return {
            "time": duracion,
            "size_mb": size_mb
        }

    # -----------------------------------------------------------
    # 1. RECORTAR VIDEO CON OPENCV
    # -----------------------------------------------------------
    def cortar_video(self, input_path, output_path, start_sec, end_sec):
        print(">>> OpenCV: Cortando video...\n")
        start_time = time.time()

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("Error: No se pudo abrir el video.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = int(cap.get(3))
        height = int(cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        start_frame = int(start_sec * fps)
        end_frame   = int(end_sec * fps)

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        curr_frame = start_frame

        while cap.isOpened() and curr_frame < end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            curr_frame += 1

        cap.release()
        out.release()

        return self.show_results(output_path, start_time)

    # -----------------------------------------------------------
    # 2. UNIR VIDEOS CON OPENCV (RENDERIZACIÓN COMPLETA)
    # -----------------------------------------------------------
    def unir_videos(self, lista_videos, output_path):
        print(">>> OpenCV: Uniendo videos...\n")
        start_time = time.time()

        # Tomamos propiedades del primer video
        cap0 = cv2.VideoCapture(lista_videos[0])
        fps = cap0.get(cv2.CAP_PROP_FPS)
        width  = int(cap0.get(3))
        height = int(cap0.get(4))
        cap0.release()

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for video in lista_videos:
            print(f"  - Procesando {video}")
            cap = cv2.VideoCapture(video)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            cap.release()

        out.release()

        return self.show_results(output_path, start_time)

    # -----------------------------------------------------------
    # 3. ESCRIBIR TEXTO SOBRE EL VIDEO
    # -----------------------------------------------------------
    def escribir_texto(self, input_path, output_path, texto):
        print(">>> OpenCV: Escribiendo texto en el video...\n")
        start_time = time.time()

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("Error: No se pudo abrir el video.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = int(cap.get(3))
        height = int(cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Agregar texto
            cv2.putText(
                frame,
                texto,
                (50, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255,255,255),
                4,
                cv2.LINE_AA
            )

            out.write(frame)

        cap.release()
        out.release()

        return self.show_results(output_path, start_time)
