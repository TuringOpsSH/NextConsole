#!/usr/bin/ksh

ftp_server=
ftp_user=
ftp_password=
ftp_dir=

echo "Start ..."

__runas=$(whoami)
__ostype=$(uname)

[ -f ~/.profile ] && { . ~/.profile >/dev/null 2>&1; }
__oraclebase=${ORACLE_BASE}
__oraclehome=${ORACLE_HOME}
[ -z "${__oraclehome}" ] && {
    [ -z "$1" ] && { echo "If ORACLE_HOME not be set in profile, please run as: sh $0 [ORACLE_HOME]"; exit 1; }
    __oraclehome=$1
    export ORACLE_HOME=$__oraclehome
}

__gridhome=${GRID_HOME}
__sqlpluscmd=${ORACLE_HOME}/bin/sqlplus
[ ! -f ${__sqlpluscmd} ] && __sqlpluscmd=sqlplus

openmode=
rac=
primary=
__dbversion=
ctltype=
multitenant=NO
tracepath=
alertpath=
psexist=YES
cluster=
crsalert=

processlist=$(ps -ef | awk '$1=="'$__runas'"{print}' | grep "ora_ckpt_" | grep -v grep | grep -v ASM | grep -v MGMTDB | grep -v '+APX' | awk '{print $NF}' | sed 's/^ora_ckpt_//'|grep -v '/')
for p in $@
do
    [ "$p" = "normal" ] && processlist=$(ps -ef | grep "ora_ckpt_" | grep -v grep | grep -v ASM | grep -v MGMTDB | grep -v '+APX' | awk '{print $NF}' | sed 's/^ora_ckpt_//'|grep -v '/')
done

[ -z "$processlist" ] && {
   psexist=NO
   echo "Oracle ora_ckpt_ process not exists, maybe not running"; exit 1;
} 

_head(){
echo $(date '+%Y-%m-%d %H:%M:%S') $*
echo "\${edith:$(echo $* | sed 's/ /@/')}" >>$__out
}

_host(){
echo os: AIX
echo oslevel: $(oslevel)
echo uptime: $(uptime)
echo hostname: $(hostname)
echo OS Time: $(date '+%Y-%m-%d %H/%M/%S')
echo OS UTC: UTC/$(date |awk '{print $5}')
echo SN: $(uname -uM | awk -F""IBM,"" '{print $3}' | awk '{print $1}')
prtconf | grep -E "System Model:|Machine Serial Number:|Processor Type:|Processor Implementation Mode:|Processor Version:|Number Of Processors:|Processor Clock Speed:|CPU Type:|Kernel Type:|LPAR Info:|Memory Size:|Good Memory Size:|Platform Firmware level:|Firmware Version:|Console Login:|Auto Restart:|Full Core:|NX Crypto Acceleration:|IP Address"
}

_limits(){
[ $(whoami) = "root" ] && {
    cat /etc/security/limits |grep -v "^$" |grep -v "^*" | awk '{print $1, $2, $3, $4}'
} || {
    ulimit -a | sed 's/)/)  =/g'
}
}

_etchosts(){
grep -vE "^#|^$" /etc/hosts | awk '{for(i=1;i<=NF;i=i+1)printf " "$i;print ""}' | sed 's/^ //' | sed 's/ /=/' | sed 's/#.*//'
}

_fspct(){
#df -g -P -t jfs2 -t gpfs -x cdrfs | grep -v ^Filesystem | grep -v '文件系统' | awk '{print $7","$1","$2","$3","$4}' | grep -v '^/proc'
df -g | grep -v ^Filesystem | awk '{print $7","$1","$2","$3","$4}' | grep -v '^/proc'
}

_inodepct(){
#df -g -P -t jfs2 -t gpfs -x cdrfs | grep -v ^Filesystem | grep -v '文件系统' | awk '{print $7","$1","$6}' | grep -v '^/proc'
df -g | grep -v ^Filesystem | awk '{print $7","$1","$6}' | grep -v '^/proc'
}

_sql(){

sid=$1
key=$2
sql=$$.sql

echo $(date '+%Y-%m-%d %H:%M:%S') $key
echo "\${edith:"${2}@${1}"}" >>$__out
grep '^#'$key':' $0 | sed 's/#'$key'://g' >/tmp/$sql; chmod +x /tmp/$sql

#export ORACLE_SID=$sid
export NLS_LANG=american_america.AL32UTF8
sqlplus -S "/as sysdba" << EOF >>$__out
start /tmp/$sql
EOF

rm -f /tmp/$sql

}

_lspatches(){
[ -d "$ORACLE_HOME" ] && $ORACLE_HOME/OPatch/opatch lspatches
}

_lsinventory(){
[ -d "$ORACLE_HOME" ] && $ORACLE_HOME/OPatch/opatch lsinventory
}

_lo(){
   echo # not surport aix
}

