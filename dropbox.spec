# NOTES:
# - Upstream Dropbox Support (https://www.dropbox.com/ticket)
# - Release Notes (check new versions here): https://www.dropbox.com/release_notes
# - Download instructions (click the download link to find current version):
#   http://www.dropbox.com/downloading?os=lnx
#   http://wiki.dropbox.com/TipsAndTricks/TextBasedLinuxInstall
Summary:	Sync and backup files between computers
Name:		dropbox
Version:	2.6.25
Release:	1
License:	Proprietary
Group:		Daemons
Source0:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86-%{version}.tar.gz
# NoSource0-md5:	4521809aa11f5b8628d36b4462622dd8
NoSource:	0
Source1:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86_64-%{version}.tar.gz
# NoSource1-md5:	a303933f7abc52c13a4b03067c87c754
NoSource:	1
URL:		http://www.dropbox.com/
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.15.1
Conflicts:	nautilus-dropbox < 0.6.3-2
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# generate no Provides from private modules
%define		_noautoprovfiles	%{_libdir}/%{name}

# provided by package itself, but autodeps disabled
%define		_noautoreq		libwx_.*.so librsync.so.1 libffi.so.6

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/dropbox

# debuginfo wouldn't be useful
%define		_enable_debug_packages	0

# prelinked library, it is missing some cairo symbols
%define		skip_post_check_so	libwx_gtk2ud_core-2.8.so.0

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

# no need to package this
# altho system python is also 2.7, don't know how to enforce using it system libs
#%{__rm} -r distribute-0.6.26-py2.7.egg

# libraries to be taken from system
# for a in *.so*; do ls -ld /lib/$a /usr/lib/$a; done 2>/dev/null
%{__rm} libpng12.so.0 libbz2.so.1.0 libpopt.so.0

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf dropbox library.zip

# fun, let's delete non-linux files from archive
unzip -l library.zip | grep -E 'arch/(mac|win32)|pynt|ui/cocoa|unittest' | awk '{print $NF}' > lib.delete
# TODO: also pymac could be cleaned if pymac.constants is not imported
zip library.zip -d $(cat lib.delete)

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

%{_libdir}/%{name}/cffi-*-py*.egg
%{_libdir}/%{name}/distribute-*-py*.egg
%{_libdir}/%{name}/dropbox_sqlite_ext-*-py*.egg
%{_libdir}/%{name}/mock-*-py*.egg
%{_libdir}/%{name}/pycparser-*-py*.egg-info

%dir %{_libdir}/%{name}/images
%{_libdir}/%{name}/images/emblems
%{_libdir}/%{name}/images/hicolor
