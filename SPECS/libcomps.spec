%define __cmake_in_source_build 1

Name:           libcomps
Version:        0.1.18
Release:        1%{?dist}
Summary:        Comps XML file manipulation library

License:        GPLv2+
URL:            https://github.com/rpm-software-management/libcomps
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  check-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s) modification.

%package devel
Summary:        Development files for libcomps library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libcomps library.

%package doc
Summary:        Documentation files for libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  doxygen

%description doc
Documentation files for libcomps library.

%package -n python-%{name}-doc
Summary:        Documentation files for python bindings libcomps library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
BuildRequires:  python3-sphinx


%description -n python-%{name}-doc
Documentation files for python bindings libcomps library.

%package -n python3-%{name}
Summary:        Python 3 bindings for libcomps library
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
Python3 bindings for libcomps library.

%prep
%autosetup -n %{name}-%{version} -p1

mkdir build-py3
mkdir build-doc

%build
pushd build-py3
  %cmake ../libcomps/
  %make_build
popd

pushd build-doc
  %cmake ../libcomps/
  make %{?_smp_mflags} docs
  make %{?_smp_mflags} pydocs
popd

%install
pushd build-py3
  %make_install
popd

%check
pushd build-py3
  make test
  make pytest
popd

%if %{undefined ldconfig_scriptlets}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files doc
%doc build-doc/docs/libcomps-doc/html

%files -n python-%{name}-doc
%doc build-doc/src/python/docs/html

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Nov 09 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.18-1
- Update to 0.1.18
- Fix issues detected by static analyzers
- Remove Python 2 support

* Fri May 21 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.16-2
- Backport patch: Don't print empty requires

* Fri Apr 30 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.16-1
- Update to 0.1.16
- Make inline function __comps_objmrtree_all also static (RhBug:1793424)
- Fix memory leaks and resource leaks
- Fix: Check result "comps_parse_parsed_init()"

* Thu Jan 14 2021 Nicola Sella <nsella@redhat.com> - 0.1.11-5
- Use already implemented clear for COMPS_HSList (RhBug:1888343)

* Mon Jan 13 2020 Ales Matej <amatej@redhat.com> - 0.1.11-4
- Do not skip type=mandatory in xml output (RhBug:1771224)

* Wed Nov 13 2019 Ales Matej <amatej@redhat.com> - 0.1.11-3
- Fix segfault caused by empty dict created by *_by_lang in python api (RhBug:1757959)

* Thu Aug 01 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.11-2
- Backport patch: Fix order of asserts in unit test (RhBug:1713220)

* Mon May 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.1.11-1
- Update to 0.1.11

* Thu Dec 13 2018 Daniel Mach <dmach@redhat.com> - 0.1.8-13
- Fix resource leaks, double free, unused code, optimize
- Resolves: rhbz#1606974

* Mon Jun 25 2018 Lumír Balhar <lbalhar@redhat.com> - 0.1.8-12
- Disable Python 2 subpackage (and dependent) by default

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-10
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.8-9
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-8
- Remove platform-python subpackage

* Fri Sep 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-7
- Disable platform python on old releases

