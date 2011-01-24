# TODO:
# - use shared STLport, not included one...
# - post install
# - cron scripts (contrib)
#
# Conditional build:
%bcond_without	static	# don't link statically
#
Summary:	Verifies file integrity
Summary(pl.UTF-8):	Program sprawdza poprawność plików
Name:		tripwire
Version:	2.4.2
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/tripwire/%{name}-%{version}-src.tar.bz2
# Source0-md5:	c174df418df13d5a97dbeaea9d544a25
Source1:	%{name}.verify
Source2:	%{name}-tw.cfg
Patch0:		%{name}-sec.patch
URL:		http://sourceforge.net/projects/tripwire/
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

%description -l pl.UTF-8
Tripwire to narzędzie do sprawdzania poprawności plików i katalogów na
podstawie wygenerowanej bazy danych.

%prep
%setup -q -n %{name}-%{version}-src

%build
%configure
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
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tw.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc MAINTAINERS ChangeLog TRADEMARK policy/policyguide.txt
%attr(700,root,root) %{_sbindir}/*
%dir %attr(700,root,root) %{_sysconfdir}/%{name}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/twpol.txt
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tw.cfg
%attr(700,root,root) %{_var}/spool/%{name}
%attr(700,root,root) %{_var}/lib/%{name}
%attr(700,root,root) %{_cron}/%{name}.verify
%{_mandir}/man*/*
