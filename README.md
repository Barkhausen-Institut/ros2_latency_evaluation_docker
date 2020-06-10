# CustomROS2Foxy

Contains Dockerfile to create an image of our custom-build ROS2 including profiling.

## Building the image
Run `./build.sh` (needs your user to be in the group `docker`) [see official docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

The script builds a container named `barkhauseninstitut/ros2custom:foxy`.

For testing, start the container with (**be careful with the `--rm` flag. It means your container is deleted upon closing. So, changes are not persistent**)

```bash
$ docker run -it --rm barkhauseninstitut/ros2custom:foxy /bin/bash
```

Within the container, you can walk around. The ROS2 build workspace is in /ros2_custom. Try e.g.

```
$ . /ros2_custom/install/setup.bash
$ . /opt/ros/foxy/setup.bash        # An alternative, symlinks to the above location
$ ros2 run demo_nodes_cpp talker
```

## Usage
Intended usage is to start the container, and mount your local src directory into the container. Files are to be edited with your normal editing environment. Then, building is performed within the container. To mount your work dir into the container, do the following from your root source directory.

```bash
docker run -d -it --name ros2custom --mount type=bind,source="$(pwd)",target=/src barkhauseninstitut/ros2custom:foxy
```

Then, attach to this container by

```bash
docker attach ros2custom
```

This attaches to the root process of the container. If you close it (`Ctrl-D` or `exit`) the container exits. See below how to restart. If you want to deattach and leave everything running in the container, type `Ctrl-p Ctrl-q`.

The container has `tmux` installed, so you can create multiple terminals from there. If you feel the need to run an extra terminal outside of tmux, do

```bash
docker exec -it ros2custom /bin/bash
```

This terminal can be exited without stopping the container. 

### Container Lifecycle
Above `docker run` command starts a container with name `ros2custom` persistently on your system. It will run forever in the background (or if you exit its root process). You can stop it with

```bash
docker stop ros2custom
```

and restart it with

```bash
docker start ros2custom
```

You can delete your container with

```bash
docker rm ros2custom
```

**This will delete all the changes that you did to the files within the container!**

### Docker Container Contents
The container contains the full ROS2 master build workspace, described by [our BI ros2 meta repo](https://github.com/Barkhausen-Institut/ros2/blob/master/ros2.repos). `colcon` was executed as

```bash
$ colcon build --merge-install --packages-up-to demo_nodes_cpp
```

So, e.g. no RViz or RQt tools are compiled, but virtually all console tools. 

A symlink to the ROS2 install dir is located in `/opt/ros/foxy/` such that a `. /opt/ros/foxy/setup.bash` sources the workspace.