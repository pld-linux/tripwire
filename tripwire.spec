#
# TODO:
# - use shared STLport, not included one...
# - some nice way to install :-/
#
# Conditional build:
%bcond_without	static	# don't link statically
#
Summary:	Verifies file integrity
Summary(pl):	Program sprawdza poprawno¶æ plikow
Name:		tripwire
Version:	2.3.1
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/tripwire/%{name}-%{version}-2.tar.gz
# Source0-md5:	6a15fe110565cef9ed33c1c7e070355e
Source1:	%{name}.verify
Patch0:		%{name}-sec.patch
URL:		http://www.tripwire.org/
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	bison
BuildRequires:	flex
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

%description -l pl
Tripwire to narzêdzie do sprawdzania poprawno¶ci plików i katalogów na
podstawie wygenerowanej bazy danych.


%prep
%setup -q -n %{name}-%{version}-2
%patch0 -p0

%build
cd src
%{__make} release \
	GMAKE=make \
	CXX="%{__cxx}" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/{man1,man5,man8}}
install -d $RPM_BUILD_ROOT{%{_var}/spool/%{name},%{_cron}}

cd src
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install lib/tw.config $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_cron}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog MAINTAINERS README Release_Notes TRADEMARK  WISHLIST
#%attr(700,root,root) %{_sbindir}/*
#%attr(600,root,root) %{_sysconfdir}/tw.config
#%attr(700,root,root) %{_var}/spool/%{name}
%attr(700,root,root) %{_cron}/%{name}.verify
#%{_mandir}/man*/*
