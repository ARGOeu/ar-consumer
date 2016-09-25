Name: argo-egi-consumer
Summary: A/R Comp Engine message consumer
Version: 1.4.4
Release: 1%{?dist}
License: ASL 2.0
Buildroot: %{_tmppath}/%{name}-buildroot
Group:     EGI/SA4
BuildArch: noarch
Source0:   %{name}-%{version}.tar.gz
Requires: stomppy >= 3.1.6, stomppy < 4
Requires: avro
Obsoletes: ar-consumer

%description
Installs the service for consuming SAM monitoring results
from the EGI message broker infrastructure.

%build
python setup.py build

%prep
%setup -n %{name}-%{version}

%install 
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/etc/init.d
install --directory %{buildroot}/etc/argo-egi-consumer/
install --directory %{buildroot}/%{_sharedstatedir}/argo-egi-consumer/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/argo-egi-consumer.py
%attr(0755,root,root) /etc/init.d/argo-egi-consumer
%attr(0750,arstats,arstats) %{_sharedstatedir}/argo-egi-consumer

%post
/sbin/chkconfig --add argo-egi-consumer

%pre
getent group arstats > /dev/null || groupadd -r arstats
getent passwd arstats > /dev/null || \
    useradd -r -g arstats -d /var/lib/argo-egi-consumer -s /sbin/nologin \
    -c "AR Comp Engine user" arstats

%preun
if [ "$1" = 0 ] ; then
   /sbin/service argo-egi-consumer stop
   /sbin/chkconfig --del argo-egi-consumer
fi

%changelog
* Sun Sep 25 2016 Themis Zamani <themiszamani@gmail.com> - 1.4.4-1%{?dist}
- New RPM package release
* Sat Sep 24 2016 Themis Zamani <themiszamani@gmail.com> - 1.4.3-1%{?dist}
- New RPM package release
* Sun Feb 14 2016 Daniel Vrcic <dvrcic@srce.hr> - 1.4.3-1%{?dist}
- updated README
  https://github.com/ARGOeu/ARGO/issues/182
- consistent log messages between daemon and nofork mode
- plaintext option moved to general section
- log wrong formatted messages
- revised plaintxt extension
- catch keyint in nofork mode
- retention period options as integers
- revised process exiting
- handler for stomppy logger
  https://github.com/ARGOeu/ARGO/issues/186
- config option checks moved to parser class
- DATE placeholder instead of string operator
- refactored writing of messages
- message retention configurable
  https://github.com/ARGOeu/ARGO/issues/185
- package dependancy revised
* Mon Jan 4 2016 Daniel Vrcic <dvrcic@srce.hr> - 1.4.2-1%{?dist}
- configurable logger name
  https://github.com/ARGOeu/ARGO/issues/178
- write also tag keys without values
* Mon Oct 5 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.1-1%{?dist}
- refactoring with introduction of class with shared informations
- report num of msgs written on received SIGTERM too
- report some runtime info on SIGUSR1 received
* Thu Jun 4 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-16%{?dist}
- on config reload, check if broker servers option changed and only then do reconnect
- one msg written report thread, not thread per reconnect
* Fri May 29 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-15%{?dist}
- remove double minuses in init script arguments
  https://github.com/ARGOeu/ARGO/issues/138
* Tue May 26 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-14%{?dist}
- fix multiple connections issues
  https://github.com/ARGOeu/ARGO/issues/137
- plaintext output option instead of debug
- config parser error informed via syslog
* Tue May 26 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-13%{?dist}
- prevent race condition on avro log writing, second try 
* Sun May 24 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-12%{?dist}
- no topics in code, just destinations
* Sun May 24 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-11%{?dist}
- prevention of multiple threads writing to the same avro log
  https://github.com/ARGOeu/ARGO/issues/135
* Fri May 22 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-10%{?dist}
- catch failed writes
- multi instance support
* Wed May 20 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-9%{?dist}
- python 2.6 has slightly different API for StreamHandler logger
* Wed May 20 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-8%{?dist}
- fix cycling to different broker on config reload
* Wed May 20 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-7%{?dist}
- load selectively StreamHandler logger
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-6%{?dist}
- subscribe to new destinations after config reload 
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-5%{?dist}
- renamed package obsoletes old named one
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-4%{?dist}
- prevent multiple threads reporting number of writmsgs
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-3%{?dist}
- reference github issues 
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-2%{?dist}
- remove autogenerated MANIFEST
- added VO topic
* Tue May 19 2015 Daniel Vrcic <dvrcic@srce.hr> - 1.4.0-1%{?dist}
- package and components renamed
- removed plaintxt writer
- refactored source code 
  https://github.com/ARGOeu/ARGO/issues/129
- simplified configuration with case insensitive sections and options
- logging via syslog; report number of written messages
  https://github.com/ARGOeu/ARGO/issues/100
- daemon process privileges dropped via os sys interface
- added SIGHUP, SIGTERM handlers
- fixed bug with messages with paired service types
- setup.py with automatic version catch from spec 
* Fri Jan 30 2015 Luko Gjenero <lgjenero@gmail.com> - 1.3.2-0%{?dist}
- Fixed avro schema typo
* Thu Jan 15 2015 Luko Gjenero <lgjenero@gmail.com> - 1.3.2-0%{?dist}
- Added configs to rpm
* Thu Jan 15 2015 Luko Gjenero <lgjenero@gmail.com> - 1.3.1-0%{?dist}
- Fixes for Avro format + fix for reconneect
* Fri Nov 28 2014 Luko Gjerneo <lgjenero@gmail.com> - 1.3.0-0%{?dist}
- Added Avro format
* Thu Sep 4 2014 Emir Imamagic <eimamagi@srce.hr> - 1.2.1-1%{?dist}
- Consumer detailed files contain messages that split to multiple lines
* Tue Jul 22 2014 Emir Imamagic <eimamagi@srce.hr> - 1.2.0-1%{?dist}
- Add support for multiple file writters
- Add detailed probe results to the output
- Timestamps @ consumer error log file
* Fri Mar 14 2014 Luko Gjenero <lgjenero@srce.hr> - 1.1.1-0%{?dist}
- SSL broker connection
* Mon Nov 4 2013 Paschalis Korosoglou <pkoro@grid.auth.gr> - 1.0.1-2%{?dist}
- Fixes for consumer
* Thu Oct 3 2013 Paschalis Korosoglou <pkoro@grid.auth.gr> - 1.0.1-1%{?dist}
- Updates and fixes for consumer
* Thu Aug 1 2013 Emir Imamagic <eimamagi@srce.hr> - 1.0.0-1%{?dist}
- Initial release
