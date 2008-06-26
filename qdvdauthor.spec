Summary: 	GUI to create DVD menus and images from media files
Name: 	 	qdvdauthor
Version: 	1.2.0
Release:	%mkrel 1
License:	GPL
Group:		Video
URL:		http://qdvdauthor.sourceforge.net/
Source:		http://downloads.sourceforge.net/qdvdauthor/%{name}-%{version}.tar.gz
Patch0:		%{name}-desktop.patch
BuildRequires:	ImageMagick-devel 
BuildRequires:	libqt3-devel		>= 3.3.7
BuildRequires:	libxine-devel
BuildRequires:	ImageMagick
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

install -d %{buildroot}{%{_bindir},%{_datadir}/qdvdauthor,%{_datadir}/applications}

install bin/%{name} %{buildroot}%{_bindir}/
install bin/qplayer %{buildroot}%{_bindir}/
install bin/qslideshow %{buildroot}%{_bindir}/
install %{name}.desktop %{buildroot}%{_datadir}/applications/
install qdvdauthor/i18n/*.qm %{buildroot}%{_datadir}/qdvdauthor/

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
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%dir %{_datadir}/%{name}
%lang(ca) %{_datadir}/%{name}/qdvdauthor_ca.qm
%lang(de) %{_datadir}/%{name}/qdvdauthor_de.qm
%lang(eo) %{_datadir}/%{name}/qdvdauthor_eo.qm
%lang(es) %{_datadir}/%{name}/qdvdauthor_es.qm
%lang(fr) %{_datadir}/%{name}/qdvdauthor_fr.qm
%lang(it) %{_datadir}/%{name}/qdvdauthor_it.qm
%lang(pl) %{_datadir}/%{name}/qdvdauthor_pl.qm
%lang(ca) %{_datadir}/%{name}/qplayer_ca.qm
%lang(de) %{_datadir}/%{name}/qplayer_de.qm
%lang(es) %{_datadir}/%{name}/qplayer_es.qm
%lang(fr) %{_datadir}/%{name}/qplayer_fr.qm
%lang(ca) %{_datadir}/%{name}/qrender_ca.qm
%lang(de) %{_datadir}/%{name}/qrender_de.qm
%lang(es) %{_datadir}/%{name}/qrender_es.qm
%lang(ca) %{_datadir}/%{name}/qslideshow_ca.qm
%lang(de) %{_datadir}/%{name}/qslideshow_de.qm
%lang(es) %{_datadir}/%{name}/qslideshow_es.qm
%lang(fr) %{_datadir}/%{name}/qslideshow_fr.qm
%lang(it) %{_datadir}/%{name}/qslideshow_it.qm