_sqlnet(){
[ -f ${ORACLE_HOME}/network/admin/sqlnet.ora ] && { cat ${ORACLE_HOME}/network/admin/sqlnet.ora | grep -v ^#; }
}

_awkalert(){
TRACEFILE=$1

m=$(wc -l $__out | awk '{print $1}')

[ -f "${TRACEFILE}" ] && {

g11=$(tail -100 ${TRACEFILE} | grep -E 'Mon|Tue|Wed|Thu|Fri|Sat|Sun' | wc -l)
g19=$(tail -100 ${TRACEFILE} | grep -E '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' | wc -l)

if [ $g19 -gt $g11 ]; then

tail -10000 ${TRACEFILE} | grep -v "^$" | grep -v "LICENSE_SESSIONS_WARNING" | awk 'BEGIN{TM_FLAG=0;ERR_FLAG=0}
{
 if(match($0,"^[1-9]") && match($0,'T')  && match($0,"-") )
   {      
    TM=$0;
    TM_FLAG=1;
    do
    {
    getline;
    if (match($0,"ORA-") ||match($0,"WARNING")||match($0,"TNS-")||match($0,"corrupted")||match($0,"Deadlock")||match($0,"timeout")||match($0,"abnormal")||match($0,"terminated")||match($0,"offline"))
     {
      print TM "  "$0 
     }
     
     if(match($0,"^[1-9]") && match($0,'T')  && match($0,"-") )
       {
         TM_FLAG=0
       }
    } while (getline ==1 && TM_FLAG==1)
  }
}'

else

tail -10000 ${TRACEFILE} | grep -v "^$" | grep -v "LICENSE_SESSIONS_WARNING" | awk 'BEGIN{TM_FLAG=0;ERR_FLAG=0}
{
 if(match($0,"Mon") || match($0,"Tue") || match($0,"Wed") || match($0,"Thu") || match($0,"Fri") || match($0,"Sat") || match($0,"Sun") )
   {      
    TM=$0;
    TM_FLAG=1;
    do
    {
    getline;
    if (match($0,"ORA-") ||match($0,"Warning")||match($0,"TNS-")||match($0,"corrupted")||match($0,"Deadlock")||match($0,"timeout")||match($0,"abnormal")||match($0,"terminated")||match($0,"offline"))
     {
      print TM "  "$0 
     }
     
     if(match($0,"Mon") || match($0,"Tue") || match($0,"Wed") || match($0,"Thu") || match($0,"Fri") || match($0,"Sat") || match($0,"Sun") )
       {
         TM_FLAG=0
       }
    } while (getline ==1 && TM_FLAG==1)
  }
}'

fi
}

n=$(wc -l $__out | awk '{print $1}')
[ $n -eq $m -a -f "${TRACEFILE}" ] && {
    tail -5 ${TRACEFILE}
}

}

_crsctlstat(){
if [ $(ps -ef |grep "crsd.bin reboot" |grep -v grep |wc -l) -eq 1 ];then
   id grid >/dev/null
   if [ $? -eq 0 ];then
      crsctl_cmd=`ps -ef |grep crsd.bin |awk '{print $(NF-1)}' |grep -v grep|grep -v color |grep -v sed|sed 's/crsd.bin/crsctl/'`
      #LSNODES=`ps -ef |grep crsd.bin |awk '{print $(NF-1)}' |grep -v grep|grep -v color |grep -v sed|sed 's/crsd.bin/olsnodes/'`
      ${crsctl_cmd} stat res -t
      #${LSNODES}
   else
      crs_stat -t
   fi
else
   crsctl_cmd=$(ps -ef| grep grid_home | grep -v grep | awk '{print $8}' | awk -F '/' '{print $1"/"$2"/"$3"/"$4"/bin/crsctl"}' | head -1)
   [ ! -z "$crsctl_cmd" -a -f "$crsctl_cmd" ] && {
      $crsctl_cmd stat res -t
   } || {
      echo "command-not-found"
   }
fi
}

_osparm(){
no -a | grep  -E 'ipqmaxlen|udp_sendspace|udp_recvspace|tcp_sendspace|tcp_recvspace|rfc1323|sb_max| tcp_ephemeral|udp_ephemeral' | awk -F "=" '{print "\""$1"\""",""\""$2"\""}'
lsattr -E -l sys0 | egrep "maxuproc|ncargs|minpout|maxpout"  | awk '{print "\""$1"\""",""\""$2"\""}' 
lsdev | grep iocp | awk '{print "\""$1"\""",""\""$2"\""}'  
}

_netstat(){
/usr/bin/netstat -in | grep -v "lo0" | grep -v "link#" | grep  -v "^Name" | grep -v '网络' | awk '{print $1",",$2",",$3",",$(NF-4)",",$(NF-3)",",$(NF-2)",",$(NF-1)",",$(NF)}'
}

_ftp() {
    
ftp -n -v -i $ftp_server <<eof >$ftpLog
    user $ftp_user $ftp_password
    bin
    prompt
    cd $ftp_dir
    put $local_file
    bye  
eof

if [ -f $ftpLog ];then 
    transferNum=`awk '/^226/' $ftpLog`
    if [ "$transferNum" = "" ];then 
        ftp -n -v -i $ftp_server <<eof >$ftpLog
            user $ftp_user $ftp_password
            bin
            prompt
            passive on
            cd $ftp_dir
            put $local_file
            bye  
eof
        transferNum=`awk '/^226/'  $ftpLog`
        if [ "$transferNum" = "" ];then
            echo "Ftp transfer failed."
            return 2
        else
            return 0
        fi
    
    else
        return 0
    fi
else
    echo "Ftp log not be found."
    return 3
fi
}

_crsalert(){
[ ! -z "$1" -a "$1" != "Unknown" -a -f "$1" ] && {
tail -50 "$1" | grep -E 'CRS-|ORA-|error|FAIL|failed' | egrep -v 'CRS-10001|CRS-1605|CRS-2772|CRS-8500|CRS-8017|CRS-2407|CRS-2408|CRS-2409|started'| sort | uniq | awk -F '@@' '{print $1}'
}
}

_start_run_sql_scripts(){
echo start run sql scripts ...
}

for sid in $processlist 
do

export ORACLE_SID=$sid

openmode=`${__sqlpluscmd} -S "/as sysdba" <<EOF
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
select status from v\\\$INSTANCE ;
exit
EOF
`

[ -z "$(echo $openmode | grep -v ":")" ] && {
echo "__________________________________________"
echo ""
echo "Warning:"
echo $openmode
echo "__________________________________________"
   openmode="ORACLE_not_available"
}


rac=`${__sqlpluscmd} -S "/as sysdba" <<EOF
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on;
set time off timing off SQLPROMPT "SQL>";
select value from gv\\\$parameter where name='cluster_database' and rownum=1;
exit
EOF
`

[ -z "$(echo $rac | grep -v ":")" ] && {
   rac="Unknown"
}

primary=`${__sqlpluscmd} -S "/as sysdba" <<EOF
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on;
set time off timing off SQLPROMPT "SQL>";
select database_role from gv\\\$database where rownum=1;
exit
EOF
`

[ -z "$(echo $primary | grep -v ":")" ] && {
   primary="Unknown"
}


[ "$openmode" = "OPEN" ] && {

cluster=$(echo `${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
select (select t2.name from v\\\$database t2) name, '@'||t1.instance_name||'@'||replace(t1.host_name, '.', '%')||',' from gv\\\$instance t1 order by t1.host_name;
exit
EOF
` | sed 's/ //g')

__dbversion=`${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
select replace(SUBSTR(VERSION,1,2), '.', '') from v\\\$INSTANCE ;
exit
EOF
`

ctltype=`${__sqlpluscmd} -S / as sysdba <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
set heading off
set feedback off
select trim(controlfile_type) from v\\\$database;
EOF
`

[ ${__dbversion} -eq 9 ] && ctltype="CURRENT"

multitenant="NO"
if [ ${__dbversion} -ge 12 ];then
multitenant=`${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
select cdb from v\\\$database ;
exit
EOF
`
[ -z "$multitenant" ] && multitenant="NO"
fi

if [ ${__dbversion} -eq 9 ];then
tracepath=
elif [ ${__dbversion} -eq 10 ];then
tracepath=`${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
select value from v\\\$parameter where name='background_dump_dest' ;
exit
EOF
`
else
tracepath=`${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
col value format a120
select value from v\\\$diag_info where name='Diag Trace' ;
exit
EOF
`
fi

if [ ${__dbversion} -eq 9 ];then
tracepath="none"
elif [ ${__dbversion} -eq 10 ];then
alertpath="none"
else
alertpath=`${__sqlpluscmd} -S "/as sysdba" <<EOF 2>/dev/null
set heading off feedback off pagesize 0 linesize 200;
set verify off echo off termout off trimout on trimspool on ;
set time off timing off SQLPROMPT "SQL>";
col value format a120
select value from v\\\$diag_info where name='Diag Alert' ;
exit
EOF
`
fi

if [ ${__dbversion} -eq 11 ];then
    crsalert=$(ls $(cat /etc/oracle/olr.loc 2>/dev/null | grep olrconfig_loc | awk -F'=' '{print $2}' | awk -F'/cdata' '{print $1}')/log/*/*.log | head -1)
    if [ -z "$crsalert" ]; then
        crsalert=$(ls $(echo $ORACLE_BASE | awk -F'/' '{$NF="grid_base";print}' | sed 's# #/#g')/log/*/*.log | head -1);
    fi
elif [ ${__dbversion} -ge 12 ];then
    crsalert=$(ls $(cat /etc/oracle/olr.loc 2>/dev/null | grep olrconfig_loc | awk -F'=' '{print $2}' | awk -F'/crsdata' '{print $1}')/diag/crs/$(hostname)/crs/trace/*.log | head -1)
    if [ -z "$crsalert" ]; then
        crsalert=$(ls $(echo $ORACLE_BASE | awk -F'/' '{$NF="grid_base";print}' | sed 's# #/#g')/diag/crs/$(hostname)/*/trace/*.log | head -1);
    fi
else
    crsalert="Unknown"
fi

} || {
cluster="Unknown@${sid}@$(hostname)"
__dbversion=$(${__sqlpluscmd} -v | sed 's/ /\n/g' | grep '[0-9].' | awk -F. '{print $1}' | head -1)
ctltype="Unknown"
multitenant="Unknown"
tracepath="Unknown"
alertpath="Unknown"
crsalert="Unknown"
}

ec=0
[ $(echo $cluster | grep -q ^Unknown; echo $?) -eq 0 ] && { echo "cluster is Unknown"; ec=1; }
[ -z "$__dbversion" ] && { echo "dbversion is empty"; ec=1; }
[ "$openmode" != "OPEN" ] && { echo "openmode is $openmode"; ec=1; }
[ $ec -ne 0 ] && { echo "[Error] some errors happend when pre check"; exit 1; } || {
	echo "[OK] pre check is OK"
}

export __out=./Oracle.$sid.$(hostname | sed 's/\./%/g').$(date +%Y%m%d%H%M%S).eout
>./$__out

_head instance $sid
echo  "sid: $sid
oraclebase: $__oraclebase
oraclehome: $__oraclehome
runas: $__runas
ostype: $__ostype
sqlpluscmd: $__sqlpluscmd
openmode: $openmode
rac: $rac
primary: $primary
dbversion: $__dbversion
ctltype: $ctltype
multitenant: $multitenant
tracepath: $tracepath
alertpath: $alertpath
crsalert: $crsalert
psexist: $psexist
cluster: $(echo $cluster)" >>$__out

_head host $sid
_host >>$__out

_head lspatches $sid
_lspatches >>$__out

_head lsinventory $sid
_lsinventory >>$__out

_head lo $sid
_lo >>$__out

_head conf/limits $sid
_limits >>$__out

_head conf/etchosts $sid
_etchosts >>$__out

_head status/fspct $sid
_fspct >>$__out

_head status/inodepct $sid
_inodepct >>$__out

_head sqlnet $sid
_sqlnet >>$__out

_head awkalert $sid
_awkalert "$tracepath/alert_$sid.log" >>$__out

_head crsctlstat $sid
_crsctlstat >>$__out

_head conf/osparm $sid
_osparm >>$__out

_head status/netstat $sid
_netstat >>$__out

_head crsalert $sid
_crsalert "$crsalert" >>$__out


########################################################################

#    "prec": "IsStandby==false && (IsMultitenant==false || VersionCompare(Version,'>=','V12'))",
[ "$ctltype" != "STANDBY" ] && {
[ "$multitenant" = "NO" -o $__dbversion -ge 12 ] && {

_sql $sid scheduler_windows
}
}

#    "prec": "IsStandby==false && IsMultitenant==false",
[ "$ctltype" != "STANDBY" -a "$multitenant" = "NO" ] && {

_sql $sid cursor_monitor
_sql $sid db_time_per_second
_sql $sid hist_undo_stat
_sql $sid logic_read_per_second
_sql $sid physic_read_per_second
_sql $sid spfile_warning
}
#    "prec": "IsStandby==false && IsMultitenant==true",
[ "$ctltype" != "STANDBY" -a "$multitenant" != "NO" ] && {

_sql $sid ges_traffic
}
#    "prec": "IsStandby==false && VersionCompare(Version,'<','V11')",
[ "$ctltype" != "STANDBY" -a $__dbversion -lt 11 ] && {
_sql $sid tbs_fragement_pct
_sql $sid topevent10g
}
#    "prec": "IsStandby==false && VersionCompare(Version,'<','V12')",
[ "$ctltype" != "STANDBY" -a $__dbversion -lt 12 ] && {

_sql $sid audit
_sql $sid audittrail
_sql $sid baseinfo
_sql $sid comp
_sql $sid datafile
_sql $sid flashback
_sql $sid foreignkey
_sql $sid fullscan
_sql $sid invalidcons
_sql $sid invalididx
_sql $sid invalidobj
_sql $sid invalidtrigger
_sql $sid jobs
_sql $sid optimizer_stats_advisor
_sql $sid parameter
_sql $sid patchapply
_sql $sid profile
_sql $sid recyclebin
_sql $sid resourcelimit
_sql $sid sequence
_sql $sid snapsetting
_sql $sid tbscheck
_sql $sid unified_audit
_sql $sid userinfo
_sql $sid userpriv
_sql $sid spparameter

}
#    "prec": "IsStandby==false && VersionCompare(Version,'>=','V11')",
[ "$ctltype" != "STANDBY" -a $__dbversion -ge 11 ] && {

_sql $sid archive_dest_status
_sql $sid asm_disk_detail
_sql $sid dstcheck
_sql $sid stats_job_running
_sql $sid topevent
}
#    "prec": "IsStandby==false && VersionCompare(Version,'>=','V12')",
[ "$ctltype" != "STANDBY" -a $__dbversion -ge 12 ] && {

_sql $sid audit12c
_sql $sid audittrail12c
_sql $sid autotask
_sql $sid baseinfo12c
_sql $sid comp12c
_sql $sid datafile12c
_sql $sid flashback12c
_sql $sid foreignkey12c
_sql $sid fullscan12c
_sql $sid invalidcons12c
_sql $sid invalididx12c
_sql $sid invalidobj12c
_sql $sid invalidtrigger12c
_sql $sid jobs12c
_sql $sid optimizer_stats_advisor12c
_sql $sid parameter12c
_sql $sid patchapply12c
_sql $sid pdbsavedstate
_sql $sid pdbstat
_sql $sid profile12c
_sql $sid recyclebin_12c
_sql $sid resourcelimit12c
_sql $sid sequence12c
_sql $sid snapsetting12c
_sql $sid tbscheck12c
_sql $sid unified_audit_12c
_sql $sid unified_audit_option
_sql $sid unified_audit_purge
_sql $sid userinfo12c
_sql $sid userpriv12c
_sql $sid compatible_rdbms
}
#    "prec": "IsStandby==false",
[ "$ctltype" != "STANDBY" -a "$openmode" != "ORACLE_not_available" ] && {

_sql $sid archsize
_sql $sid bitcoin
_sql $sid controlfile
_sql $sid dgapply
_sql $sid dlm_traffic
_sql $sid efficent
_sql $sid hiddenparms
_sql $sid indicator
_sql $sid lmscount
_sql $sid logswitch
_sql $sid onlinelog
_sql $sid rman
_sql $sid scnhealthcheck
_sql $sid sequence_cache
_sql $sid sysdba
_sql $sid timezone
_sql $sid version
_sql $sid dg_parameters

}
#    "prec": "IsStandby==true",
[ "$ctltype" = "STANDBY" ] && {

_sql $sid archive_gap
_sql $sid dataguard_stats
_sql $sid dataguard_status
}

[ "$openmode" != "ORACLE_not_available" ] && {
_sql $sid  dgdelay
_sql $sid  disk_same_size
_sql $sid  diskgroup
_sql $sid  failgroup_summary
_sql $sid  failgroup
}

echo "--------------------"
echo $__out

[ ! -z "$ftp_server" -a -f "$__out" ] && {
local_file=$__out
ftpLog=$$.ftp.log
_ftp
rm -f $ftpLog
}

done

#archive_dest_status:set lines 400
#archive_dest_status:set pages 1000
#archive_dest_status:set feedback off
#archive_dest_status:
#archive_dest_status:select chr(34)||dest_id||chr(34)       ||','||
#archive_dest_status:       chr(34)||dest_name||chr(34)     ||','||
#archive_dest_status:       chr(34)||DESTINATION||chr(34)   ||','|| 
#archive_dest_status:       chr(34)||DB_UNIQUE_NAME||chr(34)||','|| 
#archive_dest_status:       chr(34)||type||chr(34)          ||','||
#archive_dest_status:       chr(34)||DATABASE_MODE||chr(34) ||','|| 
#archive_dest_status:       chr(34)||RECOVERY_MODE||chr(34) ||','|| 
#archive_dest_status:       chr(34)||status||chr(34)    ||','||
#archive_dest_status:       chr(34)||STANDBY_LOGFILE_COUNT  ||chr(34)
#archive_dest_status:from v$archive_dest_status
#archive_dest_status:where destination is not null;
#archive_dest_status:
#archive_gap:set feedback off
#archive_gap:set heading off
#archive_gap:set lines 400 pages 0
#archive_gap:
#archive_gap:select chr(34)||USERENV('Instance')||chr(34)||','||   
#archive_gap:       chr(34)||high.thread# ||chr(34)||','||  
#archive_gap:       chr(34)||low.lsq ||chr(34)||','||  
#archive_gap:       chr(34)||high.hsq ||chr(34)
#archive_gap: from
#archive_gap:  (select a.thread#, rcvsq, min(a.sequence#)-1 hsq
#archive_gap:   from v$archived_log a,
#archive_gap:        (select lh.thread#, lh.resetlogs_change#, max(lh.sequence#) rcvsq
#archive_gap:           from v$log_history lh, v$database_incarnation di
#archive_gap:          where lh.resetlogs_time = di.resetlogs_time
#archive_gap:            and lh.resetlogs_change# = di.resetlogs_change#
#archive_gap:            and di.status = 'CURRENT'
#archive_gap:            and lh.thread# is not null
#archive_gap:            and lh.resetlogs_change# is not null
#archive_gap:            and lh.resetlogs_time is not null
#archive_gap:         group by lh.thread#, lh.resetlogs_change#
#archive_gap:        ) b
#archive_gap:   where a.thread# = b.thread#
#archive_gap:     and a.resetlogs_change# = b.resetlogs_change#
#archive_gap:     and a.sequence# > rcvsq
#archive_gap:   group by a.thread#, rcvsq) high,
#archive_gap: (select srl_lsq.thread#, nvl(lh_lsq.lsq, srl_lsq.lsq) lsq
#archive_gap:   from
#archive_gap:     (select thread#, min(sequence#)+1 lsq
#archive_gap:      from
#archive_gap:        v$log_history lh, x$kccfe fe, v$database_incarnation di
#archive_gap:      where to_number(fe.fecps) <= lh.next_change#
#archive_gap:        and to_number(fe.fecps) >= lh.first_change#
#archive_gap:        and fe.fedup!=0 and bitand(fe.festa, 12) = 12
#archive_gap:        and di.resetlogs_time = lh.resetlogs_time
#archive_gap:        and lh.resetlogs_change# = di.resetlogs_change#
#archive_gap:        and di.status = 'CURRENT'
#archive_gap:      group by thread#) lh_lsq,
#archive_gap:     (select thread#, max(sequence#)+1 lsq
#archive_gap:      from
#archive_gap:        v$log_history
#archive_gap:      where (select min( to_number(fe.fecps))
#archive_gap:             from x$kccfe fe
#archive_gap:             where fe.fedup!=0 and bitand(fe.festa, 12) = 12)
#archive_gap:      >= next_change#
#archive_gap:      group by thread#) srl_lsq
#archive_gap:   where srl_lsq.thread# = lh_lsq.thread#(+)
#archive_gap:  ) low
#archive_gap: where low.thread# = high.thread#
#archive_gap: and lsq < = hsq
#archive_gap: and hsq > rcvsq;
#archive_gap:
#archive_gap:
#archsize:set lines 200
#archsize:set pages 0
#archsize:set feedback off
#archsize:select chr(34)||to_char(first_time,'yyyymmdd') ||chr(34)||','||
#archsize:       chr(34)||nvl(round(sum(blocks * block_size) / 1024 / 1024,0),0) ||chr(34)
#archsize:from v$archived_log
#archsize:where dest_id = 1
#archsize:  and first_time > sysdate  - 15
#archsize:  and thread# in (select thread# from v$thread)
#archsize:group by to_char(first_time,'yyyymmdd')
#archsize:order by to_char(first_time,'yyyymmdd');
#archsize:
#archsize:
#archsize:
#asm_disk_detail:set lines 400
#asm_disk_detail:set pages 1000
#asm_disk_detail:set feedback off
#asm_disk_detail:select chr(34)||a.group_number  ||chr(34)||','||
#asm_disk_detail:       chr(34)||a.name          ||chr(34)||','||
#asm_disk_detail:       chr(34)||b.name          ||chr(34)||','||
#asm_disk_detail:       chr(34)||b.path          ||chr(34)||','||
#asm_disk_detail:       chr(34)||b.state         ||chr(34)||','||
#asm_disk_detail:       chr(34)||b.total_mb      ||chr(34)||','||
#asm_disk_detail:       chr(34)||b.os_mb         ||chr(34)
#asm_disk_detail:from v$asm_diskgroup a,        
#asm_disk_detail:     v$asm_disk b
#asm_disk_detail:where a.group_number = b.group_number
#asm_disk_detail:order by a.group_number,b.name
#asm_disk_detail:;
#asm_disk_detail:
#asm_disk_detail:
#asm_disk_detail:
#audit:set lines 400
#audit:set pages 1000
#audit:set feedback off
#audit:
#audit:select chr(34)||nvl(USER_NAME,' ')||chr(34)||','||
#audit:       chr(34)||PRIVILEGE         ||chr(34)||','||
#audit:       chr(34)||SUCCESS           ||chr(34)||','||
#audit:       chr(34)||FAILURE           ||chr(34)  
#audit: from dba_priv_audit_opts order by user_name,PRIVILEGE;
#audit:
#audit:
#audit12c:set lines 400
#audit12c:set pages 1000
#audit12c:set feedback off
#audit12c:
#audit12c:select chr(34)||nvl(b.name,'CDB$ROOT') ||chr(34)||','||
#audit12c:       chr(34)||nvl(USER_NAME,' ')     ||chr(34)||','||
#audit12c:       chr(34)||PRIVILEGE              ||chr(34)||','||
#audit12c:       chr(34)||SUCCESS                ||chr(34)||','||
#audit12c:       chr(34)||FAILURE                ||chr(34)  
#audit12c: from  containers(dba_priv_audit_opts) a,v$pdbs b
#audit12c: where a.con_id = b.con_id(+)
#audit12c:  order by a.con_id,a.user_name,a.PRIVILEGE;
#audit12c:
#audit12c:
#audittrail:set lines 400
#audittrail:set pages 1000
#audittrail:set heading off
#audittrail:set feedback off
#audittrail:
#audittrail:SELECT chr(34)||username||chr(34)||','||
#audittrail:       chr(34)||tm||chr(34)||','||
#audittrail:       chr(34)||nvl(obj_name,'NULL')||chr(34)||','||
#audittrail:       chr(34)||action_name||chr(34)||','||
#audittrail:       chr(34)||nvl(sql_text,'NULL')||chr(34)
#audittrail:FROM (select username, 
#audittrail:             to_char(timestamp,'yyyymmdd HH24:MI') tm, 
#audittrail:             obj_name, 
#audittrail:             action_name, 
#audittrail:             replace(substr(sql_text,1,80),chr(34),'') as sql_text
#audittrail:        from dba_audit_trail where action_name not in ('LOGON','LOGOFF') AND timestamp > SYSDATE - 15
#audittrail:        ORDER BY timestamp desc) v 
#audittrail:     WHERE ROWNUM<50; 
#audittrail:
#audittrail:
#audittrail:
#audittrail12c:set lines 400
#audittrail12c:set pages 1000
#audittrail12c:set heading off
#audittrail12c:set feedback off
#audittrail12c:
#audittrail12c:SELECT chr(34)||nvl(b.name,'CDB$ROOT')  ||chr(34)||','||
#audittrail12c:       chr(34)||username                ||chr(34)||','||
#audittrail12c:       chr(34)||tm                      ||chr(34)||','||
#audittrail12c:       chr(34)||nvl(obj_name,'NULL')    ||chr(34)||','||
#audittrail12c:       chr(34)||action_name||chr(34)    ||','||
#audittrail12c:       chr(34)||nvl(sql_text,'NULL')    ||chr(34)
#audittrail12c:FROM (select con_id,username, 
#audittrail12c:             to_char(timestamp,'yyyymmdd HH24:MI') tm, 
#audittrail12c:             obj_name, 
#audittrail12c:             action_name, 
#audittrail12c:             replace(substr(sql_text,1,80),chr(34),'') as sql_text
#audittrail12c:        from containers(dba_audit_trail )  where action_name not in ('LOGON','LOGOFF') AND timestamp > SYSDATE - 15
#audittrail12c:        ORDER BY timestamp desc) v  ,v$pdbs b 
#audittrail12c:     WHERE v.con_id = b.con_id(+) and ROWNUM<50; 
#audittrail12c:     
#audittrail12c:
#audittrail12c:
#audittrail12c:
#autotask:set lines 400
#autotask:set pages 1000
#autotask:set heading off
#autotask:set feedback off
#autotask:SELECT  CHR(34)||v.client_name ||CHR(34)||','||
#autotask:        CHR(34)||v.status||CHR(34)||','|| 
#autotask:        CHR(34)|| case
#autotask:         when v.client_name='auto optimizer stats collection' and v.status != 'ENABLED' then 'YES'
#autotask:         when v.client_name='auto space advisor' and v.status = 'ENABLED' then 'YES'
#autotask:         when v.client_name='sql tuning advisor' and v.status = 'ENABLED' then 'YES'
#autotask:         else  'NO' END ||CHR(34) 
#autotask:  FROM (select client_name,status from dba_autotask_client order by 1) v;
#autotask:
#autotask:
#baseinfo:set lines 200
#baseinfo:set  pages 1000
#baseinfo:col item format a64
#baseinfo:col  value format a80
#baseinfo:set heading off
#baseinfo:set feedback off
#baseinfo:
#baseinfo:SELECT chr(34)||'DB Name'                                        ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_name' ; 
#baseinfo:SELECT chr(34)||'DB Unique name'                                 ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_unique_name' ; 
#baseinfo:SELECT chr(34)||'Instance Name'                                  ||chr(34)||','||chr(34)|| instance_name ||chr(34)  as dbinfoparms from  v$instance ; 
#baseinfo:SELECT chr(34)||'DB Startup Time'                                ||chr(34)||','||chr(34)|| to_char(startup_time, 'YYYY-MM-DD') ||chr(34) as dbinfoparms from  v$instance ; 
#baseinfo:SELECT chr(34)||'CPU Infomation'                                 ||chr(34)||','||chr(34)|| (select to_char(value)||' Sockets ' T   from  v$osstat where stat_name='NUM_CPU_SOCKETS')||(select to_char(value)||' Cores ' T from  v$osstat where stat_name='NUM_CPU_CORES')||(select TO_CHAR(value)||' Threads ' T   from  v$osstat WHERE stat_name='NUM_CPUS') ||chr(34)  as dbinfoparms from  dual ;
#baseinfo:SELECT chr(34)||'Physical Memory Size'                           ||chr(34)||','||chr(34)|| min(to_char(round(value/1024/1024,0)))||' MB' ||chr(34) as dbinfoparms from  gv$osstat where stat_name='PHYSICAL_MEMORY_BYTES' ; 
#baseinfo:SELECT chr(34)||'OS Platform'                                    ||chr(34)||','||chr(34)|| dbms_utility.port_string ||chr(34) as dbinfoparms from  dual ;  
#baseinfo:SELECT chr(34)||'NLS_TERRITORY'                                  ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_TERRITORY' ; 
#baseinfo:SELECT chr(34)||'NLS_LANGUAGE'                                   ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_LANGUAGE' ; 
#baseinfo:SELECT chr(34)||'NLS_CHARACTERSET'                               ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_CHARACTERSET' ; 
#baseinfo:SELECT chr(34)||'NLS_NCHAR_CHARACTERSET'                         ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_NCHAR_CHARACTERSET' ; 
#baseinfo:SELECT chr(34)||'DB_BLOCK_SIZE'                                  ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_block_size' ; 
#baseinfo:SELECT chr(34)||'Number of Tablespaces'                          ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  v$tablespace ; 
#baseinfo:SELECT chr(34)||'Number of Datafiles/Tempfile'                   ||chr(34)||','||chr(34)|| to_char(sum(a))   ||chr(34) as dbinfoparms from  (select count(*) a   from  v$datafile union select count(*) a  from  v$tempfile) ; 
#baseinfo:SELECT chr(34)||'Number of Control Files'                        ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  v$controlfile ; 
#baseinfo:SELECT chr(34)||'Number of Redo Log Groups'                      ||chr(34)||','||chr(34)|| to_char(count(group#)) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo:SELECT chr(34)||'Number of Redo Log Members Per Group'           ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  (select distinct bytes  as dbinfoparms from  v$log) ; 
#baseinfo:SELECT chr(34)||'Number of Concurrent Users'                     ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  gv$session where username is not null ; 
#baseinfo:SELECT chr(34)||'Number of Active Concurrent Users'              ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  gv$session where username is not null and sid not in (select sid  as dbinfoparms from  v$mystat) and status='ACTIVE' ; 
#baseinfo:SELECT chr(34)||'Datafile Size(MB)'                              ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),999999999.99) ||chr(34) as dbinfoparms from  dba_data_files ; 
#baseinfo:SELECT chr(34)||'Tempfile Size(MB)'                              ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_temp_files ; 
#baseinfo:SELECT chr(34)||'UNDO Tablespace Size(MB)'                       ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_data_files where tablespace_name=(select value  as dbinfoparms from  v$parameter where name ='undo_tablespace') ; 
#baseinfo:SELECT chr(34)||'Segment Total Size(MB)'                         ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),999999999.99) ||chr(34) as dbinfoparms from  dba_segments ; 
#baseinfo:SELECT chr(34)||'Max Redo Log Size(MB)'                          ||chr(34)||','||chr(34)|| to_char(max(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo:SELECT chr(34)||'Min Redo Log Size(MB)'                          ||chr(34)||','||chr(34)|| to_char(min(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo:SELECT chr(34)||'Redo logs the same size'                        ||chr(34)||','||chr(34)|| decode(max(bytes)-min(bytes),0,'YES','NO') ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo:SELECT chr(34)||'Redo logs being multiplexed'                    ||chr(34)||','||chr(34)|| decode(avg(members),2,'YES',3,'YES','NO')  ||chr(34) as dbinfoparms from  v$log ;  
#baseinfo:SELECT chr(34)||'Using  SPFILE'                                  ||chr(34)||','||chr(34)|| decode (nvl(value,'NO'),'NO','NO','YES')   ||chr(34) as dbinfoparms from  v$parameter where NAME='spfile' ; 
#baseinfo:SELECT chr(34)||'Max Object ID'                                  ||chr(34)||','||chr(34)|| to_char(max(data_object_id))               ||chr(34) as dbinfoparms from  dba_objects ; 
#baseinfo:SELECT chr(34)||'Datafile File Number Useage(Pct)'               ||chr(34)||','||chr(34)|| to_char( round(100*(select count(*)        as dbinfoparms from  dba_data_files)/(select value  as dbinfoparms from  v$parameter where name='db_files'),2))  ||chr(34) as dbinfoparms from  dual ; 
#baseinfo:SELECT chr(34)||'Force Logging Enabled'                          ||chr(34)||','||chr(34)|| force_logging                              ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo:SELECT chr(34)||'Supplemental Log Enabled'                       ||chr(34)||','||chr(34)|| supplemental_log_data_min                  ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo:SELECT chr(34)||'Flashback Enabled'                              ||chr(34)||','||chr(34)|| flashback_on                               ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo:SELECT chr(34)||'Archiving Enabled'                              ||chr(34)||','||chr(34)|| log_mode                                   ||chr(34) as dbinfoparms from  v$database ;
#baseinfo:SELECT CHR(34)||'SGA Granul Size(MB)'                            ||chr(34)||','||chr(34)|| to_char(bytes/1024/1024)               ||chr(34) as dbinfoparms from  v$sgainfo where name ='Granule Size';                      
#baseinfo:
#baseinfo12c:set lines 200
#baseinfo12c:set  pages 1000
#baseinfo12c:col item format a64
#baseinfo12c:col  value format a80
#baseinfo12c:set heading off
#baseinfo12c:set feedback off
#baseinfo12c:
#baseinfo12c:SELECT chr(34)||'DB Name'                                        ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_name' ; 
#baseinfo12c:SELECT chr(34)||'DB Unique name'                                 ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_unique_name' ; 
#baseinfo12c:SELECT chr(34)||'Instance Name'                                  ||chr(34)||','||chr(34)|| instance_name ||chr(34)  as dbinfoparms from  v$instance ; 
#baseinfo12c:SELECT chr(34)||'DB Startup Time'                                ||chr(34)||','||chr(34)|| to_char(startup_time, 'YYYY-MM-DD') ||chr(34) as dbinfoparms from  v$instance ; 
#baseinfo12c:SELECT chr(34)||'CPU Infomation'                                 ||chr(34)||','||chr(34)|| (select to_char(value)||' Sockets ' T   from  v$osstat where stat_name='NUM_CPU_SOCKETS')||(select to_char(value)||' Cores ' T from  v$osstat where stat_name='NUM_CPU_CORES')||(select TO_CHAR(value)||' Threads ' T   from  v$osstat WHERE stat_name='NUM_CPUS') ||chr(34)  as dbinfoparms from  dual ;
#baseinfo12c:SELECT chr(34)||'Physical Memory Size'                           ||chr(34)||','||chr(34)|| min(to_char(round(value/1024/1024,0)))||' MB' ||chr(34) as dbinfoparms from  gv$osstat where stat_name='PHYSICAL_MEMORY_BYTES' ; 
#baseinfo12c:SELECT chr(34)||'OS Platform'                                    ||chr(34)||','||chr(34)|| dbms_utility.port_string ||chr(34) as dbinfoparms from  dual ;  
#baseinfo12c:SELECT chr(34)||'NLS_TERRITORY'                                  ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_TERRITORY' ; 
#baseinfo12c:SELECT chr(34)||'NLS_LANGUAGE'                                   ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_LANGUAGE' ; 
#baseinfo12c:SELECT chr(34)||'NLS_CHARACTERSET'                               ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_CHARACTERSET' ; 
#baseinfo12c:SELECT chr(34)||'NLS_NCHAR_CHARACTERSET'                         ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$nls_parameters where parameter='NLS_NCHAR_CHARACTERSET' ; 
#baseinfo12c:SELECT chr(34)||'DB_BLOCK_SIZE'                                  ||chr(34)||','||chr(34)|| value ||chr(34) as dbinfoparms from  v$parameter where name='db_block_size' ; 
#baseinfo12c:SELECT chr(34)||'Number of Tablespaces'                          ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  v$tablespace ; 
#baseinfo12c:SELECT chr(34)||'Number of Datafiles/Tempfile'                   ||chr(34)||','||chr(34)|| to_char(sum(a))   ||chr(34) as dbinfoparms from  (select count(*) a   from  v$datafile union select count(*) a  from  v$tempfile) ; 
#baseinfo12c:SELECT chr(34)||'Number of Control Files'                        ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  v$controlfile ; 
#baseinfo12c:SELECT chr(34)||'Number of Redo Log Groups'                      ||chr(34)||','||chr(34)|| to_char(count(group#)) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo12c:SELECT chr(34)||'Number of Redo Log Members Per Group'           ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  (select distinct bytes  as dbinfoparms from  v$log) ; 
#baseinfo12c:SELECT chr(34)||'Number of Concurrent Users'                     ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  gv$session where username is not null ; 
#baseinfo12c:SELECT chr(34)||'Number of Active Concurrent Users'              ||chr(34)||','||chr(34)|| to_char(count(*)) ||chr(34) as dbinfoparms from  gv$session where username is not null and sid not in (select sid  as dbinfoparms from  v$mystat) and status='ACTIVE' ; 
#baseinfo12c:SELECT chr(34)||'Datafile Size(MB)'                              ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_data_files ; 
#baseinfo12c:SELECT chr(34)||'Tempfile Size(MB)'                              ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_temp_files ; 
#baseinfo12c:SELECT chr(34)||'UNDO Tablespace Size(MB)'                       ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_data_files where tablespace_name=(select value  as dbinfoparms from  v$parameter where name ='undo_tablespace') ; 
#baseinfo12c:SELECT chr(34)||'Segment Total Size(MB)'                         ||chr(34)||','||chr(34)|| to_char(sum(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  dba_segments ; 
#baseinfo12c:SELECT chr(34)||'Max Redo Log Size(MB)'                          ||chr(34)||','||chr(34)|| to_char(max(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo12c:SELECT chr(34)||'Min Redo Log Size(MB)'                          ||chr(34)||','||chr(34)|| to_char(min(bytes/1024/1024),9999999.99) ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo12c:SELECT chr(34)||'Redo logs the same size'                        ||chr(34)||','||chr(34)|| decode(max(bytes)-min(bytes),0,'YES','NO') ||chr(34) as dbinfoparms from  v$log ; 
#baseinfo12c:SELECT chr(34)||'Redo logs being multiplexed'                    ||chr(34)||','||chr(34)|| decode(avg(members),2,'YES',3,'YES','NO')  ||chr(34) as dbinfoparms from  v$log ;  
#baseinfo12c:SELECT chr(34)||'Using  SPFILE'                                  ||chr(34)||','||chr(34)|| decode (nvl(value,'NO'),'NO','NO','YES')   ||chr(34) as dbinfoparms from  v$parameter where NAME='spfile' ; 
#baseinfo12c:SELECT chr(34)||'Max Object ID'                                  ||chr(34)||','||chr(34)|| to_char(max(data_object_id))               ||chr(34) as dbinfoparms from  dba_objects ; 
#baseinfo12c:SELECT chr(34)||'Datafile File Number Useage(Pct)'               ||chr(34)||','||chr(34)|| to_char( round(100*(select count(*)        as dbinfoparms from  dba_data_files)/(select value  as dbinfoparms from  v$parameter where name='db_files'),2))  ||chr(34) as dbinfoparms from  dual ; 
#baseinfo12c:SELECT chr(34)||'Force Logging Enabled'                          ||chr(34)||','||chr(34)|| force_logging                              ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo12c:SELECT chr(34)||'Supplemental Log Enabled'                       ||chr(34)||','||chr(34)|| supplemental_log_data_min                  ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo12c:SELECT chr(34)||'Flashback Enabled'                              ||chr(34)||','||chr(34)|| flashback_on                               ||chr(34) as dbinfoparms from  v$database ; 
#baseinfo12c:SELECT chr(34)||'Archiving Enabled'                              ||chr(34)||','||chr(34)|| log_mode                                   ||chr(34) as dbinfoparms from  v$database ;
#baseinfo12c:SELECT CHR(34)||'SGA Granul Size(MB)'                            ||chr(34)||','||chr(34)|| to_char(bytes/1024/1024)               ||chr(34) as dbinfoparms from  v$sgainfo where name ='Granule Size'; 
#baseinfo12c:
#baseinfo12c:
#bitcoin:SET LINES 400
#bitcoin:SET PAGES 1000
#bitcoin:SET FEEDBACK OFF
#bitcoin:COL OWNER FOR A20
#bitcoin:COL OBJECT_NAME FOR A40
#bitcoin:COL OBJECT_TYPE FOR A15
#bitcoin:COL CREATED FORMAT A20
#bitcoin:SELECT chr(34)||OWNER   ||chr(34)||','||
#bitcoin:       chr(34)||OBJECT_NAME  ||chr(34)||','||
#bitcoin:       chr(34)||OBJECT_TYPE  ||chr(34)||','||
#bitcoin:       CHR(34)||TO_CHAR(CREATED, 'YYYY-MM-DD HH24:MI:SS')||CHR(34) 
#bitcoin:  FROM DBA_OBJECTS
#bitcoin: WHERE OBJECT_NAME LIKE 'DBMS_CORE_INTERNA%'
#bitcoin:    OR OBJECT_NAME LIKE 'DBMS_SYSTEM_INTERNA%'
#bitcoin:    OR OBJECT_NAME LIKE 'DBMS_SUPPORT%';
#bitcoin:
#bitcoin:
#bitcoin:
#comp:set lines 400
#comp:set pages 1000
#comp:set feedback off
#comp:set heading off
#comp:col comp_name format a40
#comp:col version format a30
#comp:col modified format a40
#comp:col status format a24
#comp:select chr(34)||comp_id ||chr(34)||','||
#comp:       chr(34)||comp_name||chr(34)||','||  
#comp:       chr(34)||version||chr(34)||','||  
#comp:       chr(34)||status||chr(34)||','||  
#comp:       chr(34)||modified ||chr(34)
#comp: from dba_registry order by 1;
#comp:
#comp12c:set lines 400
#comp12c:set pages 1000
#comp12c:set feedback off
#comp12c:set heading off
#comp12c:
#comp12c:SELECT CHR(34)||NVL(B.NAME,'CDB$ROOT')||CHR(34)||','||
#comp12c:       chr(34)||a.comp_id ||chr(34)||','||
#comp12c:       chr(34)||a.comp_name||chr(34)||','||  
#comp12c:       chr(34)||a.version||chr(34)||','||  
#comp12c:       chr(34)||a.status||chr(34)||','||  
#comp12c:       chr(34)||a.modified ||chr(34)
#comp12c:FROM (SELECT CON_ID, COMP_ID,COMP_NAME,VERSION,STATUS,MODIFIED FROM containers(dba_registry)) A,V$PDBS B
#comp12c:WHERE B.CON_ID(+)=A.CON_ID
#comp12c:ORDER BY A.CON_ID,A.COMP_ID;
#controlfile:set lines 400
#controlfile:set pages 1000
#controlfile:set feedback off
#controlfile:set heading off
#controlfile:select chr(34)||name||chr(34)||','||
#controlfile:       chr(34)||case when (select count(*) as cnt  from v$controlfile) >1 then 'YES' ELSE 'NO' END ||chr(34)
#controlfile:from v$controlfile;
#controlfile:
#cursor_monitor:SET LINESIZE 200
#cursor_monitor:SET FEEDBACK OFF
#cursor_monitor:SET HEADING OFF
#cursor_monitor:SET PAGESIZE 0
#cursor_monitor:
#cursor_monitor:SELECT chr(34) || v.sid || chr(34) || ',' ||  
#cursor_monitor:       chr(34) || v.value || chr(34) || ',' ||   
#cursor_monitor:       chr(34) || param.value || chr(34)
#cursor_monitor:FROM  (
#cursor_monitor:        SELECT
#cursor_monitor:              cust.sid AS sid,
#cursor_monitor:              COUNT(*) AS value
#cursor_monitor:        FROM v$open_cursor cust
#cursor_monitor:        GROUP BY cust.sid
#cursor_monitor:        ORDER BY COUNT(*) DESC
#cursor_monitor:      ) v join v$parameter param on param.name = 'open_cursors'
#cursor_monitor:WHERE rownum < 11
#cursor_monitor:;
#cursor_monitor:
#datafile:
#datafile:set lines 400
#datafile:set pages 1000
#datafile:col tablespace_name format a36
#datafile:col file_name format a200
#datafile:col autoextensible format a18
#datafile:col status format a10
#datafile:col type format a16
#datafile:select  chr(34)||type||chr(34)||','||
#datafile:        chr(34)||tablespace_name||chr(34)||','||
#datafile:        chr(34)||file_name||chr(34)||','||
#datafile:        chr(34)||size_mb||chr(34)||','||
#datafile:        chr(34)||max_size_mb||chr(34)||','||
#datafile:        chr(34)||autoextensible||chr(34)||','||
#datafile:        chr(34)||status||chr(34)
#datafile:from (
#datafile:select  'Datafile' as type,tablespace_name, 
#datafile:        file_name, 
#datafile:        trunc(bytes/1024/1024) size_mb,
#datafile:        trunc(decode(autoextensible ,'YES',greatest(MAXBYTES,BYTES),'NO',BYTES)/1024/1024) max_size_mb, 
#datafile:        autoextensible,
#datafile:        status from dba_data_files
#datafile:union all
#datafile:select 'Tempfile' as type,
#datafile:        tablespace_name, 
#datafile:        file_name, 
#datafile:        trunc(bytes/1024/1024) size_mb,
#datafile:        trunc(decode(autoextensible ,'YES',greatest(MAXBYTES,BYTES),'NO',BYTES)/1024/1024)  max_size_mb, 
#datafile:        autoextensible,
#datafile:        status from dba_temp_files
#datafile:order by 1,2) v;
#datafile:
#datafile:
#datafile:
#datafile12c:set lines 400
#datafile12c:set pages 1000
#datafile12c:col tablespace_name format a36
#datafile12c:col file_name format a200
#datafile12c:col autoextensible format a18
#datafile12c:col status format a10
#datafile12c:col type format a16
#datafile12c:select  chr(34)||nvl(w.name,'CDB$ROOT')||chr(34)||','||
#datafile12c:        chr(34)||type||chr(34)||','||
#datafile12c:        chr(34)||tablespace_name||chr(34)||','||
#datafile12c:        chr(34)||file_name||chr(34)||','||
#datafile12c:        chr(34)||size_mb||chr(34)||','||
#datafile12c:        chr(34)||max_size_mb||chr(34)||','||
#datafile12c:        chr(34)||autoextensible||chr(34)||','||
#datafile12c:        chr(34)||status||chr(34)
#datafile12c:from (
#datafile12c:select  con_id,'Datafile' as type,tablespace_name, 
#datafile12c:        file_name, 
#datafile12c:        trunc(bytes/1024/1024) size_mb,
#datafile12c:        trunc(maxbytes/1024/1024) max_size_mb, 
#datafile12c:        autoextensible,status from containers(dba_data_files)
#datafile12c:union all
#datafile12c:select con_id,'Tempfile' as type,tablespace_name, file_name, trunc(bytes/1024/1024) size_mb,
#datafile12c: trunc(maxbytes/1024/1024) max_size_mb, autoextensible,status from containers(dba_temp_files)
#datafile12c:order by 1,2) v ,v$pdbs w
#datafile12c:where v.con_id = w.con_id(+);
#datafile12c:
#datafile12c:
#datafile12c:
#dataguard_stats:set feedback off heading off
#dataguard_stats:set lines 400 pages 0
#dataguard_stats:select chr(34)||name||chr(34)||','||
#dataguard_stats:       chr(34)||value ||chr(34)
#dataguard_stats:from v$dataguard_stats;
#dataguard_stats:
#dataguard_stats:
#dataguard_status:set feedback off heading off
#dataguard_status:set lines 400 pages 0
#dataguard_status:select chr(34)||inst_id    ||chr(34)||','||
#dataguard_status:       chr(34)||to_char(TIMESTAMP,'yyyymmdd hh24:mi:ss') ||chr(34)||','||
#dataguard_status:       chr(34)||dest_id ||chr(34)||','||
#dataguard_status:       chr(34)||ERROR_CODE ||chr(34)||','||
#dataguard_status:       chr(34)||substr(MESSAGE,1,60)||chr(34)  
#dataguard_status:  from gv$dataguard_status
#dataguard_status: where TIMESTAMP > sysdate  - 7
#dataguard_status:   and message not like '%Media Recovery Log%'
#dataguard_status:   and message not like '%(in transit)%'
#dataguard_status:   and message not like '%Assigned to RFS%'
#dataguard_status:   and message not like '%starting Real Time Apply%'
#dataguard_status:order by TIMESTAMP;
#dataguard_status:exit
#dataguard_status:
#db_time_per_second:set lines 200
#db_time_per_second:set pages 3000
#db_time_per_second:set feedback off
#db_time_per_second:set heading off
#db_time_per_second:col dbid new_val dbid noprint
#db_time_per_second:select dbid from v$database;
#db_time_per_second:
#db_time_per_second:col INSTANCE_NUMBER  new_val INSTANCE_NUMBER noprint
#db_time_per_second:select INSTANCE_NUMBER  from v$instance;
#db_time_per_second:
#db_time_per_second:col value_db_block_size new_val value_db_block_size noprint
#db_time_per_second:select value value_db_block_size
#db_time_per_second:          from v$parameter
#db_time_per_second:         where name = 'db_block_size' ;
#db_time_per_second:         
#db_time_per_second:col startup_time  new_val startup_time noprint      
#db_time_per_second:select to_char(startup_time, 'yyyymmddhh24mi') startup_time
#db_time_per_second:  from v$instance ;
#db_time_per_second:
#db_time_per_second:
#db_time_per_second:
#db_time_per_second:select chr(34)||to_char(b.end_interval_time,'yyyymmdd-hh24')||chr(34)||','||
#db_time_per_second:       chr(34)||to_char(round((a.dbtime  - lag(a.dbtime,1,a.dbtime) over (order by a.snap_id)) / 1000000 /60,2))||chr(34)
#db_time_per_second:from
#db_time_per_second:(select a.snap_id,
#db_time_per_second:        a.instance_number,
#db_time_per_second:        a.dbid,
#db_time_per_second:        sum(nvl(a.value,0)) as dbtime
#db_time_per_second:from  dba_hist_sys_time_model a 
#db_time_per_second:where  a.stat_name =  'DB time'
#db_time_per_second:group by a.snap_id,a.instance_number, a.dbid) a, dba_hist_snapshot b
#db_time_per_second:where a.dbtime > 0
#db_time_per_second:  and a.snap_id = b.snap_id
#db_time_per_second: and a.instance_number = b.instance_number 
#db_time_per_second: and a.instance_number = (select instance_number from v$instance)
#db_time_per_second: and a.dbid = b.dbid 
#db_time_per_second: and b.end_interval_time > sysdate - 1 
#db_time_per_second:order by a.snap_id
#db_time_per_second: ;
#db_time_per_second:
#dgapply:set  lines 400
#dgapply:set  pages 1000
#dgapply:set  feedback off
#dgapply:set heading off
#dgapply:SELECT chr(34)||v.thread#||chr(34) ||','||
#dgapply:	     chr(34)||v.name||chr(34)||','|| 
#dgapply:	     chr(34)||v.open_mode||chr(34)||','||
#dgapply:	     chr(34)||v.protection_mode||chr(34) ||','||   
#dgapply:	     chr(34)||v.protection_level||chr(34) ||','||
#dgapply:	     chr(34)||v.database_role||chr(34) ||','||
#dgapply:	     chr(34)||v.switchover_status||chr(34) ||','||
#dgapply:	     chr(34)||v.applog||chr(34) ||','||
#dgapply:	     chr(34)||V.nowlog||chr(34) ||','||
#dgapply:	     chr(34)||case when v.nowlog - v.applog > 3 then 'YES' else 'NO' end ||chr(34)
#dgapply:  FROM (
#dgapply:select a.thread#,c.name,c.open_mode,c.protection_mode,c.protection_level,c.database_role,c.switchover_status,a.applog,b.nowlog from 
#dgapply:(select thread#, max(sequence#) applog from v$archived_log where applied='YES' group by thread#) a,
#dgapply:(select thread#, max(sequence#) nowlog from v$log group by thread#) b,v$database c
#dgapply: where a.thread#=b.thread#) v;
#dgapply:
#dgapply:
#dgapply:
#dlm_traffic:set  lines 400
#dlm_traffic:set  pages 1000
#dlm_traffic:set  feedback off
#dlm_traffic:set heading off 
#dlm_traffic:select  chr(34)||INST_ID    ||chr(34)||','||
#dlm_traffic:        chr(34)||LOCAL_NID 
#dlm_traffic: ||chr(34)||','||
#dlm_traffic:        chr(34)||REMOTE_RID
#dlm_traffic: ||chr(34)||','||
#dlm_traffic:        chr(34)||REMOTE_INC
#dlm_traffic: ||chr(34)||','||
#dlm_traffic:        chr(34)||TCKT_AVAIL
#dlm_traffic: ||chr(34)||','||
#dlm_traffic:        chr(34)||TCKT_LIMIT
#dlm_traffic: ||chr(34)||','||
#dlm_traffic:        chr(34)||TCKT_WAIT  ||chr(34)
#dlm_traffic:from GV$DLM_TRAFFIC_CONTROLLER order by inst_id,local_nid;
#dlm_traffic:
#dstcheck:set lines 400
#dstcheck:set pages 0
#dstcheck:set heading off
#dstcheck:set feedback off
#dstcheck:select chr(34)|| db_version.db_version           ||chr(34) ||','||
#dstcheck:       chr(34)|| dst_version.dst_version         ||chr(34) ||','||
#dstcheck:       chr(34)|| regist_version.regist_version   ||chr(34)
#dstcheck:from
#dstcheck:(select version as db_version from v$instance) db_version,
#dstcheck:(select VERSION as dst_version from v$timezone_file) dst_version,
#dstcheck:(select  TZ_VERSION  as regist_version from registry$database) regist_version;
#efficent:set lines 400
#efficent:set pages 1000
#efficent:set feedback off
#efficent:set serverout on
#efficent:declare
#efficent:vevent varchar2(100);  
#efficent:vtime number;
#efficent:vavgtime number;
#efficent:vpctwt number;
#efficent:vwaits number;
#efficent:vwaitclass varchar2(100);
#efficent:vbid number ;
#efficent:veid number ;
#efficent:vdbid number ;
#efficent:vinid number ;
#efficent:startid number;
#efficent:endid number;
#efficent:vstarttime varchar2(200);
#efficent:vendtime varchar2(200);
#efficent:vdbname varchar2(36);
#efficent:v_inst_startup date;
#efficent:begin 
#efficent:select instance_number,STARTUP_TIME into vinid ,v_inst_startup from v$instance;
#efficent:select dbid into vdbid from v$database;
#efficent:
#efficent:--
#efficent:     begin
#efficent:         select nvl(min(snap_id),-1),nvl(max(snap_id),-1) into vbid,veid
#efficent:         from dba_hist_snapshot
#efficent:         where END_INTERVAL_TIME between  sysdate - 3/24 
#efficent:                                     and  sysdate
#efficent:           and END_INTERVAL_TIME > = v_inst_startup
#efficent:           and instance_number = vinid
#efficent:           and dbid = vdbid;
#efficent:     exception when no_data_found then
#efficent:         select nvl(min(snap_id),-1),nvl(max(snap_id),-1) into vbid,veid
#efficent:         from dba_hist_snapshot
#efficent:         where END_INTERVAL_TIME between  sysdate -1
#efficent:                                     and  sysdate -1 - 3/24
#efficent:           and END_INTERVAL_TIME > = v_inst_startup
#efficent:           and instance_number = vinid
#efficent:           and dbid = vdbid;
#efficent:     end;
#efficent:     
#efficent:     
#efficent:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vstarttime from dba_hist_snapshot a where snap_id=vbid and instance_number=vinid;
#efficent:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vendtime from dba_hist_snapshot a where snap_id=veid and instance_number=vinid;
#efficent:for c1 in (SELECT v.buffnowait ,
#efficent:	     v.redonowait ,
#efficent:	     v.buffhit,
#efficent:	     v.imsort,
#efficent:	     v.libraryhit ,
#efficent:	     v.sortparse ,
#efficent:	     v.exectoparse,
#efficent:	     v.latchhit  ,
#efficent:	     v.cputoparse ,
#efficent:	     v.noparsecpu    
#efficent:  FROM (select 
#efficent:round(100 * (1 - ((SELECT SUM(WAIT_COUNT) FROM DBA_HIST_WAITSTAT WHERE SNAP_ID = veid AND DBID = vdbid AND INSTANCE_NUMBER = vinid) -
#efficent:                  (SELECT SUM(WAIT_COUNT) FROM DBA_HIST_WAITSTAT WHERE SNAP_ID = vbid AND DBID = vdbid AND INSTANCE_NUMBER = vinid)) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('session logical reads'))
#efficent:		        - (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('session logical reads')))), 2) buffnowait,
#efficent:round(100 * (1 - ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('redo log space requests')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('redo log space requests'))) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('redo entries')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('redo entries')))), 2) redonowait,
#efficent:round(100 * (1 - ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('physical reads')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('physical reads')) -
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('physical reads direct')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('physical reads direct'))) -
#efficent:             nvl(((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('physical reads direct (lob)')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('physical reads direct (lob)'))), 0)) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('session logical reads')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('session logical reads')))), 2) buffhit,
#efficent:round(100 *      ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('sorts (memory)')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('sorts (memory)'))) /
#efficent:                (((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('sorts (memory)')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('sorts (memory)'))) +
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME in ('sorts (disk)')) -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME in ('sorts (disk)')))), 2) imsort,
#efficent:(select round(100 * (SUM(e.PINHITS) - sum(b.pinhits)) / (SUM(e.PINS) - sum(b.pins)), 2)
#efficent:                   FROM DBA_HIST_LIBRARYCACHE b, DBA_HIST_LIBRARYCACHE e
#efficent:                   WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid
#efficent:				   AND b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid) libraryhit,
#efficent:round(100 * (1 - ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse count (hard)') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse count (hard)')) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse count (total)') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse count (total)'))), 2) sortparse,
#efficent:round(100 * (1 - ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse count (total)') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse count (total)')) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'execute count') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'execute count'))), 2) exectoparse,
#efficent:(select round(100 * (1 - (SUM(e.MISSES) - sum(b.MISSES)) / (SUM(e.GETS) - sum(b.GETS))), 2)
#efficent:                   FROM DBA_HIST_LATCH b, DBA_HIST_LATCH e 
#efficent:                   WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid 
#efficent:			       AND b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid) latchhit,
#efficent:round(100 *      ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse time cpu') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse time cpu')) /
#efficent:                 ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse time elapsed') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse time elapsed')), 2) cputoparse,
#efficent:round(100 * (1 - ((SELECT sum(value) FROM DBA_HIST_SYSSTAT e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'parse time cpu') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYSSTAT b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'parse time cpu')) /
#efficent:                (((SELECT sum(value) FROM DBA_HIST_SYS_TIME_MODEL e WHERE e.SNAP_ID = veid AND e.DBID = vdbid AND e.INSTANCE_NUMBER = vinid AND e.STAT_NAME = 'DB CPU') -
#efficent:                  (SELECT sum(value) FROM DBA_HIST_SYS_TIME_MODEL b WHERE b.SNAP_ID = vbid AND b.DBID = vdbid AND b.INSTANCE_NUMBER = vinid AND b.STAT_NAME = 'DB CPU')) / 10000)), 2) noparsecpu
#efficent:  from dual) v
#efficent:) loop
#efficent:  dbms_output.put_line(vstarttime||','||vendtime);
#efficent:  dbms_output.put_line(chr(34)||'Buffer Nowait(%)'            ||chr(34)  ||','||chr(34)|| to_char(c1.buffnowait)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Redo Nowait(%)'              ||chr(34)  ||','||chr(34)|| to_char(c1.redonowait)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Buffer Hit(%)'               ||chr(34)  ||','||chr(34)|| to_char(c1.buffhit)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'In-memory Sort(%)'           ||chr(34)  ||','||chr(34)|| to_char(c1.imsort)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Library Hit(%)'              ||chr(34)  ||','||chr(34)|| to_char(c1.libraryhit)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Soft Parse(%)'               ||chr(34)  ||','||chr(34)|| to_char(c1.sortparse)||chr(34)||chr(10));   
#efficent:  dbms_output.put_line(chr(34)||'Execute to Parse(%)'         ||chr(34)  ||','||chr(34)|| to_char(c1.exectoparse)||chr(34)||chr(10));  
#efficent:  dbms_output.put_line(chr(34)||'Latch Hit(%)'                ||chr(34)  ||','||chr(34)|| to_char(c1.latchhit)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Parse CPU to Parse Elapsd(%)'||chr(34)  ||','||chr(34)|| to_char(c1.cputoparse)||chr(34)||chr(10));
#efficent:  dbms_output.put_line(chr(34)||'Non-Parse CPU(%)'            ||chr(34)  ||','||chr(34)|| to_char(c1.noparsecpu)||chr(34)||chr(10)) ;
#efficent:end loop;    
#efficent:     
#efficent:end;
#efficent:/
#efficent:
#efficent:
#efficent:
#flashback:set lines 400
#flashback:set pages 1000
#flashback:set feedback off
#flashback:set heading off
#flashback:select chr(34)||replace(FILE_TYPE,' ','_') ||chr(34)||','||
#flashback:       chr(34)||PERCENT_SPACE_USED ||chr(34)||','|| 
#flashback:       chr(34)||PERCENT_SPACE_RECLAIMABLE||chr(34)||','|| 
#flashback:       chr(34)||NUMBER_OF_FILES||chr(34)
#flashback: from v$flash_recovery_area_usage order by PERCENT_SPACE_USED;
#flashback:
#flashback:
#flashback:
#flashback12c:set lines 400
#flashback12c:set pages 1000
#flashback12c:set feedback off
#flashback12c:set heading off
#flashback12c:select chr(34)||nvl(b.name,'CDB$ROOT')       ||chr(34)||','|| 
#flashback12c:       chr(34)||replace(a.FILE_TYPE,' ','_')   ||chr(34)||','||
#flashback12c:       chr(34)||a.PERCENT_SPACE_USED           ||chr(34)||','|| 
#flashback12c:       chr(34)||a.PERCENT_SPACE_RECLAIMABLE    ||chr(34)||','|| 
#flashback12c:       chr(34)||a.NUMBER_OF_FILES              ||chr(34)
#flashback12c: from v$flash_recovery_area_usage  a,v$pdbs b
#flashback12c: where a.con_id = b.con_id(+)
#flashback12c: order by a.con_id,a.PERCENT_SPACE_USED
#flashback12c: ;
#flashback12c: 
#flashback12c: 
#flashback12c:
#flashback12c:
#flashback12c:
#foreignkey:set lines 400
#foreignkey:set pages 1000
#foreignkey:set feedback off
#foreignkey:set heading off
#foreignkey:
#foreignkey:
#foreignkey:SELECT chr(34)||v.owner ||chr(34)||','||
#foreignkey:	     chr(34)||v.constraint_name ||chr(34)||','||
#foreignkey:	     chr(34)||v.table_name ||chr(34)||','||
#foreignkey:	     chr(34)||v.column_name ||chr(34)||','||
#foreignkey:	     chr(34)||v.status  ||chr(34)
#foreignkey:  FROM (
#foreignkey:SELECT c.owner, c.constraint_name, c.table_name, cc.column_name, c.status
#foreignkey:  FROM dba_constraints c, dba_cons_columns cc
#foreignkey: WHERE c.constraint_type = 'R'
#foreignkey:   AND c.owner NOT IN
#foreignkey:       ('ADM_PARALLEL_EXECUTE_TASK','ANONYMOUS','APEX_030200','APEX_ADMINISTRATOR_ROLE','APEX_PUBLIC_USER',
#foreignkey:        'APPQOSSYS','AQ_ADMINISTRATOR_ROLE','AQ_USER_ROLE','CONNECT','CSW_USR_ROLE','CTXAPP','CTXSYS',
#foreignkey:        'CWM_USER','DATAPUMP_EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE','DBA','DBFS_ROLE','DBSNMP',
#foreignkey:        'DELETE_CATALOG_ROLE','DIP','EXECUTE_CATALOG_ROLE','EXFSYS','EXP_FULL_DATABASE','FLOWS_FILES',
#foreignkey:        'GATHER_SYSTEM_STATISTICS','HS_ADMIN_EXECUTE_ROLE','HS_ADMIN_ROLE','HS_ADMIN_SELECT_ROLE',
#foreignkey:        'IMP_FULL_DATABASE','JAVADEBUGPRIV','JAVASYSPRIV','LOGSTDBY_ADMINISTRATOR','MDDATA','MDSYS',
#foreignkey:        'MGMT_USER','MGMT_VIEW','OEM_ADVISOR','OEM_MONITOR','OLAPSYS','OLAP_DBA','OLAP_USER','OLAP_XS_ADMIN',
#foreignkey:        'ORACLE_OCM','ORDADMIN','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWB$CLIENT','OWBSYS','OWBSYS_AUDIT',
#foreignkey:        'PUBLIC','RECOVERY_CATALOG_OWNER','RESOURCE','SCHEDULER_ADMIN','SCOTT','SELECT_CATALOG_ROLE',
#foreignkey:        'SI_INFORMTN_SCHEMA','SPATIAL_CSW_ADMIN','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN',
#foreignkey:        'SPATIAL_WFS_ADMIN_USR','SQLTXADMIN','SQLTXPLAIN','SQLT_USER_ROLE','SYS','SYSMAN','SYSTEM',
#foreignkey:        'WFS_USR_ROLE','WMSYS','WM_ADMIN_ROLE','XDB','XDBADMIN','PERFSTAT','GSMADMIN_INTERNAL')
#foreignkey:   AND c.owner = cc.owner
#foreignkey:   AND c.constraint_name = cc.constraint_name
#foreignkey:   AND NOT EXISTS
#foreignkey: (SELECT 'x'
#foreignkey:          FROM dba_ind_columns ic
#foreignkey:         WHERE cc.owner = ic.table_owner
#foreignkey:           AND cc.table_name = ic.table_name
#foreignkey:           AND cc.column_name = ic.column_name
#foreignkey:           AND cc.position = ic.column_position
#foreignkey:           AND NOT EXISTS
#foreignkey:         (SELECT owner, index_name
#foreignkey:                  FROM dba_indexes i
#foreignkey:                 WHERE i.table_owner = c.owner
#foreignkey:                   AND i.index_Name = ic.index_name
#foreignkey:                   AND i.owner = ic.index_owner
#foreignkey:                   AND (i.status = 'UNUSABLE' OR
#foreignkey:                       i.partitioned = 'YES' AND EXISTS
#foreignkey:                        (SELECT 'x'
#foreignkey:                           FROM dba_ind_partitions ip
#foreignkey:                          WHERE status = 'UNUSABLE'
#foreignkey:                            AND ip.index_owner = i.owner
#foreignkey:                            AND ip.index_Name = i.index_name
#foreignkey:                         UNION ALL
#foreignkey:                         SELECT 'x'
#foreignkey:                           FROM dba_ind_subpartitions isp
#foreignkey:                          WHERE status = 'UNUSABLE'
#foreignkey:                            AND isp.index_owner = i.owner
#foreignkey:                            AND isp.index_Name = i.index_name))))
#foreignkey: ORDER BY 1, 2) v order by OWNER,TABLE_NAME,COLUMN_NAME;
#foreignkey:
#foreignkey:
#foreignkey:
#foreignkey12c:set lines 400
#foreignkey12c:set pages 1000
#foreignkey12c:set feedback off
#foreignkey12c:set heading off
#foreignkey12c:
#foreignkey12c:
#foreignkey12c:SELECT chr(34)||nvl(b.name,'CDB$ROOT') ||chr(34)||','||
#foreignkey12c:       chr(34)||v.owner                ||chr(34)||','||
#foreignkey12c:	     chr(34)||v.constraint_name      ||chr(34)||','||
#foreignkey12c:	     chr(34)||v.table_name           ||chr(34)||','||
#foreignkey12c:	     chr(34)||v.column_name          ||chr(34)||','||
#foreignkey12c:	     chr(34)||v.status               ||chr(34)
#foreignkey12c:  FROM (
#foreignkey12c:SELECT C.CON_ID,
#foreignkey12c:       c.owner, 
#foreignkey12c:       c.constraint_name, 
#foreignkey12c:       c.table_name, 
#foreignkey12c:       cc.column_name, 
#foreignkey12c:       c.status
#foreignkey12c:  FROM containers(dba_constraints) c, 
#foreignkey12c:       containers(dba_cons_columns) cc
#foreignkey12c: WHERE c.constraint_type = 'R'
#foreignkey12c:   AND c.owner NOT IN
#foreignkey12c:       ('ADM_PARALLEL_EXECUTE_TASK','ANONYMOUS','APEX_030200','APEX_ADMINISTRATOR_ROLE','APEX_PUBLIC_USER',
#foreignkey12c:        'APPQOSSYS','AQ_ADMINISTRATOR_ROLE','AQ_USER_ROLE','CONNECT','CSW_USR_ROLE','CTXAPP','CTXSYS',
#foreignkey12c:        'CWM_USER','DATAPUMP_EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE','DBA','DBFS_ROLE','DBSNMP',
#foreignkey12c:        'DELETE_CATALOG_ROLE','DIP','EXECUTE_CATALOG_ROLE','EXFSYS','EXP_FULL_DATABASE','FLOWS_FILES',
#foreignkey12c:        'GATHER_SYSTEM_STATISTICS','HS_ADMIN_EXECUTE_ROLE','HS_ADMIN_ROLE','HS_ADMIN_SELECT_ROLE',
#foreignkey12c:        'IMP_FULL_DATABASE','JAVADEBUGPRIV','JAVASYSPRIV','LOGSTDBY_ADMINISTRATOR','MDDATA','MDSYS',
#foreignkey12c:        'MGMT_USER','MGMT_VIEW','OEM_ADVISOR','OEM_MONITOR','OLAPSYS','OLAP_DBA','OLAP_USER','OLAP_XS_ADMIN',
#foreignkey12c:        'ORACLE_OCM','ORDADMIN','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWB$CLIENT','OWBSYS','OWBSYS_AUDIT',
#foreignkey12c:        'PUBLIC','RECOVERY_CATALOG_OWNER','RESOURCE','SCHEDULER_ADMIN','SCOTT','SELECT_CATALOG_ROLE',
#foreignkey12c:        'SI_INFORMTN_SCHEMA','SPATIAL_CSW_ADMIN','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN',
#foreignkey12c:        'SPATIAL_WFS_ADMIN_USR','SQLTXADMIN','SQLTXPLAIN','SQLT_USER_ROLE','SYS','SYSMAN','SYSTEM',
#foreignkey12c:        'WFS_USR_ROLE','WMSYS','WM_ADMIN_ROLE','XDB','XDBADMIN','PERFSTAT','GSMADMIN_INTERNAL')
#foreignkey12c:   AND c.owner = cc.owner
#foreignkey12c:   AND c.constraint_name = cc.constraint_name
#foreignkey12c:   and c.con_id = cc.con_id
#foreignkey12c:   AND NOT EXISTS
#foreignkey12c: (SELECT 'x'
#foreignkey12c:          FROM containers(dba_ind_columns) ic
#foreignkey12c:         WHERE cc.owner = ic.table_owner
#foreignkey12c:           AND cc.table_name = ic.table_name
#foreignkey12c:           AND cc.column_name = ic.column_name
#foreignkey12c:           AND cc.position = ic.column_position
#foreignkey12c:           AND ic.con_id = c.con_id
#foreignkey12c:           AND NOT EXISTS
#foreignkey12c:         (SELECT owner, index_name
#foreignkey12c:                  FROM containers(dba_indexes) i
#foreignkey12c:                 WHERE i.table_owner = c.owner
#foreignkey12c:                   AND i.index_Name = ic.index_name
#foreignkey12c:                   and i.con_id = c.con_id
#foreignkey12c:                   AND i.owner = ic.index_owner
#foreignkey12c:                   AND (i.status = 'UNUSABLE' OR
#foreignkey12c:                       i.partitioned = 'YES' AND EXISTS
#foreignkey12c:                        (SELECT 'x'
#foreignkey12c:                           FROM containers(dba_ind_partitions) ip
#foreignkey12c:                          WHERE status = 'UNUSABLE'
#foreignkey12c:                            AND ip.index_owner = i.owner
#foreignkey12c:                            AND ip.index_Name = i.index_name
#foreignkey12c:                            and ip.con_id = i.con_id
#foreignkey12c:                         UNION ALL
#foreignkey12c:                         SELECT 'x'
#foreignkey12c:                           FROM containers(dba_ind_subpartitions) isp
#foreignkey12c:                          WHERE status = 'UNUSABLE'
#foreignkey12c:                            AND isp.index_owner = i.owner
#foreignkey12c:                            and isp.con_id = i.con_id
#foreignkey12c:                            AND isp.index_Name = i.index_name))))
#foreignkey12c: ORDER BY 1, 2) v,v$pdbs b
#foreignkey12c:where v.con_id = b.con_id(+)
#foreignkey12c: order by B.CON_ID,V.OWNER,V.TABLE_NAME,V.COLUMN_NAME;
#foreignkey12c:
#foreignkey12c:
#foreignkey12c:
#fullscan:set lines 400
#fullscan:set pages 1000
#fullscan:set heading off
#fullscan:set feedback off
#fullscan:
#fullscan:
#fullscan:
#fullscan:with temp_sqlinfo as 
#fullscan:(select sql_id, 
#fullscan:        plan_hash_value, 
#fullscan:        sum(buffer_gets_delta) total_buffer_gets, 
#fullscan:        sum(executions_delta) TOTAL_executions, 
#fullscan:        decode(sum(executions_delta),
#fullscan:               0, 
#fullscan:               sum(buffer_gets_delta), 
#fullscan:               round(sum(buffer_gets_delta) / sum(executions_delta), 0)) buffer_get_onetime 
#fullscan:from dba_hist_sqlstat 
#fullscan:where dbid = (select dbid from v$database) 
#fullscan:      and snap_id > (select min(snap_id) from dba_hist_snapshot where BEGIN_INTERVAL_TIME > sysdate - 7) 
#fullscan:      and plan_hash_value != 0 
#fullscan:      and PARSING_SCHEMA_NAME not in (SELECT USERNAME FROM DBA_USERS WHERE DEFAULT_TABLESPACE IN ('SYSTEM','SYSAUX'))
#fullscan:group by sql_id, plan_hash_value 
#fullscan:having decode(sum(executions_delta), 0, sum(buffer_gets_delta), round(sum(buffer_gets_delta) / sum(executions_delta), 0)) > 1000)
#fullscan:SELECT chr(34)||sql_id              ||chr(34)||','||
#fullscan:       chr(34)||plan_hash_value     ||chr(34)||','||
#fullscan:       chr(34)||total_buffer_gets   ||chr(34)||','||
#fullscan:       chr(34)||total_executions    ||chr(34)||','||
#fullscan:       chr(34)||buffer_get_onetime  ||chr(34)
#fullscan:FROM (
#fullscan:select b.sql_id, 
#fullscan:       c.plan_hash_value,
#fullscan:       c.total_buffer_gets,
#fullscan:       c.total_executions,
#fullscan:       c.buffer_get_onetime
#fullscan:from dba_hist_sqltext b,temp_sqlinfo c
#fullscan:  WHERE exists (select '1' from dba_hist_sql_plan a
#fullscan:                where a.sql_id = b.sql_id and a.dbid = b.dbid
#fullscan:                  and a.options = 'FULL'
#fullscan:                  and a.operation = 'TABLE ACCESS'
#fullscan:                  and a.object_owner NOT in (SELECT USERNAME FROM DBA_USERS WHERE DEFAULT_TABLESPACE IN ('SYSTEM','SYSAUX'))  
#fullscan:               )
#fullscan:     and b.sql_id = c.sql_id
#fullscan:  ORDER BY C.total_buffer_gets DESC) V
#fullscan:WHERE rownum < 16 
#fullscan: ;
#fullscan:
#fullscan:
#fullscan:
#fullscan12c:set lines 400
#fullscan12c:set pages 1000
#fullscan12c:set heading off
#fullscan12c:set feedback off
#fullscan12c:
#fullscan12c:
#fullscan12c:
#fullscan12c:with temp_sqlinfo as 
#fullscan12c:(select sql_id, 
#fullscan12c:        plan_hash_value, 
#fullscan12c:        sum(buffer_gets_delta) total_buffer_gets, 
#fullscan12c:        sum(executions_delta) TOTAL_executions, 
#fullscan12c:        decode(sum(executions_delta),
#fullscan12c:               0, 
#fullscan12c:               sum(buffer_gets_delta), 
#fullscan12c:               round(sum(buffer_gets_delta) / sum(executions_delta), 0)) buffer_get_onetime 
#fullscan12c:from dba_hist_sqlstat 
#fullscan12c:where dbid = (select dbid from v$database) 
#fullscan12c:      and snap_id > (select min(snap_id) from dba_hist_snapshot where BEGIN_INTERVAL_TIME > sysdate - 7) 
#fullscan12c:      and plan_hash_value != 0 
#fullscan12c:      and PARSING_SCHEMA_NAME not in (SELECT USERNAME FROM DBA_USERS WHERE DEFAULT_TABLESPACE IN ('SYSTEM','SYSAUX'))
#fullscan12c:group by sql_id, plan_hash_value 
#fullscan12c:having decode(sum(executions_delta), 0, sum(buffer_gets_delta), round(sum(buffer_gets_delta) / sum(executions_delta), 0)) > 1000)
#fullscan12c:SELECT chr(34)||sql_id              ||chr(34)||','||
#fullscan12c:       chr(34)||plan_hash_value     ||chr(34)||','||
#fullscan12c:       chr(34)||total_buffer_gets   ||chr(34)||','||
#fullscan12c:       chr(34)||total_executions    ||chr(34)||','||
#fullscan12c:       chr(34)||buffer_get_onetime  ||chr(34)
#fullscan12c:FROM (
#fullscan12c:select b.sql_id, 
#fullscan12c:       c.plan_hash_value,
#fullscan12c:       c.total_buffer_gets,
#fullscan12c:       c.total_executions,
#fullscan12c:       c.buffer_get_onetime
#fullscan12c:from dba_hist_sqltext b,temp_sqlinfo c
#fullscan12c:  WHERE exists (select '1' from dba_hist_sql_plan a
#fullscan12c:                where a.sql_id = b.sql_id and a.dbid = b.dbid
#fullscan12c:                  and a.options = 'FULL'
#fullscan12c:                  and a.operation = 'TABLE ACCESS'
#fullscan12c:                  and a.object_owner NOT in (SELECT USERNAME FROM DBA_USERS WHERE DEFAULT_TABLESPACE IN ('SYSTEM','SYSAUX'))  
#fullscan12c:               )
#fullscan12c:     and b.sql_id = c.sql_id
#fullscan12c:  ORDER BY C.total_buffer_gets DESC) V
#fullscan12c:WHERE rownum < 16 
#fullscan12c: ;
#fullscan12c:
#fullscan12c:
#fullscan12c:
#ges_traffic:set  lines 400
#ges_traffic:set  pages 1000
#ges_traffic:set  feedback off
#ges_traffic:set heading off 
#ges_traffic:select  chr(34)||INST_ID    ||chr(34)||','||
#ges_traffic:        chr(34)||LOCAL_NID 
#ges_traffic: ||chr(34)||','||
#ges_traffic:        chr(34)||REMOTE_RID
#ges_traffic: ||chr(34)||','||
#ges_traffic:        chr(34)||REMOTE_INC
#ges_traffic: ||chr(34)||','||
#ges_traffic:        chr(34)||TCKT_AVAIL
#ges_traffic: ||chr(34)||','||
#ges_traffic:        chr(34)||TCKT_LIMIT
#ges_traffic: ||chr(34)||','||
#ges_traffic:        chr(34)||TCKT_WAIT  ||chr(34)
#ges_traffic:from GV$GES_TRAFFIC_CONTROLLER order by inst_id,local_nid;
#hiddenparms:set lines 400
#hiddenparms:set pages 1000
#hiddenparms:set feedback off
#hiddenparms:set heading off
#hiddenparms:SELECT chr(34)||x.ksppinm ||chr(34)||','||
#hiddenparms:       chr(34)||upper(y.ksppstvl) ||chr(34)
#hiddenparms:  FROM SYS.x$ksppi x, 
#hiddenparms:       SYS.x$ksppcv y
#hiddenparms:WHERE x.inst_id = USERENV ('Instance')
#hiddenparms:  AND y.inst_id = USERENV ('Instance')
#hiddenparms:  AND x.indx = y.indx
#hiddenparms:  AND ( x.ksppinm LIKE '%optimizer_use_feedback' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_adaptive_cursor_sharing' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_extended_cursor_sharing' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_extended_cursor_sharing_rel' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_partial_join_eval' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_aggr_groupby_elim' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_reduce_groupby_key' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_cost_based_transformation' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_squ_bottomup' or
#hiddenparms:        x.ksppinm LIKE '%optim_peek_user_binds' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_mjc_enabled' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_ads_use_result_cache' or
#hiddenparms:        x.ksppinm LIKE '%optimizer_gather_stats_on_conventional_dml' or
#hiddenparms:        x.ksppinm LIKE '%gc_policy_time' or
#hiddenparms:        x.ksppinm LIKE '%gc_undo_affinity' or
#hiddenparms:        x.ksppinm LIKE '%gc_defer_time' or
#hiddenparms:        x.ksppinm LIKE '%gc_bypass_readers' or
#hiddenparms:        x.ksppinm LIKE '%gc_override_force_cr' or
#hiddenparms:        x.ksppinm LIKE '%gc_read_mostly_locking' or
#hiddenparms:        x.ksppinm LIKE '%cursor_obsolete_threshold' or
#hiddenparms:        x.ksppinm LIKE '%cleanup_rollback_entries' or
#hiddenparms:        x.ksppinm LIKE '%clusterwide_global_transactions' or 
#hiddenparms:        x.ksppinm LIKE '%cr_max_rollback' or
#hiddenparms:        x.ksppinm LIKE '%use_single_log_writer' or
#hiddenparms:        x.ksppinm LIKE '%use_adaptive_log_file_sync' or
#hiddenparms:        x.ksppinm LIKE '%undo_autotune' or
#hiddenparms:        x.ksppinm LIKE '%serial_direct_read' or
#hiddenparms:        x.ksppinm LIKE '%sql_plan_directive_mgmt_control' or
#hiddenparms:        x.ksppinm LIKE '%smu_debug_mode' or
#hiddenparms:        x.ksppinm LIKE '%trace_files_public%' or
#hiddenparms:        x.ksppinm LIKE '%rollback_segment_count' or
#hiddenparms:        x.ksppinm LIKE '%report_capture_cycle_time' or
#hiddenparms:        x.ksppinm LIKE '%rowsets_enabled' or
#hiddenparms:        x.ksppinm LIKE '%ktb_debug_flags' or
#hiddenparms:        x.ksppinm LIKE '%ksmg_granule_size' or
#hiddenparms:        x.ksppinm LIKE '%partition_large_extents' or
#hiddenparms:        x.ksppinm LIKE '%px_use_large_pool' or
#hiddenparms:        x.ksppinm LIKE '%lm_tickets%' or 
#hiddenparms:        x.ksppinm LIKE '%lm_sync_timeout' or 
#hiddenparms:        x.ksppinm LIKE '%high_priority_processes' or
#hiddenparms:        x.ksppinm LIKE '%fast_index_maintenance' or
#hiddenparms:        x.ksppinm LIKE '%enable_automatic_sqltune' or
#hiddenparms:        x.ksppinm LIKE '%enable_shared_pool_durations' or
#hiddenparms:        x.ksppinm LIKE '%enable_NUMA_support' or
#hiddenparms:        x.ksppinm LIKE '%resource_manager_always_off' or
#hiddenparms:        x.ksppinm LIKE '%memory_imm_mode_without_autosga' or
#hiddenparms:        x.ksppinm LIKE '%max_outstanding_log_writes' or
#hiddenparms:        x.ksppinm LIKE '%abort_on_mrp_crash%' or
#hiddenparms:        x.ksppinm LIKE '%adg_parselock_timeout' or
#hiddenparms:        x.ksppinm LIKE '%ash_size%' or
#hiddenparms:        x.ksppinm LIKE '%ash_enable' or
#hiddenparms:        x.ksppinm LIKE '%use_single_log_writer' or
#hiddenparms:        x.ksppinm LIKE '%dlm_stats_collect' or
#hiddenparms:        x.ksppinm LIKE '%max_outstanding_log_writes' or
#hiddenparms:        x.ksppinm LIKE '%PX_use_large_pool' or
#hiddenparms:        x.ksppinm LIKE '%sys_logon_delay' or
#hiddenparms:        x.ksppinm LIKE '%use_single_log_writer' or
#hiddenparms:        x.ksppinm LIKE 'cluster_database' or
#hiddenparms:        x.ksppinm LIKE '%datafile_write_errors_crash_instance' ) and 
#hiddenparms:         x.ksppinm not like '%kffmap%' and
#hiddenparms:         x.ksppinm not like '%kffmlk%' and
#hiddenparms:         x.ksppinm not like '%kffmop%' and  
#hiddenparms:         x.ksppinm not like '%kffmspw%' and
#hiddenparms:         x.ksppinm <> '_optimizer_ads_use_result_cache' and 
#hiddenparms:         x.ksppinm <> '_optimizer_aggr_groupby_elim' and 
#hiddenparms:         x.ksppinm <> '_optimizer_cost_based_transformation' and
#hiddenparms:         x.ksppinm <> '_optimizer_gather_stats_on_conventional_dml' and
#hiddenparms:         x.ksppinm <> '_optimizer_mjc_enabled' and
#hiddenparms:         x.ksppinm <> '_optimizer_partial_join_eval' and
#hiddenparms:         x.ksppinm <> '_optimizer_reduce_groupby_key' and
#hiddenparms:         x.ksppinm <> '_optimizer_squ_bottomup' and
#hiddenparms:         x.ksppinm <> '_sql_plan_directive_mgmt_control' 
#hiddenparms:order by 1;
#hiddenparms:
#hist_undo_stat:set lines 200
#hist_undo_stat:set pages 3000
#hist_undo_stat:set feedback off
#hist_undo_stat:set heading off
#hist_undo_stat:col dbid new_val dbid noprint
#hist_undo_stat:select dbid from v$database;
#hist_undo_stat:
#hist_undo_stat:col INSTANCE_NUMBER  new_val INSTANCE_NUMBER noprint
#hist_undo_stat:select INSTANCE_NUMBER  from v$instance;
#hist_undo_stat:
#hist_undo_stat:
#hist_undo_stat:col value_db_block_size new_val value_db_block_size noprint
#hist_undo_stat:select value value_db_block_size
#hist_undo_stat:          from v$parameter
#hist_undo_stat:         where name = 'db_block_size' ;
#hist_undo_stat:         
#hist_undo_stat:col startup_time  new_val startup_time noprint      
#hist_undo_stat:select to_char(startup_time, 'yyyymmddhh24mi') startup_time
#hist_undo_stat:  from v$instance ;
#hist_undo_stat:
#hist_undo_stat:select chr(34)||end_time          ||chr(34)||','||
#hist_undo_stat:       chr(34)||active_size_mb    ||chr(34)||','||
#hist_undo_stat:       chr(34)||unexpired_size_mb ||chr(34)||','||
#hist_undo_stat:       chr(34)||total_size_mb     ||chr(34)
#hist_undo_stat:from
#hist_undo_stat:(select to_char(end_time,'yyyymmdd-hh24') as end_time,
#hist_undo_stat:       round(sum(ACTIVEBLKS * &value_db_block_size / 8192 / 1024),0) as active_size_mb, 
#hist_undo_stat:       round(sum(UNEXPIREDBLKS * &value_db_block_size / 8192 / 1024),0) as unexpired_size_mb,
#hist_undo_stat:       round(sum((ACTIVEBLKS + UNEXPIREDBLKS) * &value_db_block_size / 8192 / 1024),0) as total_size_mb
#hist_undo_stat:from dba_hist_undostat a
#hist_undo_stat:where a.instance_number = &INSTANCE_NUMBER
#hist_undo_stat:  and  a.end_time  > sysdate  -7 
#hist_undo_stat:group by to_char(end_time,'yyyymmdd-hh24')
#hist_undo_stat:order by end_time) v;
#hist_undo_stat:
#hist_undo_stat:
#hist_undo_stat:
#indicator:set  lines 400
#indicator:set  pages 1000
#indicator:set  feedback off
#indicator:set heading off
#indicator:SELECT chr(34)||v.current_scn ||chr(34)||','||
#indicator:	     chr(34)||v.indicator ||chr(34)
#indicator:  FROM (select date_time,current_scn,indicator
#indicator:  from (select to_char(SYSDATE,'YYYY/MM/DD HH24:MI:SS') DATE_TIME, current_scn,
#indicator:   trunc((((((to_number(to_char(sysdate,'YYYY'))-1988)*12*31*24*60*60) +
#indicator:            ((to_number(to_char(sysdate,'MM'))-1)*31*24*60*60) +
#indicator:           (((to_number(to_char(sysdate,'DD'))-1))*24*60*60) +
#indicator:             (to_number(to_char(sysdate,'HH24'))*60*60) +
#indicator:             (to_number(to_char(sysdate,'MI'))*60) +
#indicator:             (to_number(to_char(sysdate,'SS'))) ) * (16*1024)) - 
#indicator:			 current_scn ) / (16*1024*60*60*24)) indicator from v$database)) v;
#indicator:			 
#indicator:
#invalidcons:set lines 400
#invalidcons:set pages 1000
#invalidcons:set feedback off
#invalidcons:set heading off
#invalidcons:
#invalidcons:select chr(34)||owner ||chr(34)||','||
#invalidcons:       chr(34)||constraint_name ||chr(34)||','||
#invalidcons:       chr(34)||constraint_type ||chr(34)||','||
#invalidcons:       chr(34)||table_name ||chr(34)
#invalidcons:from dba_constraints 
#invalidcons:where status='DISABLED' and owner not in('SYS','SYSTEM')
#invalidcons:order by owner,table_name;
#invalidcons:
#invalidcons:
#invalidcons:
#invalidcons12c:set lines 400
#invalidcons12c:set pages 1000
#invalidcons12c:set feedback off
#invalidcons12c:set heading off
#invalidcons12c:
#invalidcons12c:select chr(34)||nvl(b.name,'CDB$ROOT')   ||chr(34)||','||
#invalidcons12c:       chr(34)||A.owner                  ||chr(34)||','||
#invalidcons12c:       chr(34)||A.constraint_name        ||chr(34)||','||
#invalidcons12c:       chr(34)||A.constraint_type        ||chr(34)||','||
#invalidcons12c:       chr(34)||A.table_name             ||chr(34)
#invalidcons12c:from containers(dba_constraints ) a,v$pdbs b
#invalidcons12c:where a.status='DISABLED' and a.owner not in('SYS','SYSTEM')
#invalidcons12c:  and a.con_id = b.con_id(+)
#invalidcons12c:order by a.con_id,
#invalidcons12c:         a.owner,
#invalidcons12c:         a.table_name;
#invalidcons12c:
#invalidcons12c:
#invalidcons12c:
#invalididx:
#invalididx:set lines 400
#invalididx:set pages 1000
#invalididx:set feedback off
#invalididx:set heading off
#invalididx:
#invalididx:select chr(34)||owner                 ||chr(34)||',' ||
#invalididx:       chr(34)||index_name            ||chr(34)||',' ||
#invalididx:       chr(34)||index_type            ||chr(34)||',' ||
#invalididx:       chr(34)||'N/A'                 ||chr(34)||',' ||
#invalididx:       chr(34)||status                ||chr(34)||',' || 
#invalididx:       chr(34)||table_name            ||chr(34)||',' ||
#invalididx:       chr(34)||tablespace_name ||chr(34)
#invalididx:  from dba_indexes
#invalididx: where status = 'UNUSABLE'
#invalididx:union all
#invalididx:select chr(34)||a.index_owner     ||chr(34)||','||
#invalididx:       chr(34)||a.index_name      ||chr(34)||','||
#invalididx:       chr(34)||b.index_type      ||chr(34)||','||
#invalididx:       chr(34)||a.partition_name  ||chr(34)||','||
#invalididx:       chr(34)||a.status          ||chr(34)||','||
#invalididx:       chr(34)||b.table_name      ||chr(34)||','||
#invalididx:       chr(34)||a.tablespace_name ||chr(34)
#invalididx:  from dba_ind_partitions a, dba_indexes b
#invalididx: where a.index_name = b.index_name
#invalididx:   and a.index_owner = b.owner
#invalididx:   and a.status = 'UNUSABLE'
#invalididx:union all
#invalididx:select chr(34)||a.index_owner       ||chr(34)||',' ||
#invalididx:       chr(34)||a.index_name        ||chr(34)||',' ||
#invalididx:       chr(34)||b.index_type        ||chr(34)||',' ||
#invalididx:       chr(34)||a.partition_name    ||chr(34)||',' ||
#invalididx:       chr(34)||a.status            ||chr(34)||',' ||
#invalididx:       chr(34)||b.table_name        ||chr(34)||',' ||
#invalididx:       chr(34)||a.tablespace_name   ||chr(34)
#invalididx:  from dba_ind_subpartitions a, dba_indexes b
#invalididx: where a.index_name = b.index_name
#invalididx:   and a.index_owner = b.owner
#invalididx:   and a.status = 'UNUSABLE'
#invalididx:;
#invalididx:
#invalididx:
#invalididx:
#invalididx12c:
#invalididx12c:set lines 400
#invalididx12c:set pages 1000
#invalididx12c:set feedback off
#invalididx12c:set heading off
#invalididx12c:
#invalididx12c:select chr(34)||nvl(b.name,'CDB$ROOT')  ||chr(34)||',' ||
#invalididx12c:       chr(34)||A.owner                 ||chr(34)||',' ||
#invalididx12c:       chr(34)||A.index_name            ||chr(34)||',' ||
#invalididx12c:       chr(34)||A.index_type            ||chr(34)||',' ||
#invalididx12c:       chr(34)||'N/A'                   ||chr(34)||',' ||
#invalididx12c:       chr(34)||A.status                ||chr(34)||',' || 
#invalididx12c:       chr(34)||A.table_name            ||chr(34)||',' ||
#invalididx12c:       chr(34)||A.tablespace_name ||chr(34)
#invalididx12c:  from containers(dba_indexes) a,v$pdbs b
#invalididx12c: where a.status = 'UNUSABLE' and a.con_id =b.con_id(+)
#invalididx12c:union all
#invalididx12c:select chr(34)||nvl(c.name,'CDB$ROOT')  ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.index_owner           ||chr(34)||','||
#invalididx12c:       chr(34)||a.index_name            ||chr(34)||','||
#invalididx12c:       chr(34)||b.index_type            ||chr(34)||','||
#invalididx12c:       chr(34)||a.partition_name        ||chr(34)||','||
#invalididx12c:       chr(34)||a.status                ||chr(34)||','||
#invalididx12c:       chr(34)||b.table_name            ||chr(34)||','||
#invalididx12c:       chr(34)||a.tablespace_name       ||chr(34)
#invalididx12c:  from containers(dba_ind_partitions) a, containers(dba_indexes) b,V$PDBS c
#invalididx12c: where a.index_name = b.index_name and a.con_id = b.con_id and b.con_id = c.con_id(+)
#invalididx12c:   and a.index_owner = b.owner
#invalididx12c:   and a.status = 'UNUSABLE'
#invalididx12c:union all
#invalididx12c:select chr(34)||nvl(c.name,'CDB$ROOT')  ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.index_owner           ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.index_name            ||chr(34)||',' ||
#invalididx12c:       chr(34)||b.index_type            ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.partition_name        ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.status                ||chr(34)||',' ||
#invalididx12c:       chr(34)||b.table_name            ||chr(34)||',' ||
#invalididx12c:       chr(34)||a.tablespace_name       ||chr(34)
#invalididx12c:  from containers(dba_ind_subpartitions) a, containers(dba_indexes) b,v$pdbs c
#invalididx12c: where a.index_name = b.index_name and a.con_id = b.con_id and b.con_id = c.con_id(+)
#invalididx12c:   and a.index_owner = b.owner
#invalididx12c:   and a.status = 'UNUSABLE'
#invalididx12c:;
#invalididx12c:
#invalididx12c:
#invalididx12c:
#invalidobj:
#invalidobj:set lines 400
#invalidobj:set pages 1000
#invalidobj:set feedback off
#invalidobj:set heading off
#invalidobj:
#invalidobj:
#invalidobj:select chr(34)||owner ||chr(34)||','||
#invalidobj:       chr(34)||object_name ||chr(34)||','||
#invalidobj:       chr(34)||replace( object_type,' ','-') ||chr(34)
#invalidobj:from (	   
#invalidobj:select owner,object_name,object_type
#invalidobj:  from dba_objects where status = 'INVALID'
#invalidobj:     and owner not in ('ADM_PARALLEL_EXECUTE_TASK','ANONYMOUS','APEX_030200','APEX_ADMINISTRATOR_ROLE','APEX_PUBLIC_USER',
#invalidobj:                       'APPQOSSYS','AQ_ADMINISTRATOR_ROLE','AQ_USER_ROLE','CONNECT','CSW_USR_ROLE','CTXAPP','CTXSYS',
#invalidobj:                       'CWM_USER','DATAPUMP_EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE','DBA','DBFS_ROLE','DBSNMP',
#invalidobj:                       'DELETE_CATALOG_ROLE','DIP','EXECUTE_CATALOG_ROLE','EXFSYS','EXP_FULL_DATABASE','FLOWS_FILES',
#invalidobj:                       'GATHER_SYSTEM_STATISTICS','HS_ADMIN_EXECUTE_ROLE','HS_ADMIN_ROLE','HS_ADMIN_SELECT_ROLE',
#invalidobj:                       'IMP_FULL_DATABASE','JAVADEBUGPRIV','JAVASYSPRIV','LOGSTDBY_ADMINISTRATOR','MDDATA','MDSYS',
#invalidobj:                       'MGMT_USER','MGMT_VIEW','OEM_ADVISOR','OEM_MONITOR','OLAPSYS','OLAP_DBA','OLAP_USER','OLAP_XS_ADMIN',
#invalidobj:                       'ORACLE_OCM','ORDADMIN','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWB$CLIENT','OWBSYS','OWBSYS_AUDIT',
#invalidobj:                       'PUBLIC','RECOVERY_CATALOG_OWNER','RESOURCE','SCHEDULER_ADMIN','SCOTT','SELECT_CATALOG_ROLE',
#invalidobj:                       'SI_INFORMTN_SCHEMA','SPATIAL_CSW_ADMIN','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN',
#invalidobj:                       'SPATIAL_WFS_ADMIN_USR','SQLTXADMIN','SQLTXPLAIN','SQLT_USER_ROLE','SYS','SYSMAN','SYSTEM',
#invalidobj:                       'WFS_USR_ROLE','WMSYS','WM_ADMIN_ROLE','XDB','XDBADMIN','AUDSYS','OJVMSYS','GSMADMIN_INTERNAL','PERFSTAT')
#invalidobj:	) v 
#invalidobj:where rownum < 31;
#invalidobj:
#invalidobj:
#invalidobj:
#invalidobj12c:
#invalidobj12c:set lines 400
#invalidobj12c:set pages 1000
#invalidobj12c:set feedback off
#invalidobj12c:set heading off
#invalidobj12c:
#invalidobj12c:
#invalidobj12c:select chr(34)||nvl(b.name,'CDB$ROOT')||chr(34)||','||
#invalidobj12c:       chr(34)||owner                 ||chr(34)||','||
#invalidobj12c:       chr(34)||object_name ||chr(34) ||','||
#invalidobj12c:       chr(34)||replace( object_type,' ','-') ||chr(34)
#invalidobj12c:from (	   
#invalidobj12c:select con_id,owner,object_name,object_type
#invalidobj12c:  from containers(dba_objects)
#invalidobj12c:   where status = 'INVALID'
#invalidobj12c:     and owner not in ('ADM_PARALLEL_EXECUTE_TASK','ANONYMOUS','APEX_030200','APEX_ADMINISTRATOR_ROLE','APEX_PUBLIC_USER',
#invalidobj12c:                       'APPQOSSYS','AQ_ADMINISTRATOR_ROLE','AQ_USER_ROLE','CONNECT','CSW_USR_ROLE','CTXAPP','CTXSYS',
#invalidobj12c:                       'CWM_USER','DATAPUMP_EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE','DBA','DBFS_ROLE','DBSNMP',
#invalidobj12c:                       'DELETE_CATALOG_ROLE','DIP','EXECUTE_CATALOG_ROLE','EXFSYS','EXP_FULL_DATABASE','FLOWS_FILES',
#invalidobj12c:                       'GATHER_SYSTEM_STATISTICS','HS_ADMIN_EXECUTE_ROLE','HS_ADMIN_ROLE','HS_ADMIN_SELECT_ROLE',
#invalidobj12c:                       'IMP_FULL_DATABASE','JAVADEBUGPRIV','JAVASYSPRIV','LOGSTDBY_ADMINISTRATOR','MDDATA','MDSYS',
#invalidobj12c:                       'MGMT_USER','MGMT_VIEW','OEM_ADVISOR','OEM_MONITOR','OLAPSYS','OLAP_DBA','OLAP_USER','OLAP_XS_ADMIN',
#invalidobj12c:                       'ORACLE_OCM','ORDADMIN','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWB$CLIENT','OWBSYS','OWBSYS_AUDIT',
#invalidobj12c:                       'PUBLIC','RECOVERY_CATALOG_OWNER','RESOURCE','SCHEDULER_ADMIN','SCOTT','SELECT_CATALOG_ROLE',
#invalidobj12c:                       'SI_INFORMTN_SCHEMA','SPATIAL_CSW_ADMIN','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN',
#invalidobj12c:                       'SPATIAL_WFS_ADMIN_USR','SQLTXADMIN','SQLTXPLAIN','SQLT_USER_ROLE','SYS','SYSMAN','SYSTEM',
#invalidobj12c:                       'WFS_USR_ROLE','WMSYS','WM_ADMIN_ROLE','XDB','XDBADMIN','AUDSYS','OJVMSYS','GSMADMIN_INTERNAL','PERFSTAT')
#invalidobj12c:	) v ,v$pdbs b
#invalidobj12c:where v.con_id = b.con_id(+)
#invalidobj12c:  and rownum < 31;
#invalidobj12c:
#invalidobj12c:
#invalidobj12c:
#invalidtrigger:set lines 400
#invalidtrigger:set pages 1000
#invalidtrigger:set feedback off
#invalidtrigger:set heading off
#invalidtrigger:
#invalidtrigger:select chr(34)||owner ||chr(34)||','||
#invalidtrigger:       chr(34)||trigger_name   ||chr(34)||','||  
#invalidtrigger:       chr(34)||trigger_type   ||chr(34)||','||    
#invalidtrigger:       chr(34)||status         ||chr(34)||','||  
#invalidtrigger:       chr(34)||table_owner||'.'||table_name ||chr(34)
#invalidtrigger:from dba_triggers where status='DISABLED' and owner not in ('SYS','EXFSYS','WMSYS')
#invalidtrigger:order by owner,table_name,trigger_name;
#invalidtrigger:
#invalidtrigger12c:set lines 400
#invalidtrigger12c:set pages 1000
#invalidtrigger12c:set feedback off
#invalidtrigger12c:set heading off
#invalidtrigger12c:
#invalidtrigger12c:select chr(34)||nvl(b.name,'CDB$ROOT')           ||chr(34)||','|| 
#invalidtrigger12c:       chr(34)||a.owner                          ||chr(34)||','||
#invalidtrigger12c:       chr(34)||a.trigger_name                   ||chr(34)||','||  
#invalidtrigger12c:       chr(34)||a.trigger_type                   ||chr(34)||','||    
#invalidtrigger12c:       chr(34)||a.status                         ||chr(34)||','||  
#invalidtrigger12c:       chr(34)||a.table_owner||'.'||a.table_name ||chr(34)
#invalidtrigger12c:from containers(dba_triggers) a,v$pdbs b
#invalidtrigger12c:where a.status='DISABLED' and a.con_id = b.con_id(+)
#invalidtrigger12c:  and a.owner not in ('SYS','EXFSYS','WMSYS','SYSMAN')
#invalidtrigger12c:order by A.CON_ID,A.owner,A.table_name,A.trigger_name;
#invalidtrigger12c:
#jobs:set lines 400
#jobs:set pages 1000
#jobs:set feedback off
#jobs:set heading off
#jobs:
#jobs:select chr(34)||job                ||chr(34)||','||
#jobs:       chr(34)||priv_user          ||chr(34)||','||  
#jobs:       chr(34)||substr(replace(replace(what,chr(13),' '),chr(10),' '),1,60)  ||chr(34)||','||  
#jobs:       chr(34)||decode(nvl(broken,'Y'), 'Y', 'Broken', 'Normal')||chr(34)||','||  
#jobs:       chr(34)||decode(nvl(broken,'Y'), 'Y','YES','NO') ||chr(34)
#jobs:FROM sys.dba_jobs
#jobs:where priv_user not like 'APEX%' and priv_user not like 'SYSMAN%'
#jobs:order by job
#jobs:;
#jobs:
#jobs:
#jobs12c:set lines 400
#jobs12c:set pages 1000
#jobs12c:set feedback off
#jobs12c:set heading off
#jobs12c:
#jobs12c:select chr(34)||nvl(b.name,'CDB$ROOT')  ||chr(34)||','||
#jobs12c:       chr(34)||A.job                   ||chr(34)||','||
#jobs12c:       chr(34)||A.priv_user             ||chr(34)||','||  
#jobs12c:       chr(34)||substr(replace(replace(what,chr(13),' '),chr(10),' '),1,60)  ||chr(34)||','||  
#jobs12c:       chr(34)||decode(nvl(A.broken,'Y'), 'Y', 'Broken', 'Normal')||chr(34)||','||  
#jobs12c:       chr(34)||decode(nvl(A.broken,'Y'), 'Y','YES','NO') ||chr(34)
#jobs12c:FROM   containers(dba_jobs) a,
#jobs12c:       v$pdbs b
#jobs12c:where a.priv_user not like 'APEX%' and  a.priv_user not like 'SYSMAN%'
#jobs12c:  and a.con_id = b.con_id(+)
#jobs12c:order by A.CON_ID,a.job
#jobs12c:;
#jobs12c:
#jobs12c:
#lmscount:set lines 400
#lmscount:set pages 1000
#lmscount:set heading off
#lmscount:set feedback off
#lmscount:
#lmscount:select chr(34) ||inst_id ||chr(34)||','||
#lmscount:       chr(34) ||nvl(count(*),0) ||chr(34)
#lmscount:  from gv$process
#lmscount:  where program like  'oracle%LMS%'
#lmscount:  group by inst_id;
#lmscount:
#logic_read_per_second:set lines 200
#logic_read_per_second:set pages 3000
#logic_read_per_second:set feedback off
#logic_read_per_second:set heading off
#logic_read_per_second:col dbid new_val dbid noprint
#logic_read_per_second:select dbid from v$database;
#logic_read_per_second:
#logic_read_per_second:col INSTANCE_NUMBER  new_val INSTANCE_NUMBER noprint
#logic_read_per_second:select INSTANCE_NUMBER  from v$instance;
#logic_read_per_second:
#logic_read_per_second:col value_db_block_size new_val value_db_block_size noprint
#logic_read_per_second:select value value_db_block_size
#logic_read_per_second:          from v$parameter
#logic_read_per_second:         where name = 'db_block_size' ;
#logic_read_per_second:         
#logic_read_per_second:col startup_time  new_val startup_time noprint      
#logic_read_per_second:select to_char(startup_time, 'yyyymmddhh24mi') startup_time
#logic_read_per_second:  from v$instance ;
#logic_read_per_second:
#logic_read_per_second:select chr(34)||substr(end_interval_time, 1, 8)||'-'||substr(end_interval_time, 9, 4)||chr(34) 
#logic_read_per_second:        ||','||chr(34)||
#logic_read_per_second:       round((value - value_prev) /
#logic_read_per_second:             ((to_date(end_interval_time, 'yyyymmddhh24miss') -
#logic_read_per_second:             to_date(end_interval_time_prev, 'yyyymmddhh24miss')) * 24 * 3600),0)||chr(34)
#logic_read_per_second:  from (select snap_id,
#logic_read_per_second:               end_interval_time,
#logic_read_per_second:               value,
#logic_read_per_second:               lag(value) over(order by snap_id) value_prev,
#logic_read_per_second:               lag(end_interval_time) over(order by snap_id) end_interval_time_prev
#logic_read_per_second:          from (select a.snap_id,
#logic_read_per_second:                       to_char(b.end_interval_time, 'yyyymmddhh24miss') end_interval_time,
#logic_read_per_second:                       sum(a.value) value
#logic_read_per_second:                  from dba_hist_sysstat a, dba_hist_snapshot b
#logic_read_per_second:                 where a.stat_name='session logical reads'
#logic_read_per_second:                   AND a.DBID=&DBID
#logic_read_per_second:                   and a.instance_number=&INSTANCE_NUMBER
#logic_read_per_second:                   and b.snap_id = a.snap_id
#logic_read_per_second:                   and a.instance_number = b.instance_number
#logic_read_per_second:                   and to_char(b.end_interval_time, 'yyyymmddhh24mi') > &startup_time
#logic_read_per_second:                   and b.end_interval_time >= sysdate - 7 
#logic_read_per_second:                 group by a.snap_id,
#logic_read_per_second:                          to_char(b.end_interval_time, 'yyyymmddhh24miss'))) result_a
#logic_read_per_second: where value_prev is not null
#logic_read_per_second:   and end_interval_time_prev is not null
#logic_read_per_second: order by snap_id ;
#logic_read_per_second:
#logic_read_per_second:
#logic_read_per_second:
#logswitch:
#logswitch:set lines 400
#logswitch:set pages 1000
#logswitch:set feedback off
#logswitch:col day format a12
#logswitch:select
#logswitch:  substr(to_char(first_time, 'YYYYMMDD'),1,8) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'00',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'01',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'02',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'03',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'04',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'05',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'06',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'07',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'08',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'09',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'10',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'11',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'12',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'13',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'14',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'15',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'16',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'17',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'18',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'19',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'20',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'21',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'22',1,0)) ||','||
#logswitch:  sum(decode(substr(to_char(first_time, 'YYYY-MM-DD HH24'),12,2),'23',1,0)) ||','||
#logswitch:  count(*) total 
#logswitch:from v$log_history  a 
#logswitch:where first_time > sysdate - 10
#logswitch:  and thread# =(select thread# from v$instance )
#logswitch: group by substr(to_char(first_time, 'YYYYMMDD'),1,8)
#logswitch:   order by substr(to_char(first_time, 'YYYYMMDD'),1,8)
#logswitch:;
#logswitch:
#onlinelog:
#onlinelog:set lines 400
#onlinelog:set pages 1000
#onlinelog:set feedback off
#onlinelog:set heading off
#onlinelog:
#onlinelog:select chr(34)||a.thread#||chr(34)||','||
#onlinelog:       chr(34)||a.group#||chr(34)||','||
#onlinelog:       chr(34)||b.member||chr(34)||','||
#onlinelog:       chr(34)||a.status||chr(34)||','||
#onlinelog:       chr(34)||a.sequence#||chr(34)||','||
#onlinelog:       chr(34)||trunc(a.bytes/1024/1024) ||chr(34)||','||
#onlinelog:       chr(34)||DECODE(NVL(C.GROUP#,-1),-1,'ONLINE_LOG','STANDBY_LOG') ||chr(34)
#onlinelog:from v$log a,
#onlinelog:     v$logfile b,
#onlinelog:     v$standby_log c
#onlinelog:where a.group#=b.group# 
#onlinelog:  and a.group# = c.group#(+)
#onlinelog:order by a.thread#,a.group#
#onlinelog:;
#onlinelog:
#onlinelog:
#optimizer_stats_advisor:
#optimizer_stats_advisor:set  lines 200
#optimizer_stats_advisor:set  pages 100
#optimizer_stats_advisor:set feedback off
#optimizer_stats_advisor:set heading off
#optimizer_stats_advisor:SELECT chr(34)||parameter_name||chr(34)||','|| 
#optimizer_stats_advisor:       chr(34)||parameter_value ||chr(34)
#optimizer_stats_advisor:FROM   DBA_ADVISOR_PARAMETERS
#optimizer_stats_advisor:WHERE task_name='AUTO_STATS_ADVISOR_TASK'
#optimizer_stats_advisor:  and PARAMETER_NAME IN 'EXECUTION_DAYS_TO_EXPIRE';
#optimizer_stats_advisor:
#optimizer_stats_advisor:
#optimizer_stats_advisor12c:
#optimizer_stats_advisor12c:set  lines 200
#optimizer_stats_advisor12c:set  pages 100
#optimizer_stats_advisor12c:set feedback off
#optimizer_stats_advisor12c:set heading off  
#optimizer_stats_advisor12c:SELECT chr(34)||nvl(b.name,'CDB$ROOT')||chr(34)||','||
#optimizer_stats_advisor12c:       chr(34)||a.parameter_name||chr(34)||','|| 
#optimizer_stats_advisor12c:       chr(34)||a.parameter_value||chr(34) 
#optimizer_stats_advisor12c:FROM   containers(DBA_ADVISOR_PARAMETERS) a,
#optimizer_stats_advisor12c:       v$pdbs b
#optimizer_stats_advisor12c:WHERE a.task_name='AUTO_STATS_ADVISOR_TASK'
#optimizer_stats_advisor12c:  and a.PARAMETER_NAME IN 'EXECUTION_DAYS_TO_EXPIRE'
#optimizer_stats_advisor12c:  and a.con_id = b.con_id(+)
#optimizer_stats_advisor12c:order by a.con_id;
#optimizer_stats_advisor12c:
#optimizer_stats_advisor12c:
#parameter:set lines 400
#parameter:set pages 1000
#parameter:set feedback off
#parameter:set heading off
#parameter:col name format a40
#parameter:col value format a120
#parameter:
#parameter:select chr(34)||inst_id||chr(34)||'___'||
#parameter:       chr(34)||name||chr(34)||'___'||
#parameter:       chr(34)||nvl(replace(value,'"',' '),'NOT-CONFIGURE') ||chr(34)
#parameter:from gv$parameter
#parameter:where name  in ('processes','sessions','resource_limit','cpu_count','trace_files_public','max_dump_file_size','aq_tm_processes',
#parameter:                'sga_max_size','sga_target','memory_target','result_cache_max_size','undo_retention','recovery_parallelism',
#parameter:                'audit_trail','timed_statistics','shared_pool_size','large_pool_size','compatible','fast_start_parallel_rollback',
#parameter:                'db_files','db_recovery_file_dest','db_recovery_file_dest_size','local_listener','inmemory_query','recyclebin',
#parameter:                'standby_file_management','remote_listener','optimizer_mode','db_block_size','cursor_sharing','undo_management',
#parameter:                'db_file_name_convert','log_file_name_convert','db_create_file_dest','db_create_online_log_dest_1','db_recovery_file_dest','db_recovery_file_dest_size',
#parameter:                'statistics_level','enable_ddl_logging','log_archive_dest_1','log_archive_dest_2','log_archive_dest_3','log_archive_dest_state_3','optimizer_index_cost_adj','job_queue_processes',
#parameter:                'db_cache_size','memory_max_target','log_archive_dest_state_1' ,'log_archive_dest_state_2','control_management_pack_access','control_file_record_keep_time',
#parameter:                'open_cursors','parallel_force_local','pga_aggregate_target','deferred_segment_creation','gcs_server_processes',
#parameter:                'filesystemio_options','audit_file_dest','audit_sys_operations','audit_trail','event','log_archive_config','parallel_max_servers','cluster_database','session_cached_cursors')
#parameter:order by name,inst_id;
#parameter:
#parameter:
#parameter:
#parameter12c:set lines 400
#parameter12c:set pages 1000
#parameter12c:set feedback off
#parameter12c:set heading off
#parameter12c:col name format a40
#parameter12c:col value format a120
#parameter12c:
#parameter12c:select chr(34)||nvl(b.name,'CDB$ROOT')||chr(34)||'___'||
#parameter12c:       chr(34)||A.inst_id||chr(34)||'___'||
#parameter12c:       chr(34)||A.name||chr(34)||'___'||
#parameter12c:       chr(34)||upper(nvl(replace(value,'"',' '),'NOT-CONFIGURE')) ||chr(34)
#parameter12c:from gv$parameter a, v$pdbs b
#parameter12c:where a.name  in ('processes','sessions','resource_limit','cpu_count','trace_files_public','max_dump_file_size','aq_tm_processes',
#parameter12c:                'sga_max_size','sga_target','memory_target','result_cache_max_size','undo_retention','recovery_parallelism',
#parameter12c:                'audit_trail','timed_statistics','shared_pool_size','large_pool_size','compatible','fast_start_parallel_rollback',
#parameter12c:                'db_files','db_recovery_file_dest','db_recovery_file_dest_size','local_listener','inmemory_query','recyclebin',
#parameter12c:                'db_file_name_convert','log_file_name_convert','db_create_file_dest','db_create_online_log_dest_1','db_recovery_file_dest','db_recovery_file_dest_size',
#parameter12c:                'standby_file_management','remote_listener','optimizer_mode','db_block_size','cursor_sharing','undo_management',
#parameter12c:                'statistics_level','enable_ddl_logging','enable_ddl_logging','log_archive_dest_1','log_archive_dest_2','log_archive_dest_3','log_archive_dest_state_3','optimizer_index_cost_adj','job_queue_processes',
#parameter12c:                'db_cache_size','memory_max_target','log_archive_dest_state_1' ,'log_archive_dest_state_2','control_management_pack_access','control_file_record_keep_time',
#parameter12c:                'open_cursors','parallel_force_local','pga_aggregate_target','deferred_segment_creation','gcs_server_processes',
#parameter12c:                'filesystemio_options','audit_file_dest','audit_sys_operations','audit_trail','event','parallel_max_servers','Unified Auditing','awr_pdb_autoflush_enabled','cluster_database','session_cached_cursors')
#parameter12c: AND a.con_id = b.con_id(+)
#parameter12c:union all
#parameter12c:select chr(34)||nvl(b.name,'CDB$ROOT')    ||chr(34)||'___'||
#parameter12c:       chr(34)||a.sid     ||chr(34)||'___'||
#parameter12c:       chr(34)||a.name    ||chr(34)||'___'||
#parameter12c:       chr(34)||a.value$  ||chr(34)
#parameter12c:from pdb_spfile$ a ,v$pdbs b
#parameter12c:where a.pdb_uid(+)=b.dbid
#parameter12c:;
#parameter12c:
#parameter12c:
#parameter12c:
#patchapply:
#patchapply:set lines 400
#patchapply:set pages 1000
#patchapply:set feedback off
#patchapply:set heading off
#patchapply:col action_time format a16
#patchapply:col ACTION format a30
#patchapply:col COMMENTS format a80
#patchapply:col namespace format a40
#patchapply:col version format a40
#patchapply:select chr(34)||to_char(ACTION_TIME,'yyyymmdd') ||chr(34)||','||
#patchapply:       chr(34)||ACTION ||chr(34)||','||
#patchapply:       chr(34)||nvl(NAMESPACE,'none') ||chr(34)||','||
#patchapply:       chr(34)||nvl(VERSION,'none') ||chr(34)||','||
#patchapply:       chr(34)||nvl(ID,-1) ||chr(34)||','||
#patchapply:       chr(34)||nvl(replace(substr(COMMENTS ,1,40),' ','_'),'null') ||chr(34)
#patchapply:from dba_registry_history
#patchapply:;
#patchapply:
#patchapply:
#patchapply12c:
#patchapply12c:set lines 400
#patchapply12c:set pages 1000
#patchapply12c:set feedback off
#patchapply12c:set heading off
#patchapply12c:col action_time format a16
#patchapply12c:col ACTION format a30
#patchapply12c:col COMMENTS format a80
#patchapply12c:col namespace format a40
#patchapply12c:col version format a40
#patchapply12c:select chr(34)||nvl(b.name,'CDB$ROOT')          ||chr(34)||','||
#patchapply12c:       chr(34)||to_char(a.ACTION_TIME,'yyyymmdd') ||chr(34)||','||
#patchapply12c:       chr(34)||a.ACTION                          ||chr(34)||','||
#patchapply12c:       chr(34)||nvl(a.NAMESPACE,'none')           ||chr(34)||','||
#patchapply12c:       chr(34)||nvl(a.VERSION,'none')             ||chr(34)||','||
#patchapply12c:       chr(34)||nvl(a.ID,-1)                      ||chr(34)||','||
#patchapply12c:       chr(34)||nvl(replace(substr(a.COMMENTS ,1,40),' ','_'),'null') ||chr(34)
#patchapply12c:from containers(dba_registry_history) a,v$pdbs b
#patchapply12c:where a.con_id = b.con_id(+)
#patchapply12c:order by a.con_id,a.ACTION_TIME
#patchapply12c:;
#patchapply12c:
#patchapply12c:
#pdbsavedstate:set lines 400
#pdbsavedstate:set pages 1000
#pdbsavedstate:set feedback off
#pdbsavedstate:set heading off
#pdbsavedstate:SELECT CHR(34)||CON_NAME||CHR(34)||','||
#pdbsavedstate:       CHR(34)||INSTANCE_NAME||CHR(34)||','|| 
#pdbsavedstate:       CHR(34)||STATE||CHR(34)||','||
#pdbsavedstate:       CHR(34)||RESTRICTED||CHR(34)
#pdbsavedstate:FROM DBA_PDB_SAVED_STATES;
#pdbsavedstate:
#pdbstat:set lines 400
#pdbstat:set pages 1000
#pdbstat:set feedback off
#pdbstat:set heading off
#pdbstat:
#pdbstat:select chr(34)||con_id         ||chr(34)||','||
#pdbstat:       chr(34)||name           ||chr(34)||','||
#pdbstat:       chr(34)||inst_id        ||chr(34)||','||
#pdbstat:       chr(34)||open_mode      ||chr(34)||','||
#pdbstat:       chr(34)||RESTRICTED     ||chr(34) 
#pdbstat:from gv$pdbs
#pdbstat:order by con_id,inst_id
#pdbstat:;
#pdbstat:
#pdbstat:
#pdbstat:
#physic_read_per_second:set lines 200
#physic_read_per_second:set pages 3000
#physic_read_per_second:set feedback off
#physic_read_per_second:set heading off
#physic_read_per_second:col dbid new_val dbid noprint
#physic_read_per_second:select dbid from v$database;
#physic_read_per_second:
#physic_read_per_second:col INSTANCE_NUMBER  new_val INSTANCE_NUMBER noprint
#physic_read_per_second:select INSTANCE_NUMBER  from v$instance;
#physic_read_per_second:
#physic_read_per_second:col value_db_block_size new_val value_db_block_size noprint
#physic_read_per_second:select value value_db_block_size
#physic_read_per_second:          from v$parameter
#physic_read_per_second:         where name = 'db_block_size' ;
#physic_read_per_second:         
#physic_read_per_second:col startup_time  new_val startup_time noprint      
#physic_read_per_second:select to_char(startup_time, 'yyyymmddhh24mi') startup_time
#physic_read_per_second:  from v$instance ;
#physic_read_per_second:
#physic_read_per_second:select chr(34)||substr(end_interval_time, 1, 8)||'-'||substr(end_interval_time, 9, 4)||chr(34) 
#physic_read_per_second:        ||','||chr(34)||
#physic_read_per_second:       round((value - value_prev) /
#physic_read_per_second:             ((to_date(end_interval_time, 'yyyymmddhh24miss') -
#physic_read_per_second:             to_date(end_interval_time_prev, 'yyyymmddhh24miss')) * 24 * 3600),0)||chr(34)
#physic_read_per_second:  from (select snap_id,
#physic_read_per_second:               end_interval_time,
#physic_read_per_second:               value,
#physic_read_per_second:               lag(value) over(order by snap_id) value_prev,
#physic_read_per_second:               lag(end_interval_time) over(order by snap_id) end_interval_time_prev
#physic_read_per_second:          from (select a.snap_id,
#physic_read_per_second:                       to_char(b.end_interval_time, 'yyyymmddhh24miss') end_interval_time,
#physic_read_per_second:                       sum(a.value) value
#physic_read_per_second:                  from dba_hist_sysstat a, dba_hist_snapshot b
#physic_read_per_second:                 where a.stat_name='physical reads'
#physic_read_per_second:                   AND a.DBID=&DBID
#physic_read_per_second:                   and a.instance_number=&INSTANCE_NUMBER
#physic_read_per_second:                   and b.snap_id = a.snap_id
#physic_read_per_second:                   and a.instance_number = b.instance_number
#physic_read_per_second:                   and to_char(b.end_interval_time, 'yyyymmddhh24mi') > &startup_time
#physic_read_per_second:                   and b.end_interval_time >= sysdate - 7 
#physic_read_per_second:                 group by a.snap_id,
#physic_read_per_second:                          to_char(b.end_interval_time, 'yyyymmddhh24miss'))) result_a
#physic_read_per_second: where value_prev is not null
#physic_read_per_second:   and end_interval_time_prev is not null
#physic_read_per_second: order by snap_id ;
#physic_read_per_second:
#physic_read_per_second:
#physic_read_per_second:
#profile:
#profile:set lines 400
#profile:set pages 1000
#profile:set feedback off
#profile:set heading off
#profile:select chr(34)||profile        ||chr(34)||','||
#profile:       chr(34)||resource_name  ||chr(34)||','||
#profile:       chr(34)||resource_type  ||chr(34)||','||
#profile:       chr(34)||limit ||chr(34)
#profile:from dba_profiles
#profile:WHERE RESOURCE_NAME IN ('FAILED_LOGIN_ATTEMPTS','PASSWORD_GRACE_TIME','PASSWORD_LIFE_TIME','PASSWORD_LOCK_TIME')
#profile:order by profile,resource_name;
#profile:
#profile:
#profile:
#profile12c:
#profile12c:set lines 400
#profile12c:set pages 1000
#profile12c:set feedback off
#profile12c:set heading off
#profile12c:select chr(34)||nvl(b.name,'CDB$ROOT')||chr(34)||','||
#profile12c:       chr(34)||a.profile               ||chr(34)||','||
#profile12c:       chr(34)||a.resource_name         ||chr(34)||','||
#profile12c:       chr(34)||a.resource_type         ||chr(34)||','||
#profile12c:       chr(34)||to_char(a.limit) ||chr(34) 
#profile12c: from containers(dba_profiles) a,v$pdbs b
#profile12c:WHERE a.RESOURCE_NAME IN ('FAILED_LOGIN_ATTEMPTS','PASSWORD_GRACE_TIME','PASSWORD_LIFE_TIME','PASSWORD_LOCK_TIME')
#profile12c:  and a.con_id = b.con_id(+)
#profile12c:order by profile,resource_name;
#profile12c:
#profile12c:
#profile12c:
#recyclebin:set lines 200
#recyclebin:set pages 1000
#recyclebin:set feedback off
#recyclebin:set heading off
#recyclebin:
#recyclebin:select chr(34)|| r.ts_name ||chr(34)||','||
#recyclebin:       chr(34)|| to_char(nvl(count(*),0)) ||chr(34)
#recyclebin:from dba_recyclebin r
#recyclebin:group by r.ts_name;
#recyclebin:
#recyclebin:
#recyclebin_12c:select p.name pdb_name,ts_name tablespace_name,count(*) cnt 
#recyclebin_12c:from cdb_recyclebin r,(select con_id,name from v$pdbs union all select 1,'CDB$ROOT' from dual) p
#recyclebin_12c:where r.con_id=p.con_id group by p.name,ts_name
#resourcelimit:
#resourcelimit:set  lines 400
#resourcelimit:set pages 1000
#resourcelimit:set heading off
#resourcelimit:set feedback off
#resourcelimit:
#resourcelimit:SELECT chr(34)||v.RESOURCE_NAME       ||chr(34)||','||
#resourcelimit:	     chr(34)||v.CURRENT_UTILIZATION ||chr(34)||','||
#resourcelimit:       chr(34)||v.MAX_UTILIZATION     ||chr(34)||','||
#resourcelimit:       chr(34)||v.INITIAL_ALLOCATION  ||chr(34)||','||
#resourcelimit:	     chr(34)||v.LIMIT_VALUE         ||chr(34)||','||
#resourcelimit:	     chr(34)||case when v.CURRENT_UTILIZATION/decode(to_number(translate(v.LIMIT_VALUE,'UNLIMITED','10000000000')),'0','10000000000') > 0.8 then 'YES' else 'NO' end  ||chr(34)
#resourcelimit:  FROM (select RESOURCE_NAME,CURRENT_UTILIZATION,MAX_UTILIZATION,INITIAL_ALLOCATION,LIMIT_VALUE 
#resourcelimit:         from gv$resource_limit where INST_ID=(select instance_number from v$instance) order by 1,2) V
#resourcelimit:order by 1;
#resourcelimit:
#resourcelimit:
#resourcelimit:
#resourcelimit12c:
#resourcelimit12c:set  lines 400
#resourcelimit12c:set pages 1000
#resourcelimit12c:set heading off
#resourcelimit12c:set feedback off
#resourcelimit12c:
#resourcelimit12c:SELECT chr(34)||NVL(B.NAME,'CBD$ROOT')   ||chr(34)||','||
#resourcelimit12c:       chr(34)||v.RESOURCE_NAME       ||chr(34)||','||
#resourcelimit12c:	     chr(34)||v.CURRENT_UTILIZATION ||chr(34)||','||
#resourcelimit12c:       chr(34)||v.MAX_UTILIZATION     ||chr(34)||','||
#resourcelimit12c:       chr(34)||v.INITIAL_ALLOCATION  ||chr(34)||','||
#resourcelimit12c:	     chr(34)||v.LIMIT_VALUE         ||chr(34)||','||
#resourcelimit12c:	     chr(34)||case when v.CURRENT_UTILIZATION/decode(to_number(translate(v.LIMIT_VALUE,'UNLIMITED','10000000000')),'0','10000000000') > 0.8 then 'YES' else 'NO' end  ||chr(34)
#resourcelimit12c:  FROM (select CON_ID,
#resourcelimit12c:               RESOURCE_NAME,
#resourcelimit12c:               CURRENT_UTILIZATION,
#resourcelimit12c:               MAX_UTILIZATION,INITIAL_ALLOCATION,
#resourcelimit12c:               LIMIT_VALUE 
#resourcelimit12c:         from  containers(gv$resource_limit) where INST_ID=(select instance_number from v$instance) order by 1,2) V,V$PDBS B
#resourcelimit12c:WHERE V.CON_ID = B.CON_ID(+)
#resourcelimit12c:order by v.con_id,v.resource_name;
#resourcelimit12c:
#resourcelimit12c:
#resourcelimit12c:
#rman:
#rman:SET LINES 400
#rman:SET PAGES 1000
#rman:set feedback off
#rman:set heading off
#rman:col stat format a24
#rman:col dates format a14
#rman:with a as 
#rman:(select /*+ materialize */ trunc(sysdate - 1) - rownum +1 dates from dual connect by rownum <= 15),
#rman:b as 
#rman:(select /*+ materialize */ trunc(START_TIME) dates ,max(STATUS) stat
#rman:   from v$rman_backup_job_details 
#rman:  where start_time > sysdate - 15 
#rman:    and INPUT_TYPE in ('DB INCR','DB FULL')
#rman:  group by trunc(START_TIME))
#rman:SELECT chr(34)||v.dates ||chr(34)||','||
#rman:	     chr(34)||nvl(v.stat,'NOTRUNING')|| chr(34)
#rman:  FROM (select trunc(sysdate)-a.dates dys,to_char(a.dates,'YYYY-MM-DD') dates,b.stat from a,b where a.dates=b.dates(+) order by 1 desc) v order by 1;
#rman:
#scheduler_windows:set lines 200
#scheduler_windows:set pages 0
#scheduler_windows:set feedback off
#scheduler_windows:select CHR(34)||window_name ||CHR(34)||','||
#scheduler_windows:       CHR(34)||to_char(NEXT_START_DATE,'yyyymmdd hh24:mi:ss')||CHR(34)||','||
#scheduler_windows:       CHR(34)||enabled ||CHR(34)||','||
#scheduler_windows:       CHR(34)||active  ||CHR(34)
#scheduler_windows:from DBA_SCHEDULER_WINDOWS
#scheduler_windows:where window_name not in ('WEEKNIGHT_WINDOW','WEEKEND_WINDOW') 
#scheduler_windows:AND (( NEXT_START_DATE < SYSDATE AND ACTIVE <> 'TRUE') OR  (enabled <> 'TRUE'))
#scheduler_windows:;
#scheduler_windows:
#scheduler_windows:
#scheduler_windows:
#scnhealthcheck:Rem
#scnhealthcheck:Rem $Header: tfa/src/orachk/src/scnhealthcheck.sql /main/1 2015/12/15 21:08:37 cgirdhar Exp $
#scnhealthcheck:Rem
#scnhealthcheck:Rem scnhealthcheck.sql
#scnhealthcheck:Rem
#scnhealthcheck:Rem Copyright (c) 2015, Oracle and/or its affiliates. All rights reserved.
#scnhealthcheck:Rem
#scnhealthcheck:Rem    NAME
#scnhealthcheck:Rem      scnhealthcheck.sql - <one-line expansion of the name>
#scnhealthcheck:Rem
#scnhealthcheck:Rem    DESCRIPTION
#scnhealthcheck:Rem      <short description of component this file declares/defines>
#scnhealthcheck:Rem
#scnhealthcheck:Rem    NOTES
#scnhealthcheck:Rem      <other useful comments, qualifications, etc.>
#scnhealthcheck:Rem
#scnhealthcheck:Rem    BEGIN SQL_FILE_METADATA 
#scnhealthcheck:Rem    SQL_SOURCE_FILE: tfa/src/orachk/src/scnhealthcheck.sql 
#scnhealthcheck:Rem    SQL_SHIPPED_FILE: 
#scnhealthcheck:Rem    SQL_PHASE: 
#scnhealthcheck:Rem    SQL_STARTUP_MODE: NORMAL 
#scnhealthcheck:Rem    SQL_IGNORABLE_ERRORS: NONE 
#scnhealthcheck:Rem    SQL_CALLING_FILE: 
#scnhealthcheck:Rem    END SQL_FILE_METADATA
#scnhealthcheck:Rem
#scnhealthcheck:Rem    MODIFIED   (MM/DD/YY)
#scnhealthcheck:Rem    cgirdhar    12/15/15 - SCN healthcheck script
#scnhealthcheck:Rem    cgirdhar    12/15/15 - Created
#scnhealthcheck:
#scnhealthcheck:Rem
#scnhealthcheck:Rem $Header: tfa/src/orachk/src/scnhealthcheck.sql /main/1 2015/12/15 21:08:37 cgirdhar Exp $
#scnhealthcheck:Rem
#scnhealthcheck:Rem scnhealthcheck.sql
#scnhealthcheck:Rem
#scnhealthcheck:Rem Copyright (c) 2012, 2015, Oracle and/or its affiliates. 
#scnhealthcheck:Rem All rights reserved.
#scnhealthcheck:Rem
#scnhealthcheck:Rem    NAME
#scnhealthcheck:Rem      scnhealthcheck.sql - Scn Health check
#scnhealthcheck:Rem
#scnhealthcheck:Rem    DESCRIPTION
#scnhealthcheck:Rem      Checks scn health of a DB
#scnhealthcheck:Rem
#scnhealthcheck:Rem    NOTES
#scnhealthcheck:Rem      .
#scnhealthcheck:Rem
#scnhealthcheck:Rem    MODIFIED   (MM/DD/YY)
#scnhealthcheck:Rem    tbhukya     01/11/12 - Created
#scnhealthcheck:Rem
#scnhealthcheck:Rem
#scnhealthcheck:
#scnhealthcheck:define LOWTHRESHOLD=10
#scnhealthcheck:define MIDTHRESHOLD=62
#scnhealthcheck:define VERBOSE=FALSE
#scnhealthcheck:
#scnhealthcheck:set veri off;
#scnhealthcheck:set feedback off;
#scnhealthcheck:
#scnhealthcheck:set serverout on
#scnhealthcheck:DECLARE
#scnhealthcheck: verbose boolean:=&&VERBOSE;
#scnhealthcheck:BEGIN
#scnhealthcheck: For C in (
#scnhealthcheck:  select 
#scnhealthcheck:   version, 
#scnhealthcheck:   date_time,
#scnhealthcheck:   dbms_flashback.get_system_change_number current_scn,
#scnhealthcheck:   indicator
#scnhealthcheck:  from
#scnhealthcheck:  (
#scnhealthcheck:   select
#scnhealthcheck:   version,
#scnhealthcheck:   to_char(SYSDATE,'YYYY/MM/DD HH24:MI:SS') DATE_TIME,
#scnhealthcheck:   ((((
#scnhealthcheck:    ((to_number(to_char(sysdate,'YYYY'))-1988)*12*31*24*60*60) +
#scnhealthcheck:    ((to_number(to_char(sysdate,'MM'))-1)*31*24*60*60) +
#scnhealthcheck:    (((to_number(to_char(sysdate,'DD'))-1))*24*60*60) +
#scnhealthcheck:    (to_number(to_char(sysdate,'HH24'))*60*60) +
#scnhealthcheck:    (to_number(to_char(sysdate,'MI'))*60) +
#scnhealthcheck:    (to_number(to_char(sysdate,'SS')))
#scnhealthcheck:    ) * (16*1024)) - dbms_flashback.get_system_change_number)
#scnhealthcheck:   / (16*1024*60*60*24)
#scnhealthcheck:   ) indicator
#scnhealthcheck:   from v$instance
#scnhealthcheck:  ) 
#scnhealthcheck: ) LOOP
#scnhealthcheck:  dbms_output.put_line( '-----------------------------------------------------'
#scnhealthcheck:                        || '---------' );
#scnhealthcheck:  dbms_output.put_line( 'ScnHealthCheck' );
#scnhealthcheck:  dbms_output.put_line( '-----------------------------------------------------'
#scnhealthcheck:                        || '---------' );
#scnhealthcheck:  dbms_output.put_line( 'Current Date: '||C.date_time );
#scnhealthcheck:  dbms_output.put_line( 'Current SCN:  '||C.current_scn );
#scnhealthcheck:  if (verbose) then
#scnhealthcheck:    dbms_output.put_line( 'SCN Headroom: '||round(C.indicator,2) );
#scnhealthcheck:  end if;
#scnhealthcheck:  dbms_output.put_line( 'Version:      '||C.version );
#scnhealthcheck:  dbms_output.put_line( '-----------------------------------------------------'
#scnhealthcheck:                        || '---------' );
#scnhealthcheck:
#scnhealthcheck:  IF C.version > '10.2.0.5.0' and 
#scnhealthcheck:     C.version NOT LIKE '9.2%' THEN
#scnhealthcheck:    IF C.indicator>&MIDTHRESHOLD THEN 
#scnhealthcheck:      dbms_output.put_line('Result: A - SCN Headroom is good');
#scnhealthcheck:      dbms_output.put_line('Apply the latest recommended patches');
#scnhealthcheck:      dbms_output.put_line('based on your maintenance schedule');
#scnhealthcheck:      IF (C.version < '11.2.0.2') THEN
#scnhealthcheck:        dbms_output.put_line('AND set _external_scn_rejection_threshold_hours='
#scnhealthcheck:                             || '24 after apply.');
#scnhealthcheck:      END IF;
#scnhealthcheck:    ELSIF C.indicator<=&LOWTHRESHOLD THEN
#scnhealthcheck:      dbms_output.put_line('Result: C - SCN Headroom is low');
#scnhealthcheck:      dbms_output.put_line('If you have not already done so apply' );
#scnhealthcheck:      dbms_output.put_line('the latest recommended patches right now' );
#scnhealthcheck:      IF (C.version < '11.2.0.2') THEN
#scnhealthcheck:        dbms_output.put_line('set _external_scn_rejection_threshold_hours=24 '
#scnhealthcheck:                             || 'after apply');
#scnhealthcheck:      END IF;
#scnhealthcheck:      dbms_output.put_line('AND contact Oracle support immediately.' );
#scnhealthcheck:    ELSE
#scnhealthcheck:      dbms_output.put_line('Result: B - SCN Headroom is low');
#scnhealthcheck:      dbms_output.put_line('If you have not already done so apply' );
#scnhealthcheck:      dbms_output.put_line('the latest recommended patches right now');
#scnhealthcheck:      IF (C.version < '11.2.0.2') THEN
#scnhealthcheck:        dbms_output.put_line('AND set _external_scn_rejection_threshold_hours='
#scnhealthcheck:                             ||'24 after apply.');
#scnhealthcheck:      END IF;
#scnhealthcheck:    END IF;
#scnhealthcheck:  ELSE
#scnhealthcheck:    IF C.indicator<=&MIDTHRESHOLD THEN
#scnhealthcheck:      dbms_output.put_line('Result: C - SCN Headroom is low');
#scnhealthcheck:      dbms_output.put_line('If you have not already done so apply' );
#scnhealthcheck:      dbms_output.put_line('the latest recommended patches right now' );
#scnhealthcheck:      IF (C.version >= '10.1.0.5.0' and 
#scnhealthcheck:          C.version <= '10.2.0.5.0' and 
#scnhealthcheck:          C.version NOT LIKE '9.2%') THEN
#scnhealthcheck:        dbms_output.put_line(', set _external_scn_rejection_threshold_hours=24'
#scnhealthcheck:                             || ' after apply');
#scnhealthcheck:      END IF;
#scnhealthcheck:      dbms_output.put_line('AND contact Oracle support immediately.' );
#scnhealthcheck:    ELSE
#scnhealthcheck:      dbms_output.put_line('Result: A - SCN Headroom is good');
#scnhealthcheck:      dbms_output.put_line('Apply the latest recommended patches');
#scnhealthcheck:      dbms_output.put_line('based on your maintenance schedule ');
#scnhealthcheck:      IF (C.version >= '10.1.0.5.0' and
#scnhealthcheck:          C.version <= '10.2.0.5.0' and
#scnhealthcheck:          C.version NOT LIKE '9.2%') THEN
#scnhealthcheck:       dbms_output.put_line('AND set _external_scn_rejection_threshold_hours=24'
#scnhealthcheck:                             || ' after apply.');
#scnhealthcheck:      END IF;
#scnhealthcheck:    END IF;
#scnhealthcheck:  END IF;
#scnhealthcheck:  dbms_output.put_line(
#scnhealthcheck:    'For further information review MOS document id 1393363.1');
#scnhealthcheck:  dbms_output.put_line( '-----------------------------------------------------'
#scnhealthcheck:                        || '---------' );
#scnhealthcheck: END LOOP;
#scnhealthcheck:end;
#scnhealthcheck:/
#scnhealthcheck:
#sequence:
#sequence:set lines 400
#sequence:set pages 1000
#sequence:set feedback off
#sequence:set heading off
#sequence:SELECT chr(34)||v.sequence_owner       ||chr(34)||','||
#sequence:	     chr(34)||v.sequence_name        ||chr(34)||','|| 
#sequence:	     chr(34)||v.used_pct             ||chr(34)||','|| 
#sequence:	     chr(34)||v.min_value            ||chr(34)||','|| 
#sequence:	     chr(34)||v.max_value            ||chr(34)||','|| 
#sequence:	     chr(34)||v.increment_by         ||chr(34)||','|| 
#sequence:       chr(34)||v.cycle_flag           ||chr(34)||','|| 
#sequence:	     chr(34)||v.order_flag           ||chr(34)||','|| 
#sequence:	     chr(34)||v.cache_size           ||chr(34)||','|| 
#sequence:       chr(34)||v.last_number          ||chr(34)
#sequence:  FROM 
#sequence:(select sequence_owner,
#sequence:        sequence_name,
#sequence:        round(100 * (case
#sequence:               when increment_by < 0 then abs(a.last_number - a.max_value) / abs(a.max_value - min_value)
#sequence:               when increment_by > 0 then abs(a.last_number - a.min_value) / abs(a.max_value - min_value)
#sequence:               end), 2) || '%' as used_pct, 
#sequence:        min_value,
#sequence:        max_value,
#sequence:        increment_by, 
#sequence:        cycle_flag,
#sequence:        order_flag,
#sequence:        cache_size,
#sequence:        last_number
#sequence:  from dba_sequences a
#sequence: where cycle_flag = 'N'
#sequence:   and round(100 * (case
#sequence:               when increment_by < 0 then abs(a.last_number - a.max_value) / abs(a.max_value - min_value)
#sequence:               when increment_by > 0 then abs(a.last_number - a.min_value) / abs(a.max_value - min_value)
#sequence:             end), 2) >= 70) v order by sequence_owner,sequence_name;
#sequence:
#sequence:
#sequence12c:
#sequence12c:set lines 400
#sequence12c:set pages 1000
#sequence12c:set feedback off
#sequence12c:set heading off
#sequence12c:SELECT chr(34)||nvl(b.name,'CDB$ROOT') ||chr(34)||','||
#sequence12c:       chr(34)||v.sequence_owner       ||chr(34)||','||
#sequence12c:	     chr(34)||v.sequence_name        ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.used_pct             ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.min_value            ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.max_value            ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.increment_by         ||chr(34)||','|| 
#sequence12c:       chr(34)||v.cycle_flag           ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.order_flag           ||chr(34)||','|| 
#sequence12c:	     chr(34)||v.cache_size           ||chr(34)||','|| 
#sequence12c:       chr(34)||v.last_number          ||chr(34)
#sequence12c:  FROM 
#sequence12c:(select con_id,
#sequence12c:        sequence_owner,
#sequence12c:        sequence_name,
#sequence12c:        round(100 * (case
#sequence12c:               when increment_by < 0 then abs(a.last_number - a.max_value) / abs(a.max_value - min_value)
#sequence12c:               when increment_by > 0 then abs(a.last_number - a.min_value) / abs(a.max_value - min_value)
#sequence12c:               end), 2) || '%' as used_pct, 
#sequence12c:        min_value,
#sequence12c:        max_value,
#sequence12c:        increment_by, 
#sequence12c:        cycle_flag,
#sequence12c:        order_flag,
#sequence12c:        cache_size,
#sequence12c:        last_number
#sequence12c:  from containers(dba_sequences) a
#sequence12c: where cycle_flag = 'N'
#sequence12c:   and round(100 * (case
#sequence12c:               when increment_by < 0 then abs(a.last_number - a.max_value) / abs(a.max_value - min_value)
#sequence12c:               when increment_by > 0 then abs(a.last_number - a.min_value) / abs(a.max_value - min_value)
#sequence12c:             end), 2) >= 70) v ,v$pdbs b
#sequence12c:where v.con_id = b.con_id(+)        
#sequence12c:order by B.CON_ID,V.sequence_owner,V.sequence_name;
#sequence12c:
#sequence12c:
#sequence_cache:set lines 400
#sequence_cache:set pages 0
#sequence_cache:set feedback off
#sequence_cache:set heading off
#sequence_cache:
#sequence_cache:select chr(34)||sequence_owner ||chr(34)||
#sequence_cache:       chr(34)||SEQUENCE_NAME  ||chr(34)||
#sequence_cache:       chr(34)||to_char(cache_size) ||chr(34)||
#sequence_cache:       chr(34)||ORDER_FLAG ||chr(34)
#sequence_cache:from dba_sequences A,
#sequence_cache:     (SELECT VALUE FROM V$PARAMETER WHERE NAME ='cluster_database') B
#sequence_cache:where sequence_owner not in (select username from dba_users where default_tablespace in ('SYSTEM','SYSAUX'))
#sequence_cache:  AND A.CACHE_SIZE <= 500
#sequence_cache:  and a.ORDER_FLAG = 'Y'
#sequence_cache:  AND NVL(B.VALUE,'FALSE')='TRUE'
#sequence_cache:order by a.sequence_owner ,a.SEQUENCE_NAME;
#snapsetting:set lines 400
#snapsetting:set pages 1000
#snapsetting:set feedback off
#snapsetting:set heading off
#snapsetting:
#snapsetting:select  chr(34)||round((sysdate-(sysdate- TO_DSINTERVAL(SNAP_INTERVAL)))*86400/60,0) ||chr(34)||','||
#snapsetting:        chr(34)||round((sysdate-(sysdate- TO_DSINTERVAL(retention)))*86400/60/60/24,0) ||chr(34)
#snapsetting:from dba_hist_wr_control;
#snapsetting12c:set lines 400
#snapsetting12c:set pages 1000
#snapsetting12c:set feedback off
#snapsetting12c:set heading off
#snapsetting12c:
#snapsetting12c:select  chr(34)||nvl(b.name,'CDB$ROOT') ||chr(34)||','||
#snapsetting12c:        chr(34)||round((sysdate-(sysdate- TO_DSINTERVAL(SNAP_INTERVAL)))*86400/60,0) ||chr(34)||','||
#snapsetting12c:        chr(34)||round((sysdate-(sysdate- TO_DSINTERVAL(retention)))*86400/60/60/24,0) ||chr(34)
#snapsetting12c:from containers(dba_hist_wr_control) a,v$pdbs b
#snapsetting12c:where a.con_id = b.con_id(+) ;
#spfile_warning:
#spfile_warning:SET LINES 200
#spfile_warning:SET PAGES 0
#spfile_warning:SET FEEDBACK OFF
#spfile_warning:select chr(34)||inst_id||chr(34)||','||
#spfile_warning:       chr(34)||sid||chr(34)||','||
#spfile_warning:       chr(34)||name||chr(34)||','||
#spfile_warning:       chr(34)||value||chr(34)||','||
#spfile_warning:       chr(34)||warning||chr(34)
#spfile_warning:from (
#spfile_warning:select inst_id, sid,name,value,
#spfile_warning:       case (select count(*) 
#spfile_warning:               from gv$parameter b 
#spfile_warning:               where a.inst_id = b.inst_id 
#spfile_warning:                 and a.name = b.name ) 
#spfile_warning:       when 1 then 'NO' ELSE 'YES' END AS WARNING
#spfile_warning:from gv$spparameter a
#spfile_warning:where value is not null
#spfile_warning:  and name not in ('undo_tablespace','instance_number','thread')
#spfile_warning:order by 1,3,2)
#spfile_warning:where warning ='YES'
#spfile_warning:order by inst_id,name,sid;
#spfile_warning:
#spfile_warning:
#stats_job_running:set lines 400
#stats_job_running:set pages 1000
#stats_job_running:set feedback off
#stats_job_running:set heading off
#stats_job_running:
#stats_job_running:
#stats_job_running:select chr(34) || to_char(b.job_start_time,'yyyy-mm-dd hh24:mi:ss') ||chr(34)||','||
#stats_job_running:       chr(34) || b.job_status  ||chr(34)||','||
#stats_job_running:       chr(34) || to_char(b.JOB_DURATION) ||chr(34)
#stats_job_running: from dba_autotask_task        a,
#stats_job_running:      dba_autotask_job_history b
#stats_job_running:where a.client_name=b.client_name
#stats_job_running:and   a.client_name='auto optimizer stats collection'
#stats_job_running:and   b.job_start_time >= sysdate-7
#stats_job_running:order by 1;
#stats_job_running:
#sysdba:
#sysdba:set lines 400
#sysdba:set pages 1000
#sysdba:set heading off
#sysdba:set feedback off
#sysdba:     
#sysdba:select chr(34)||username ||chr(34)||','||
#sysdba:       chr(34)||sysdba ||chr(34)||','||
#sysdba:       chr(34)||sysoper ||chr(34)||','||
#sysdba:       chr(34)||case when (username NOT in ( 'SYS','SYSBACKUP','SYSDG','SYSKM') and (sysdba  = 'TRUE' or sysoper  = 'TRUE')) then 'YES' else 'NO' end ||chr(34)
#sysdba:from v$pwfile_users 
#sysdba:order by 1
#sysdba:;
#sysdba:
#sysdba:
#sysdba:
#tbscheck:set lines 200
#tbscheck:set pages 1000
#tbscheck:col tbsname format a30
#tbscheck:set heading off
#tbscheck:set feedback off
#tbscheck:select chr(34)||a.tablespace_name                                                                     ||chr(34)||','|| 
#tbscheck:       chr(34)||c.bigfile                                                                             ||chr(34)||','||  
#tbscheck:       chr(34)||a.count_file                                                                          ||chr(34)||','|| 
#tbscheck:       chr(34)||nvl(trunc((1-b.free/a.total)*100),100)                                                ||chr(34)||','|| 
#tbscheck:	     chr(34)||nvl(trunc(((a.total-b.free)/decode(a.extent_total,0,a.total,a.extent_total))*100),100)||chr(34)||','|| 
#tbscheck:       chr(34)||nvl(trunc(a.total),0)                                                                 ||chr(34)||','|| 
#tbscheck:	     chr(34)||nvl(trunc(a.total-b.free), 0)                                                         ||chr(34)||','|| 
#tbscheck:       chr(34)||nvl(trunc(b.free),0)                                                                  ||chr(34)||','||  
#tbscheck:	     chr(34)||nvl(trunc(a.extent_total),0)                                                          ||chr(34)||','|| 
#tbscheck:	     chr(34)||nvl(trunc(max_fragment_mb),0)                                                         ||chr(34)||','||  
#tbscheck:	     chr(34)||nvl(trunc(b.fsfi),0)                                                                  ||chr(34)||','|| 
#tbscheck:	     chr(34)||case when a.extent_able=1 then 'YES' when a.extent_able=0 then 'NO' else 'MIXED' end  ||chr(34)
#tbscheck:  from (select a.tablespace_name, 
#tbscheck:               trunc(sum(nvl(a.bytes,0))/1024/1024) total,
#tbscheck:			         trunc(sum(decode(a.autoextensible,'YES',greatest(decode(maxbytes,0,bytes,maxbytes),bytes),'NO',BYTES))/1024/1024) extent_total,
#tbscheck:			         avg(decode(a.autoextensible,'YES',1,'NO',0)) extent_able,
#tbscheck:			   count(a.file_name) count_file
#tbscheck:          from dba_data_files a,dba_tablespaces b
#tbscheck:          where a.tablespace_name = b.tablespace_name
#tbscheck:         group by a.tablespace_name) a,
#tbscheck:       (select tablespace_name, 
#tbscheck:               trunc(sum(nvl(bytes,0))/1024/1024) free, 
#tbscheck:               trunc(max(BYTES/1024/1024)) max_fragment_mb,
#tbscheck:	             round(sqrt(max(blocks) / sum(blocks)) * (100 / sqrt(sqrt(count(blocks)))),2) fsfi
#tbscheck:          from dba_free_space
#tbscheck:         group by tablespace_name) b,
#tbscheck:        dba_tablespaces c
#tbscheck: where c.tablespace_name = a.tablespace_name
#tbscheck:   and c.tablespace_name = b.tablespace_name(+)
#tbscheck: order by 1;
#tbscheck:
#tbscheck:
#tbscheck:
#tbscheck12c:set lines 200
#tbscheck12c:set pages 1000
#tbscheck12c:col tbsname format a30
#tbscheck12c:set heading off
#tbscheck12c:set feedback off
#tbscheck12c:select chr(34)||NVL(d.name,'CDB$ROOT')||chr(34)||','|| 
#tbscheck12c:       chr(34)||a.tablespace_name||chr(34)||','|| 
#tbscheck12c:       chr(34)||c.bigfile||chr(34)||','||  
#tbscheck12c:       chr(34)||a.count_file||chr(34)||','|| 
#tbscheck12c:       chr(34)||nvl(trunc((1-b.free/a.total)*100),100)||chr(34)||','|| 
#tbscheck12c:	     chr(34)||nvl(trunc(((a.total-b.free)/decode(a.extent_total,0,a.total,a.extent_total))*100),100)||chr(34)||','|| 
#tbscheck12c:       chr(34)||nvl(trunc(a.total),0)||chr(34)||','|| 
#tbscheck12c:	     chr(34)||nvl(trunc(a.total-b.free), 0)||chr(34)||','|| 
#tbscheck12c:       chr(34)||nvl(trunc(b.free),0)||chr(34)||','||  
#tbscheck12c:	     chr(34)||nvl(trunc(a.extent_total),0)||chr(34)||','|| 
#tbscheck12c:	     chr(34)||nvl(trunc(max_fragment_mb),0)||chr(34)||','||  
#tbscheck12c:	     chr(34)||nvl(trunc(b.fsfi),0)||chr(34)||','|| 
#tbscheck12c:	     chr(34)||case when a.extent_able=1 then 'YES' when a.extent_able=0 then 'NO' else 'MIXED' end ||chr(34)
#tbscheck12c:  from (select a.con_id,
#tbscheck12c:               a.tablespace_name, 
#tbscheck12c:               sum(nvl(a.bytes,0))/1024/1024 total,
#tbscheck12c:			         trunc(sum(decode(a.autoextensible,'YES',greatest(maxbytes,bytes),'NO',BYTES))/1024/1024) extent_total,
#tbscheck12c:			         avg(decode(a.autoextensible,'YES',1,'NO',0)) extent_able,
#tbscheck12c:			         count(a.file_name) count_file
#tbscheck12c:          from containers(dba_data_files) a
#tbscheck12c:         group by a.con_id,a.tablespace_name) a,
#tbscheck12c:       (select a.con_id ,
#tbscheck12c:               a.tablespace_name, 
#tbscheck12c:               sum(nvl(a.bytes,0))/1024/1024 free, 
#tbscheck12c:               max(a.BYTES/1024/1024) max_fragment_mb,
#tbscheck12c:	             round(sqrt(max(a.blocks) / sum(a.blocks)) * (100 / sqrt(sqrt(count(blocks)))),2) fsfi
#tbscheck12c:          from containers(dba_free_space) a
#tbscheck12c:         group by a.tablespace_name,a.con_id) b,
#tbscheck12c:       cdb_tablespaces c,v$pdbs d
#tbscheck12c: where a.tablespace_name = c.tablespace_name
#tbscheck12c:   and a.con_id = d.con_id(+)
#tbscheck12c:   and a.con_id = c.con_id(+)
#tbscheck12c:   and a.con_id = b.con_id(+)
#tbscheck12c:   and c.tablespace_name = b.tablespace_name(+)
#tbscheck12c: order by A.con_id,c.tablespace_name;
#tbscheck12c:
#tbscheck12c:
#tbscheck12c:
#tbs_fragement_pct:
#tbs_fragement_pct:set lines 200
#tbs_fragement_pct:set pages 200
#tbs_fragement_pct:set feedback off
#tbs_fragement_pct:set heading off
#tbs_fragement_pct:
#tbs_fragement_pct:select chr(34)||a.tablespace_name||chr(34)||','|| 
#tbs_fragement_pct:       chr(34)||trunc(sqrt(max(blocks)/sum(blocks))* (100/sqrt(sqrt(count(blocks)))),0) ||chr(34)  
#tbs_fragement_pct:from dba_free_space a,
#tbs_fragement_pct:     dba_tablespaces b 
#tbs_fragement_pct:where a.tablespace_name=b.tablespace_name 
#tbs_fragement_pct:  and b.contents not in('TEMPORARY','UNDO','SYSAUX') 
#tbs_fragement_pct:group by A.tablespace_name 
#tbs_fragement_pct:; 
#tbs_fragement_pct:
#tbs_fragement_pct:
#tbs_fragement_pct:
#timezone:
#timezone:set line 200
#timezone:set heading off
#timezone:set feedback off
#timezone:select chr(34)||'DB_time_zone'||chr(34)||','||chr(34)||dbtimezone||chr(34) from dual;
#timezone:
#timezone:
#topevent:
#topevent:
#topevent:set lines 400
#topevent:set pages 1000
#topevent:set feedback off
#topevent:set serverout on
#topevent:declare
#topevent:vevent varchar2(100);  
#topevent:vtime number;
#topevent:vavgtime number;
#topevent:vpctwt number;
#topevent:vwaits number;
#topevent:vwaitclass varchar2(100);
#topevent:vbid number ;
#topevent:veid number ;
#topevent:vdbid number ;
#topevent:vinid number ;
#topevent:startid number;
#topevent:endid number;
#topevent:vstarttime varchar2(200);
#topevent:vendtime varchar2(200);
#topevent:vdbname varchar2(36);
#topevent:v_inst_startup date;
#topevent:begin 
#topevent:select instance_number,STARTUP_TIME into vinid ,v_inst_startup from v$instance;
#topevent:select dbid into vdbid from v$database;
#topevent:
#topevent:--
#topevent:     begin
#topevent:         select min(snap_id),max(snap_id) into vbid,veid
#topevent:         from dba_hist_snapshot
#topevent:         where END_INTERVAL_TIME between  sysdate - 3/24 
#topevent:                                     and  sysdate
#topevent:           and END_INTERVAL_TIME > = v_inst_startup
#topevent:           and instance_number = vinid
#topevent:           and dbid = vdbid;
#topevent:     exception when no_data_found then
#topevent:         select min(snap_id),max(snap_id) into vbid,veid
#topevent:         from dba_hist_snapshot
#topevent:         where END_INTERVAL_TIME between  sysdate -1
#topevent:                                     and  sysdate -1 - 3/24
#topevent:           and END_INTERVAL_TIME > = v_inst_startup
#topevent:           and instance_number = vinid
#topevent:           and dbid = vdbid;
#topevent:     end;
#topevent:     
#topevent:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vstarttime from dba_hist_snapshot a where snap_id=vbid and instance_number=vinid;
#topevent:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vendtime from dba_hist_snapshot a where snap_id=veid and instance_number=vinid;
#topevent:for c1 in (
#topevent:SELECT EVENT,
#topevent:       WAITS,
#topevent:       round(TIME,0) tm,
#topevent:       round(DECODE(WAITS,
#topevent:              NULL,
#topevent:              TO_NUMBER(NULL),
#topevent:              0,
#topevent:              TO_NUMBER(NULL),
#topevent:              TIME / WAITS * 1000),0) AVGWT,
#topevent:       round(PCTWTT,2) PCTWTT,
#topevent:       WAIT_CLASS
#topevent:  FROM (SELECT EVENT, WAITS, TIME, PCTWTT, WAIT_CLASS
#topevent:          FROM (SELECT E.EVENT_NAME EVENT,
#topevent:                       E.TOTAL_WAITS_FG - NVL(B.TOTAL_WAITS_FG, 0) WAITS,
#topevent:                       (E.TIME_WAITED_MICRO_FG - NVL(B.TIME_WAITED_MICRO_FG, 0)) /
#topevent:                       1000000 TIME,
#topevent:                       100 *
#topevent:                       (E.TIME_WAITED_MICRO_FG - NVL(B.TIME_WAITED_MICRO_FG, 0)) /
#topevent:                       ((SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent:                          WHERE e.SNAP_ID = veid
#topevent:                            AND e.INSTANCE_NUMBER = vinid
#topevent:                            AND e.STAT_NAME = 'DB time') -
#topevent:                       (SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent:                          WHERE b.SNAP_ID = vbid
#topevent:                            AND b.INSTANCE_NUMBER = vinid
#topevent:                            AND b.STAT_NAME = 'DB time')) PCTWTT,
#topevent:                       E.WAIT_CLASS WAIT_CLASS
#topevent:                  FROM DBA_HIST_SYSTEM_EVENT B, DBA_HIST_SYSTEM_EVENT E
#topevent:                 WHERE B.SNAP_ID(+) = vbid
#topevent:                   AND E.SNAP_ID = veid
#topevent:                   AND B.INSTANCE_NUMBER(+) = vinid
#topevent:                   AND E.INSTANCE_NUMBER = vinid
#topevent:                   AND B.EVENT_ID(+) = E.EVENT_ID
#topevent:                   AND E.TOTAL_WAITS > NVL(B.TOTAL_WAITS, 0)
#topevent:                   AND E.WAIT_CLASS != 'Idle'
#topevent:                UNION ALL
#topevent:                SELECT 'CPU time' EVENT,
#topevent:                       TO_NUMBER(NULL) WAITS,
#topevent:                       ((SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent:                          WHERE e.SNAP_ID = veid
#topevent:                            AND e.INSTANCE_NUMBER = vinid
#topevent:                            AND e.STAT_NAME = 'DB CPU') -
#topevent:                       (SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent:                          WHERE b.SNAP_ID = vbid
#topevent:                            AND b.INSTANCE_NUMBER = vinid
#topevent:                            AND b.STAT_NAME = 'DB CPU')) / 1000000 TIME,
#topevent:                       100 * ((SELECT sum(value)
#topevent:                                 FROM DBA_HIST_SYS_TIME_MODEL e
#topevent:                                WHERE e.SNAP_ID = veid
#topevent:                                  AND e.INSTANCE_NUMBER = vinid
#topevent:                                  AND e.STAT_NAME = 'DB CPU') -
#topevent:                       (SELECT sum(value)
#topevent:                                 FROM DBA_HIST_SYS_TIME_MODEL b
#topevent:                                WHERE b.SNAP_ID = vbid
#topevent:                                  AND b.INSTANCE_NUMBER = vinid
#topevent:                                  AND b.STAT_NAME = 'DB CPU')) /
#topevent:                       ((SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent:                          WHERE e.SNAP_ID = veid
#topevent:                            AND e.INSTANCE_NUMBER = vinid
#topevent:                            AND e.STAT_NAME = 'DB time') -
#topevent:                       (SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent:                          WHERE b.SNAP_ID = vbid
#topevent:                            AND b.INSTANCE_NUMBER = vinid
#topevent:                            AND b.STAT_NAME = 'DB time')) PCTWTT,
#topevent:                       NULL WAIT_CLASS
#topevent:                  from dual
#topevent:                 WHERE ((SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent:                          WHERE e.SNAP_ID = veid
#topevent:                            AND e.INSTANCE_NUMBER = vinid
#topevent:                            AND e.STAT_NAME = 'DB CPU') -
#topevent:                       (SELECT sum(value)
#topevent:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent:                          WHERE b.SNAP_ID = vbid
#topevent:                            AND b.INSTANCE_NUMBER = vinid
#topevent:                            AND b.STAT_NAME = 'DB CPU')) > 0)
#topevent:         ORDER BY TIME DESC, WAITS DESC)
#topevent: WHERE ROWNUM <= 5) loop
#topevent:  dbms_output.put_line(vstarttime||','||vendtime||','||
#topevent:                           chr(34)||c1.EVENT||chr(34)||','||
#topevent:                           chr(34)|| nvl(to_char(c1.WAITS),'---')||chr(34)||','||
#topevent:                           chr(34)|| nvl(to_char(c1.Tm),'---')||chr(34)||','||
#topevent:                           chr(34)|| nvl(to_char(c1.AVGWT),'---')||chr(34)||','||
#topevent:                           chr(34)|| nvl(to_char(c1.PCTWTT),'---')||chr(34)||','||
#topevent:                           chr(34)|| nvl(to_char(c1.WAIT_CLASS),'---')||chr(34));
#topevent:end loop;    
#topevent:     
#topevent:end;
#topevent:/
#topevent:
#topevent:
#topevent:
#topevent:
#topevent:
#topevent:
#topevent10g:
#topevent10g:
#topevent10g:
#topevent10g:set lines 400
#topevent10g:set pages 1000
#topevent10g:set feedback off
#topevent10g:set serverout on
#topevent10g:declare
#topevent10g:vevent varchar2(100);  
#topevent10g:vtime number;
#topevent10g:vavgtime number;
#topevent10g:vpctwt number;
#topevent10g:vwaits number;
#topevent10g:vwaitclass varchar2(100);
#topevent10g:vbid number ;
#topevent10g:veid number ;
#topevent10g:vdbid number ;
#topevent10g:vinid number ;
#topevent10g:startid number;
#topevent10g:endid number;
#topevent10g:vstarttime varchar2(200);
#topevent10g:vendtime varchar2(200);
#topevent10g:vdbname varchar2(36);
#topevent10g:v_inst_startup date;
#topevent10g:begin 
#topevent10g:select instance_number,STARTUP_TIME into vinid ,v_inst_startup from v$instance;
#topevent10g:select dbid into vdbid from v$database;
#topevent10g:
#topevent10g:--
#topevent10g:     begin
#topevent10g:         select min(snap_id),max(snap_id) into vbid,veid
#topevent10g:         from dba_hist_snapshot
#topevent10g:         where END_INTERVAL_TIME between  sysdate - 3/24 
#topevent10g:                                     and  sysdate
#topevent10g:           and END_INTERVAL_TIME > = v_inst_startup
#topevent10g:           and instance_number = vinid
#topevent10g:           and dbid = vdbid;
#topevent10g:     exception when no_data_found then
#topevent10g:         select min(snap_id),max(snap_id) into vbid,veid
#topevent10g:         from dba_hist_snapshot
#topevent10g:         where END_INTERVAL_TIME between  sysdate -1
#topevent10g:                                     and  sysdate -1 - 3/24
#topevent10g:           and END_INTERVAL_TIME > = v_inst_startup
#topevent10g:           and instance_number = vinid
#topevent10g:           and dbid = vdbid;
#topevent10g:     end;
#topevent10g:     
#topevent10g:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vstarttime from dba_hist_snapshot a where snap_id=vbid and instance_number=vinid;
#topevent10g:     select chr(34)||to_char(a.end_interval_time,'yyyy-mm-dd hh24:mi')||chr(34) into vendtime from dba_hist_snapshot a where snap_id=veid and instance_number=vinid;
#topevent10g:for c1 in (
#topevent10g:SELECT EVENT,
#topevent10g:       WAITS,
#topevent10g:       round(TIME,0) tm,
#topevent10g:       round(DECODE(WAITS,
#topevent10g:              NULL,
#topevent10g:              TO_NUMBER(NULL),
#topevent10g:              0,
#topevent10g:              TO_NUMBER(NULL),
#topevent10g:              TIME / WAITS * 1000),0) AVGWT,
#topevent10g:       round(PCTWTT,2) PCTWTT,
#topevent10g:       WAIT_CLASS
#topevent10g:  FROM (SELECT EVENT, WAITS, TIME, PCTWTT, WAIT_CLASS
#topevent10g:          FROM (SELECT E.EVENT_NAME EVENT,
#topevent10g:                       E.TOTAL_WAITS - NVL(B.TOTAL_WAITS, 0) WAITS,
#topevent10g:                       (E.TIME_WAITED_MICRO - NVL(B.TIME_WAITED_MICRO, 0)) /
#topevent10g:                       1000000 TIME,
#topevent10g:                       100 *
#topevent10g:                       (E.TIME_WAITED_MICRO - NVL(B.TIME_WAITED_MICRO, 0)) /
#topevent10g:                       ((SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent10g:                          WHERE e.SNAP_ID = veid
#topevent10g:                            AND e.INSTANCE_NUMBER = vinid
#topevent10g:                            AND e.STAT_NAME = 'DB time') -
#topevent10g:                       (SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent10g:                          WHERE b.SNAP_ID = vbid
#topevent10g:                            AND b.INSTANCE_NUMBER = vinid
#topevent10g:                            AND b.STAT_NAME = 'DB time')) PCTWTT,
#topevent10g:                       E.WAIT_CLASS WAIT_CLASS
#topevent10g:                  FROM DBA_HIST_SYSTEM_EVENT B, DBA_HIST_SYSTEM_EVENT E
#topevent10g:                 WHERE B.SNAP_ID(+) = vbid
#topevent10g:                   AND E.SNAP_ID = veid
#topevent10g:                   AND B.INSTANCE_NUMBER(+) = vinid
#topevent10g:                   AND E.INSTANCE_NUMBER = vinid
#topevent10g:                   AND B.EVENT_ID(+) = E.EVENT_ID
#topevent10g:                   AND E.TOTAL_WAITS > NVL(B.TOTAL_WAITS, 0)
#topevent10g:                   AND E.WAIT_CLASS != 'Idle'
#topevent10g:                UNION ALL
#topevent10g:                SELECT 'CPU time' EVENT,
#topevent10g:                       TO_NUMBER(NULL) WAITS,
#topevent10g:                       ((SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent10g:                          WHERE e.SNAP_ID = veid
#topevent10g:                            AND e.INSTANCE_NUMBER = vinid
#topevent10g:                            AND e.STAT_NAME = 'DB CPU') -
#topevent10g:                       (SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent10g:                          WHERE b.SNAP_ID = vbid
#topevent10g:                            AND b.INSTANCE_NUMBER = vinid
#topevent10g:                            AND b.STAT_NAME = 'DB CPU')) / 1000000 TIME,
#topevent10g:                       100 * ((SELECT sum(value)
#topevent10g:                                 FROM DBA_HIST_SYS_TIME_MODEL e
#topevent10g:                                WHERE e.SNAP_ID = veid
#topevent10g:                                  AND e.INSTANCE_NUMBER = vinid
#topevent10g:                                  AND e.STAT_NAME = 'DB CPU') -
#topevent10g:                       (SELECT sum(value)
#topevent10g:                                 FROM DBA_HIST_SYS_TIME_MODEL b
#topevent10g:                                WHERE b.SNAP_ID = vbid
#topevent10g:                                  AND b.INSTANCE_NUMBER = vinid
#topevent10g:                                  AND b.STAT_NAME = 'DB CPU')) /
#topevent10g:                       ((SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent10g:                          WHERE e.SNAP_ID = veid
#topevent10g:                            AND e.INSTANCE_NUMBER = vinid
#topevent10g:                            AND e.STAT_NAME = 'DB time') -
#topevent10g:                       (SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent10g:                          WHERE b.SNAP_ID = vbid
#topevent10g:                            AND b.INSTANCE_NUMBER = vinid
#topevent10g:                            AND b.STAT_NAME = 'DB time')) PCTWTT,
#topevent10g:                       NULL WAIT_CLASS
#topevent10g:                  from dual
#topevent10g:                 WHERE ((SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL e
#topevent10g:                          WHERE e.SNAP_ID = veid
#topevent10g:                            AND e.INSTANCE_NUMBER = vinid
#topevent10g:                            AND e.STAT_NAME = 'DB CPU') -
#topevent10g:                       (SELECT sum(value)
#topevent10g:                           FROM DBA_HIST_SYS_TIME_MODEL b
#topevent10g:                          WHERE b.SNAP_ID = vbid
#topevent10g:                            AND b.INSTANCE_NUMBER = vinid
#topevent10g:                            AND b.STAT_NAME = 'DB CPU')) > 0)
#topevent10g:         ORDER BY TIME DESC, WAITS DESC)
#topevent10g: WHERE ROWNUM <= 5) loop
#topevent10g:  dbms_output.put_line(vstarttime||','||vendtime||','||
#topevent10g:                           chr(34)||c1.EVENT||chr(34)||','||
#topevent10g:                           chr(34)|| nvl(to_char(c1.WAITS),'---')||chr(34)||','||
#topevent10g:                           chr(34)|| nvl(to_char(c1.Tm),'---')||chr(34)||','||
#topevent10g:                           chr(34)|| nvl(to_char(c1.AVGWT),'---')||chr(34)||','||
#topevent10g:                           chr(34)|| nvl(to_char(c1.PCTWTT),'---')||chr(34)||','||
#topevent10g:                           chr(34)|| nvl(to_char(c1.WAIT_CLASS),'---')||chr(34));
#topevent10g:end loop;    
#topevent10g:     
#topevent10g:end;
#topevent10g:/
#topevent10g:
#topevent10g:
#topevent10g:
#topevent10g:
#topevent10g:
#topevent10g:
#topevent10g:
#unified_audit:set lines 200
#unified_audit:set pages 1000
#unified_audit:set heading off
#unified_audit:set feedback off
#unified_audit:
#unified_audit:SELECT  CHR(34)||A.PARAMETER||CHR(34)||','||
#unified_audit:       CHR(34)||A.VALUE||CHR(34)
#unified_audit:FROM V$OPTION A
#unified_audit:WHERE A.PARAMETER = 'Unified Auditing'
#unified_audit:; 
#unified_audit:
#unified_audit:
#unified_audit_12c:
#unified_audit_12c:set lines 200
#unified_audit_12c:set pages 1000
#unified_audit_12c:set heading off
#unified_audit_12c:set feedback off
#unified_audit_12c:
#unified_audit_12c:SELECT CHR(34)||NVL(B.name,'CDB$ROOT')||CHR(34)||','||
#unified_audit_12c:       CHR(34)||A.PARAMETER||CHR(34)||','||
#unified_audit_12c:       CHR(34)||A.VALUE||CHR(34)
#unified_audit_12c:FROM V$OPTION A,
#unified_audit_12c:     V$PDBS B
#unified_audit_12c:WHERE A.PARAMETER = 'Unified Auditing'
#unified_audit_12c:  AND A.CON_ID = B.CON_ID(+)
#unified_audit_12c:ORDER BY A.CON_ID; 
#unified_audit_12c:
#unified_audit_12c:
#unified_audit_option:
#unified_audit_option:set lines 200
#unified_audit_option:set pages 1000
#unified_audit_option:set heading off
#unified_audit_option:set feedback off
#unified_audit_option:
#unified_audit_option:SELECT chr(34)||PARAMETER_NAME||chr(34)||','||
#unified_audit_option:       chr(34)||PARAMETER_VALUE||chr(34)
#unified_audit_option:FROM   DBA_AUDIT_MGMT_CONFIG_PARAMS 
#unified_audit_option:where audit_trail = 'UNIFIED AUDIT TRAIL';
#unified_audit_option:
#unified_audit_option:
#unified_audit_purge:
#unified_audit_purge:set lines 200
#unified_audit_purge:set pages 1000
#unified_audit_purge:set feedback off
#unified_audit_purge:set heading off
#unified_audit_purge:
#unified_audit_purge:select chr(34)||trim(JOB_NAME)                   ||chr(34)||','||
#unified_audit_purge:       chr(34)||trim(JOB_STATUS)                 ||chr(34)||','||
#unified_audit_purge:       chr(34)||trim(AUDIT_TRAIL)                ||chr(34)||','||
#unified_audit_purge:       chr(34)||trim(JOB_FREQUENCY)	             ||chr(34)||','||
#unified_audit_purge:       chr(34)||trim(USE_LAST_ARCHIVE_TIMESTAMP) ||chr(34)||','||
#unified_audit_purge:       chr(34)||trim(JOB_CONTAINER)	             ||chr(34)
#unified_audit_purge:from   DBA_AUDIT_MGMT_CLEANUP_JOBS;
#unified_audit_purge:
#unified_audit_purge:
#userinfo:set lines 400
#userinfo:set pages 1000
#userinfo:set feedback off
#userinfo:set heading off
#userinfo:select chr(34)||username||chr(34)||','||
#userinfo:       chr(34)||default_tablespace||chr(34)||','||
#userinfo:       chr(34)||temporary_tablespace||chr(34)||','||
#userinfo:       chr(34)||to_char(created,'yyyymmdd')||chr(34) ||','||
#userinfo:       chr(34)||nvl(to_char(LOCK_DATE,'yyyymmdd'),'---')||chr(34) ||','||  
#userinfo:       chr(34)||nvl(to_char(EXPIRY_DATE,'yyyymmdd'),'---')||chr(34) ||','||
#userinfo:       chr(34)||profile||chr(34)||','||
#userinfo:       chr(34)||account_status||chr(34) ||','||
#userinfo:       chr(34)||case when username <> 'SYS' AND USERNAME <> 'SYSTEM' AND TRUNC(NVL(EXPIRY_DATE,TO_DATE('20991231 00:00:00','YYYYMMDD HH24:MI:SS')) -SYSDATE) < 91 THEN 'YES' ELSE 'NO' END ||chr(34)
#userinfo:from dba_users
#userinfo:where account_status = 'OPEN'
#userinfo:order by created;
#userinfo:       
#userinfo:
#userinfo:
#userinfo12c:set lines 400
#userinfo12c:set pages 1000
#userinfo12c:set feedback off
#userinfo12c:set heading off
#userinfo12c:select chr(34)||nvl(b.name,'CDB$ROOT')||chr(34)||','||
#userinfo12c:       chr(34)||username||chr(34)||','||
#userinfo12c:       chr(34)||default_tablespace||chr(34)||','||
#userinfo12c:       chr(34)||temporary_tablespace||chr(34)||','||
#userinfo12c:       chr(34)||to_char(created,'yyyymmdd')||chr(34) ||','||
#userinfo12c:       chr(34)||nvl(to_char(LOCK_DATE,'yyyymmdd'),'---')||chr(34) ||','||  
#userinfo12c:       chr(34)||nvl(to_char(EXPIRY_DATE,'yyyymmdd'),'---')||chr(34) ||','||
#userinfo12c:       chr(34)||profile||chr(34)||','||
#userinfo12c:       chr(34)||account_status||chr(34) ||','||
#userinfo12c:       chr(34)||case when username <> 'SYS' AND USERNAME <> 'SYSTEM' AND TRUNC(NVL(EXPIRY_DATE,TO_DATE('20991231 00:00:00','YYYYMMDD HH24:MI:SS')) -SYSDATE) < 91 THEN 'YES' ELSE 'NO' END ||chr(34)
#userinfo12c:from containers(dba_users) a,
#userinfo12c:     v$pdbs b
#userinfo12c:where account_status = 'OPEN'
#userinfo12c:  and a.con_id = b.con_id(+)
#userinfo12c:order by created;
#userinfo12c:       
#userinfo12c:
#userinfo12c:
#userpriv:
#userpriv:set lines 400
#userpriv:set pages 1000
#userpriv:set heading off
#userpriv:set feedback off
#userpriv:col username format a24
#userpriv:col granted_role format a24
#userpriv:col  admin_option format a18
#userpriv:col  default_role format a18 
#userpriv:col warning format a18
#userpriv:select chr(34)||b.username ||chr(34)||','||
#userpriv:       chr(34)||a.granted_role||chr(34)||','||
#userpriv:       chr(34)||a.admin_option ||chr(34)||','|| 
#userpriv:       chr(34)||a.default_role ||chr(34)||','||
#userpriv:       chr(34)||case when (b.username <> 'SYS' and b.USERNAME <> 'SYSTEM') then 'YES' else  'NO' END ||chr(34)
#userpriv: from dba_role_privs a ,
#userpriv:      dba_users b 
#userpriv:where b.username=a.grantee  AND 
#userpriv:		  b.account_status='OPEN'  AND
#userpriv:		  a.granted_role in ('DBA','SYSDBA','SYSOPER','EXP_FULL_DATABASE','DELETE_CATALOG_ROLE','IMP_FULL_DATABASE') 
#userpriv:      order by a.granted_role;
#userpriv:
#userpriv12c:
#userpriv12c:set lines 400
#userpriv12c:set pages 1000
#userpriv12c:set heading off
#userpriv12c:set feedback off
#userpriv12c:col username format a24
#userpriv12c:col granted_role format a24
#userpriv12c:col  admin_option format a18
#userpriv12c:col  default_role format a18 
#userpriv12c:col warning format a18
#userpriv12c:select chr(34)||nvl(c.name,'CDB$ROOT') ||chr(34)||','||
#userpriv12c:       chr(34)||b.username ||chr(34)||','||
#userpriv12c:       chr(34)||a.granted_role||chr(34)||','||
#userpriv12c:       chr(34)||a.admin_option ||chr(34)||','|| 
#userpriv12c:       chr(34)||a.default_role ||chr(34)||','||
#userpriv12c:       chr(34)||case when (b.username <> 'SYS' and b.USERNAME <> 'SYSTEM') then 'YES' else  'NO' END ||chr(34)
#userpriv12c: from containers(dba_role_privs) a ,
#userpriv12c:      containers(dba_users) b ,v$pdbs c
#userpriv12c:where b.username=a.grantee  AND 
#userpriv12c:		  b.account_status='OPEN'  AND
#userpriv12c:		  a.con_id = b.con_id and
#userpriv12c:		  a.con_id = c.con_id(+) and
#userpriv12c:		  a.granted_role in ('DBA','SYSDBA','SYSOPER','EXP_FULL_DATABASE','DELETE_CATALOG_ROLE','IMP_FULL_DATABASE') 
#userpriv12c:      order by C.CON_ID,a.granted_role;
#userpriv12c:
#version:set pagesize 0 linesize 200 echo off feedback off
#version:SELECT
#version:				DBID||'||'||
#version:				NAME||'||'||
#version:               (select VERSION from v$INSTANCE where rownum=1) ||'||'||
#version:               (SELECT value FROM gv$parameter WHERE name='cluster_database' AND rownum=1) ||'||'||
#version:				CREATED||'||'||
#version:				RESETLOGS_CHANGE#||'||'||
#version:				RESETLOGS_TIME||'||'||
#version:				LOG_MODE||'||'||
#version:				CHECKPOINT_CHANGE#||'||'||
#version:				OPEN_MODE||'||'||
#version:				PROTECTION_MODE||'||'||
#version:				PROTECTION_LEVEL||'||'||
#version:				DATABASE_ROLE||'||'||
#version:				FORCE_LOGGING||'||'||
#version:				PLATFORM_ID||'||'||
#version:				PLATFORM_NAME||'||'||
#version:				FLASHBACK_ON
#version:FROM V$DATABASE;
#version:
#dgdelay:set  lines 400
#dgdelay:set  pages 1000
#dgdelay:set  feedback off
#dgdelay:set heading off   
#dgdelay:
#dgdelay:SELECT chr(34)||v.process       ||chr(34)||','||
#dgdelay:       chr(34)||v.status        ||chr(34)||','||
#dgdelay:       chr(34)||v.group#        ||chr(34)||','||
#dgdelay:       chr(34)||v.thread#       ||chr(34)||','||
#dgdelay:       chr(34)||v.sequence#     ||chr(34)||','||
#dgdelay:       chr(34)||v.delay_mins    ||chr(34)||','||
#dgdelay:       chr(34)||case when v.delay_mins > 5 then 'YES' else 'NO' end || chr(34)
#dgdelay:  FROM (select process,pid,status,client_process,client_pid,group#,resetlog_id,
#dgdelay:               thread#,sequence#,block#,blocks,delay_mins,known_agents,active_agents from v$managed_standby order by process,group#) v;
#dgdelay:
#disk_same_size:col name format a20
#disk_same_size:set heading off
#disk_same_size:set feedback off
#disk_same_size:
#disk_same_size:select chr(34)||name               ||chr(34)||','||
#disk_same_size:       chr(34)||disk_same_size     ||chr(34)
#disk_same_size:from (
#disk_same_size:select a.group_number,
#disk_same_size:       a.name,
#disk_same_size:       decode(count(distinct b.total_mb),1,'YES','NO') AS disk_same_size
#disk_same_size:from v$asm_diskgroup a,
#disk_same_size:     v$asm_disk b
#disk_same_size:where a.group_number = b.group_number
#disk_same_size:group by a.group_number,a.name
#disk_same_size:)
#disk_same_size:;#diskgroup.sql:set lines 400
#diskgroup:set pages 1000
#diskgroup:col name format a20
#diskgroup:set heading off
#diskgroup:set feedback off
#diskgroup:
#diskgroup:select chr(34)||name               ||chr(34)||','||
#diskgroup:       chr(34)||au_size            ||chr(34)||','||
#diskgroup:       chr(34)||state              ||chr(34)||','||
#diskgroup:       chr(34)||nvl(type ,'Error') ||chr(34)||','||
#diskgroup:       chr(34)||total_disk_sizeMB  ||chr(34)||','||
#diskgroup:       chr(34)||dg_total_mb        ||chr(34)||','||
#diskgroup:       chr(34)||dg_free_mb         ||chr(34)||','||
#diskgroup:       chr(34)||to_char(round((1 - dg_free_mb /dg_total_mb),2) * 100) ||chr(34)||','||
#diskgroup:       chr(34)||OFFLINE_DISKS      ||chr(34)||','||
#diskgroup:       chr(34)||redundancy         ||chr(34)
#diskgroup:from 
#diskgroup:(
#diskgroup:select m.group_number,
#diskgroup:       m.name,
#diskgroup:       m.ALLOCATION_UNIT_SIZE / 1024 /1024 as au_size,
#diskgroup:       m.type,
#diskgroup:       m.state,
#diskgroup:       m.OFFLINE_DISKS,
#diskgroup:       decode(m.type,'EXTERN',1,'NORMAL',2,3) as redundancy,
#diskgroup:       m.total_mb as total_disk_sizeMB ,
#diskgroup:       (m.free_mb ) / decode (n.redundancy,0,1,n.redundancy) / decode(m.type,'EXTERN',1,'NORMAL',2,3)  as total_disk_freeMB,
#diskgroup:       (m.total_mb - REQUIRED_MIRROR_FREE_MB) / decode (n.redundancy,0,1,n.redundancy) / decode(m.type,'EXTERN',1,'NORMAL',2,3)  as dg_total_mb,
#diskgroup:       (m.free_mb -  REQUIRED_MIRROR_FREE_MB) / decode (n.redundancy,0,1,n.redundancy) / decode(m.type,'EXTERN',1,'NORMAL',2,3)  as dg_free_mb
#diskgroup:from v$asm_diskgroup m,
#diskgroup:     (select group_number,count(distinct failgroup) as redundancy 
#diskgroup:        from v$asm_disk 
#diskgroup:        where name <> failgroup 
#diskgroup:        group BY group_number
#diskgroup:      union
#diskgroup:       select distinct group_number,0 
#diskgroup:       from v$asm_disk 
#diskgroup:        where name = failgroup
#diskgroup:       ) n
#diskgroup:where m.group_number = N.group_number
#diskgroup:);
#compatible_rdbms:set pages 1000
#compatible_rdbms:col name format a20
#compatible_rdbms:set heading off
#compatible_rdbms:set feedback off
#compatible_rdbms:
#compatible_rdbms:select chr(34)||diskgroup_name    ||chr(34)||','||
#compatible_rdbms:       chr(34)||path              ||chr(34)||','||
#compatible_rdbms:       chr(34)||os_mb             ||chr(34)||','||
#compatible_rdbms:       chr(34)||total_mb          ||chr(34)||','||
#compatible_rdbms:       chr(34)||compatible_asm    ||chr(34)||','||
#compatible_rdbms:       chr(34)||compatible_rdbms  ||chr(34)
#compatible_rdbms:from 
#compatible_rdbms:(
#compatible_rdbms:select g.name diskgroup_name,
#compatible_rdbms:       d.path,
#compatible_rdbms:       d.os_mb,
#compatible_rdbms:	      d.total_mb,
#compatible_rdbms:	      g.COMPATIBILITY compatible_asm,
#compatible_rdbms:	      g.DATABASE_COMPATIBILITY compatible_rdbms 
#compatible_rdbms:from v$asm_diskgroup g,v$asm_disk d 
#compatible_rdbms:where g.group_number = d.group_number and (d.os_mb>=2000000 or d.total_mb>=2000000) and #compatible_rdbms:g.COMPATIBILITY>='12.1.0.0.0' and g.DATABASE_COMPATIBILITY<'12.1.0.0.0' 
#compatible_rdbms:order by g.name,d.path
#compatible_rdbms:);
#failgroup_summary:set lines 200
#failgroup_summary:set pages 1000
#failgroup_summary:set feedback off
#failgroup_summary:select CHR(34)||b.name  ||CHR(34)||','||
#failgroup_summary:       CHR(34)||TO_CHAR(decode(count(distinct a.disk_cnt),1,'YES','NO')) ||CHR(34)
#failgroup_summary:from (
#failgroup_summary:    select group_number,
#failgroup_summary:       failgroup,
#failgroup_summary:       count(*) as disk_cnt 
#failgroup_summary:        from v$asm_disk 
#failgroup_summary:        where name <> failgroup 
#failgroup_summary:        group BY group_number,failgroup
#failgroup_summary:      union
#failgroup_summary:       select group_number,
#failgroup_summary:              'NOT-CONFIGURE',
#failgroup_summary:              count(*) as disk_cnt
#failgroup_summary:       from v$asm_disk 
#failgroup_summary:        where name = failgroup
#failgroup_summary:        group by group_number) a, 
#failgroup_summary:        v$asm_diskgroup b
#failgroup_summary:where a.group_number = b.group_number
#failgroup_summary:group by b.name;
#failgroup_summary:
#failgroup_summary:
#failgroup:set lines 200
#failgroup:set pages 1000
#failgroup:set feedback off
#failgroup:select chr(34)||b.name               ||chr(34)||','||
#failgroup:       chr(34)||b.type               ||chr(34)||','||
#failgroup:       chr(34)||a.failgroup          ||chr(34)||','||
#failgroup:       chr(34)||to_char(a.disk_cnt)  ||chr(34)
#failgroup:from (
#failgroup:    select group_number,
#failgroup:       failgroup,
#failgroup:       count(*) as disk_cnt 
#failgroup:        from v$asm_disk 
#failgroup:        where name <> failgroup 
#failgroup:        group BY group_number,failgroup
#failgroup:      union
#failgroup:       select group_number,
#failgroup:              'NOT-CONFIGURE',
#failgroup:              count(*) as disk_cnt
#failgroup:       from v$asm_disk 
#failgroup:        where name = failgroup
#failgroup:        group by group_number) a, 
#failgroup:        v$asm_diskgroup b
#failgroup:where a.group_number = b.group_number
#failgroup:order by a.group_number,a.failgroup;
#failgroup:
#failgroup:
#dg_parameters:set lines 200
#dg_parameters:set  pages 1000
#dg_parameters:col item format a64
#dg_parameters:col  value format a80
#dg_parameters:set heading off
#dg_parameters:set feedback off
#dg_parameters:select name|| '___' || value from v$parameter where name in (
#dg_parameters:'db_file_name_convert',
#dg_parameters:'log_file_name_convert',
#dg_parameters:'log_archive_dest_1',
#dg_parameters:'log_archive_dest_2',
#dg_parameters:'log_archive_dest_3',
#dg_parameters:'log_archive_dest_state_1',
#dg_parameters:'log_archive_dest_state_2',
#dg_parameters:'log_archive_dest_state_3',
#dg_parameters:'db_create_file_dest',
#dg_parameters:'db_create_online_log_dest_1',
#dg_parameters:'db_create_online_log_dest_2',
#dg_parameters:'db_create_online_log_dest_3',
#dg_parameters:'db_create_online_log_dest_4',
#dg_parameters:'db_create_online_log_dest_5',
#dg_parameters:'fal_server',
#dg_parameters:'fal_client',
#dg_parameters:'log_archive_config',
#dg_parameters:'log_archive_format',
#dg_parameters:'log_archive_max_processes',
#dg_parameters:'standby_file_management',
#dg_parameters:'remote_login_passwordfile',
#dg_parameters:'db_name',
#dg_parameters:'db_unique_name',
#dg_parameters:'audit_file_dest',
#dg_parameters:'diagnostic_dest',
#dg_parameters:'control_files',
#dg_parameters:'local_listener',
#dg_parameters:'remote_listener','cluster_database',
#dg_parameters:'spfile',
#dg_parameters:'undo_tablespace',
#dg_parameters:'compatible',
#dg_parameters:'enable_pluggable_database',
#dg_parameters:'sga_max_size',
#dg_parameters:'sga_target',
#dg_parameters:'pga_aggregate_target',
#dg_parameters:'memory_target',
#dg_parameters:'memory_max_target',
#dg_parameters:'job_queue_processes',
#dg_parameters:'processes',
#dg_parameters:'filesystemio_options')
#dg_parameters:union all
#dg_parameters:select 'FORCE_LOGGING'||','||force_logging  from v$database
#dg_parameters:union all
#dg_parameters:select 'NLS_CHARACTERSET' ||','|| VALUE  from v$nls_parameters where parameter='NLS_CHARACTERSET'
#dg_parameters:order by 1;
#spparameter:set lines 400
#spparameter:set pages 1000
#spparameter:set feedback off
#spparameter:set heading off
#spparameter:select chr(34)||FAMILY||chr(34)||'___'||
#spparameter:chr(34)||SID||chr(34)||'___'||
#spparameter:chr(34)||NAME||chr(34)||'___'||
#spparameter:chr(34)||TYPE||chr(34)||'___'||
#spparameter:chr(34)||VALUE||chr(34)||'___'||
#spparameter:chr(34)||DISPLAY_VALUE||chr(34)||'___'||
#spparameter:chr(34)||ORDINAL||chr(34)||'___'||
#spparameter:chr(34)||UPDATE_COMMENT||chr(34)||'___'||
#spparameter:chr(34)||CON_ID||chr(34) from v$spparameter where isspecified='TRUE' order by name,sid;