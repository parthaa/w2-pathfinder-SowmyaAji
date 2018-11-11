#!/usr/bin/python3
from PIL import Image, ImageColor
import sys

class PathFinder:
  def __init__(self, file = "elevation_small.txt", out = "out.png"):
    self.file = file
    self.out = out
    self.__parse()
    self.image = Image.new('RGBA',(len(self.data[0]),len(self.data)))

  def __parse(self):
    self.data = [[int(item) for item in line.strip().split()] for line in open(self.file).readlines()]

  def __min_max_elevation(self):
    largest = self.data[0][0]
    smallest = self.data[0][0]
    for row in self.data:
      for column in row:
        if largest < column:
          largest = column
        if smallest > column:
          smallest = column
    return (smallest, largest)

  def draw(self):
    lowest, highest = self.__min_max_elevation() # 4000
    difference = highest - lowest # 1000

    for row in range(len(self.data)):
      for column in range(len(self.data[0])):
        value = int((self.data[row][column] - lowest) * 255.0 / difference)
        self.__draw_pixel(value, column, row)

    elevations = [self.trace_path(row, 0) for row in range(len(self.data))]
    row = elevations.index(min(elevations))
    self.__trace_path(row, 0, ImageColor.getcolor('red', 'RGB'))
    self.image.save(self.out)

  def __trace_path(self, row, column, color = ImageColor.getcolor('cyan', 'RGB'), total_elevation = 0, backwards = False):
    current_value = self.data[row][column]
    self.__draw_pixel(255, column, row, color)
    next_row = row
    next_column = column + 1
    if next_column < len(self.data[0]):
      values = [sys.maxsize] * 3
      if row > 0:
        values[0] = abs(current_value - self.data[row -1][next_column])

      values[1] = abs(current_value - self.data[row][next_column])
      if row + 1 < len(self.data[0]):
        values[2] = abs(current_value - self.data[row + 1][next_column])
      next_row = row - 1 + values.index(min(values))
      total_elevation += min(values)
      return self.trace_path(next_row, next_column, color, total_elevation)
    return total_elevation

  def __draw_pixel(self, opacity, x, y, color = ImageColor.getcolor('white', 'RGB')):
    self.image.putpixel((x, y), color + (opacity,))

def main(file = "elevation_small.txt", out = "out.png"):
  PathFinder(file, out).draw()

if __name__ == "__main__":
  main()