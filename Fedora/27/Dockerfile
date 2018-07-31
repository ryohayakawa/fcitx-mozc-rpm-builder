FROM fedora:27
MAINTAINER Ryo HAYAKAWA <ryo@fastriver.net>
ADD fcitx-mozc.spec /
RUN dnf update -y && \
    dnf install -y python3-dnf-plugins-core rpm-build rpmdevtools which mozc && \
    dnf builddep --define "mozc_ver $(rpm -q --qf %{VERSION} mozc)" \
       --define "mozc_rel $(rpm -q --qf %{RELEASE} mozc)" -y /fcitx-mozc.spec && \
    dnf download -y --source mozc && \
    rpm -i mozc*
    
RUN spectool -g -R /fcitx-mozc.spec && \
    rpmbuild -ba --define "mozc_ver $(rpm -q --qf %{VERSION} mozc)" \
      --define "mozc_rel $(rpm -q --qf %{RELEASE} mozc)" /fcitx-mozc.spec

CMD ["/bin/true"]

