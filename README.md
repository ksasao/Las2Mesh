# Las2Mesh

点群(.las形式)ファイルを3Dモデル(.ply)に変換するツールです。

## ダウンロード

- [v0.1](https://github.com/ksasao/Las2Mesh/releases/download/v0.1/las2mesh_v0.1.zip) (2022/04/10)

## 利用方法

las2mesh.exe に 点群ファイル(.las) を Drag&Drop してください。複数まとめて Drag&Drop すると1つの3Dモデルとして出力されます。デフォルトのファイル名は output.ply です。出力形式は、.ply, .stl, .obj, .off, .gltf に対応しています。-o オプションで指定したファイル名で自動判別します。なお、いずれも頂点カラーで出力されます。

![伊豆急下田駅周辺(-d 11オプションを指定)](material/izukyushimoda_d11.png)
[G空間情報センター 静岡県　富士山南東部・伊豆東部　点群データLPデータ](https://www.geospatial.jp/ckan/dataset/shizuoka-2019-pointcloud/resource/d5e98a7b-f15c-45b0-bf40-0287f5b1de68) の .las ファイルを用いて作成 (ライセンス: [クリエイティブ・コモンズ 表示](http://opendefinition.org/licenses/cc-by/))

### オプション

```txt
usage: las2mesh.exe [-h] [-d DEPTH] [-o OUTPUT] [-n] [files ...]

.lasファイルからメッシュ(.ply)を生成します

positional arguments:
  files                 対象の .lasファイル。複数指定できます。

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        メッシュの細かさを整数で指定します。デフォルト値は 9 です。
  -o OUTPUT, --output OUTPUT
                        出力ファイル名を指定します。デフォルト値は output.ply です。
  -n, --nopreview       3Dプレビュー表示を無効にします
```
