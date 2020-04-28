Name:		ddcw
Version:	2020
Release:	0428
Summary:	this is set habbit for ddcw

Group:		Applications/System
License:	ddcw
URL:		https://github.com/ddcw/shell

Requires:grep
	

%description
this is set ddcw some habi


%prep
echo -e "\033[1;41;33m pre install NOTHING\033[0mprep"

%build
echo -e "\033[1;41;33m build NOTHING\033[0mprep"


%install


%post
cat << EOF > /usr/bin/scanportDDCW
#!/bin/env bash
#modified by ddcw at 20200428
dtbegin=\`date +%s\`
if [ ! -z \$1 ] && [ \${1} -eq \${1} 2>/dev/null ] 
then
	export port_o=\$1
else
	export host_o=\$1
fi

if [ ! -z \$2 ]
then
	export port_o=\$2
	export host_o=\$1
fi

if [ \${1} -eq \${1} 2>/dev/null ] && [ \${2} -eq \${2} 2>/dev/null ] && [ ! -z \${2} ]
then
	export port_o=\$1
	export sleep_time=\$2
	export host_o=127.0.0.1
	export scan_continue=1
fi


protocol=tcp
[ -z \${host_o} ] && export host_o="127.0.0.1"
if [ ! -z \$3 ] && [ \$3 -eq \$3 2>/dev/null ]
then
	export sleep_time=\$3
fi
[ -z \${sleep_time} ] && export sleep_time=0.2
if ping -c 1 \${host_o} >/dev/null ;then
        echo -e "\${host_o} \tTCP PORT \tSTATUS \tServices or Program name"
else
        echo -e "\033[31;40m\${host_o} net unreachable\033[0m"
        exit 1
fi
if [ -z \${port_o} ]
then
	for i in {1..65536}
	do
        	if echo &>/dev/null > /dev/tcp/\${host_o}/\${i} ;then
			service_name=''
			ifconfig | grep \${host_o} 1>/dev/null &&  service_name=\`netstat -natp | grep :\${i} | grep -v - | tail -1 | awk '{print \$7}' | awk -F / '{print \$2}'\`
			[ "\${service_name}" == "master"  ] && service_name=\`grep " \${i}/tcp" /etc/services | head -3 | awk '{print \$1}'\`
			[ "\${service_name}" == "systemd"  ] && service_name=\`grep " \${i}/tcp" /etc/services | head -3 | awk '{print \$1}'\`
			ifconfig | grep "\${host_o} " 1>/dev/null && [ -z \${service_name:0:1} ] && service_name='maybe ssh sessions'
			[ -z \${service_name:0:1} ] && service_name=\`grep " \${i}/tcp" /etc/services | head -3 | awk '{print \$1}'\`
                	echo -e "\${host_o}\t\033[31;40m\${i}\t\033[0m  is \033[32;40mOPEN\033[0m \t\${service_name}"
        	fi
	done
else
if [ \${port_o} -eq \${port_o} 2>/dev/null ] &&  [ \${port_o} -ge 1 2>/dev/null ] &&  [ \${port_o} -le 65536 2>/dev/null ] 
then
	if [ ! -z \$3 ] || [ ! -z \${scan_continue} ]
	then
		while [ True ]
		do
			if echo &>/dev/null > /dev/tcp/\${host_o}/\${port_o} ;then
				service_name=\`grep " \${port_o}/tcp" /etc/services | head -3 | awk '{print \$1}'\`
        	        	echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[32;40mOPEN\033[0m \t\${service_name}"
			else
				echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[31;40mNOT OPEN\033[0m"
        		fi
			sleep \${sleep_time}
		done
	else
                if echo &>/dev/null > /dev/tcp/\${host_o}/\${port_o} ;then
			service_name=\`grep " \${port_o}/tcp" /etc/services | head -3 | awk '{print \$1}'\`
                        echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[32;40mOPEN\033[0m \t\${service_name}"
		else
			echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[31;40mNOT OPEN\033[0m"
                fi
	fi
else
	echo -e "\033[31;40m\${port_o} is NOT AVAILABLE PORT\033[0m"
	exit 1
fi
fi
	
dtend=\`date +%s\`
echo -e "this script cost time: \033[32;40m\`expr \${dtend} - \${dtbegin}\`\033[0m second"
EOF
chmod 777 /usr/bin/scanportDDCW


cat << EOF > /usr/bin/CheckCommDDCW
#!/bin/env bash
#write by ddcw
#https://cloud.tencent.com/developer/column/6121
#scriptname:CheckCommDDCW.sh
begintime=\`date +%s\`
file_name=~/.UserCheckCom.txt
new_comm_n=0
change_comm_n=0
new_comm=""
change_comm=""
[ -f \${file_name} ] || touch \${file_name}
for i in \$(compgen -c)
do
	if which \$i >/dev/null  2>&1 
	then
		md5_n=\$(md5sum \$(which \$i) | awk '{print \$1}')
		if  cat \${file_name} | grep "\#\$i\#" >/dev/null  2>&1 
		then
		#	echo \$(cat \${file_name} | grep "\#\$i\#")
			md5_o=\$(cat \${file_name} | grep "\#\$i\#" | tail -1 | awk '{print \$NF}')
			if [ "\${md5_n}" != "\${md5_o}" ]
			then
				#echo -e "COMMD \033[1;41;33m \$i \033[0m may be Changed: old_MD5: \${md5_o}    new_MD5: \${md5_n}"
				[ -z \$1 ] || echo -e "#\${i}# \t \$(date +%Y%m%d-%H:%M:%S) \t \${md5_n}" >> \${file_name}
				change_comm_n=\$[ \${change_comm_n} + 1]
				change_comm="\${change_comm}  \${i}"
			fi
		else
			if [ "\${i}" != '[' ]
			then
				new_comm_n=\$[ \${new_comm_n} + 1]
				new_comm="\${new_comm}  \${i}"
				#echo -e "\033[32;40m\$i \033[0m"
				echo -e "#\${i}# \t \$(date +%Y%m%d-%H:%M:%S) \t \${md5_n}" >> \${file_name}
			fi
		fi
	fi	
done
echo ""
if [ \${new_comm_n} -gt 0 ]
then
	echo -e "\033[31;40m Total Add  \${new_comm_n} commd \033[0m"
	echo "\${new_comm}"
else
	echo -e "\033[32;40m No Command  Added ,It's Seccurity!\033[0m\n"
fi
if [ \${change_comm_n} -gt 0 ]
then
	echo -e "\033[31;40m Total Changed  \${change_comm_n} commd \033[0m"
	echo "\${change_comm}"
else
	echo -e "\033[32;40m No Command Changed  ,It's Seccurity!\033[0m"
fi
endtime=\`date +%s\`
costm=\`echo \${begintime} \${endtime} | awk '{print (\$2-\$1)/60}'\`
echo -e "\n\033[32;40m \`date +%Y%m%d-%H:%M:%S\` cost \${costm} minutes\033[0m"
EOF
chmod 777 /usr/bin/CheckCommDDCW

cat << EF > /usr/bin/sshNopasswd
#!/bin/env bash
#write by ddcw at 20200410
#modified by ddcw at 20200428

export LANG=en_US.UTF-8

if  ! which expect >/dev/null 2>&1 
then
	echo -e " [\033[1;5;41;33mERROR\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[1;41;33myou should install expect first\033[0m :\n\t\t \033[32;40myum install expect -y\033[0m"
	exit 1
fi

dt=\$(date +%Y%m%d-%H%M%SOURCE)

function get_ssh_keygen() {
	tpe=\$1
        expect << EOF >/dev/null
        set timeout 30
        spawn  /usr/bin/ssh-keygen -t \${tpe}
        expect {
                        "sa):" {send "\r";exp_continue}
                        "passphrase):" {send "\r";exp_continue}
                        "again:" {send "\r"}
        }
        expect eof
EOF
}
function ssh_command(){
        user_host=\$1
	user=\$(echo \${user_host} | awk -F @ '{print \$1}')
	[ -z \${user} ] && user=\${user_host}
        commd=\$2
        password=\$3
	expect << EOF >/dev/null
        set timeout 30
        spawn ssh  -p \${sshport} \${user_host} \${commd}
        expect { 
                        "(yes/no" {send "yes\r";exp_continue}
                        "password:" {send "\${password}\r"}
        }
        expect "\${user}@*" {send "exit\r"}
        expect eof
EOF
}


function help_this_script() {
	echo '------------------------'
	echo -e "[\033[1;5;41;33mHELP\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[1;41;33mexample: sshNopasswd [USERNAME@]hsotname[:SSHPORT] [PASSWORD]\033[0m"
	#echo "example: sshNopasswd \$(whoami)@\$(last | head -1 | awk '{print \$3}') "
	echo '------------------------'
	echo -e "[\033[32;40mINFO\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[32;40myou can set sshNopassword sshport in ~/.sshNopasswd.conf; formats:HOSTNAME  SSHPORT\033[0m"
	echo '------------------------'
	exit 0
}

case \$1 in
	-h|-H|h|H|help|HELP|-help|-HELP|--help|--HELP|help=y|HELP=Y|?|-?)
		help_this_script;;
esac

if [ -z \$1 ]
then
	help_this_script
	exit 1
fi

export username=\$(echo \$1 | awk -F \@ '{print \$1}' | awk -F : '{print \$1}')
export host_d=\$(echo \$1 | awk -F @ '{print \$2}' | awk -F : '{print \$1}')
echo \$1 | grep : 1>/dev/null && export sshport=\$(echo \$1 | awk -F : '{print \$NF}')
[ -z \${host_d} ] && export username=\$(whoami) && export host_d=\$(echo \$1 | awk -F : '{print \$1}')
[ -z \${sshport} ] && [ -f ~/.sshNopasswd.conf ] && export sshport=\$(grep \${host_d} ~/.sshNopasswd.conf 2>/dev/null | tail -1 | awk '{print \$2}')
[ -z \${sshport} ] && export sshport=22

if ping -c 1 \${host_d} >/dev/null ;then
	if echo &>/dev/null > /dev/tcp/\${host_d}/\${sshport}
	then
		echo -e "[\033[32;40mINFO\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[32;40mbegin ssh(user port \${sshport}) config for \${1}\033[0m"
	else
		echo -e "[\033[1;5;41;33mERROR\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[1;41;33m \${host_d}:\${sshport} is not ESTABLISHED\033[0m"
		exit 1
	fi
else
	echo -e "[\033[1;5;41;33mERROR\033[0m \`date +%Y%m%d-%H:%M:%S\`] \033[1;41;33m \${host_d} Network unreachable\033[0m"
	exit 1
fi

	
if [ ! -f ~/.ssh/id_rsa ]
then
mv ~/.ssh ~/.ssh\${dt}
get_ssh_keygen rsa
get_ssh_keygen dsa
fi
if [ ! -f ~/.ssh/id_rsa.pub ]
then
mv ~/.ssh ~/.ssh\${dt}
get_ssh_keygen rsa
get_ssh_keygen dsa
fi

if [ ! -f ~/.ssh/id_dsa ]
then
mv ~/.ssh ~/.ssh\${dt}
get_ssh_keygen dsa
get_ssh_keygen rsa
fi
if [ ! -f ~/.ssh/id_dsa.pub ]
then
mv ~/.ssh ~/.ssh\${dt}
get_ssh_keygen dsa
get_ssh_keygen rsa
fi

[ -f ~/.ssh\${dt}/authorized_keys ] && cp ~/.ssh\${dt}/authorized_keys ~/.ssh/authorized_keys


ssh_rsa_pub=\$(cat  ~/.ssh/id_rsa.pub | awk '{print \$1 " " \$2}')
ssh_dsa_pub=\$(cat  ~/.ssh/id_dsa.pub | awk '{print \$1 " " \$2}')

[ -z \${2} ] && read -t 60 -p "please input \${username}@\${host_d} password:" password
[ -z \${2} ] || export password=\$2

ssh_command  \${username}@\${host_d} 'mkdir -p touch ~/.ssh' \${password}
ssh_command  \${username}@\${host_d} '\[ -f ~/.ssh/authorized_keys \] || touch ~/.ssh/authorized_keys' \${password}
ssh_command  \${username}@\${host_d} " grep '\${ssh_rsa_pub}' ~/.ssh/authorized_keys >/dev/null || echo '\${ssh_rsa_pub}' >> ~/.ssh/authorized_keys" \${password}
ssh_command  \${username}@\${host_d} " grep '\${ssh_dsa_pub}' ~/.ssh/authorized_keys >/dev/null || echo '\${ssh_dsa_pub}' >> ~/.ssh/authorized_keys" \${passwd}
EF

chmod 777 /usr/bin/sshNopasswd


grep -v '#' /etc/profile | grep "HISTTIMEFORMAT=" >/dev/null 2>&1 || echo '''export HISTTIMEFORMAT="FLAG_BFH_DDCWF FLAG_BFH_DDCWT "''' >> /etc/profile
sed -i 's/FLAG_BFH_DDCW/%/g' /etc/profile
grep -v '#' /etc/profile | grep "PS1=" >/dev/null 2>&1 || echo """export PS1='\t [\[\e[31;40m\]\u\[\e[0m\]@\h \[\e[36;40m\]\W\[\e[0m\]]\\$' """ >> /etc/profile
echo -e "you shuold run:\033[31;40msource /etc/profile\033[0m"

%files

%postun
rm -rf /usr/bin/scanportDDCW
sed -i '/HISTTIMEFORMAT=/s/^/#/g' /etc/profile
sed -i '/PS1=/s/^/#/g' /etc/profile
rm -rf /usr/bin/sshNopasswd
rm -rf /usr/bin/CheckCommDDCW

%changelog
