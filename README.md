# pyperfmon

**pyperfmon** is a simple performance measuring tool for web server, which uses python multiprocessing lib to simulater user loading condition on web server. pyperfmon can be used to simulate following perfromance loading condition on any given web server under test
 * single or multiple api(s) having different mix ratio
 * different user concurrency
 * different data size both post and get

Perfromance is measuer in terms of Response time and Request per sec (RPS) during the test.

## Prerequisite

 * python 2.6
 * numpy
 
### TCP/IP fine tunning for Perfromance testing 
Fine tune following linux kernel TCP/IP parameter to optimize network traffic during perfromance testing

    sudo echo 0 > /proc/sys/net/ipv4/tcp_timestamps 
    sudo echo 1 > /proc/sys/net/ipv4/tcp_sack 
    sudo echo 1 > /proc/sys/net/ipv4/tcp_window_scaling
    sudo sysctl -p

For further optimization fine tune following linux kernel TCP/IP parameter

    sudo echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout
    sudo echo 30 > /proc/sys/net/ipv4/tcp_keepalive_intvl
    sudo echo 5 > /proc/sys/net/ipv4/tcp_keepalive_probes
    sudo echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle
    sudo echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse
    sudo sysctl -p

Note : Please save you original setting and revert back to it your are done with your testing

    
## Config

    config/perperfmon.cfg

## Usage

    python26 perfmon

