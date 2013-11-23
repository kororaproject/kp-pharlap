Name:           pharlap
Version:        1.1
Release:        2%{?dist}
Summary:        System handling for proprietary drivers

Group:          System Environment/Base
License:        GPLv2
URL:            https://github.com/kororaproject/kp-pharlap
Source0:        %{name}-%{version}.tar.gz
Requires:       python
BuildArch:      noarch
Requires:       yumdaemon python-yumdaemon pharlap-modaliases
BuildRequires:  python2-devel desktop-file-utils

%description
Common driver handler for additional devices.

%prep
%setup -q

echo "WOOT: " %{python_sitelib}

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/detect
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/Pharlap
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/Quirks
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/NvidiaDetector

install -m 0755 pharlap $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 pharlap-cli $RPM_BUILD_ROOT%{_bindir}/

install -m 0755 pharlap-modalias-generator.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/pharlap-modalias-generator

install -m 0644 detect-plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/detect/
install -m 0644 quirks/* $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks/

install -m 0755 share/fake-devices-wrapper $RPM_BUILD_ROOT%{_datadir}/%{name}/fake-devices-wrapper
install -m 0644 share/obsolete $RPM_BUILD_ROOT%{_datadir}/%{name}/obsolete

install -m 0644 Pharlap/* $RPM_BUILD_ROOT%{python_sitelib}/Pharlap/
install -m 0644 Quirks/* $RPM_BUILD_ROOT%{python_sitelib}/Quirks/
install -m 0644 NvidiaDetector/* $RPM_BUILD_ROOT%{python_sitelib}/NvidiaDetector/

install -m 0644 COPYING $RPM_BUILD_ROOT%{_datadir}/%{name}/COPYING
install -m 0644 README $RPM_BUILD_ROOT%{_datadir}/%{name}/README

install -m 0644 pharlap.desktop %{buildroot}%{_datadir}/applications/pharlap.desktop

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
%{python_sitelib}/Pharlap/
%{python_sitelib}/Quirks/
%{python_sitelib}/NvidiaDetector/

%changelog
* Sat Nov 23 2013 Chris Smart <csmart@kororaproject.org> - 1.1-2
- Add desktop file, dependency on pharlap-modaliases

* Sat Jul 13 2013 Ian Firns <firnsy@kororaproject.org> - 1.1-1
- Changed namespace to pharlap.

* Sat Jul 13 2013 Ian Firns <firnsy@kororaproject.org> - 1.0-1
- Initial spec.

