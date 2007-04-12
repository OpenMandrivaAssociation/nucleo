# export CVSROOT=:pserver:anonymous@cvs.lri.fr:/users/asspro/roussel/cvsroot
# cvs login # no password
# DATE=$(date +%Y%m%d)
# cvs export -D now -d nucleo-$DATE nucleo
# tar cvjf nucleo-$DATE.tar.bz2 nucleo-$DATE

%define name nucleo
%define version 0.6
#%define cvs 20061224
%define rel 7
%define release %mkrel %{rel}
%define distname %{name}-%{version}

%define common_summary explore video and human-computer interaction
%define common_description Nucleo is a toolkit for exploring new uses of video and new\
human-computer interaction techniques.
%define lib_major 0

%define lib_name %mklibname %{name} %{lib_major}

Summary: Toolkit to %{common_summary}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{distname}.tar.bz2
# (gb) 64-bit fixes (API change)
Patch0: nucleo-20061224-64bit-fixes.patch
# (fc) 0.6-1mdv fix build without dns-sd
Patch1: nucleo-0.6-fixdnssd.patch
# (fc) 0.6-2mdv fix debug in 32bit
Patch2: nucleo-0.6-32bit.patch
# (fc) 0.6-3mdv fix plugins names (CVS)
Patch3: nucleo-0.6-fixplugins.patch
# (fc) 0.6-3mdv fix DNS-SD support with avahi
Patch4: nucleo-0.6-avahi.patch

License: LGPL
Group: System/Libraries
Url: http://www.lri.fr/~roussel/projects/nucleo/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: automake1.9
BuildRequires: mesaglu-devel jpeg-devel png-devel libexif-devel freetype2-devel
BuildRequires: ffmpeg-devel
BuildRequires: libxi-devel
BuildRequires: avahi-compat-libdns_sd-devel
BuildRequires: qt4-devel


%description
%{common_description}

%package -n	%{lib_name}
Summary:	A library to %{common_summary}
Group:		System/Libraries

%description -n	%{lib_name}
%{common_description}

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name}-plugins-ffmpeg
Summary:	FFMpeg plugin for nucleo
Group:		System/Libraries

%description -n	%{lib_name}-plugins-ffmpeg
This package contains FFMPEG plugin for nucleo.

%package -n	%{lib_name}-plugins-qt
Summary:	QT4 plugin for nucleo
Group:		System/Libraries

%description -n	%{lib_name}-plugins-qt
This package contains QT4 plugin for nucleo.

%package -n	%{lib_name}-devel
Summary:	Development tools for programs using %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q -n %{distname}
%patch0 -p1 -b .64bit-fixes
%patch1 -p1 -b .fixdnssd
%patch2 -p1 -b .32bit
%patch3 -p1 -b .fixplugins
%patch4 -p1 -b .avahi

#needed by patches 1, 3 & 4
aclocal-1.9
automake-1.9

#needed by patch4
autoconf

%build
%configure2_5x 
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/nucleo/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README
%{_bindir}/nBundle
%{_bindir}/nTest
%{_bindir}/videoClient
%{_bindir}/videoServer
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Info.plist.tmpl
%{_datadir}/%{name}/%{name}.icns
%{_datadir}/%{name}/%{name}.pdf
%{_datadir}/%{name}/plugin-list
%dir %{_datadir}/%{name}/fonts
%{_datadir}/%{name}/fonts/*.ttf

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libNucleo.so.*
%{_libdir}/libNucleo.la

%files -n %{lib_name}-plugins-ffmpeg
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/nPffmpeg.so

%files -n %{lib_name}-plugins-qt
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/nPqt.so

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/libNucleo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_bindir}/nucleo-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

