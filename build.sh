ORG=barkhauseninstitut
IMAGE=ros2custom
VERSION=foxy20201211
TAG_BUILD=$ORG/$IMAGE:$VERSION

docker build -t $TAG_BUILD -f Dockerfile.foxy --build-arg CACHEBUST=$(date +%s) .
