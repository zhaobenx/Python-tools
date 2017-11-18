from PIL import Image
import numpy as np

# Refer to https://zhuanlan.zhihu.com/p/31164700


def blender(image_1: np.array, image_2: np.array)-> Image:
    """
    image_1 will be the white, while image_2 on the black background
    """
    image_array = np.full(shape=image_1.shape, fill_value=255, dtype='uint8')
    image_alpha = np.full(shape=image_1.shape, fill_value=1, dtype='uint8')

    image_alpha = 1 - (image_1 - image_2*0.5) / 255
    image_array = image_2*0.5 / image_alpha

    image = Image.fromarray(image_array).convert('LA')
    alpha = Image.fromarray(image_alpha * 255).convert('L')
    image.putalpha(alpha)
    image.show()
    image.save('./output/test-1.png')
    

def main():
    test()


def test():

    image_1 = np.asarray(Image.open('test/test-1.png').convert(mode='L'))
    image_2 = np.asarray(Image.open('test/test-2.png').convert(mode='L'))
    blender(image_1, image_2)


if __name__ == "__main__":
    main()
