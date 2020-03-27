Name:		ddcw
Version:	2020
Release:	0318
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
protocol=tcp
[ -z \${host_o} ] && export host_o="127.0.0.1"
if [ ! -z \$3 ] && [ \$3 -eq \$3 2>/dev/null ]
then
	export sleep_time=\$3
fi
[ -z \${sleep_time} ] && export sleep_time=0.2


if ping -c 1 \${host_o} >/dev/null ;then
        echo -e "\${host_o} \tTCP PORT \tSTATUS"
else
        echo -e "\033[31;40m\${host_o} net unreachable\033[0m"
        exit 1
fi


if [ -z \${port_o} ]
then
	for i in {1..65536}
	do
        	if echo &>/dev/null > /dev/tcp/\${host_o}/\${i} ;then
                	echo -e "\${host_o}\t\033[31;40m\${i}\033[0m  is \033[32;40mOPEN\033[0m"
        	fi
	done
else
if [ \${port_o} -eq \${port_o} 2>/dev/null ] &&  [ \${port_o} -ge 1 2>/dev/null ] &&  [ \${port_o} -le 65536 2>/dev/null ] 
then
	if [ ! -z \$3 ]
	then
		while [ True ]
		do
			if echo &>/dev/null > /dev/tcp/\${host_o}/\${port_o} ;then
        	        	echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[32;40mOPEN\033[0m"
			else
				echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[31;40mNOT OPEN\033[0m"
        		fi
			sleep \${sleep_time}
		done
	else
                if echo &>/dev/null > /dev/tcp/\${host_o}/\${port_o} ;then
                        echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[32;40mOPEN\033[0m"
		else
			echo -e "\${host_o}\t\033[31;40m\${port_o}\033[0m \t\t  is \033[31;40mNOT OPEN\033[0m"
                fi

	fi
else
	echo -e "\033[31;40m\${port_o} is NOT AVAILABLE PORT\033[0m"
	exit 1
fi

fi
	
dtend=\`date +\%s\`
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

grep -v '#' /etc/profile | grep "HISTTIMEFORMAT=" >/dev/null 2>&1 || echo '''export HISTTIMEFORMAT="FLAG_BFH_DDCWF FLAG_BFH_DDCWT "''' >> /etc/profile
sed -i 's/FLAG_BFH_DDCW/%/g' /etc/profile
grep -v '#' /etc/profile | grep "PS1=" >/dev/null 2>&1 || echo """export PS1='\t [\[\e[31;40m\]\u\[\e[0m\]@\h \[\e[36;40m\]\W\[\e[0m\]]\\$' """ >> /etc/profile
echo -e "you shuold run:\033[31;40msource /etc/profile\033[0m"

%files

%postun
rm -rf /usr/bin/scanportDDCW
sed -i '/HISTTIMEFORMAT=/s/^/#/g' /etc/profile
sed -i '/PS1=/s/^/#/g' /etc/profile

%changelog

