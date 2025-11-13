import os
import numpy as np
import matplotlib.pyplot as plt


# 从TXT文件中读取坐标数据
def read_coordinates_from_files(directory):
    coordinates = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    x, y = map(float, line.strip().split(','))
                    coordinates.append([x, y])
    return np.array(coordinates)


# 计算点到直线的距离
def point_to_line_distance(point, line_point, line_slope):
    x0, y0 = point
    x1, y1 = line_point
    m = line_slope
    return abs(m * x0 - y0 + y1 - m * x1) / np.sqrt(m ** 2 + 1)


# 根据角度计算直线的斜率
def slope_from_angle(angle_deg):
    return np.tan(np.radians(angle_deg))

# 计算线段与画布边界的交点
def calculate_intersection(center, slope, canvas_width, canvas_height):
    x0, y0 = center
    intersections = []

    # 与左边界相交
    if slope != float('inf') and slope != float('-inf'):
        y_left = slope * (0 - x0) + y0
        if 0 <= y_left <= canvas_height:
            intersections.append((0, y_left))

    # 与右边界相交
    if slope != float('inf') and slope != float('-inf'):
        y_right = slope * (canvas_width - x0) + y0
        if 0 <= y_right <= canvas_height:
            intersections.append((canvas_width, y_right))

    # 与上边界相交
    if slope != 0:
        x_top = (0 - y0) / slope + x0
        if 0 <= x_top <= canvas_width:
            intersections.append((x_top, 0))

    # 与下边界相交
    if slope != 0:
        x_bottom = (canvas_height - y0) / slope + x0
        if 0 <= x_bottom <= canvas_width:
            intersections.append((x_bottom, canvas_height))

    return intersections

# 主函数
def main(directory, center_x, center_y):
    # 从文件中读取坐标
    coordinates = read_coordinates_from_files(directory)

    # 设定中心点坐标
    center = np.array([center_x, center_y])

    # 定义直线的角度与对应颜色
    angles = np.arange(0, 180, 22.5)
    colors = plt.cm.viridis(np.linspace(0, 1, len(angles)))

    # 初始化点的直线归属
    line_assignments = -1 * np.ones(len(coordinates))

    # 首次计算距离时，初始化最小距离数组
    min_distances = np.full(len(coordinates), np.inf)

    # 计算各点到每条直线的距离，并确定其归属
    for i, angle in enumerate(angles):
        slope = slope_from_angle(angle)
        distances = [point_to_line_distance(point, center, slope) for point in coordinates]
        for j in range(len(distances)):
            if distances[j] < min_distances[j]:
                line_assignments[j] = i
                min_distances[j] = distances[j]

    # 绘制图像
    plt.figure(figsize=(3072 / 100, 4096 / 100))
    for i, color in enumerate(colors):
        points_in_line = coordinates[line_assignments == i]
        plt.scatter(points_in_line[:, 0], points_in_line[:, 1], color=color, marker='.')
        # 绘制从中心点到直线的线段（可选）
        slope = slope_from_angle(angles[i])
        intersections = calculate_intersection(center, slope, 3072, 4096)
        if len(intersections) == 2:
            x_ends, y_ends = zip(*intersections)
            plt.plot(x_ends, y_ends, color=color)
        # x_ends = [center[0], center[0] + 100 * np.cos(np.radians(angles[i]))]
        # y_ends = [center[1], center[1] + 100 * np.sin(np.radians(angles[i]))]
        # plt.plot(x_ends, y_ends, color=color)

    # 绘制中心点
    plt.scatter(center[0], center[1], color='red', marker='x', s=100)
    plt.title('根据最近距离将点分配到直线上')
    plt.xlim(0, 3072)
    plt.ylim(0, 4096)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


# 指定包含txt文件的目录路径及中心点坐标
directory_path = 'F:/YOLOv8/ultralytics-main/runs/detect'
center_x, center_y = 1497, 838.5  # 示例中心点坐标
main(directory_path, center_x, center_y)