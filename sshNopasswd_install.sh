#!/bin/bash
#write by ddcw at 20200410
thiscript=$0
function exits(){
  echo -e "[`date +%Y%m%d-%H:%M:%S`] \033[31;40m$1\033[0m"
  exit 0
}
function install_sshNopasswd(){
	[ -f /usr/bin/sshNopasswd ] && exits "this OS has /usr/bin/sshNopasswd"
	tail -n +19 ${thiscript} > /usr/bin/sshNopasswd
	chmod 777 /usr/bin/sshNopasswd
	echo -e "[`date +%Y%m%d-%H:%M:%S`] [\033[32;40mINSTALL FINISH\033[0m] \033[31;40m you can run \033[0m \033[32;40msshNopasswd -h\033[0m \033[31;40mto get help\033[0m"
	exit 0 
}
[ -z $1 ] && install_sshNopasswd



#!/bin/env bash
#write by ddcw at 20200410


dt=$(date +%Y%m%d-%H%M%S)

function get_ssh_keygen() {
	tpe=$1
        expect << EOF
        set timeout 30
        spawn  /usr/bin/ssh-keygen -t ${tpe}
        expect {
                        "sa):" {send "\r";exp_continue}
                        "passphrase):" {send "\r";exp_continue}
                        "again:" {send "\r"}
        }
        expect eof
EOF
}
function scp_file_auto(){
        [ $# -eq 3 ] || echo_color red "script has internal err DDCW_0001"
        password=$3
        dir_tmp=$1
        host_and_dir=$2
        expect << EOF
        set timeout 30
        spawn scp ${dir_tmp} ${host_and_dir}
        expect {
                        "(yes/no" {send "yes\r";exp_continue}
                        "password:" {send "${password}\r"}
        }
        expect eof
EOF
}
function ssh_command(){
#        [ $# -eq 3 ] || echo_color red "script has internal err DDCW_0003"
        user=`echo $1 | awk -F "@" '{print $1}'` ||  echo_color red "script has internal err DDCW_0004"
        user_host=$1
        commd=$2
        password=$3
        expect << EOF
        set timeout 30
        spawn ssh ${user_host} ${commd}
        expect {
                        "(yes/no" {send "yes\r";exp_continue}
                        "password:" {send "${password}\r"}
        }
        expect "${user}@*" {send "exit\r"}
        expect eof
EOF
}


function help_this_script() {
	echo '---------------------------------------'
	echo 'sshNopasswd [USER]@HOSTNAME [PASSWORD] '
	echo "example: sshNopasswd $(whoami)@$(last | head -1 | awk '{print $3}') "
	echo '---------------------------------------'
	exit 0
}

case $1 in
	-h|-H|h|H|help|HELP|-help|-HELP|--help|--HELP|help=y|HELP=Y|?|-?)
		help_this_script;;
esac
	
if [ ! -f ~/.ssh/id_rsa ]
then
mv ~/.ssh ~/.ssh${dt}
get_ssh_keygen rsa
get_ssh_keygen dsa
fi
if [ ! -f ~/.ssh/id_rsa.pub ]
then
mv ~/.ssh ~/.ssh${dt}
get_ssh_keygen rsa
get_ssh_keygen dsa
fi

if [ ! -f ~/.ssh/id_dsa ]
then
mv ~/.ssh ~/.ssh${dt}
get_ssh_keygen dsa
get_ssh_keygen rsa
fi
if [ ! -f ~/.ssh/id_dsa.pub ]
then
mv ~/.ssh ~/.ssh${dt}
get_ssh_keygen dsa
get_ssh_keygen rsa
fi


ssh_rsa_pub=$(cat  ~/.ssh/id_rsa.pub | awk '{print $1 " " $2}')
ssh_dsa_pub=$(cat  ~/.ssh/id_dsa.pub | awk '{print $1 " " $2}')

[ -z ${2} ] && read -t 60 -p "please input ${1} password:" password
[ -z ${2} ] || export password=$2

ssh_command $1 'mkdir -p touch ~/.ssh' ${password}
ssh_command $1 '\[ -f ~/.ssh/authorized_keys \] || touch ~/.ssh/authorized_keys' ${password}
ssh_command $1 " grep '${ssh_rsa_pub}' ~/.ssh/authorized_keys >/dev/null || echo '${ssh_rsa_pub}' >> ~/.ssh/authorized_keys" ${password}
ssh_command $1 " grep '${ssh_dsa_pub}' ~/.ssh/authorized_keys >/dev/null || echo '${ssh_dsa_pub}' >> ~/.ssh/authorized_keys" ${passwd}
