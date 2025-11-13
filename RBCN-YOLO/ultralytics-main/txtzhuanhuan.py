def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            # 使用逗号分隔符来分割坐标
            x, y = map(float, line.strip().replace(',', ' ').split())
            coordinates.append((x, y))
    return coordinates


def transform_coordinates(coordinates, width, height):
    transformed_coordinates = []
    for x, y in coordinates:
        new_x = x
        new_y = height - y
        transformed_coordinates.append((new_x, new_y))
    return transformed_coordinates


def write_coordinates(file_path, coordinates):
    with open(file_path, 'w') as file:
        for x, y in coordinates:
            file.write(f"{x} {y}\n")


def main(input_file, output_file, width, height):
    # 读取原始坐标
    coordinates = read_coordinates(input_file)

    # 转换坐标
    transformed_coordinates = transform_coordinates(coordinates, width, height)

    # 写入新的坐标
    write_coordinates(output_file, transformed_coordinates)


if __name__ == "__main__":
    # 示例：输入文件为'input.txt'，输出文件为'output.txt'
    # 需要根据实际情况设置图像的宽度和高度
    input_file = 'F:\\YOLOv8\\ultralytics-main\\runs\\detect\\location\\center.txt'
    output_file = 'F:\\YOLOv8\\ultralytics-main\\runs\\detect\\out.txt'
    width = 3072  # 图像宽度
    height = 4096  # 图像高度

    main(input_file, output_file, width, height)
