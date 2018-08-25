FROM fedora:28
MAINTAINER Ryo HAYAKAWA <ryo@fastriver.net>
ADD fcitx-mozc.spec /
#RUN dnf install -y python3-dnf-plugins-core rpm-build rpmdevtools which mozc && \
RUN dnf install -y python3-dnf-plugins-core rpm-build rpmdevtools mozc && \
    sed -i -e "s/%{mozc_ver}/$(rpm -q --qf %{VERSION} mozc)/" \
        -e "s/%{mozc_rel}/$(rpm -q --qf %{RELEASE} mozc | cut -d. -f1)\%{?dist}/" \
        /fcitx-mozc.spec && \
#    dnf builddep -y /fcitx-mozc.spec && \
    dnf download -y --source mozc && \
    rpm -i mozc*
    
RUN spectool -g -R /fcitx-mozc.spec && \
    rpmbuild -bs /fcitx-mozc.spec

CMD ["/bin/true"]

