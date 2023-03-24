import base64

with open('flag2/Morocco – angielski.svg', 'rb') as image_file:
    encode_string = base64.b64encode(image_file.read())
    print(encode_string)