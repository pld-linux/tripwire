Summary:	Verifies file integrity.
Summary(pl):	Program sprawdza poprawnosc plikow. 
Name:		tripwire
Version:	1.2
Release:	1
License:	BSD
Group:		Utilities/System
Group(pl):	Narzedzia/System
Source0:	ftp://ftp.cert.org/pub/tools/tripwire/tripwire-1.2.tar.Z
Source1:	tripwire.verify
Patch0:		tripwire-1.2-rhlinux.patch
Patch1:		tripwire-1.2-latin1.patch
Patch2:		tripwire-1.2-rewind.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
#BuildRoot:	/tmp/%{name}-%{version}-root-%(id -u -n)

%define		_cron		%{_sysconfdir}/cron.daily

%description
Tripwire is a file integrity checker - a utility that compares a
designated set of files and directories against information stored in
a previously generated database.  Added or deleted files are flagged
and reported, as are any files that have changed from their previously
recorded state in the database.  When run against system files on a
regular basis, any file changes would be spotted when Tripwire is next
run, giving system administrators information to enact damage control
measures immediately.


%description -l pl
Tripwire to narz�dzie do sprawdzania poprawno�ci plik�w i katalog�w
 na podstawie wygenerowanej bazy danych.


%prep
%setup -q -c
tar -C .. -xf T1.2.tar
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -ggdb"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/{man1,man5,man8}}
install -d $RPM_BUILD_ROOT{%{_var}/spool/%{name},%{_cron}}
make MANDIR="$RPM_BUILD_ROOT%{_mandir}" TOPDIR="$RPM_BUILD_ROOT" install
install lib/tw.config $RPM_BUILD_ROOT/%{_sysconfdir}
install $RPM_SOURCE_DIR/%{name}.verify $RPM_BUILD_ROOT/%{_cron} 

gzip -9nf FAQ Changelog INTERNALS README README.FIRST Readme TODO \
 WHATSNEW docs/* $RPM_BUILD_ROOT%{_mandir}/{man5,man8}/* 


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(700,root,root) %{_sbindir}/*
%attr(600,root,root) %{_sysconfdir}/tw.config
%attr(700,root,root) %{_var}/spool/%{name}
%attr(700,root,root) %{_cron}/%{name}.verify
%doc *.gz docs/*
%{_mandir}/man*/*