* Thu Aug 10 2017 Lumír Balhar <lbalhar@redhat.com> - 0.1.8-6
- Add Platform Python subpackage (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.1.8-2
- Rebuild for Python 3.6

* Thu Sep 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.7-6
- Add %%{?system_python_abi}

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.7-4
- Adopt to new packaging guidelines
- Use %%license macro
- Fix file ownerships

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.1.7-2
- Rebuilt for Python3.5 rebuild

* Thu Jul 02 2015 Jindrich Luza <jluza@redhat.com> 0.1.7
- added langpacks to union process
- comps DOCTYPE read-write-read fix
- support biarchonly attribute
- fixed rhbz#1073885 rhbz#1073890 rhbz#1073907 rhbz#1073979
- fix rhbz#1073079
- comps_*_match() now support fnmatching
- added libpycomps.MATCH_IGNORECASE as matching flag
- added group.packages_match
- added comps.groups_match, comps.categories_match, comps.entironments_match
- PyCOMPS_Package hash
- cmake-2.6, python-2.6, RHEL-6 compatible
- '_arch' attribute change to 'arch'
- empty 'arch' attribute will be ommited from output from now

* Wed Jan 29 2014 Jindrich Luza <jluza@redhat.com> 0.1.6
- version bumped
- added libcomps.MDict.keys()
-         libcomps.MDict.values()
-         libcomps.MDict.items()
-         libcomps.MDict.clear()
-         libcomps.MDict.update()
-         libcomps.MDict.copy()
- COMPS_List replaced with COMPS_HSList
- added missing basearchonly to DocGroupPackage
- python3/CMakeLists.txt fixed
- added explicit attributes support for xml options
- added arch_filter test for python
- insert method in libcomps.Sequence
- Unioning is now accomplished with replace x append policy
- Weaker package equality check (comparing only name now)
- Fixed leeks in unioning
- modified test_merge_comps test_libcomps
- dictionaries are now storing keys in alphabetical order
- comps parser redesigned
- change python/tests directory composition
- added elem attributes check in parser
- xml output '_arch' attribute support
- parser and xml output defaults options for specify defaults values
- comps object validation in python
- added validity checker before append/set object to list (python only)
- .validate() method
- added libcomps.Dict.keys
-         libcomps.Dict.values
-         libcomps.Dict.items
-         libcomps.Dict.clear
-         libcomps.Dict.update
-         libcomps.Dict.copy
- added xml output options (comps.xml_str([options = {}]), comps.xml_f(options = {}))

* Wed Oct 23 2013 Jindrich Luza <jluza@redhat.com> 0.1.4-4
- group.uservisible is true by default now.
- fixed comps_mobjradix parent node problem
- implemented bindings for blacklist, whiteout and langpacks
- COMPS_Logger redesigned

* Tue Oct 08 2013 Jindrich Luza <jluza@redhat.com> 0.1.5
- version bump
- PyCOMPS_Sequence.__getitem__["objectid"] implemented for libcomps.GroupList, libcomps.CategoryList, libcomps.EnvList
- added missing files
- missing display_order fix for libcomps.Environment

* Tue Oct 01 2013 Jindrich Luza <jluza@redhat.com> 0.1.4
- added missing files
- architectural redesign finished
- fixed #1003986 by Gustavo Luiz Duarte guidelines (but not tested on ppc)
- fixed bug #1000449
- fixed bug #1000442
- added GroupId.default test
- some minor unreported bugs discovered during testing fixed
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log
- version bumped. Python bindings is now easier.
- added missing files

* Tue Aug 20 2013 Jindrich Luza <jluza@redhat.com> 0.1.3
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log
- finished default attribute support in groupid object
- Comps.get_last_parse_errors and Comps.get_last_parse_log has been renamed
-   as Comps.get_last_errors and Comps.get_last_log

* Thu Jul 18 2013 Jindrich Luza <jluza@redhat.com> 0.1.2
- automatic changelog system
- fixed issue #14
- libcomps.Dict is now behave more like python dict. Implemented iter(libcomps.Dict)
- libcomps.iteritems() and libcomps.itervalues()
- remaked error reporting system.
-     libcomps.Comps.fromxml_f and libcomps.Comps.fromxml_str now return
-     -1, 0 or 1. 0 means parse procedure completed without any problem,
-     1 means there's some errors or warnings but not fatal. -1 indicates
-     fatal error problem (some results maybe given, but probably incomplete
-     and invalid)
- errors catched during parsing can be obtained by calling
-     libcomps.Comps.get_last_parse_errors
- all log is given by
-     libcomps.Comps.get_last_parse_log
- prop system complete
- fixed issue 1
- fixed issue 3
- added <packagereq requires=...> support
- new prop system in progress....
- separated doc package
- some minor fixes in CMakeFiles
- improved integrated tests

* Tue Jun 25 2013 Jindrich Luza <jluza@redhat.com> 0.1.1-1
- Automatic commit of package [libcomps] release [0.1.1-1].

