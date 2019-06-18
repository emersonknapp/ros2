Documentation is at https://index.ros.org/doc/ros2/

This feature branch is for an attempt at compiling portions of rviz with Emscripten, to embed in a browser-based RViz.

Need to mount and activate the Emscripten latest SDK, then invoke the incantations. See FIND_ROOT_PATH necessary override after specifying the toolchain file. Not sure why.

```
colcon build \
  --cmake-args \
    -DCMAKE_TOOLCHAIN_FILE=/root/emsdk/fastcomp/emscripten/cmake/Modules/Platform/Emscripten.cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING:BOOL=OFF \
    -DCMAKE_FIND_ROOT_PATH=$(pwd)/eminstall \
  --build-base embuild --install-base eminstall --symlink-install \
  --packages-up-to rviz_rendering
```
