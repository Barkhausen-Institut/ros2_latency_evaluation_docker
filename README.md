# CustomROS2Foxy

Contains Dockerfile to create an image of our custom-build ROS2 including profiling.

## Prerequisites
1. Copy the RTI Connext installation folder into the root of this repo with the name `rti_connext_dds`. You can get the zip-file containing the contents of the folder by
    ```bash
    $ apt-get install smbclient
    $ smbget -U youruser smb://SR-LAB-NAS-01/public/Software/rti_connext_dds-6.0.1.tar.gz
    $ tar -xzf rti_connext_dds-6.0.1.tar.gz
    ```
2. Copy a valid license to the root folder of this repo with the name `rti_license.dat`. You will get the license file as an attachment to the `RTI Connext DDS` Entry within the Corola Credentials File. 


## Building the image
Run `./build.sh` (needs your user to be in the group `docker`) [see official docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user). Maybe you need to run it with `sudo`.

The script builds a container named `barkhauseninstitut/ros2custom:foxy20201211`.

For testing, start the container with (**be careful with the `--rm` flag. It means your container is deleted upon closing. So, changes are not persistent**)

```bash
$ docker run -it --rm barkhauseninstitut/ros2custom:foxy20201211 /bin/bash
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
docker run -it --name ros2custom -v path/to/ros2_workspace:/workspace barkhauseninstitut/ros2custom:foxy20201211
```

This will prompt you to the containers bash. If you close it (`Ctrl-D` or `exit`) the container exits. See below how to restart. If you want to deattach and leave everything running in the container, type `Ctrl-p Ctrl-q`.

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

**This will delete all the changes that you did to the files within the container! (but not in your mounted folder)**. If your container is still running, docker complains. Then you can either stop the container or force-rm it:

```bash
$ docker rm -f ros2custom
```

### Docker Container Contents
The container contains the full ROS2 master build workspace. It clones the ROS2 foxy release given in the Dockerfile, downloads [ros2profiling from github](https://github.com/Barkhausen-Institut/ros2profiling), applies contained patches and compiles the ROS2 stack. 

Only frequently used ROS2 tools are compiled. 

So, e.g. no RViz or RQt tools are compiled, but virtually all console tools. 

A symlink to the ROS2 install dir is located in `/opt/ros/foxy/` such that a `. /opt/ros/foxy/setup.bash` sources the workspace.

Obviously, the container has `emacs` and `tmux` installed. 
