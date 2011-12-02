Summary: A basic system library for accessing the termcap database
Name: compat-libtermcap
Version: 2.0.8
Release: 49%{?dist}
Source: termcap-2.0.8.tar.bz2
Url: ftp://metalab.unc.edu/pub/Linux/GCC/
License: GPLv2+
Group: System Environment/Libraries
Patch0: termcap-2.0.8-shared.patch
Patch1: termcap-2.0.8-setuid.patch
Patch2: termcap-2.0.8-instnoroot.patch
Patch3: termcap-2.0.8-compat21.patch
Patch4: termcap-2.0.8-xref.patch
Patch5: termcap-2.0.8-fix-tc.patch
Patch6: termcap-2.0.8-ignore-p.patch
Patch7: termcap-buffer.patch
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8: termcap-2.0.8-bufsize.patch
Patch9: termcap-2.0.8-colon.patch
Patch10: libtermcap-aaargh.patch
Patch11: termcap-2.0.8-glibc22.patch
Patch12: libtermcap-2.0.8-ia64.patch
Patch13: termcap-116934.patch
Patch14: termcap-2.0.8-shrink.patch
Patch15: termcap-2.0.8-octal.patch
Patch16: termcap-2.0.8-nofree.patch
Requires: ncurses-base ncurses
BuildRequires: texinfo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The libtermcap package contains a basic system library needed to
access the termcap database.  The termcap library supports easy access
to the termcap database, so that programs can output character-based
displays in a terminal-independent manner.

%prep
%setup -q -n termcap-2.0.8
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .nochown
%patch3 -p1 -b .compat21
%patch4 -p1
%patch5 -p1 -b .fix-tc
%patch6 -p1 -b .ignore-p
%patch7 -p1 -b .buffer
%patch8 -p1 -b .bufsize
%patch9 -p1 -b .colon
%patch10 -p1 -b .aaargh
%patch11 -p1 -b .glibc22
%ifarch ia64
%patch12 -p1 -b .ia64
%endif
%patch13 -p1 -b .116934
%patch14 -p1 -b .shrink
%patch15 -p1 -b .octal
%patch16 -p1 -b .nofree

%build
make AR=%{__ar} CC=%{__cc} CFLAGS="$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/%{_lib},%{_sysconfdir}}

install libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/
ln -sf libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/libtermcap.so.2

touch $RPM_BUILD_ROOT%{_sysconfdir}/termcap

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%triggerin -- ncurses-base ncurses-term
# generate termcap database from installed terminfos
toe -a | while read term rest; do
	infocmp -Ct $term
done > %{_sysconfdir}/termcap
exit 0

%files
%defattr(-,root,root)
/%{_lib}/libtermcap.so.2*
%ghost %{_sysconfdir}/termcap

%changelog
* Wed Jun 30 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.8-49
- review fixes (#607251)

* Wed Jun 30 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.8-48
- make compat package
- generate termcap database from terminfo in %%trigger script

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.8-47
- update license tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.8-46.1
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com> - 2.0.8-46
- no need for the trigger, if info files are in the -devel subrpm

* Mon Feb 27 2006 Miloslav Trmac <mitr@redhat.com> - 2.0.8-45
- Add Requires(postun): /sbin/install-info to libtermcap-devel (#182836)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.8-44.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.8-44.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 2 2006 Petr Raszyk <praszyk@redhat.com> 2.0.8-44
- Rebuild. 

* Mon Jan 2 2006 Petr Raszyk <praszyk@redhat.com> 2.0.8-43
- libtermcap does not 'free()'memory. See #74346
  A patch termcap-2.0.8-nofree.patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- build with newest rpm

* Fri Mar 18 2005 Nalin Dahyabhai <nalin@redhat.com> 2.0.8-41
- don't trip over capabilities which end in '^' or '\'
- don't accept numbers with '8' or '9' in them as valid octal numbers

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 2.0.8-40
- rebuild

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May  7 2004 Tim Waugh <twaugh@redhat.com> 2.0.8-38
- Fix tgetent() (bug #116934).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared lib

* Mon Jan 27 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.8-34
- don't strip libraries directly, that's the job of the buildroot policy
- rework part of %%install to handle cases where %%{_libdir} = /usr/lib

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.8-33
- Cross-compile changes

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com>
- Pull in hammer changes, rebuild

* Tue Sep 24 2002 Jeremy Katz <katzj@redhat.com>
- libdir fun

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.8-29
- Add workaround for libgcc/glibc breakage on ia64
- s/Copyright/License/ in spec file
- bzip2 source to save space

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- make libtermcap-devel require the same version as the main package

* Thu Jun 21 2001 Than Ngo <than@redhat.com>
- add missing libtermcap symlink

* Sat Oct  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Uninstall info pages in %%postun devel rather than %%postun
  (Bug #18545)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix broken symlink (#16285)

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- absolute --> relative symlink (#16131)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Matt Wilson <msw@redhat.com>
- move the trigger to the devel package, that's where the info pages
  live now

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- rebuild for next release
- move info pages to the development package
- use %%{_infodir}
- patched to build against new glibc (patch11)

* Sun Feb  6 2000 Bernhard Rosenkränzer <bero@redhat.com>
- BuildPrereq: texinfo (#8927)

* Sat Feb  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- strip library
- fix up handling of RPM_OPT_FLAGS

* Tue Aug 30 1999 Bill Nottingham <notting@redhat.com>
- ignore the first argument to tgetent, so the last change doesn't
  keep blowing up programs.
- ignore the second argument to tgetstr() as well. 

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- increase default size of malloc'ed tgetent buffer from 1024 to 1536.
- don't shrink colons (#4270).
- rebuild for 6.1.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- add buffer overflow patch from Kevin Vajk <kvajk@ricochet.net>

* Sat May 15 1999 Jeff Johnson <jbj@redhat.com>
- permit multiple tc= continuations and ignore unnecessary %%p ("push arg") (#54)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 13)
- fix to make the texi documenattion compile

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- use __PMT(...) prototypes (#761)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- run install-info from a %%trigger so we don't have to make it a prereq; as
  termcap is used by bash, the install ordering issues are hairy
- commented out the chown stuff from 'make install' so you don't have to
  be root to build this
- don't run ldconfig if prefix= is used during 'make install'

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- But assume system termcap is sane. Also handle setfsuid return right.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- TERMCAP environment hole for setuid apps squished.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
