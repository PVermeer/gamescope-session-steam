# Create an option to build locally without fetchting own repo
# for sourcing and patching
%bcond local 0

# Source repo
%global author pvermeer
%global source gamescope-session-steam
%global sourcerepo https://github.com/PVermeer/gamescope-session-steam
%global tag v0.0.0

Name: gamescope-session-steam
Version: 0.0.0
Release: 0%{?dist}
License: GPL-3.0 license
Summary: Gamescope session for steam
Url: %{sourcerepo}

BuildRequires: systemd-rpm-macros
BuildRequires: git

Requires: steam
Requires: gamescope

%description
A simple gamescope session for steam 

%define workdir %{_builddir}/%{name}
%define sourcedir %{workdir}/%{source}

%prep
# To apply working changes handle sources / patches locally
# COPR should clone the commited changes
%if %{with local}
  # Get sources - local build
  mkdir -p %{sourcedir}
  cp -r %{_topdir}/SOURCES/* %{sourcedir}
%else
  # Get sources - COPR build
  git clone %{sourcerepo} %{sourcedir}
  cd %{sourcedir}
  git reset --hard %{tag}
  cd %{workdir}
%endif

# Do src stuff
cd %{sourcedir}
rm -rf .git
cd %{workdir}

%define license_dir %{_licensedir}/%{name}
%define steam_bin_dir %{_bindir}/steamos-polkit-helpers
%define package_config_dir %{_sysconfdir}/environment.d
%define session_dir %{_datadir}/wayland-sessions

%install
mkdir -p %{buildroot}/%{license_dir}
mkdir -p %{buildroot}/%{steam_bin_dir}
mkdir -p %{buildroot}/%{package_config_dir}
mkdir -p %{buildroot}/%{session_dir}
mkdir -p %{buildroot}/%{_userunitdir}

install -m 0644 %{sourcedir}/LICENSE %{buildroot}/%{license_dir}/LICENSE

install -m 0755 %{sourcedir}/src/jupiter-biosupdate %{buildroot}/%{steam_bin_dir}/
install -m 0755 %{sourcedir}/src/steamos-set-timezone %{buildroot}/%{steam_bin_dir}/
install -m 0755 %{sourcedir}/src/steamos-update %{buildroot}/%{steam_bin_dir}/

install -m 0755 %{sourcedir}/src/%{name} %{buildroot}/%{_bindir}/
install -m 0755 %{sourcedir}/src/steamos-select-branch %{buildroot}/%{_bindir}/
install -m 0755 %{sourcedir}/src/steamos-session-select %{buildroot}/%{_bindir}/

install -m 0644 %{sourcedir}/assets/%{name}.conf %{buildroot}/%{package_config_dir}/
install -m 0644 %{sourcedir}/assets/%{name}.desktop %{buildroot}/%{session_dir}/
install -m 0644 %{sourcedir}/assets/gamescope-session.target %{buildroot}/%{_userunitdir}/

%files
%license %{license_dir}/LICENSE
%{_bindir}/*
%config(noreplace) %{package_config_dir}/*
%{session_dir}/*
%{_userunitdir}/gamescope-session.target
