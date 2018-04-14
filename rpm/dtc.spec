# Based on the dtc spec from the Fedora project

Name:          dtc
Version:       1.4.6
Release:       4+mer0
Summary:       Device Tree Compiler
License:       GPLv2+
URL:           https://devicetree.org/

Source:        %{name}-%{version}.tar.bz2

BuildRequires: gcc make
BuildRequires: flex bison swig
BuildRequires: python-devel python-setuptools

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package -n libfdt
Summary: Device tree library

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n libfdt-devel
Summary: Development headers for device tree library
Requires: libfdt = %{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
make NO_PYTHON=1 %{?_smp_mflags} V=1 CC="gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS"

%install
make install NO_PYTHON=1 DESTDIR=$RPM_BUILD_ROOT SETUP_PREFIX=$RPM_BUILD_ROOT/usr PREFIX=/usr LIBDIR=%{_libdir}
find %{buildroot} -type f -name "*.a" -delete

# we don't want or need ftdump and it conflicts with freetype-demos, so drop
# it (rhbz 797805)
rm -f $RPM_BUILD_ROOT/%{_bindir}/ftdump

%post -n libfdt -p /sbin/ldconfig

%postun -n libfdt -p /sbin/ldconfig

%files
%doc Documentation/manual.txt
%{_bindir}/*

%files -n libfdt
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%{_libdir}/libfdt.so
%{_includedir}/*
