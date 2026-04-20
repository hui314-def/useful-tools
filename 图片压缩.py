import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

def pca_compress_channel(channel, num_components):
    # 均值中心化
    mean = np.mean(channel, axis=0)
    centered = channel - mean
    # 协方差矩阵
    cov = np.cov(centered, rowvar=False)
    # 特征值分解
    eigvals, eigvecs = np.linalg.eigh(cov)
    # 取最大的num_components个特征向量
    idx = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, idx[:num_components]]
    # 投影到主成分空间
    compressed = np.dot(centered, eigvecs)
    # 重构
    reconstructed = np.dot(compressed, eigvecs.T) + mean
    return reconstructed

def compress_image_pca(img_path, num_components=50):
    img = Image.open(img_path)
    img = img.convert('RGB')
    img_np = np.array(img, dtype=np.float64)
    compressed_channels = []
    for i in range(3):  # R, G, B
        channel = img_np[:, :, i]
        reconstructed = pca_compress_channel(channel, num_components)
        # 裁剪到合法范围
        reconstructed = np.clip(reconstructed, 0, 255)
        compressed_channels.append(reconstructed)
    compressed_img = np.stack(compressed_channels, axis=2).astype(np.uint8)
    return img_np.astype(np.uint8), compressed_img

def show_info(original, compressed):
    print("原图尺寸:", original.shape)
    print("压缩后尺寸:", compressed.shape)
    mse = np.mean((original - compressed) ** 2)
    print("均方误差(MSE):", mse)
    psnr = 10 * np.log10(255**2 / mse) if mse != 0 else float('inf')
    print("峰值信噪比(PSNR):", psnr)

if __name__ == "__main__":
    img_path = "t.jpg"
    num_components = 100  # 可调整主成分数量
    original, compressed = compress_image_pca(img_path, num_components)
    show_info(original, compressed)
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(original)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title(f"PCA Compressed ({num_components} components)")
    plt.imshow(compressed)
    plt.axis('off')
    plt.show()