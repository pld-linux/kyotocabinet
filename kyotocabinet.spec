#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Straightforward implementation of DBM
Summary(pl.UTF-8):	Bezpośrednia implementacja DBM
Name:		kyotocabinet
Version:	1.2.77
Release:	1
License:	GPL v3+ with FOSS exception
Group:		Libraries
Source0:	https://fallabs.com/kyotocabinet/pkg/%{name}-%{version}.tar.gz
# Source0-md5:	0f1fa6d10cb5501ebc0ad6ded7a90f68
URL:		https://fallabs.com/kyotocabinet/
BuildRequires:	libstdc++-devel
BuildRequires:	lzo-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kyoto Cabinet is a library of routines for managing a database. The
database is a simple data file containing records, each is a pair of a
key and a value. Every key and value is serial bytes with variable
length. Both binary data and character string can be used as a key and
a value. Each key must be unique within a database. There is neither
concept of data tables nor data types. Records are organized in hash
table or B+ tree.

%description -l pl.UTF-8
Kyoto Cabinet to biblioteka procedur do zarządzania bazą danych. Baza
danych jest prostym plikiem danych zawierającym rekordy, z których
każdy jest parą składającą się z klucza i wartości. Każdy klucz i
wartość to szereg bajtów o zmiennej długości. Jako klucze i wartości
mogą być używane dane binarne i znakowe. Każdy klucz musi być
unikatowy w bazie danych. Nie ma pojęcia tabel ani typów danych.
Rekordy są przechowywane w tablicy haszującej lub B+-drzewie.

%package libs
Summary:	Shared library for Kyoto Cabinet
Summary(pl.UTF-8):	Biblioteka współdzielona Kyoto Cabinet
Group:		Libraries

%description libs
Shared library for Kyoto Cabinet.

%description libs -l pl.UTF-8
Biblioteka współdzielona Kyoto Cabinet.

%package devel
Summary:	Header files for kyotocabinet library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki kyotocabinet
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	zlib-devel

%description devel
Header files for kyotocabinet library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki kyotocabinet.

%package static
Summary:	Static kyotocabinet library
Summary(pl.UTF-8):	Statyczna biblioteka kyotocabinet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static kyotocabinet library.

%description static -l pl.UTF-8
Statyczna biblioteka kyotocabinet.

%package doc
Summary:	Kyoto Cabinet documentation
Summary(pl.UTF-8):	Dokumentacja biblioteki Kyoto Cabinet
Group:		Documentation

%description doc
Kyoto Cabinet documentation.

%description doc -l pl.UTF-8
Dokumentacja biblioteki Kyoto Cabinet.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}/doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/{COPYING,ChangeLog,FOSSEXCEPTION}

install -d $RPM_BUILD_ROOT%{_datadir}/idl/kyotocabinet
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}/kyotocabinet.idl $RPM_BUILD_ROOT%{_datadir}/idl/kyotocabinet/kyotocabinet.idl

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FOSSEXCEPTION README
%attr(755,root,root) %{_bindir}/kcdirmgr
%attr(755,root,root) %{_bindir}/kcforestmgr
%attr(755,root,root) %{_bindir}/kchashmgr
%attr(755,root,root) %{_bindir}/kcpolymgr
%attr(755,root,root) %{_bindir}/kctreemgr
%attr(755,root,root) %{_bindir}/kcutilmgr
%attr(755,root,root) %{_bindir}/kc*test
%{_mandir}/man1/kc*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkyotocabinet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkyotocabinet.so.16

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkyotocabinet.so
%{_includedir}/kc*.h
%{_pkgconfigdir}/kyotocabinet.pc
%{_datadir}/idl/kyotocabinet
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libkyotocabinet.a
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/{api,*.{css,html,png}}
