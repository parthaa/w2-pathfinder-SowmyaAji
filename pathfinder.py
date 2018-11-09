#!/usr/bin/python3
from PIL import Image, ImageColor
import sys

def get_data(file):
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

def trace_path(data, image, row, column, color = ImageColor.getcolor('cyan', 'RGBA'), total_elevation = 0):
  current_value = data[row][column]
  draw_pixel(image, 255, column, row, color)
  next_row = row
  next_column = column + 1
  if next_column < len(data[0]):
    values = [sys.maxsize] * 3
    if row > 0:
      values[0] = abs(current_value - data[row -1][next_column])

    values[1] = abs(current_value - data[row][next_column])
    if row + 1 < len(data[0]):
      values[2] = abs(current_value - data[row + 1][next_column])
    next_row = row - 1 + values.index(min(values))
    total_elevation += min(values)
    return trace_path(data, image, next_row, next_column, color, total_elevation)
  return total_elevation

def draw_pixel(image, value, x, y, color = ImageColor.getcolor('white', 'RGBA')):
  pixels = list(color[0:3]) + [value]
  image.putpixel((x, y), tuple(pixels))

def main(file = "elevation_small.txt", out = "out.png"):
  data = get_data(file)
  lowest, highest = min_max(data) # 4000
  difference = highest - lowest # 1000

  image = Image.new('RGBA',(len(data[0]),len(data)))
  for y in range(len(data)):
    for x in range(len(data[0])):
      value = int((data[y][x] - lowest) * 255.0 / difference)
      draw_pixel(image, value, x, y)

  elevations = [trace_path(data, image, row, 0) for row in range(len(data))]
  row = elevations.index(min(elevations))
  trace_path(data, image, row, 0, ImageColor.getcolor('red', 'RGBA'))
  image.save(out)

if __name__ == "__main__":
  main()