import os
import glob
import argparse
from PIL import Image, UnidentifiedImageError

formats = ["jpg", "jpeg", "bmp", "png"]


def crop_screenshot(filename: str, dark=False):

    try:
        screen = Image.open(filename)
    except UnidentifiedImageError:
        if args.mode == "single":
            print("Error: The image file is either corrupted or in an unknown format.")
            exit(-1)
        else:
            print("Error: Image file is either corrupted or in an unknown format. Skipping {}...".format(filename))
            return
    except IOError as e:
        if args.mode == "single":
            print("IO Error while opening image: {}".format(str(e)))
            exit(-1)
        else:
            print("IO Error while opening image. Skipping {}...".format(filename))
            return

    width, height = screen.size
    center_line = height // 2
    cropped = None
    filename_original, extension = os.path.splitext(filename)

    color = (0, 0, 0) if dark else (255, 255, 255)

    for y in range(center_line, 0, -1):

        if len([1 for x in range(width) if screen.getpixel((x, y)) == color]) == width:
            cropped = screen.crop((0, y, width, height))
            break
        elif y == 1:
            if args.mode == "single":
                print("Unable to find area to crop. Check your theme option.")
                exit(-1)
            else:
                print("Unable to find area to crop. Skipping {}...".format(filename))
                return

    for y in range(1, height):
        if len([1 for x in range(width) if cropped.getpixel((x, y)) == color]) == width:
            cropped = cropped.crop((0, 0, width, y))
            print("Saving file as " + filename_original + "_cropped" + extension)
            try:
                cropped.save(filename_original + "_cropped" + extension)
            except Exception as e:
                if args.mode == "single":
                    print("Error while saving image: {}".format(str(e)))
                    exit(-1)
                else:
                    print("Error while saving. Skipping {}...".format(filename))
                    return
            break
        elif y == height-1:
            if args.mode == "single":
                print("Unable to find area to crop. Check your theme option.")
                exit(-1)
            else:
                print("Unable to find area to crop. Skipping {}...".format(filename))
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically crops your instagram screenshots")
    parser.add_argument("mode", type=str, choices=["all", "single"], help="\"all\" processes all files in the current directory. \"single\" processes a single file specified by the \"--file\" option.")
    parser.add_argument("--file", type=str, help="the file to process. Ignored if not using single mode.")
    parser.add_argument("--theme", choices=["light", "dark"], help="specifies the instagram theme used.")
    args = parser.parse_args()
    if args.mode == "single" and args.file is None:
        print("Error: Please specify a file")
        exit(-1)
    elif args.mode == "single" and not os.path.isfile(args.file):
        print("Error: File \"{0}\" not found or inaccessible".format(args.file))

    if args.mode == "single":
        crop_screenshot(args.file, args.theme == "dark")
    elif args.mode == "all":
        files = [file for ext in [glob.glob("*." + g) for g in formats] for file in ext]    # get all files in valid image formats
        for file in files:
            crop_screenshot(file, args.theme == "dark")
