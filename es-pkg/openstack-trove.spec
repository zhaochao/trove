%global release_name mitaka
%global service trove
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 0

%global dist_eayunstack .eayunstack.dev

Name:             openstack-%{service}
Epoch:            1
Version:          6.0.0
Release:          4%{?dist_eayunstack}
Summary:          OpenStack DBaaS (%{service})

License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Trove
Source0:          http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source1:          %{service}.logrotate
Source2:          guest_info

Source10:         %{name}-api.service
Source11:         %{name}-taskmanager.service
Source12:         %{name}-conductor.service
Source13:         %{name}-guestagent.service

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr >= 1.8
BuildRequires:    python-d2to1
BuildRequires:    python-sphinx
BuildRequires:    crudini
BuildRequires:    intltool

Requires:         %{name}-api = %{epoch}:%{version}-%{release}
Requires:         %{name}-taskmanager = %{epoch}:%{version}-%{release}
Requires:         %{name}-conductor = %{epoch}:%{version}-%{release}


%description
OpenStack DBaaS (codename %{service}) provisioning service.

%package common
Summary:          Components common to all OpenStack %{service} services

Requires:         python-%{service} = %{epoch}:%{version}-%{release}

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd

Requires(pre):    shadow-utils
Requires:         python-pbr >= 1.8

%description common
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains scripts, config and dependencies shared
between all the OpenStack %{service} services.


%package api
Summary:          OpenStack %{service} API service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description api
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains the %{service} interface daemon.


%package taskmanager
Summary:          OpenStack %{service} taskmanager service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description taskmanager
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains the %{service} taskmanager service.


%package conductor
Summary:          OpenStack %{service} conductor service
Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description conductor
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains the %{service} conductor service.


%package guestagent
Summary:          OpenStack %{service} guest agent
%if 0%{?rhel}
Requires:         pexpect
%else
Requires:         python-pexpect
%endif
Requires:         python-netifaces

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description guestagent
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains the %{service} guest agent service
that runs within the database VM instance.


%package -n       python-%{service}
Summary:          Python libraries for %{service}

Requires:         MySQL-python

Requires:         python-kombu

Requires:         python-eventlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-six >= 1.9.0
Requires:         python-stevedore >= 1.5.0
Requires:         python-xmltodict >= 0.10.1

Requires:         python-webob >= 1.2.3
Requires:         python-migrate >= 0.9.6

Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-routes

Requires:         python-troveclient
Requires:         python-cinderclient >= 1.6.0
Requires:         python-designateclient >= 2.0.0
Requires:         python-heatclient >= 1.0.0
Requires:         python-keystoneclient >= 1:2.3.1
Requires:         python-keystonemiddleware >= 4.3.0
Requires:         python-neutronclient >= 4.1.1
Requires:         python-novaclient >= 3.3.0
Requires:         python-swiftclient >= 3.0.0

Requires:         python-oslo-concurrency >= 3.6.0
Requires:         python-oslo-config >= 2:3.9.0
Requires:         python-oslo-context >= 0.2.0
Requires:         python-oslo-db >= 4.6.0
Requires:         python-oslo-i18n >= 3.4.0
Requires:         python-oslo-log >= 3.2.0
Requires:         python-oslo-messaging >= 4.5.0
Requires:         python-oslo-middleware >= 3.7.0
Requires:         python-oslo-serialization >= 2.4.0
Requires:         python-oslo-service >= 1.7.0
Requires:         python-oslo-utils >= 3.7.0

Requires:         python-osprofiler >= 1.2.0
Requires:         python-jsonschema
Requires:         python-babel
Requires:         python-jinja2

Requires:         python-httplib2
Requires:         python-passlib

%description -n   python-%{service}
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains the %{service} python library.

%package -n python-%{service}-tests
Summary:        Trove tests
Requires:       python-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
This package contains the Trove test files

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack %{service}


%description      doc
OpenStack DBaaS (codename %{service}) provisioning service.

This package contains documentation files for %{service}.
%endif

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Avoid non-executable-script rpmlint while maintaining timestamps
find %{service} -name \*.py |
while read source; do
  if head -n1 "$source" | grep -F '/usr/bin/env'; then
    touch --ref="$source" "$source".ts
    sed -i '/\/usr\/bin\/env python/{d;q}' "$source"
    touch --ref="$source".ts "$source"
    rm "$source".ts
  fi
done

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

%if 0%{?with_doc}
pushd doc

SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd
%endif

# Setup directories
%if 0%{?rhel} != 6
install -d -m 755 %{buildroot}%{_unitdir}
%endif
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 750 %{buildroot}%{_localstatedir}/log/%{service}

# Install config files
install -p -D -m 640 etc/%{service}/%{service}.conf.sample %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
# Use crudini to set some configuration keys
crudini --set %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf database connection mysql://trove:trove@localhost/trove
crudini --set %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf DEFAULT log_file %{_localstatedir}/log/%{service}/%{service}.log
install -p -D -m 644 etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 etc/%{service}/trove-taskmanager.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-taskmanager.conf
install -p -D -m 640 etc/%{service}/trove-conductor.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-conductor.conf
install -p -D -m 640 etc/%{service}/trove-guestagent.conf.sample %{buildroot}%{_sysconfdir}/%{service}/trove-guestagent.conf
install -p -D -m 660 etc/%{service}/trove-guestagent-monitoring.ini %{buildroot}%{_sysconfdir}/%{service}/trove-guestagent-monitoring.ini
install -p -D -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{service}/guest_info

