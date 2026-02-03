#!/usr/bin/env bash

generate_data(){
	local PST=$1
	local D2=$2
	local D4=$3
	local D5=$4
	local PT=$5

	echo '{"pt":"$PT","pst":"$PST","d2":"$D2","d4":"$D4","d5":"$D5","d6":"null","driverType":"all","cookieEmpty":false,"sa":"1"}' | sed 's|"|%22|g'
}

test_request(){
	local PST=$1
	local D2=$2
	local D4=$3
	local D5=$4
	local PT=$5
	local URL="https://gfwsl.geforce.com/nvidia_web_services/controller.php?com.nvidia.services.Drivers.getMenuArrays/"
	local PARAMS=$(generate_data %PST $D2 $D4 $D5 $PT)

	curl -s "$URL$PARMS" | jq
}
