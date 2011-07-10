%{?filter_provides_in: %filter_provides_in .*/h5py/.*\.so}
%{?filter_setup}

Summary:        A Python interface to the HDF5 library
Name:           h5py
Version:        1.3.1
Release:        4%{?dist}
Group:          Applications/Engineering
License:        BSD
URL:            http://h5py.alfven.org/
Source0:        http://h5py.googlecode.com/files/h5py-%{version}.tar.gz
# patch to use a system liblzf rather than bundled liblzf
Patch0:         h5py-1.3.1-system-lzf.patch
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  hdf5-devel >= 1.8.2
BuildRequires:  numpy >= 1.0.3
BuildRequires:  liblzf-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       numpy >= 1.0.3

%description
The h5py package provides both a high- and low-level interface to the
HDF5 library from Python. The low-level interface is intended to be a
complete wrapping of the HDF5 API, while the high-level component
supports access to HDF5 files, data sets and groups using established
Python and NumPy concepts.

A strong emphasis on automatic conversion between Python (Numpy)
data types and data structures and their HDF5 equivalents vastly
simplifies the process of reading and writing data from Python.

%prep
%setup -q
# use system libzlf and remove private copy
%patch0 -p1 
rm -rf lzf/lzf

%build
export CC="%{__cc}"
export CFLAGS="%{optflags} -fopenmp -llzf"
%{__python} setup.py configure --hdf5=%{_libdir} --api=18
%{__python} setup.py build
# build docs 
dir=$(basename build/lib.linux-*)
PYTHONPATH=$(pwd)/build/$dir make -C docs html
rm -f docs/build/html/.buildinfo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
chmod 0755 %{buildroot}%{python_sitearch}/%{name}/*.so

%check
%{__python} setup.py nosetests

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.txt LICENSE.txt h5py.egg-info licenses 
%doc docs/build/html
%{python_sitearch}/%{name}/
%{python_sitearch}/%{name}-%{version}-*.egg-info/

%changelog
* Mon May 23 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.3.1-4
- add patch from Steve Traylen (thanks!) to use system liblzf
 
* Thu Jan 13 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.3.1-3
- fix buildroot
- add filter
- don't remove egg-info files
- remove explicit hdf5 req

* Sun Jan  2 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.3.1-2
- build and ship docs as html

* Mon Dec 27 2010 Terje Rosten <terje.rosten@ntnu.no> - 1.3.1-1
- 1.3.1
- license is BSD only
- run tests
- new url

* Sat Jul  3 2009 Joseph Smidt <josephsmidt@gmail.com> - 1.2.0-1
- initial RPM release
