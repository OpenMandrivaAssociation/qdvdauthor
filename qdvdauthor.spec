Summary: 	GUI to create DVD menus and images from media files
Name: 	 	qdvdauthor
Version: 	1.5.0
Release:	%mkrel 3
License:	GPL
Group:		Video
URL:		http://qdvdauthor.sourceforge.net/
Source:		%{name}-%{version}-2.tar.gz
Patch0:		%{name}-desktop.patch
BuildRequires:	imagemagick-devel 
BuildRequires:	qt3-devel		>= 3.3.7
BuildRequires:	libxine-devel
BuildRequires:	imagemagick
Requires:	dvdauthor
Requires:	mjpegtools
Requires:	sox
Requires:	dvd-slideshow		>= 0.8.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
'Q' DVD-Author is a GUI frontend for dvdauthor and related tools. The goal is
to provide an easy-to-use, yet powerful and complete interface to generate DVD
menus, slideshows, and videos to burn on a DVD under Linux.

%prep
%setup -q
%patch0 -p0

#remove all CVS directories
find -name CVS* | xargs rm -dr

%build
./configure \
	--build-qplayer \
	--build-qslideshow \
	--with-xine-support \
	--prefix=/usr \
	--qt-dir=%{_prefix}/lib/qt3

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %buildroot/%{_bindir}
mkdir -p %buildroot/%{_datadir}/qdvdauthor
mkdir -p %buildroot/%{_datadir}/applications
mkdir -p %buildroot/%{_datadir}/pixmaps

make install INSTALL_ROOT=%buildroot
cp %name.png %buildroot/%_datadir/pixmaps/
cp %name.desktop %buildroot/%_datadir/applications/

mkdir -p %{buildroot}/%{_iconsdir}
mkdir -p %{buildroot}/%{_miconsdir}
mkdir -p %{buildroot}/%{_liconsdir}

convert %{name}.png -size 16x16 %{buildroot}/%{_miconsdir}/%{name}.png
convert %{name}.png -size 32x32 %{buildroot}/%{_iconsdir}/%{name}.png
convert %{name}.png -size 48x48 %{buildroot}/%{_liconsdir}/%{name}.png

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%files
%defattr(644,root,root,755)
%doc README TODO CHANGELOG doc/*
%attr(755,root,root) %{_bindir}/q*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_datadir}/%{name}
