from PIL import Image
import opensimplex
import random
import numpy as np
import base64
import io

class ImageUtil:

    def generate_image(alpha=0.07):
        arr = np.zeros((100,100,4), dtype=np.uint8)
        R = random.randint(10, 255)
        G = random.randint(10, 255)
        B = random.randint(10, 255)

        opensimplex.random_seed()
        n1 = 0
        for x in range(100):
            n2 = 0
            for y in range(100):
                noise = opensimplex.noise2(n1, n2)
                if round(255 * (noise+1) / 2) > 127:
                    arr[x][y] = [R, G, B, 255]
                else:
                    arr[x][y] = [0, 0, 0, 255]
                    
                n2 += alpha
            n1 += alpha

        data = np.zeros((200,200,4), dtype=np.uint8)
        data[:100, :100] = arr
        data[:100, 100:200] = np.flip(arr, 1)
        data[100:200, :200] = np.flip(data[0:100, :200], 0)

        return Image.fromarray(data, mode='RGBA')

    def convert_image_to_base64(image: Image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def convert_base64_to_image(encoded_img: str):
        return Image.open(io.BytesIO(base64.b64decode(encoded_img)))