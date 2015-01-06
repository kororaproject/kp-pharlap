Name:           pharlap
Version:        1.3.1
Release:        2%{?dist}
Summary:        System handling for proprietary drivers

Group:          System Environment/Base
License:        GPLv2
URL:            https://github.com/kororaproject/kp-pharlap
Source0:        %{name}-%{version}.tar.gz
Requires:       python3
BuildArch:      noarch
Requires:       dnfdaemon python3-dnfdaemon python3-hwdata
Requires:       python3-lens >= 0.7.5
BuildRequires:  python3-devel desktop-file-utils

%description
Common driver handler for additional devices.

%prep
%setup -q

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/detect
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

mkdir -p $RPM_BUILD_ROOT%{python3_sitelib}/Pharlap
mkdir -p $RPM_BUILD_ROOT%{python3_sitelib}/Quirks
mkdir -p $RPM_BUILD_ROOT%{python3_sitelib}/NvidiaDetector

install -m 0755 pharlap $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 pharlap-cli $RPM_BUILD_ROOT%{_bindir}/

install -m 0755 pharlap-modalias-generator.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/pharlap-modalias-generator

install -m 0644 detect-plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/detect/
install -m 0644 quirks/* $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks/

install -m 0755 share/fake-devices-wrapper $RPM_BUILD_ROOT%{_datadir}/%{name}/fake-devices-wrapper
install -m 0644 share/obsolete $RPM_BUILD_ROOT%{_datadir}/%{name}/obsolete

install -m 0644 Pharlap/* $RPM_BUILD_ROOT%{python3_sitelib}/Pharlap/
install -m 0644 Quirks/* $RPM_BUILD_ROOT%{python3_sitelib}/Quirks/
install -m 0644 NvidiaDetector/* $RPM_BUILD_ROOT%{python3_sitelib}/NvidiaDetector/

install -m 0644 COPYING $RPM_BUILD_ROOT%{_datadir}/%{name}/COPYING
install -m 0644 README $RPM_BUILD_ROOT%{_datadir}/%{name}/README

install -m 0644 pharlap.desktop %{buildroot}%{_datadir}/applications/pharlap.desktop

cp -r data/* %{buildroot}%{_datadir}/%{name}

# validate desktop files
desktop-file-validate %{buildroot}%{_datadir}/applications/pharlap.desktop
#desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/pharlap.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/%{name}/
%{_bindir}/pharlap
%{_bindir}/pharlap-cli
%{_datadir}/applications/pharlap.desktop
%{python3_sitelib}/Pharlap/
%{python3_sitelib}/Quirks/
%{python3_sitelib}/NvidiaDetector/

%changelog
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

