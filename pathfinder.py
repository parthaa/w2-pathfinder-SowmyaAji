#!/usr/bin/python3
from PIL import Image

def getData(file):
  return [[int(item) for item in line.strip().split()] for line in open(file).readlines()]

def min_max(d2array):
  largest = d2array[0][0]
  smallest = d2array[0][0]
  for row in d2array:
    for column in row:
      if largest < column:
        largest = column
      if smallest > column:
        smallest = column
  return (smallest, largest)

def draw_pixel(image, value, x, y):
  image.putpixel((x, y), (255,255,255, value))

def main(file = "elevation_small.txt", out = "out.png"):
  data = getData(file)
  lowest, greatest = min_max(data) # 4000
  difference = greatest - lowest # 1000

  image = Image.new('RGBA',(len(data[0]),len(data)))
  for y in range(len(data)):
    for x in range(len(data[0])):
      value = int((data[y][x] - lowest) * 255.0 / difference)
      draw_pixel(image, value, x, y)
  image.save(out)

if __name__ == "__main__":
  main()