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

# 计算点到直线的垂足
def perpendicular_distance(point, line_angle, center):
    # 将角度转换为弧度
    theta = np.radians(line_angle)
    # 旋转矩阵
    rotation_matrix = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    # 平移点以便直线通过原点
    translated_point = point - center
    # 旋转点
    rotated_point = np.dot(rotation_matrix, translated_point)
    # 垂足在旋转后的坐标系中的y坐标为0
    rotated_perpendicular_point = np.array([rotated_point[0], 0])
    # 旋转回原始坐标系
    perpendicular_point = np.dot(rotation_matrix.T, rotated_perpendicular_point) + center
    return perpendicular_point


# 主函数
def main(directory, center_x, center_y, interval):
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

    center = np.array([center_x, center_y])

    # 绘制图像
    plt.figure(figsize=(3072 / 100, 4096 / 100))
    for i, color in enumerate(colors):
        points_in_line = coordinates[line_assignments == i]

        if len(points_in_line) > 0:
            perpendicular_points = np.array(
                [perpendicular_distance(point, angles[i], center) for point in points_in_line])
            distances_from_center = np.linalg.norm(perpendicular_points - center, axis=1)

            left_points = points_in_line[distances_from_center < 0]
            right_points = points_in_line[distances_from_center >= 0]

            left_distances = np.linalg.norm(perpendicular_points[distances_from_center < 0] - center, axis=1)
            right_distances = np.linalg.norm(perpendicular_points[distances_from_center >= 0] - center, axis=1)
            left_sorted_indices = np.argsort(np.abs(left_distances))
            right_sorted_indices = np.argsort(right_distances)
            left_sorted_points = left_points[left_sorted_indices]
            right_sorted_points = right_points[right_sorted_indices]

            # 间隔标记点，并从中心点向外绘制
            for points, sorted_indices, direction in [(left_sorted_points, left_sorted_indices, -1),
                                                      (right_sorted_points, right_sorted_indices, 1)]:
                for j in range(0, len(sorted_indices), interval):
                    plt.scatter(points[j, 0], points[j, 1], color='red', marker='o', s=50, edgecolors='black')
                    # 可选：连接中心点和标记点
                    # plt.plot([center[0], points[j, 0]], [center[1], points[j, 1]], color='gray', linestyle='--')

        plt.scatter(points_in_line[:, 0], points_in_line[:, 1], color=color, marker='.')

        # 绘制从中心点到直线的参考线段（可选，用于可视化）
        # ...（代码内容保持不变）

    # 绘制中心点
    plt.scatter(center[0], center[1], color='red', marker='x', s=100)
    plt.title('根据垂足到中心点的距离排序并间隔标记点（以中心点为界分两部分）')
    plt.xlim(0, 3072)
    plt.ylim(0, 4096)
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.grid(True)
    plt.show()


# 指定包含txt文件的目录路径、中心点坐标及间隔距离
directory_path = 'F:/YOLOv8/ultralytics-main/runs/detect'
center_x, center_y = 367.5, 3948.0  # 示例中心点坐标
interval = 2  # 示例间隔距离（表示每隔5个点标记一个）
main(directory_path, center_x, center_y, interval)