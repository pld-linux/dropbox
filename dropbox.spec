# TODO
# - avoid dropboxd relaunching itself with newer version if there's update available (disable auto updating):
#   glen     25034 19.9  1.5 1496132 81256 pts/46  Sl+  11:02   1:02 /home/glen/.dropbox-dist/dropbox /newerversion
# NOTES:
# - Upstream Dropbox Support (https://www.dropbox.com/ticket)
# - Release Notes (check new versions here): https://www.dropbox.com/release_notes
# - Download instructions (click the download link to find current version):
#   http://www.dropbox.com/downloading?os=lnx
#   http://wiki.dropbox.com/TipsAndTricks/TextBasedLinuxInstall
Summary:	Sync and backup files between computers
Name:		dropbox
# https://www.dropboxforum.com/hc/en-us/community/posts/206682016-New-Versioning-Scheme
Version:	11.4.22
Release:	1
License:	Proprietary
Group:		Daemons
Source0:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86-%{version}.tar.gz
# NoSource0-md5:	0be3ce1990b811439d6f76b936595084
NoSource:	0
Source1:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86_64-%{version}.tar.gz
# NoSource1-md5:	12bd23402fa69996d95730b87d4e39b2
NoSource:	1
URL:		http://www.dropbox.com/
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.15.1
BuildRequires:	unzip
BuildRequires:	zip
Conflicts:	nautilus-dropbox < 0.6.3-2
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# generate no Provides from private modules
%define		_noautoprovfiles	%{_libdir}/%{name}

# libicu-42, but pld th already has 54
%define		icu_libs	libicudata.so.42 libicui18n.so.42 libicuuc.so.42

# provided by package itself, but autodeps disabled
%define		_noautoreq		libwx_.*.so %{icu_libs} libffi.so.6 librsync.so.1

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/dropbox

# debuginfo wouldn't be useful
%define		_enable_debug_packages	0

# prelinked library, it is missing some cairo symbols
#define		skip_post_check_so	libwx_gtk2ud_core-2.8.so.0

%description
Dropbox is software that syncs your files online and across your
computers.

Put your files into your Dropbox on one computer, and they'll be
instantly available on any of your other computers that you've
installed Dropbox on (Windows, Mac, and Linux too!) Because a copy of
your files are stored on Dropbox's secure servers, you can also access
them from any computer or mobile device using the Dropbox website.

%package gui
Summary:	Gtk+2 GUI of Dropbox
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Gtk+2 Systray of Dropbox Daemon status.

%prep
%setup -qcT
%ifarch %{ix86}
%{__tar} --strip-components=1 -xzf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -xzf %{SOURCE1}
%endif
mv dropbox-lnx.*-%{version}/* .

# no need to package this
# altho system python is also 2.7, don't know how to enforce using it system libs
#%{__rm} -r distribute-0.6.26-py2.7.egg

# libraries to be taken from system
# for a in *.so*; do ls -ld /lib64/$a /us?/lib64/$a; done 2>/dev/null
%{__rm} libpopt.so.0 libdrm.so.2 libGL.so.1
%{__rm} libffi.so.6
%{__rm} libX11-xcb.so.1
%{__rm} libQt5{Core,DBus,Gui,Network,OpenGL,PrintSupport,Qml,Quick,Sql,WebKit,WebKitWidgets,Widgets,XcbQpa}.so.5
%{__rm} qt.conf
%{__rm} -r plugins

# keep librsync, won't finish syncing if not using upstream copy
test -f librsync.so.1

# fun, let's delete non-linux files from archive
unzip -l library.zip | \
	grep -E '(arch|dropbox)/(mac|win32)|_(win32|mac)\.py|pymac|ui/cocoa|unittest' | \
	grep -vE 'pymac/(__init__|constants|types|lazydll|lazyframework)\.py' | \
	grep -vE 'dropbox/mac/(version|__init__).py' | \
	awk '{print $NF}' > lib.delete
zip library.zip -d $(cat lib.delete)

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf dropbox library.zip

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{_libdir}/%{name}/dropboxd $RPM_BUILD_ROOT%{_bindir}/dropboxd

# install everything else
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib.delete

# in doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{ACKNOWLEDGEMENTS,VERSION,README}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS VERSION README
%attr(755,root,root) %{_bindir}/dropboxd
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%attr(755,root,root) %{_libdir}/%{name}/dropbox
%attr(755,root,root) %{_libdir}/%{name}/dropboxd
%{_libdir}/%{name}/library.zip

%{_libdir}/%{name}/dropbox_sqlite_ext-*-py*.egg
%{_libdir}/%{name}/psutil-*-py*.egg
%{_libdir}/%{name}/setuptools-*-py*.egg

# need +x bits for .so files
%defattr(-,root,root,-)
%{_libdir}/%{name}/cryptography-*-py*-linux-*.egg

# GUI parts
%exclude %{_libdir}/%{name}/PyQt5.*.so
%exclude %{_libdir}/%{name}/dbus.mainloop.pyqt5.so

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/wmctrl
%attr(755,root,root) %{_libdir}/%{name}/PyQt5.*.so
%attr(755,root,root) %{_libdir}/%{name}/dbus.mainloop.pyqt5.so
%dir %{_libdir}/%{name}/images
%{_libdir}/%{name}/images/emblems
%{_libdir}/%{name}/images/hicolor
%{_libdir}/%{name}/resources
