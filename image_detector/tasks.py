import os
from skimage import io
from django.conf import settings
from django.core.files import File
from celery import shared_task, current_task

from .libs.image_forgery_detector.blockartifactgrid import BlockArtifactGrid
from .models import Detection


def report_progress(progress):
    current_task.update_state(state='PROGRESS', meta={'progress': progress})


def save_result(result, detection):
    result_dir_path = os.path.join(settings.BASE_DIR, f"{settings.MEDIA_ROOT}/result")
    result_path = f"{result_dir_path}/result_{detection.id}.jpg"
    io.imsave(result_path, result)
    saved_result_img = open(result_path, "rb")
    saved_result_file = File(saved_result_img)

    detection.result_img.save(
        f"result_{detection.id}.jpg",
        saved_result_file,
        save=True
    )

    return 1


@shared_task(bind=True)
def detect_image(self, image_path, detection_id):
    detection = Detection.objects.get(pk=detection_id)
    image = io.imread(image_path)
    img_detector = BlockArtifactGrid(image)
    img_detector.detect(report_progress)

    return save_result(img_detector.result_image, detection)
