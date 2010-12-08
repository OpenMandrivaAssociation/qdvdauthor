Summary: 	GUI to create DVD menus and images from media files
Name: 	 	qdvdauthor
Version: 	2.1.0
Release:	%mkrel 3
License:	GPLv2
Group:		Video
URL:		http://qdvdauthor.sourceforge.net/
Source:		http://downloads.sourceforge.net/qdvdauthor/%{name}-%{version}.tar.gz
Patch0:		%{name}-desktop.patch
BuildRequires:	qt3-devel		>= 3.3.7
BuildRequires:	qt4-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	imagemagick
BuildRequires:	mjpegtools              >= 1.6.2
BuildRequires:	dvdauthor               >= 0.6.10
Buildrequires:	libxine-devel
BuildRequires:	mplayer			>= 1.0
Requires:	dvdauthor		>= 0.6.10
Requires:	mjpegtools		>= 1.6.2
Requires:	netpbm
Requires:	sox
Suggests:	mplayer			>= 1.0
Suggests:	dv2sub
Suggests:	ffmpeg
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
'Q' DVD-Author is a GUI frontend for dvdauthor and related tools. The goal is
to provide an easy-to-use, yet powerful and complete interface to generate DVD
menus, slideshows, and videos to burn on a DVD under Linux.

%prep
%setup -q
%patch0 -p0

#remove all CVS directories
find -name CVS* | sed '/CVS\/CVS/d' | xargs rm -rf

#fix EOL
sed -i 's/\r//' doc/todo2.txt doc/lookinto.txt

#adjust some paths to fix build
for p in complexdvd simpledvd
do
  sed -i -e 's:-L/usr/lib$:-L%{_libdir}:' %{name}/plugins/$p/$p.pro
done

%build
%define _jobs $(echo %{_smp_mflags}| sed 's:-j:-j :')
./configure \
	--no-configurator \
	--omit-local-ffmpeg \
	--prefix=%{_prefix} \
	--with-qt-lib=qt-mt \
	--qt3-dir=%{qt3dir} \
	--qt4-dir=%{qt4dir} \
	%{_jobs}

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
