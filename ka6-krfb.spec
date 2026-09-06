#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	26.08.0
%define		kframever	6.2.0
%define		qtver		6.5.0
%define		kaname		krfb
Summary:	krfb
Name:		ka6-%{kaname}
Version:	26.08.0
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications/Games
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	6d1c2212deb3abf364778672d20077d2
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kstatusnotifieritem-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kp6-kpipewire-devel
BuildRequires:	kp6-kwayland-devel >= 5.93
BuildRequires:	libvncserver-devel >= 0.9.14
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pipewire-devel >= 0.3
BuildRequires:	plasma-wayland-protocols-devel >= 1.5.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel
BuildRequires:	xcb-util-image-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Krfb Desktop Sharing is a server application that allows you to share
your current session with a user on another machine, who can use a VNC
client to view or even control the desktop.

%description -l pl.UTF-8
Kfrb Współdzielenie Desktopu jest aplikacją serwerową pozwalającą Ci
współdzielić bieżącą sesję z użytkownikiem na innej maszynie, który
może użyć klienta VNC do podejrzenia a nawet kontrolowania Twojego
desktopu.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/krfb
%attr(755,root,root) %{_bindir}/krfb-virtualmonitor
%ghost %{_libdir}/libkrfbprivate.so.5
%{_libdir}/libkrfbprivate.so.*.*
%dir %{_libdir}/qt6/plugins/krfb
%dir %{_libdir}/qt6/plugins/krfb/events
%{_libdir}/qt6/plugins/krfb/events/x11.so
%{_libdir}/qt6/plugins/krfb/events/xdp.so
%dir %{_libdir}/qt6/plugins/krfb/framebuffer
%{_libdir}/qt6/plugins/krfb/framebuffer/pw.so
%{_libdir}/qt6/plugins/krfb/framebuffer/xcb.so
%{_desktopdir}/org.kde.krfb.desktop
%{_desktopdir}/org.kde.krfb.virtualmonitor.desktop
%{_iconsdir}/hicolor/48x48/apps/krfb.png
%{_iconsdir}/hicolor/scalable/apps/krfb.svgz
%{_datadir}/krfb
%{_datadir}/metainfo/org.kde.krfb.appdata.xml
%{_datadir}/qlogging-categories6/krfb.categories
