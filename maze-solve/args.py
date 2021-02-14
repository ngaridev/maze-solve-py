import argparse

my_parser = argparse.ArgumentParser(description="Solve a maze file in png format")
my_parser.add_argument("Image",
                       metavar='image',
                       type=str,
                       help="directory of the image file")

my_parser.add_argument("Save",
                       metavar='save',
                       type=str,
                       help="Save Location of the solved maze")
my_parser.add_argument("-s",
                       "--show",
                       action="store_true",
                       help="Show the final image")
args = my_parser.parse_args()