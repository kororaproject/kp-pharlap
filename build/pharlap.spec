Name:           pharlap
Version:        1.4.4
Release:        1%{?dist}
Summary:        System handling for proprietary drivers

Group:          System Environment/Base
License:        GPLv2
URL:            https://github.com/kororaproject/kp-pharlap
Source0:        %{name}-%{version}.tar.gz
Requires:       python3
BuildArch:      noarch
BuildRequires:  python3-devel desktop-file-utils

Requires:       dnf >= 1.1
Requires:       pharlap-modaliases
Requires:       dnfdaemon python3-dnfdaemon
Requires:       polkit
Requires:       python3-lens >= 0.8
Requires(post):     policycoreutils-python
Requires(postun):   policycoreutils-python

%description
Common driver handler for additional devices.


%prep
%setup -q

%install
mkdir -p %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor

mkdir -p %{buildroot}%{_datadir}/%{name}/detect
mkdir -p %{buildroot}%{_datadir}/%{name}/quirks

mkdir -p %{buildroot}%{_datadir}/applications

mkdir -p %{buildroot}%{python3_sitelib}/Pharlap
mkdir -p %{buildroot}%{python3_sitelib}/Quirks
mkdir -p %{buildroot}%{python3_sitelib}/NvidiaDetector

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d

install -m 0755 pharlap-modalias-generator.py %{buildroot}%{_datadir}/%{name}/pharlap-modalias-generator

install -m 0755 pharlap %{buildroot}%{_bindir}/
install -m 0755 pharlap-cli %{buildroot}%{_bindir}/

install -m 0644 detect-plugins/* %{buildroot}%{_datadir}/%{name}/detect/
install -m 0644 quirks/* %{buildroot}%{_datadir}/%{name}/quirks/

install -m 0755 share/fake-devices-wrapper %{buildroot}%{_datadir}/%{name}/fake-devices-wrapper
install -m 0644 share/obsolete %{buildroot}%{_datadir}/%{name}/obsolete

install -m 0644 Pharlap/* %{buildroot}%{python3_sitelib}/Pharlap/
install -m 0644 Quirks/* %{buildroot}%{python3_sitelib}/Quirks/
install -m 0644 NvidiaDetector/* %{buildroot}%{python3_sitelib}/NvidiaDetector/

install -m 0644 COPYING %{buildroot}%{_datadir}/%{name}/COPYING
install -m 0644 README %{buildroot}%{_datadir}/%{name}/README

install -m 0644 pharlap.desktop %{buildroot}%{_datadir}/applications/pharlap.desktop

install -m 0644 modalias/pharlap-modalias.map %{buildroot}%{_datadir}/%{name}/pharlap-modalias.map

cp -a icons/* %{buildroot}%{_datadir}/icons/hicolor/

cp -r data/* %{buildroot}%{_datadir}/%{name}


install -m 0644 dbus/org.kororaproject.Pharlap.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 0644 dbus/org.kororaproject.Pharlap.service %{buildroot}%{_datadir}/dbus-1/system-services/
install -m 0755 pharlapd %{buildroot}%{_datadir}/%{name}/
install -m 0644 polkit/org.kororaproject.Pharlap.policy %{buildroot}%{_datadir}/polkit-1/actions/

# validate desktop files
desktop-file-validate %{buildroot}%{_datadir}/applications/pharlap.desktop

%clean
rm -rf %{buildroot}

%post
semanage fcontext -a -t rpm_exec_t '%{_datadir}/%{name}/pharlapd' 2>/dev/null || :
restorecon -R %{_datadir}/%{name}/pharlapd || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  semanage fcontext -d -t rpm_exec_t '%{_datadir}/%{name}/pharlapd' 2>/dev/null || :

  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%package -n pharlap-modaliases
Summary:        Modalias to package map for the Pharlap
Group:          System Environment/Base

%description -n pharlap-modaliases
Modalias to package map for the Pharlap.

%files -n pharlap-modaliases
%{_datadir}/%{name}/pharlap-modalias.map


%files
%{_datadir}/dbus-1/system-services/org.kororaproject.Pharlap*
%{_datadir}/%{name}/
%exclude %{_datadir}/%{name}/pharlap-modalias.map
%{_datadir}/polkit-1/actions/org.kororaproject.Pharlap*
# this should not be edited by the user, so no %%config
%{_sysconfdir}/dbus-1/system.d/org.kororaproject.Pharlap*

%{_datadir}/%{name}/*
%{_bindir}/pharlap
%{_bindir}/pharlap-cli
%{_datadir}/applications/pharlap.desktop
%{python3_sitelib}/Pharlap/
%{python3_sitelib}/Quirks/
%{python3_sitelib}/NvidiaDetector/
%{_datadir}/icons/hicolor/*/*/*

%changelog
* Wed Aug 19 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.4-1
- Fixed cache generation in line with latest DNF changes.

* Mon Jul 27 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.3-2
- Remove duplicate control center entries.

* Fri Jul 24 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.3-1
- Updated modalias map and ensure resilience to older maps.

* Mon Feb 02 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.2-1
- Fixed missing DBus signals for daemon.

* Fri Jan 30 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.1-1
- Fixed defunct process in pharlapd and cleaned console output.

* Wed Jan 28 2015 Ian Firns <firnsy@kororaproject.org> - 1.4.0-1
- New pharlap daemon for system configuration management.

* Mon Jan 26 2015 Chris Smart <csmart@kororaproject.org> - 1.3.4-1
- Support for NVIDIA 340 series drivers thanks to RPMFusion
- Copy in correct generator script

* Tue Jan 20 2015 Chris Smart <csmart@kororaproject.org> - 1.3.3-1
- Add generic hwinfo icon for themes that have none.

* Tue Dec 30 2014 Ian Firns <firnsy@kororaproject.org> - 1.3.2-1
- Updated pharlap-cli for new modules.
- No -modalias dependency

* Mon Dec 15 2014 Ian Firns <firnsy@kororaproject.org> - 1.3.1-1
- Updated to latest upstream using lens system information

* Sun Dec 14 2014 Chris Smart <csmart@kororaproject.org> - 1.3-2
- Convert yum deps to dnf deps

* Sat Dec 13 2014 Ian Firns <firnsy@kororaproject.org> - 1.3-1
- Updated to latest upstream with package update support

* Wed Dec 10 2014 Chris Smart <csmart@kororaproject.org> - 1.2-1
- New code based, requires python3 and lens

* Sat Nov 23 2013 Chris Smart <csmart@kororaproject.org> - 1.1-2
- Add desktop file, dependency on pharlap-modaliases

* Sat Jul 13 2013 Ian Firns <firnsy@kororaproject.org> - 1.1-1
- Changed namespace to pharlap.

* Sat Jul 13 2013 Ian Firns <firnsy@kororaproject.org> - 1.0-1
- Initial spec.

