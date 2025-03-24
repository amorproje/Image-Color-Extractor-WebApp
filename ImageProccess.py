import numpy as np
from PIL import Image,ImageEnhance


class ImageProccessing():
    def __init__(self,path):
        self.factor = 32
        self.filepath = path


    def get_colors_in_image(self):

        def reduce_brightness_size(img_file):
            size = img_file.size
            width = size[0]
            height = size[1]
            print(size)
            keep = True
            #dividing height and width by 2 until its around 100 and return it .
            while keep:
                width = width / 2
                height = height / 2

                if width < 100:
                    new_w = width
                    new_h = height
                    img2 = img_file.resize(size=(int(new_w), int(new_h)))
                    enhancer = ImageEnhance.Brightness(img2)
                    img2 = enhancer.enhance(0.9)
                    return img2

                elif height < 100:
                    new_w = width
                    new_h = height
                    img2 = img_file.resize(size=(int(new_w), int(new_h)))
                    enhancer = ImageEnhance.Brightness(img2)
                    img2 = enhancer.enhance(0.9)
                    print(img2.size)
                    return img2

        image_file = Image.open(self.filepath)
        rbs = reduce_brightness_size(image_file)

        image_array = np.array(rbs)
        shape = image_array.shape
        x = shape[0]
        y = shape[1]
        hex_list = [] #list of extracted hex colors

        def quantize_color(value, factor=self.factor):
            #reducing the similar colors by operating this to have the top 10 colors with main colors .it combine very similar and near rgb codes.
            return round(value / factor) * factor
        #iterating through every pixel in x and y.
        for x in range(x):
            for y in range(y):
                rgb = image_array[x, y, :]

                # Reduce precision of RGB values
                r = quantize_color(rgb[0], factor=32)  # Rounding to nearest multiple of 16
                g = quantize_color(rgb[1], factor=32)
                b = quantize_color(rgb[2], factor=32)
                rgb_to_hex = "#{:02X}{:02X}{:02X}".format(r,g,b) #converting rgb to hex .

                hex_list.append(rgb_to_hex)
        #measuring the amount of every colors in a dictionary.
        hex_frequency = {}
        for item in hex_list:
            if item in hex_frequency:
                hex_frequency[item] += 1
            else:
                hex_frequency[item] = 1

        sorted_hex_dic = dict(sorted(hex_frequency.items(), key=lambda item: item[1], reverse=True)) #converting dictionary to tupel by .items() and using values of the tuple to compare values and sorting from largest.
        final_list = [a for a in sorted_hex_dic][:10]  # slice 10 most used colors from the list
        print(final_list)

        return final_list

