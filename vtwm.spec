Summary: A Windows Manager based on twm with virtual screen
Name: vtwm
Version: 5.5.0
Release: 0.2%{?dist}
Url: http://www.vtwm.org
Source0: %{name}-%{version}-rc8.tar.gz
License: MIT
Group: Graphical desktop/Other
# Manually added
#BuildRequires:	XFree86-devel
#BuildRequires:	xorg-x11
#BuildRequires:	xpm-devel

BuildRequires:  %{_bindir}/xmkmf
BuildRequires:	%{_includedir}/X11/Intrinsic.h
BuildRequires:	%{_includedir}/X11/Xft/Xft.h
BuildRequires:	%{_includedir}/X11/Xlib.h
BuildRequires:	%{_includedir}/X11/Xmu/CharSet.h
BuildRequires:	%{_includedir}/X11/extensions/Xinerama.h
BuildRequires:	%{_includedir}/X11/extensions/Xrandr.h
BuildRequires:	%{_includedir}/X11/extensions/shape.h
BuildRequires:	%{_includedir}/X11/xpm.h


BuildRequires:	bison
BuildRequires:	flex
# Explicitly required for flex in different RHEL versions
BuildRequires:	%{_includedir}/FlexLexer.h
BuildRequires:	%{_libdir}/libfl.a
# Explicitly required for RHEL 5
BuildRequires:	%{_libdir}/libXinerama.so
# Explicitely required for libpng in RHEL 7
BuildRequires:	libpng
BuildRequires:	libpng-devel

BuildRoot: %{_tmppath}/%{name}-buildroot

%description
Twm is make by the Xconsortium and it is included with Xfree Package,
but it is very light. Vtwm is an extension of twm,
it implements some extensions such as virtual desktop.   

This package is in plf because it mimic Windows(tm) look and feel.

%prep
%setup -q -n %{name}-%{version}-rc8

%build
xmkmf
# %make doesn't work
make

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR="${RPM_BUILD_ROOT}"

# session stuff
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmsession.d
cat > $RPM_BUILD_ROOT/etc/X11/wmsession.d/13vtwm << EOF
NAME=vtwm
EXEC=%{_bindir}/vtwm
DESC=An extension of twm
SCRIPT:
exec %{_bindir}/vtwm
EOF

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT/usr/X11R6/lib/X11/doc/html/vtwm.1.html

%clean
rm -rf $RPM_BUILD_ROOT

%postun
%make_session

%files
%defattr(-,root,root)
%config(noreplace)/etc/X11/wmsession.d/13vtwm
# _datarootdi not set for RHEL 5
#%config(noreplace) %{_datarootdir}/X11/vtwm/system.vtwmrc
%config(noreplace) %{_prefix}/share/X11/vtwm/system.vtwmrc
%{_bindir}/vtwm
%{_mandir}/man1/vtwm.1x*

%changelog
* Sun Feb  1 2015 Nico Kadel-Garcia <nkadel@gmail.com> 5.5.0-0.2
- Add flex and flex-devel dependency for RHEL 7.
- Add Xft/Xft.h dependency for RHEL 7.
- Add various extens/*.h dependencies for RHEL 7.

* Sun Jul  7 2013 Nico Kadel-Garcia <nkadel@gmail.com> 5.5.0-rc8
- Update for Fedora 19 and RHEL 5
- Throw out "mkrel" macro from Mandriva, use hardcoded release number.
- Correct 2002 changelog dates to valid numbers.
- Update to 5.5.0 rc8 to avoid RPLAY dependencies
- Change URL to www.vtwm.org

* Tue Nov 15 2005 Olivier Thauvin <nanardon@zarb.org> 5.4.7-1plf
- 5.4.7

* Sat Oct 08 2005 Stefan van der Eijk <stefan@zarb.org> 5.4.6b-2plf
- BuildRequires: xorg-x11 for rman
- remove unpackaged file
- %%mkrel

* Sun Oct 17 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.4.6b-1plf
- 5.4.6b

* Thu Sep 02 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.4.6a-1plf
- 5.4.6a
- plf reason
- remove vendor from spec

* Fri Apr 26 2002 Stefan van der Eijk <stefan@eijk.nu> 5.4.6-3plf
- BuildRequires

* Thu Mar 14 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.4.6-2plf
- plf package

* Wed Mar 13 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.4.6-2mdk
- Fix typo

* Sun Mar 10 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.4.6-1mdkot
- First mdk release

