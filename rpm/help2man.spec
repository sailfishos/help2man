Name:		help2man
Summary:	Create simple man pages from --help output
Version:	1.47.4
Release:	1
Group:		Development/Tools
License:	GPLv3+
URL:		http://www.gnu.org/software/help2man
Source0:	ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz
Source1:	README

BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Text::ParseWords)
BuildRequires:	perl(Text::Tabs)
BuildRequires:	perl(strict)
BuildRequires:	texinfo

Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
# To copy missing scripts
AM_DIR=$(ls -d /usr/share/automake* 2>/dev/null | tail -1)
cp $AM_DIR/{install-sh,missing,mkinstalldirs} build-aux

cp %{SOURCE1} .

autoconf
%configure --disable-nls --libdir=%{_libdir}/help2man
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/help2man.info \
		%{_infodir}/dir 2>/dev/null || :
fi

%files
%{_bindir}/help2man
%doc %{_infodir}/*
%doc %{_mandir}/man1/*
