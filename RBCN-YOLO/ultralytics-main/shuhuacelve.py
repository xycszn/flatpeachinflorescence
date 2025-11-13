from PIL import Image, ImageDraw

# 定义画布的尺寸
width, height = 3072, 4096

# 创建一个白色画布
canvas = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(canvas)

# 定义坐标点的颜色和大小
point_color = (0, 0, 255)  # 黑色
point_size = 20

# 读取txt文件中的坐标点
file_path = 'F:\\YOLOv8\\ultralytics-main\\runs\\detect\\location\\center.txt'  # 使用双反斜杠或原始字符串
print("尝试打开的文件路径是：", file_path)  # 调试输出

try:
    # file_path = 'F:YOLOv8/ultralytics-main/runs/detect/location/center.txt'  # 假设这是正确的路径
    with open(file_path, 'r') as file:  # 明确指定打开模式为'r'
        for line in file:
            # 去掉每行的换行符，并分割x和y坐标
            x, y = map(float, line.strip().split(','))
            # 在画布上绘制点
            draw.ellipse((x - point_size, y - point_size, x + point_size, y + point_size), fill=point_color)
except FileNotFoundError:
    print("center.txt 文件未找到")
except Exception as e:
    print(f"读取文件时发生错误: {e}")

# 保存画布为图像文件
canvas.save('output_image.png')

# 显示画布（可选）
canvas.show()