# Install initscripts
%if 0%{?rhel} == 6
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_initrddir}/%{name}-taskmanager
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/%{name}-conductor
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_initrddir}/%{name}-guestagent
install -p -m 755 %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{buildroot}%{_datadir}/%{service}
%else
install -p -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{buildroot}%{_unitdir}
%endif

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Remove unneeded in production stuff
rm -fr %{buildroot}%{_bindir}/trove-fake-mode
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
%pre common
# Origin: http://fedoraproject.org/wiki/Packaging:UsersAndGroups#Dynamic_allocation
USERNAME=%{service}
GROUPNAME=$USERNAME
HOMEDIR=%{_sharedstatedir}/$USERNAME
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
    -c "$USERNAME Daemons" $USERNAME
exit 0

%post api
%systemd_post openstack-trove-api.service
%post taskmanager
%systemd_post openstack-trove-taskmanager.service
%post conductor
%systemd_post openstack-trove-conductor.service
%post guestagent
%systemd_post openstack-trove-guestagent.service

%preun api
%systemd_preun openstack-trove-api.service
%preun taskmanager
%systemd_preun openstack-trove-taskmanager.service
%preun conductor
%systemd_preun openstack-trove-conductor.service
%preun guestagent
%systemd_preun openstack-trove-guestagent.service

%postun api
%systemd_postun_with_restart openstack-trove-api.service
%postun taskmanager
%systemd_postun_with_restart openstack-trove-taskmanager.service
%postun conductor
%systemd_postun_with_restart openstack-trove-conductor.service
%postun guestagent
%systemd_postun_with_restart openstack-trove-guestagent.service


%files
%license LICENSE

%files common
%license LICENSE
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}
%dir %attr(0755, %{service}, root) %{_localstatedir}/run/%{service}

%{_bindir}/%{service}-manage
%{_bindir}/trove-mgmt-taskmanager

%{_datarootdir}/%{service}

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}

%files api
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service

%files taskmanager
%{_bindir}/%{service}-taskmanager
%{_unitdir}/%{name}-taskmanager.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-taskmanager.conf

%files conductor
%{_bindir}/%{service}-conductor
%{_unitdir}/%{name}-conductor.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-conductor.conf

%files guestagent
%{_bindir}/%{service}-guestagent
%{_unitdir}/%{name}-guestagent.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}-guestagent.conf
%config(noreplace) %attr(0660, root, %{service}) %{_sysconfdir}/%{service}/%{service}-guestagent-monitoring.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/guest_info

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-%{version}*.egg-info
%exclude %{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Oct 26 2017 Zhao Chao <chao.zhao@eayun.com> 1:6.0.0-4.eayunstack.dev
- github pull request #29, fixes: redmine #10072
- github pull request #37, fixes: redmine #10087
- github pull request #38, fixes: redmine #10877
- github pull request #39, fixes: redmine #10086
- github pull request #40, fixes: redmine #10917
- github pull request #41, fixes: redmine #9627
- github pull request #42, fixes: redmine #9618
- github pull request #43, fixes: redmine #10798
- github pull request #44, fixes: redmine #11038
- github pull request #45, fixes: redmine #10202
- github pull request #46, fixes: redmine #10272
- github pull request #47, fixes: redmine #10284
- github pull request #48, fixes: redmine #10887
- github pull request #51, fixes: redmine #10278

* Mon Jun 5 2017 Zhao Chao <chao.zhao@eayun.com> 1:6.0.0-3.eayunstack
- fb49139b Wait for replication snapshot status before deleting.
- 540fccb8 Catch exceptions from backup runner
- 6107f345 Add notification for async log publish.
- c303d693 Remove the call of guestagent when _delete_log_files
- 4812aa12 Fix invalid token when log-publish
- 04469124 Fix incorrectly calling _delete_files_from_swift from eventlet spawn_n.
- 6f299f3f Get rid of unnecessary '\r\n' in request body of debug logging.

* Thu Apr 13 2017 Zhao Chao <chao.zhao@eayun.com> 1:6.0.0-2.eayunstack
- fae1707d Support Swift CORS.
- 9267df3b Can't delete instance when using other tenant
- 5a72cece Delete log files in swift when delete instance
- 89f28b60 Can't delete instance when backup
- 72d10ee4 Add files_published_attime to api
- 0ad82a4a Fix log-publish condition
- 95fecaab Convert publish-log to asynchronous
- 493ef180 Fix wrong backup quota when create replca
- 76b29967 Fix api exception with unicode tenant name.
- f736190a Allow use utf8 (visible) characters in object names.
- 80e01816 Can't delete backup when using other tenant
- 6591040c Make root-disable actually work.
- 0e0544d7 Add tenant_id to database logs container name
- 2b989aad Add API log publish status
- 1cbd4483 Initialize BadRequest exception with correct message.
- c1b7ee7b fix unittests for do_prepare in test_mysql_manager.
- 01280eea Fix type introspection in _validate_configuration
- c908461c Support swift_url in the configuration file use radosgw swift
- f0decdbb Clear log file after log-publish
- 8713d2b8 use new NovaClient in single_tenant_remote.
- b9dbd1e9 Make MySQL guestagent setting data_dir correctly in do_prepare.
- 6cdb3c22 Add charset to API list_databases
- 00b53560 Fail on deleting non-existing database
- e6ed64a9 use force delete when delete a instance of trove
- 3e245dcc Fix backup of mysql variants on Centos
- b0a092bb Add tenant_id to backup container name
- c0144e36 Use old methods to backup

* Thu Oct 06 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:6.0.0-1
- Update to 6.0.0

* Fri Sep 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:6.0.0-0.3.0rc2
- Update to 6.0.0.0rc2

* Wed Sep 21 2016 Alfredo Moralejo <amoralej@redhat.com> 1:6.0.0-0.2.0rc1
- Update to 6.0.0.0rc1

* Thu Sep 15 2016 Haikel Guemar <hguemar@fedoraproject.org> 1:6.0.0-0.1.0b3
- Update to 6.0.0.0b3

