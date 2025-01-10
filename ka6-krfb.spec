#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		krfb
Summary:	krfb
Name:		ka6-%{kaname}
Version:	24.12.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications/Games
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	cfd31d3d2abff595fe86468696f77e94
URL:		http://www.kde.org/
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6WaylandClient-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kp6-kpipewire-devel
BuildRequires:	kp6-kwayland-devel >= 5.93
BuildRequires:	libepoxy-devel
BuildRequires:	libvncserver-devel
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pipewire-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/krfb
%attr(755,root,root) %{_bindir}/krfb-virtualmonitor
%ghost %{_libdir}/libkrfbprivate.so.5
%attr(755,root,root) %{_libdir}/libkrfbprivate.so.*.*
%dir %{_libdir}/qt6/plugins/krfb
%dir %{_libdir}/qt6/plugins/krfb/events
%attr(755,root,root) %{_libdir}/qt6/plugins/krfb/events/x11.so
%attr(755,root,root) %{_libdir}/qt6/plugins/krfb/events/xdp.so
%dir %{_libdir}/qt6/plugins/krfb/framebuffer
%attr(755,root,root) %{_libdir}/qt6/plugins/krfb/framebuffer/pw.so
%attr(755,root,root) %{_libdir}/qt6/plugins/krfb/framebuffer/xcb.so
%{_desktopdir}/org.kde.krfb.desktop
%{_desktopdir}/org.kde.krfb.virtualmonitor.desktop
%{_iconsdir}/hicolor/48x48/apps/krfb.png
%{_iconsdir}/hicolor/scalable/apps/krfb.svgz
%{_datadir}/krfb
%{_datadir}/metainfo/org.kde.krfb.appdata.xml
%{_datadir}/qlogging-categories6/krfb.categories
