import io

from numpy import ndarray
from PIL import Image

from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array


def pre_process(image_data: bytes) -> ndarray:
    """Convert an image to RGB,
    resize to 224 x 224,
    and reshape it for the MobileNet V1 model
    """
    with Image.open(io.BytesIO(image_data)) as image:
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = image.resize((224, 224,))
        # Convert the PIL image to a 3D numpy array
        # with 3 color channels and values in the range [0, 255]
        image = img_to_array(image)
        # Prepend a dimension of 1: the classifier expects a list of samples
        image = image.reshape(1, *image.shape,)
        # Scale the pixel values in the range [-1, 1], sample-wise
        image = preprocess_input(image)

    return image