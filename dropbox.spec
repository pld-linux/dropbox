# NOTES:
# - Upstream Dropbox Support (https://www.dropbox.com/ticket)
# - Download instructions (click the download link to find current version):
#   http://wiki.dropbox.com/TipsAndTricks/TextBasedLinuxInstall
Summary:	Sync and backup files between computers
Name:		dropbox
Version:	0.7.110
Release:	0.10
License:	Proprietary
Group:		Daemons
URL:		http://www.dropbox.com/
Source0:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86-%{version}.tar.gz
# NoSource0-md5:	e6cb1751ba33542a82b794cea7dc8dbd
NoSource:	0
Source1:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86_64-%{version}.tar.gz
# NoSource1-md5:	434fb3451d1f638bddde2f5691beb426
NoSource:	1
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.15.1
Conflicts:	nautilus-dropbox < 0.6.3-2
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# generate no Provides from private modules
%define		_noautoprovfiles	%{_libdir}/%{name}

# provided by package itself, but autodeps disabled
%define		_noautoreq		libcrypto.so libssl.so libwx_.*.so

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/dropbox

# debuginfo wouldn't be useful
%define		_enable_debug_packages	0

%description
Dropbox is software that syncs your files online and across your
computers.

Put your files into your Dropbox on one computer, and they'll be
instantly available on any of your other computers that you've
installed Dropbox on (Windows, Mac, and Linux too!) Because a copy of
your files are stored on Dropbox's secure servers, you can also access
them from any computer or mobile device using the Dropbox website.

%prep
%setup -qcT
%ifarch %{ix86}
%{__tar} --strip-components=1 -xzf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -xzf %{SOURCE1}
%endif

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf dropbox library.zip

# use system lib, or we get weird errors like:
# (dropbox:13225): Gtk-WARNING **: Error loading theme icon 'gtk-ok' for stock:
# Unable to load image-loading module: /usr/lib64/gtk-2.0/2.10.0/loaders/svg_loader.so:
# /usr/lib64/dropbox/libz.so.1: version `ZLIB_1.2.3.3' not found (required by /usr/lib64/libxml2.so.2)
rm -f libz.so.1

# don't really need test at runtime
rm -rf ncrypt-*.egg/ncrypt/test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{_libdir}/dropbox/dropboxd $RPM_BUILD_ROOT%{_bindir}/dropboxd

# install everything else
install -d $RPM_BUILD_ROOT%{_libdir}/dropbox
cp -a . $RPM_BUILD_ROOT%{_libdir}/dropbox

# in doc
rm -f $RPM_BUILD_ROOT%{_libdir}/dropbox/{ACKNOWLEDGEMENTS,VERSION}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS VERSION
%attr(755,root,root) %{_bindir}/dropboxd
%dir %{_libdir}/dropbox
%attr(755,root,root) %{_libdir}/dropbox/*.so*
%attr(755,root,root) %{_libdir}/dropbox/dropbox
%attr(755,root,root) %{_libdir}/dropbox/dropboxd
%{_libdir}/dropbox/library.zip

%dir %{_libdir}/dropbox/ncrypt-*.egg
%attr(755,root,root) %{_libdir}/dropbox/ncrypt-*.egg/*.so
%{_libdir}/dropbox/ncrypt-*.egg/*.pyc
%{_libdir}/dropbox/ncrypt-*.egg/ncrypt
%{_libdir}/dropbox/ncrypt-*.egg/EGG-INFO

%dir %{_libdir}/dropbox/netifaces-*.egg
%attr(755,root,root) %{_libdir}/dropbox/netifaces-*.egg/*.so
%{_libdir}/dropbox/netifaces-*.egg/*.pyc
%{_libdir}/dropbox/netifaces-*.egg/EGG-INFO
