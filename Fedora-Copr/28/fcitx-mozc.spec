%define specver 0.1
Name:		fcitx-mozc
Version:	%{mozc_ver}
Release:	%{mozc_rel}
Summary:	The mozc engine for Fcitx input method

Group:		System Environment/Libraries
License:	BSD and ASL 2.0 and UCD
URL:		https://fcitx-im.org/wiki/Fcitx

Source0:	mozc-%{version}.tar.bz2
Source1:	https://download.fcitx-im.org/fcitx-mozc/fcitx-mozc-icon.tar.gz

Patch0:		mozc-build-ninja.patch
## to avoid undefined symbols with clang.
Patch1:		mozc-build-gcc.patch
Patch2:		mozc-build-verbosely.patch
Patch3:		mozc-build-id.patch
Patch4:         mozc-fix-build-stdc.patch
Patch5:		https://download.fcitx-im.org/fcitx-mozc/fcitx-mozc-2.23.2815.102.1.patch

BuildRequires:	python gettext
BuildRequires:	libstdc++-devel zlib-devel libxcb-devel protobuf-devel protobuf-c glib2-devel qt5-devel zinnia-devel gtk2-devel
BuildRequires:	clang ninja-build
BuildRequires:	gyp >= 0.1-0.4.840svn
BuildRequires:  fcitx-devel
# https://bugzilla.redhat.com/show_bug.cgi?id=1419949
ExcludeArch:	ppc ppc64 sparcv9 sparc64

Requires:	mozc = %{version}-%{release}
Requires:	fcitx

%description
Mozc is a Japanese Input Method Editor (IME) designed for
multi-platform such as Chromium OS, Windows, Mac and Linux.

This package contains the Input Method Engine for Fcitx.

%prep
%setup -q -c -n mozc-%{version}
%patch0 -p1 -b .0-ninja
#%%patch1 -p1 -b .1-gcc
%patch2 -p1 -b .2-verbose
%patch3 -p1 -b .3-build-id
%patch4 -p1 -b .4-stdc
%patch5 -p2 -b .5-fcitx


%build
# replace compiler flags to build with the proper debugging information
t=`mktemp /tmp/mozc.gyp-XXXXXXXX`
#opts=$(for i in $(echo $RPM_OPT_FLAGS); do #|sed -e 's/-fstack-clash-protection//g' -e 's/-fcf-protection//g'); do
opts=$(for i in $(echo $RPM_OPT_FLAGS |sed -e 's/-fstack-clash-protection//g' -e 's/-fcf-protection//g'); do
        echo "i \\"
        echo "\"$i\","
done)
sed -ne "/'linux_cflags':/{p;n;p;:a;/[[:space:]]*\],/{\
$opts
p;b b};n;b a;};{p};:b" gyp/common.gypi > $t && mv $t gyp/common.gypi || exit 1
GYP_DEFINES="use_libprotobuf=1 use_libzinnia=1 zinnia_model_file=/usr/share/zinnia/model/tomoe/handwriting-ja.model ibus_mozc_path=%{_libexecdir}/ibus-engine-mozc ibus_mozc_icon_path=%{_datadir}/ibus-mozc/product_icon.png use_fcitx=YES use_fcitx5=NO" python build_mozc.py gyp --gypdir=%{_bindir} --server_dir=%{_libexecdir}/mozc --target_platform=Linux
python build_mozc.py build -c Release unix/fcitx/fcitx.gyp:fcitx-mozc


%install
%define fcitx_icon_dir %{_datadir}/fcitx/mozc/icon/
%define fcitx_addon_dir %{_datadir}/fcitx/addon/
%define fcitx_inputmethod_dir %{_datadir}/fcitx/inputmethod/
%define fcitx_lib_dir %{_libdir}/fcitx/
for mofile in out_linux/Release/gen/unix/fcitx/po/*.mo
do
        filename=`basename $mofile`
        lang=${filename/.mo/}
        install -D -m 644 "$mofile" "${RPM_BUILD_ROOT}%{_datadir}/locale/$lang/LC_MESSAGES/fcitx-mozc.mo"
done
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_addon_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_inputmethod_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_icon_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_lib_dir}
install -m 755 out_linux/Release/fcitx-mozc.so ${RPM_BUILD_ROOT}%{fcitx_lib_dir}
install -m 644 unix/fcitx/fcitx-mozc.conf ${RPM_BUILD_ROOT}%{fcitx_addon_dir}
install -m 644 unix/fcitx/mozc.conf ${RPM_BUILD_ROOT}%{fcitx_inputmethod_dir}
install -m 644 data/images/product_icon_32bpp-128.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc.png
install -m 644 data/images/unix/ui-alpha_full.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-alpha_full.png
install -m 644 data/images/unix/ui-alpha_half.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-alpha_half.png
install -m 644 data/images/unix/ui-direct.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-direct.png
install -m 644 data/images/unix/ui-hiragana.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-hiragana.png
install -m 644 data/images/unix/ui-katakana_full.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-katakana_full.png
install -m 644 data/images/unix/ui-katakana_half.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-katakana_half.png
install -m 644 data/images/unix/ui-dictionary.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-dictionary.png
install -m 644 data/images/unix/ui-properties.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-properties.png
install -m 644 data/images/unix/ui-tool.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-tool.png

# cp -r %{SOURCE1} ./
# tar -xzf fcitx-mozc-icons.tar.gz
tar xzf %{SOURCE1}
cp -r fcitx-mozc-icons/* ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/
rm -rf fcitx-mozc-icons
rm -rf fcitx-mozc-icons.tar.gz

%find_lang fcitx-mozc %no_lang_C

%files
%defattr(-,root,root)

%{fcitx_lib_dir}/fcitx-mozc.so
%{fcitx_addon_dir}/fcitx-mozc.conf
%dir %{fcitx_inputmethod_dir}
%{fcitx_inputmethod_dir}/mozc.conf
%dir %{_datadir}/fcitx/mozc
%{_datadir}/locale/*/LC_MESSAGES/fcitx-mozc.mo
%dir %{fcitx_icon_dir}
%{fcitx_icon_dir}/mozc.png
%{fcitx_icon_dir}/mozc-alpha_full.png
%{fcitx_icon_dir}/mozc-alpha_half.png
%{fcitx_icon_dir}/mozc-direct.png
%{fcitx_icon_dir}/mozc-hiragana.png
%{fcitx_icon_dir}/mozc-katakana_full.png
%{fcitx_icon_dir}/mozc-katakana_half.png
%{fcitx_icon_dir}/mozc-dictionary.png
%{fcitx_icon_dir}/mozc-properties.png
%{fcitx_icon_dir}/mozc-tool.png


%changelog
* Sat Aug 25 2018 Ryo HAYAKAWA <ryo@fastriver.net> - specver 0.3
- Modified to match to the Fedora Copr system.

* Sun Jan 7 2018 Ryo HAYAKAWA <ryo@fastriver.net> - specver 0.1
- Initial build.

