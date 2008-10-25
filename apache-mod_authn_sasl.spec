%define	mod_name	authn_sasl
%define apxs		/usr/sbin/apxs
Summary:	Basic authentication for the Apache Web server using SASL
Summary(pl.UTF-8):	Podstawowe uwierzytelnianie (Basic) dla serwera WWW Apache przy użyciu SASL
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1
License:	BSD
Group:		Networking/Daemons/HTTP
Source0:	http://dl.sourceforge.net/mod-authn-sasl/mod_authn_sasl-%{version}.tar.bz2
# Source0-md5:	53e60c13cdb749128da13a91d413789c
URL:		http://mod-authn-sasl.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module allows you to use SASL to authenticate a user.

%description -l pl.UTF-8
Ten moduł umożliwia używanie SASL do uwierzytelniania użytkownika.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
