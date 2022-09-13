import numpy as np
import open3d as o3d
import laspy
import argparse

lasviewer_version = "LasViewer v1.0 based on Las2Mesh"

# lasファイルから点群を追加する
def add_points(filename,points,colors):
    las = laspy.read(filename)
    scales = las.header.scales
    points = np.vstack([points,np.column_stack([las.points.X * scales[0], las.points.Y * scales[1], las.points.Z * scales[2]])])
    if hasattr(las.points,'red'):
        # カラーあり
        colors = np.vstack([colors,np.column_stack([las.points.red,las.points.green,las.points.blue])/65535.])
    else:
        # カラーなし(グレー表示)
        colors = np.vstack([colors,np.column_stack([np.full((len(las.X), 3),0.5)])])
    return points,colors

# 複数の .lasファイルを読み込み1つの点群にする
def load_files(files):
    vec = np.empty((0,3))
    col = np.empty((0,3))

    for filename in files:
        vec,col = add_points(filename,vec,col)
        print(filename + " => " + str(len(vec)) + " points(total)")

    # 端が原点となるように移動
    min = np.amin(vec, axis=0)
    max = np.amax(vec, axis=0)
    vec = vec - min
    bbox = max-min
    print(f"size: {bbox[0]:.1f} x {bbox[1]:.1f} x {bbox[2]:.1f} (m)")
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(vec)
    pcd.colors = o3d.utility.Vector3dVector(col)
    return pcd

def main():
    print(lasviewer_version)
    parser = argparse.ArgumentParser(description='.lasファイルを表示します') 
    parser.add_argument('files', help='対象の .lasファイル。複数指定できます。', nargs='*')
    args = parser.parse_args()

    if len(args.files)==0:
        parser.print_help()
        return

    pcd = load_files(args.files)

    # 操作方法 http://www.open3d.org/docs/latest/tutorial/Basic/visualization.html
    o3d.visualization.draw_geometries([pcd],window_name=lasviewer_version) # 画面表示

if __name__ == '__main__':
    main()
