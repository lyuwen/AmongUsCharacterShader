import os
import yaml
import numpy as np
from PIL import Image
import matplotlib as mpl


def get_colored_character(texturefile, bodycolor, shadedbodycolor, visorcolor):
  img = Image.open(texturefile)
  arr = np.array(img)

  r = arr[:, :, 0].copy() / 255
  g = arr[:, :, 1].copy() / 255
  b = arr[:, :, 2].copy() / 255
  a = arr[:, :, 3].copy()

  allchannels = r + g + b
  mask = np.min([np.min([b, g], axis=0), allchannels], axis=0)

  brightMask = r - mask
  shadowMask = b - mask
  visorMask  = g - mask

  result = np.zeros(arr.shape)

  result += brightMask[:, :, np.newaxis] * bodycolor[np.newaxis, np.newaxis, :]
  result += shadowMask[:, :, np.newaxis] * shadedbodycolor[np.newaxis, np.newaxis, :]
  result += visorMask[:, :, np.newaxis]  * visorcolor[np.newaxis, np.newaxis, :]
  result += mask[:, :, np.newaxis] * 255
  result[:, :, 3] = a

  result = result.astype("uint8")
  return result


def save_image(imgarray, filename):
  new_img = Image.fromarray(imgarray)
  new_img.save(filename)


def main():
  colorfile = "assets/colors.yml"
  texturefile = "assets/Player.png"
  output_dir = "output"
  output_format = "player_{}.png"

  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  colors = yaml.load(open(colorfile, "r"), Loader=yaml.SafeLoader)

  visorcolor_hex = colors["visor_color"]
  visorcolor = np.array(mpl.colors.to_rgba(visorcolor_hex)) * 255

  for colorname in colors["body_colors"].keys():
    print("Processing color:", colorname, "...")
    bodycolor_hex = colors["body_colors"][colorname]["bright"]
    shadedbodycolor_hex = colors["body_colors"][colorname]["shaded"]

    bodycolor = np.array(mpl.colors.to_rgba(bodycolor_hex)) * 255
    shadedbodycolor = np.array(mpl.colors.to_rgba(shadedbodycolor_hex)) * 255

    img = get_colored_character(
        texturefile=texturefile,
        bodycolor=bodycolor,
        shadedbodycolor=shadedbodycolor,
        visorcolor=visorcolor,
        )

    save_image(
        imgarray=img,
        filename=os.path.join(output_dir, output_format.format(colorname)),
        )


if __name__ == "__main__":
  main()
