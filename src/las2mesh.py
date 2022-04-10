import numpy as np
import open3d as o3d
import laspy
import argparse

# lasファイルから点群を追加する
def add_points(filename,points,colors):
    las = laspy.read(filename)
    points = np.vstack([points,np.column_stack([las.points.X,las.points.Y,las.points.Z])/1000.])
    colors = np.vstack([colors,np.column_stack([las.points.red,las.points.green,las.points.blue])/65535.])
    return points,colors

# 複数の .lasファイルを読み込み1つの点群にする
def load_files(files):
    vec = np.empty((0,3))
    col = np.empty((0,3))

    for filename in files:
        vec,col = add_points(filename,vec,col)
        print(filename + " => " + str(len(vec)) + " points(total)")

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(vec)
    pcd.colors = o3d.utility.Vector3dVector(col)
    return pcd

# 点群からメッシュを生成
def create_mesh(point_cloud, mesh_depth):
    # 法線の推定
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(knn=20))
    point_cloud.orient_normals_to_align_with_direction(orientation_reference=np.array([0., 0., 1.]))

    # メッシュ化
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            point_cloud, depth=mesh_depth)
    print(poisson_mesh)

    bbox = point_cloud.get_axis_aligned_bounding_box()
    mesh = poisson_mesh.crop(bbox)

    # メッシュの軽量化
    # decimation_ratio = 0.5
    # count = len(mesh.triangles)
    # mesh = mesh.simplify_quadric_decimation(int(count * decimation_ratio))
    return mesh

def main():
    parser = argparse.ArgumentParser(description='.lasファイルからメッシュ(.ply)を生成します') 
    parser.add_argument('files', help='対象の .lasファイル。複数指定できます。', nargs='*')
    parser.add_argument('-d','--depth',default=9, type=int, help='メッシュの細かさを整数で指定します。デフォルト値は 9 です。')
    parser.add_argument('-o','--output',default='output.ply', help='出力ファイル名を指定します。デフォルト値は output.ply です。')
    parser.add_argument('-n','--nopreview', action='store_true', help='3Dプレビュー表示を無効にします')
    args = parser.parse_args()

    if len(args.files)==0:
        parser.print_help()
        return

    pcd = load_files(args.files)
    output_path = args.output
    depth = args.depth

    mesh = create_mesh(pcd,depth)
    if not args.nopreview:
        o3d.visualization.draw_geometries([mesh]) # 画面表示
    o3d.io.write_triangle_mesh(output_path, mesh,write_ascii=False,write_vertex_normals =True)

if __name__ == '__main__':
    main()