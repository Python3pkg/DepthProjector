## DepthProjector

![DESCRIPTION1](https://github.com/kanairen/DepthProjector/blob/img-patch/res/rotated_bunny.gif)    ![DESCRIPTION2](https://github.com/kanairen/DepthProjector/blob/img-patch/res/depth_images.png)

<!--
・DepthProjectorは3D形状データから深度マップを生成するためのモジュールです。-->
DepthProjector is a python module to create depth maps from 3D shape data(.obj file only).
<!--
・DepthProjectorは、深度マップを指定された拡張子(.png, .jpg, .gif)の画像ファイルとして出力します。
 また、バイナリ形式でのファイル出力も行うことができます。-->
This module outputs some depth maps as image and binary files.
<!--
・深度マップの取得は、3D形状データを三次元ユークリッド座標系の中心に置き、
 カメラを半径rの球面座標上で動かしながら、カメラプレーンに対する透視投影によって行います。
 球面座標は２つのパラメタThetaとPhiによって定義され、各々のパラメタは一定間隔で変動します。
 Theta,Phiの取りうる角度の集合をそれぞれT,Pとしたとき、T,Pはデフォルトで
 T={30t|0≦t<12}, P={-60, -30, 0, 30, 60}と定義されます。すなわち、この時生成される深度マップの枚数は3D形状データ一つあたり
 12×5=60となります。
-->

To get depth maps, DepthProjector set 3D shape in center of three-dimensional orthogonal coordinate system,
and project to the camera plane of view camera on spherical coordinate system.
Spherical coordinate system has two angles: Theta and Phi.

![PP_FIGURE](https://github.com/kanairen/DepthProjector/blob/img-patch/res/pp_angles.png)

Default angle sets of Theta and Phi (T, P) are defined as
```math
T={30t|0 ≦ t < 12}, P={30p|-2 ≦ p ≦ 2}
```
In this case, the number of depth maps are 12×5=60 maps.

## Demo


![DEMO](https://github.com/kanairen/DepthProjector/blob/img-patch/res/demo.gif)

## Installation

```
sudo pip install DepthProjector
```

## Usage

```
python -m DepthProjector [FILE_PATH]
```

Also, you can refer some descriptions with command '--help'.
```
$[kanairen]~% python -m DepthProjector --help
Usage: __main__.py [OPTIONS] FILE_PATH

Options:
  -t, --theta_angle_range <INTEGER INTEGER INTEGER>...
                                  Range of theta angle([FROM] [TO] [STEP]).
                                  Default is (0 360 30).
  -p, --phi_angle_range <INTEGER INTEGER INTEGER>...
                                  Range of phi angle([FROM] [TO] [STEP]).
                                  Default is (-60 61 30).
  -i, --init_rotation <INTEGER INTEGER INTEGER>...
                                  Initial rotation of 3d shape([X] [Y] [Z]).
                                  Default is (0 0 0).
  -r, --radius FLOAT              Radius of camera coordinate.
  -v, --is_view_only BOOLEAN      option whether is DepthProjector executed as
                                  3D Viewer(projection is not executed) or
                                  not.
  --help                          Show this message and exit.
```

## Author
[kanairen](https://github.com/kanairen)



