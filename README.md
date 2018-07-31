# fcitx-mozc RPM builder for Fedora

A Dockerfile and a SPEC file to build fcitx-mozc RPM package on Fedora 27 or 28.

### Building RPM package
1. Building a docker image.
 
```
$ cd Fedora/*version* 
$ docker build -t fcitx-mozc-builder  .
```

2. Creating a docker container from the image.

```
$ docker create --name fcitx-mozc fcitx-mozc-builder
```

3. Taking a RPM package of the conatiner.

```
$ docker cp fcitx-mozc:/root/rpmbuild /var/tmp/
```

4. Delete the container and the image.

```
$ docker rm fcitx-mozc
$ docker rmi fcitx-mozc-builder
```

