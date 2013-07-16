Name:           korora-drivers-common
Version:        1.0
Release:        1%{?dist}
Summary:        Script to move cache files in homedir to tmpfs

Group:          System Environment/Base
License:        GPLv2
URL:            https://github.com/xtaran/unburden-home-dir
Source0:        %{name}-%{version}.tar.gz
Requires:       python
BuildArch:      noarch
#Requires:       yumdaemon
BuildRequires:  python2-devel

%description
Common driver handler for additional devices.

%prep
%setup -q

echo "WOOT: " %{python_sitelib}

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/detect
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks

mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/KororaDrivers
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/Quirks
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/NvidiaDetector

install -m 0755 korora-drivers $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 korora-drivers-cli $RPM_BUILD_ROOT%{_bindir}/

install -m 0755 korora-drivers-modalias-generator.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/korora-drivers-modalias-generator

install -m 0644 detect-plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/detect/
install -m 0644 quirks/* $RPM_BUILD_ROOT%{_datadir}/%{name}/quirks/

install -m 0755 share/fake-devices-wrapper $RPM_BUILD_ROOT%{_datadir}/%{name}/fake-devices-wrapper
install -m 0644 share/obsolete $RPM_BUILD_ROOT%{_datadir}/%{name}/obsolete

install -m 0644 KororaDrivers/* $RPM_BUILD_ROOT%{python_sitelib}/KororaDrivers/
install -m 0644 Quirks/* $RPM_BUILD_ROOT%{python_sitelib}/Quirks/
install -m 0644 NvidiaDetector/* $RPM_BUILD_ROOT%{python_sitelib}/NvidiaDetector/

install -m 0644 COPYING $RPM_BUILD_ROOT%{_datadir}/%{name}/COPYING
install -m 0644 README $RPM_BUILD_ROOT%{_datadir}/%{name}/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/%{name}/
%{_bindir}/korora-drivers
%{_bindir}/korora-drivers-cli
%{python_sitelib}/KororaDrivers/
%{python_sitelib}/Quirks/
%{python_sitelib}/NvidiaDetector/

%changelog
* Sat Jul 13 2013 Ian Firns <firnsy@kororaproject.org> - 1.0-1
- Initial spec.

