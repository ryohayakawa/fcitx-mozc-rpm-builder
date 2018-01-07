# fcitx-mozc RPM builder for Fedora

A Dockerfile and a SPEC file to build fcitx-mozc RPM package on Fedora.

### Building RPM package
1. Building a docker image.
 
```
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

### Notes 

If you want to have the RPM package on another Fedora version, you just
modify the first line in the Dockerfile. For example, if you want a RPM
package for Fedora 26, modify the Dockerfile as follows:

```
FROM fedora:26
```

