Summary:	Verifies file integrity
Summary(pl):	Program sprawdza poprawno¶æ plikow
Name:		tripwire
Version:	1.2
Release:	2
License:	BSD
Group:		Applications/System
Source0:	ftp://ftp.cert.org/pub/tools/tripwire/%{name}-%{version}.tar.Z
Source1:	%{name}.verify
Patch0:		%{name}-rhlinux.patch
Patch1:		%{name}-latin1.patch
Patch2:		%{name}-rewind.patch
Patch3:		%{name}-shared.patch
%{?!_without_static:BuildRequires:	glibc-static}
BuildRequires:	byacc
BuildRequires:	flex
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

%description -l pl
Tripwire to narzêdzie do sprawdzania poprawno¶ci plików i katalogów na
podstawie wygenerowanej bazy danych.


%prep
%setup -q -c
tar -C .. -xf T1.2.tar
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{?!_without_static:%{__make} OPT_FLAGS="%{rpmcflags}" static}
%{?_without_static:%{__make} OPT_FLAGS="%{rpmcflags}" shared}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/{man1,man5,man8}}
install -d $RPM_BUILD_ROOT{%{_var}/spool/%{name},%{_cron}}

%{__make} %{?!_without_static:install_static}%{?_without_static:install_shared} \
	MANDIR="$RPM_BUILD_ROOT%{_mandir}" \
	TOPDIR="$RPM_BUILD_ROOT"

install lib/tw.config $RPM_BUILD_ROOT/%{_sysconfdir}
install $RPM_SOURCE_DIR/%{name}.verify $RPM_BUILD_ROOT/%{_cron}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(700,root,root) %{_sbindir}/*
%attr(600,root,root) %{_sysconfdir}/tw.config
%attr(700,root,root) %{_var}/spool/%{name}
%attr(700,root,root) %{_cron}/%{name}.verify
%doc FAQ Changelog INTERNALS README README.FIRST Readme TODO WHATSNEW docs/[a-s]*
%{_mandir}/man*/*
