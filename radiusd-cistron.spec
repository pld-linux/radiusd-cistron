# $Revision: 1.2 $
Summary:	RADIUS Server 
Name:		radiusd-cistron
Version:	1.6.1
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	GPL
Source0:	%{name}-%{version}-stable.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.initd
Source3:	%{name}.log
URL:		http://www.miquels.cistrom.nl/radius
BuildRoot:	/tmp/%{name}-%{version}-root
Provides:	radius
Obsoletes:	radius

%description
RADIUS server with a lot of functions. Short overview: 

- PAM support
- Supports access based on huntgroups
- Multiple DEFAULT entries in users file
- All users file entries can optionally "fall through"
- Caches all config files in-memory
- Keeps a list of logged in users (radutmp file)
- "radwho" program can be installed as "fingerd"
- Logs both UNIX "wtmp" file format and RADIUS detail logfiles
- Supports Simultaneous-Use = X parameter. Yes, this means
  that you can now prevent double logins!

%prep
%setup -q -n %{name}-%{version}-stable
%build
cd src
make PAM=-DPAM PAMLIB="-lpam -ldl" CFLAGS="$RPM_OPT_FLAGS"
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{raddb,logrotate.d,rc.d/init.d,pam.d},var/log/radacct}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

cd src
make install BINDIR="$RPM_BUILD_ROOT%{_bindir}" SBINDIR="$RPM_BUILD_ROOT%{_sbindir}"
cd ..

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/radius
install %{SOURCE3}	$RPM_BUILD_ROOT/etc/logrotate.d/radius

install raddb/* 	$RPM_BUILD_ROOT%{_sysconfdir}/raddb
install doc/*.1		$RPM_BUILD_ROOT%{_mandir}/man1
install doc/*.8		$RPM_BUILD_ROOT%{_mandir}/man8
install doc/builddbm.8rad	$RPM_BUILD_ROOT%{_mandir}/man8/builddbm.5
install doc/clients.5rad	$RPM_BUILD_ROOT%{_mandir}/man5/clients.5
install doc/naslist.5rad	$RPM_BUILD_ROOT%{_mandir}/man5/naslist.5

touch 			$RPM_BUILD_ROOT/var/log/radutmp
touch 			$RPM_BUILD_ROOT/var/log/radwtmp
touch 			$RPM_BUILD_ROOT/var/log/radius.log

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	doc/{ChangeLog,README,README.pam,README.proxy} \
	doc/{README.usersfile,README.simul,INSTALL.OLD} \
	doc/{Makefile.README,README.cisco} \
	{COPYRIGHT.Cistron,COPYRIGHT.Livingston,todo/*}

%post
touch /var/log/radutmp
touch /var/log/radwtmp
/sbin/chkconfig --add radius
if test -r /var/lock/subsys/radius; then
	/etc/rc.d/init.d/radius stop >&2
	/etc/rc.d/init.d/radius start >&2
else
	echo "Run \"/etc/rc.d/init.d/radius start\" to start radius daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/radius stop >&2
	/sbin/chkconfig --del radius
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{ChangeLog,README,README.pam,README.proxy}.gz
%doc doc/{README.usersfile,README.simul,INSTALL.OLD}.gz
%doc doc/{Makefile.README,README.cisco}.gz
%doc {COPYRIGHT.Cistron,COPYRIGHT.Livingston,todo/*}.gz

%attr(750,root,root) %dir /var/log/radacct
%attr(750,root,root) %dir %{_sysconfdir}/raddb

%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/raddb/*

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/*/*

%attr(754,root,root) /etc/rc.d/init.d/radius
%attr(640,root,root) /etc/logrotate.d/radius

%attr(640,root,root) %ghost /var/log/radutmp
%attr(640,root,root) %ghost /var/log/radwtmp
%attr(640,root,root) %ghost /var/log/radius.log
