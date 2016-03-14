## DepthProjector

DepthProjector create depth maps from your 3d shape file,
which maps are captured from multi-view points.

DepthProjector is available for '.obj' shape file only.

You can specify the range of angles: 'Theta' and 'Phi'.

![PP_FIGURE](https://github.com/kanairen/DepthProjector/blob/img-patch/res/pp_angles.png)

## Demo

![DEMO](https://github.com/kanairen/DepthProjector/blob/img-patch/res/demo.gif)    ![DEMO](https://github.com/kanairen/DepthProjector/blob/img-patch/res/depth-images.png)


## Installation

```
sudo pip install DepthProjector
```

## Usage

```
python -m DepthProjector [FILE_PATH]
```

Also, you can refer some explanation with command '--help'.
```
python -m DepthProjector --help
Usage: __main__.py [OPTIONS] FILE_PATH

Options:
  -t, --theta_angle_range <INTEGER INTEGER INTEGER>...
                                  Range of theta angle([FROM]
                                  [TO] [STEP]). Default is (0
                                  360 30).
  -p, --phi_angle_range <INTEGER INTEGER INTEGER>...
                                  Range of phi angle([FROM]
                                  [TO] [STEP]). Default is (-60
                                  61 30).
  -i, --init_rotation <INTEGER INTEGER INTEGER>...
                                  Initial rotation of 3d
                                  shape([X] [Y] [Z]). Default
                                  is (0 0 0).
  -r, --radius FLOAT              Radius of camera coordinate.
  -v, --is_view_only BOOLEAN      option whether is
                                  DepthProjector executed as 3D
                                  Viewer(procjection is not
                                  executed) or not.
  --help                          Show this message and exit.
```

## Author
[kanairen](https://github.com/kanairen)



