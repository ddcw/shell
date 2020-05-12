Name:		rlwrapDDCW
Version:	2020
Release:	0512
Summary:	linux 6 7

Group:		Applications/System
License:	https://github.com/ddcw/shell
URL:		https://github.com/ddcw/shell

Requires:	readline,ncurses

%description
for linux 6 or linux 7 to set sqlplus rlwrap, install this package , you can pageup or pagedown content in sqlplus


%prep
echo "nothing"

%build
echo "nothing,because this install another pack rlwrap"


%install
mkdir -p %{buildroot}/tmp/rlwrapDDCW
install -m 744 rlwrap-0.42-1.el6.x86_64.rpm %{buildroot}/tmp/rlwrapDDCW/rlwrap-0.42-1.el6.x86_64.rpm
install -m 744 rlwrap-0.43-2.el7.x86_64.rpm %{buildroot}/tmp/rlwrapDDCW/rlwrap-0.43-2.el7.x86_64.rpm

%post
rm -rf /var/lib/rpm/.rpm.lock
systemctl -h >/dev/null 2>&1 && rpm -ivh /tmp/rlwrapDDCW/rlwrap-0.43-2.el7.x86_64.rpm --nodeps >/dev/null 2>&1 || rpm -ivh /tmp/rlwrapDDCW/rlwrap-0.42-1.el6.x86_64.rpm --nodeps >/dev/null 2>&1
echo 'alias sqlplus="rlwrap sqlplus"' >> /etc/profile
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] \033[32;40m~/.sqlplus_history  note your sql\033[0m"




%files
/tmp/rlwrapDDCW/rlwrap-0.42-1.el6.x86_64.rpm
/tmp/rlwrapDDCW/rlwrap-0.43-2.el7.x86_64.rpm

%postun
#echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you should run \033[31;40mrpm -e rlwrap\033[0m"
sleep 3 && rpm -e rlwrap >/dev/null 2>&1 &
sed -i '/#alias sqlplus="rlwrap sqlplus"/d' /etc/profile
sed -i '/sqlplus=/s/^/#/g' /etc/profile

%changelog

