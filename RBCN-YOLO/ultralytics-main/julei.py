import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# 读取TXT文件中的坐标
def read_coordinates_from_files(directory):
    coordinates = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    x, y = map(float, line.strip().split(','))
                    coordinates.append([x, y])
    return np.array(coordinates)


# 计算距离矩阵
def compute_distance_matrix(coordinates):
    dist_matrix = squareform(pdist(coordinates, metric='euclidean'))
    np.fill_diagonal(dist_matrix, np.inf)  # 将对角线元素设置为无穷大，避免自身作为最近邻
    return dist_matrix


# 计算局部密度
def compute_local_density(dist_matrix, dc):
    density = np.sum(np.exp(-(dist_matrix / dc) ** 2), axis=1)
    return density


# 计算到更高密度点的最小距离
def compute_min_distance_to_higher_density(density, dist_matrix):
    sorted_idxs = np.argsort(-density)  # 按照密度降序排序的索引
    min_dist = np.inf * np.ones(len(density))
    for i in range(len(density)):
        for j in range(i):
            if density[sorted_idxs[j]] > density[sorted_idxs[i]]:
                min_dist[sorted_idxs[i]] = dist_matrix[sorted_idxs[i], sorted_idxs[j]]
                break
    return min_dist


# 选择聚类中心
def select_cluster_centers(density, min_dist, num_centers):
    center_idxs = np.argsort(density * min_dist)[-num_centers:]
    return center_idxs


# 分配簇标签
# def assign_cluster_labels(coordinates, center_idxs, dist_matrix):
    # labels = -1 * np.ones(len(coordinates))
    # for i, center_idx in enumerate(center_idxs):
        # labels[center_idx] = i
        # for j in range(len(coordinates)):
            # if labels[j] == -1 and dist_matrix[j, center_idx] < dist_matrix[j, labels[labels > -1]].min():
                # labels[j] = i
    # return labels

def assign_cluster_labels(coordinates, center_idxs, dist_matrix):
    labels = -1 * np.ones(len(coordinates))
    for i, center_idx in enumerate(center_idxs):
        labels[center_idx] = i
        for j in range(len(coordinates)):
            if labels[j] == -1:
                valid_indices = np.where(labels != -1)[0]  # 获取所有已分配的标签的索引
                if len(valid_indices) > 0:
                    min_distance = np.min([dist_matrix[j, k] for k in valid_indices])
                    if dist_matrix[j, center_idx] < min_distance:
                        labels[j] = i
    return labels

# 绘制聚类结果
def plot_clusters(coordinates, labels, centers, width=3072, height=4096):
    plt.figure(figsize=(width / 100, height / 100))
    scatter = plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap='viridis', marker='.')
    for center in centers:
        plt.scatter(center[0], center[1], c='red', marker='x', s=100)
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.title('Density Peaks Clustering')
    plt.colorbar(scatter)
    # plt.gca().invert_xaxis()  # 翻转x轴
    # plt.gca().invert_yaxis()  # 翻转y轴
    plt.show()


# 主函数
def main(directory, num_centers):
    coordinates = read_coordinates_from_files(directory)
    dist_matrix = compute_distance_matrix(coordinates)

    # dc 是截止距离，通常选择为使得平均每个点的邻居数为总点数的某个比例（如1-2%）
    dc = np.percentile(dist_matrix, 2)

    density = compute_local_density(dist_matrix, dc)
    min_dist = compute_min_distance_to_higher_density(density, dist_matrix)
    center_idxs = select_cluster_centers(density, min_dist, num_centers)
    centers = coordinates[center_idxs]

    labels = assign_cluster_labels(coordinates, center_idxs, dist_matrix)
    plot_clusters(coordinates, labels, centers)

    # 打印聚类中心的坐标
    for i, center in enumerate(centers):
        print(f"Cluster {i + 1} center: {center}")


# 替换为包含txt文件的目录路径和期望的聚类中心数量
directory_path = 'F:/YOLOv8/ultralytics-main/runs/detect'
# directory_path = r'F:\YOLOv8\ultralytics-main\runs\detect\location'
num_clusters = 1  # 假设我们想要1个聚类中心
main(directory_path, num_clusters)