%define	major %{version}
%define libname	%mklibname oasys %{major}
%define develname %mklibname -d oasys

Summary:	Object-oriented Adaptors to SYStem interfaces library
Name:		oasys
Version:	1.4.0
Release:	%mkrel 2
Group:		System/Libraries
License:	Apache License
URL:		http://sourceforge.net/projects/dtn/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/dtn/%{name}-%{version}.tgz
#Patch0:		oasys-1.3.0-gcc43_fixes.diff
Patch1:		oasys-1.3.0-soname_fixes.diff
# Fix build for Tcl 8.6 (interp->result usage, TIP #330)
Patch2:		oasys-1.3.0-tcl86.patch
BuildRequires:	autoconf
BuildRequires:	db4-devel
BuildRequires:	google-perftools-devel
BuildRequires:	libbluez-devel
BuildRequires:	libexpat-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	tcl-devel
BuildRequires:	xerces-c28-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OASYS is a C++ library that provides a set of wrapper classes and utilities for
systems programming projects.

%package -n	%{libname}
Summary:	Object-oriented Adaptors to SYStem interfaces library
Group:          System/Libraries
Requires:	tcl

%description -n	%{libname}
OASYS is a C++ library that provides a set of wrapper classes and utilities for
systems programming projects.

This package contains the shared oasys library.

%package -n	%{develname}
Summary:	Static library and header files for the oasys library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	xerces-c28-devel

%description -n	%{develname}
OASYS is a C++ library that provides a set of wrapper classes and utilities for
systems programming projects.

This package contains the static oasys library and its header files.

%prep

%setup -q -n %{name}-%{version}
#%patch0 -p1
%patch1 -p0
%patch2 -p1 -b .tcl86

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" aclocal/*

%build
%serverbuild

rm -f configure
autoreconf

%define Werror_cflags %{nil}

export EXTLIB_CFLAGS="%{optflags}"
export EXTLIB_LDFLAGS="%{?ldflags}"

%configure2_5x \
    --disable-atomic-asm \
    --with-python=%{_bindir}/python \
    --with-tcl=%{_prefix} \
%if %mdkversion >= 200810
    --with-tclver=%{tcl_version} \
%else
    --with-tclver=8.4 \
%endif
    --with-google-perftools=%{_prefix} \
    --with-bluez \
    --with-expat=%{_prefix} \
    --with-zlib \
    --disable-eds \
    --with-db=%{_prefix} \
    --with-dbver=4.8
                                                                                                              
make

#check
#make test

%install
rm -rf %{buildroot}

%makeinstall_std

install -m0644 lib/liboasys-%{version}.a %{buildroot}%{_libdir}/
install -m0644 lib/liboasyscompat-%{version}.a %{buildroot}%{_libdir}/

# fix deps
find %{buildroot}%{_includedir}/oasys -type f -exec chmod 644 {} \;

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE README TODO
%{_bindir}/oasys_tclsh
%{_libdir}/liboasys-%{version}.so
%{_libdir}/liboasyscompat-%{version}.so

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/oasys
%{_libdir}/liboasys.so
%{_libdir}/liboasyscompat.so
%{_libdir}/liboasys-%{version}.a
%{_libdir}/liboasyscompat-%{version}.a
%{_datadir}/oasys

