# TODO:
# - post install
# - cron scripts (contrib)
#
# Conditional build:
%bcond_without	static	# don't link statically
#
Summary:	Verifies file integrity
Summary(pl.UTF-8):	Program sprawdza poprawność plików
Name:		tripwire
Version:	2.4.3.6
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/Tripwire/tripwire-open-source/archive/%{version}/%{name}-open-source-%{version}.tar.gz
# Source0-md5:	0bd68d1ab2684ab0e78ea3cc05d3a3a8
Source1:	%{name}.verify
Source2:	%{name}-tw.cfg
Source3:	README.SuSE
Patch0:		%{name}-sec.patch
Patch1:		off_t.patch
Patch2:		policyconfig.patch
Patch3:		%{name}-gcc47.patch
URL:		https://github.com/Tripwire/tripwire-open-source
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	libstdc++-devel
Requires:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cron		%{_sysconfdir}/cron.daily

%description
Tripwire is a file integrity checker - a utility that compares a
designated set of files and directories against information stored in
a previously generated database. Added or deleted files are flagged
and reported, as are any files that have changed from their previously
recorded state in the database. When run against system files on a
regular basis, any file changes would be spotted when Tripwire is next
run, giving system administrators information to enact damage control
measures immediately.

%prep
%setup -q -n %{name}-open-source-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
install %{SOURCE3} .

%build
%configure --sysconfdir=/etc/tripwire
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/{man4,man5,man8},%{_sysconfdir}/%{name}}
install -d $RPM_BUILD_ROOT{%{_var}/{spool/%{name},lib/%{name}},%{_cron}}

install bin/* $RPM_BUILD_ROOT%{_sbindir}
install man/man4/*.4 $RPM_BUILD_ROOT%{_mandir}/man4
install man/man5/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install man/man8/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install policy/twpol-Linux.txt $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/twpol.txt
install %{SOURCE1} $RPM_BUILD_ROOT%{_cron}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/twcfg.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc MAINTAINERS ChangeLog README.SuSE TRADEMARK policy/policyguide.txt
%attr(700,root,root) %{_sbindir}/*
%dir %attr(700,root,root) %{_sysconfdir}/%{name}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/twpol.txt
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/twcfg.txt
%attr(700,root,root) %{_var}/spool/%{name}
%attr(700,root,root) %{_var}/lib/%{name}
%attr(700,root,root) %{_cron}/%{name}.verify
%{_mandir}/man*/*
