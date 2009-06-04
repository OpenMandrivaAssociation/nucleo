# export CVSROOT=:pserver:anonymous@cvs.lri.fr:/users/asspro/roussel/cvsroot
# cvs login # no password
# DATE=$(date +%Y%m%d)
# cvs export -D now -d nucleo-$DATE nucleo
# tar cvjf nucleo-$DATE.tar.bz2 nucleo-$DATE

%define name nucleo
%define version 0.7.5
#define cvs 20061224
%define distname %{name}-%{version}

%define common_summary explore video and human-computer interaction
%define common_description Nucleo is a toolkit for exploring new uses of video and new\
human-computer interaction techniques.
%define lib_major 0

%define lib_name %mklibname %{name} %{lib_major}

Summary: Toolkit to %{common_summary}
Name: %{name}
Version: %{version}
Release: %mkrel 1
Source0: http://insitu.lri.fr/metisse/download/nucleo/%{distname}.tar.bz2
#gw add a header for the internal and deprecated imgconvert function of
#ffmpeg's libavcocec
Patch0:   nucleo-0.7.3-imgconvert-header.patch
Patch1: nucleo-0.7.3-gcc44.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.lri.fr/~roussel/projects/nucleo/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: automake
BuildRequires: mesaglu-devel jpeg-devel png-devel libexif-devel freetype2-devel
BuildRequires: ffmpeg-devel
BuildRequires: libxi-devel
BuildRequires: avahi-compat-libdns_sd-devel
BuildRequires: qt4-devel
Buildrequires: gd-devel

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

%package -n	%{lib_name}-plugins-gd
Summary:	GD plugin for nucleo
Group:		System/Libraries

%description -n	%{lib_name}-plugins-gd
This package contains GD plugin for nucleo.

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
%patch0 -p1 -b .ffmpeg
%patch1 -p1 -b .gcc44

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

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

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

%files -n %{lib_name}-plugins-gd
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/nPgd.so

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/libNucleo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_bindir}/nucleo-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

