#!/bin/bash

SAT=$1
FREQ=$2
DECIMATION=$3
FILEKEY=$4
TLE_FILE=$5
START_TIME=$6
DURATION=$7

ARG_SOAPY=$WX_GROUND_ARG_SOAPY
SOAPY_SAMPLERATE=$WX_GROUND_SOAPY_SAMPLERATE
ROTCTLD_SERVER=$WX_GROUND_ROTCTLD_SERVER
ROTCTLD_PORT=$WX_GROUND_ROTCTLD_PORT
GAIN=$WX_GROUND_SPY_GAIN
RX_LAT=$WX_GROUND_LAT
RX_LON=$WX_GROUND_LON
RX_ALT=$WX_GROUND_ALT
OFFSET=$WX_GROUND_RX_OFFSET
FLOWCHARTS_DIR=${WX_GROUND_DIR}/flowcharts

AUDIO_DIR=$WX_GROUND_DIR/audio
LOG_DIR=$WX_GROUND_DIR/logs
IQ_FILE=${AUDIO_DIR}/${FILEKEY}.iq
DEMODED_FILE=${AUDIO_DIR}/${FILEKEY}.s
QPSK_FILE=${AUDIO_DIR}/${FILEKEY}.qpsk
LOGFILE=${LOG_DIR}/${FILEKEY}.log

echo $@ >> $LOGFILE

if [[ "$SAT" == "NOAA 19" || "$SAT" == "NOAA 15" || "$SAT" == "NOAA 18" ]]; then
  echo "/usr/bin/timeout $DURATION \"${FLOWCHARTS_DIR}/WXsat_APT.py\" --arg-soapy \"${ARG_SOAPY}\" --samp-rate-soapy ${SOAPY_SAMPLERATE} --freq ${FREQ} --decim ${DECIMATION} --tle-file ${TLE_FILE} --sat-id \"${SAT}\" --gnd-lat ${RX_LAT} --gnd-lon ${RX_LON} --gnd-altitude ${RX_ALT} --salida ${DEMODED_FILE} 2>> $LOGFILE" >> $LOGFILE

  /usr/bin/timeout $DURATION "${FLOWCHARTS_DIR}/WXsat_APT.py" --arg-soapy "${ARG_SOAPY}" --samp-rate-soapy ${SOAPY_SAMPLERATE} --freq ${FREQ} --decim ${DECIMATION} --tle-file ${TLE_FILE} --sat-id "${SAT}" --gnd-lat ${RX_LAT} --gnd-lon ${RX_LON} --gnd-altitude ${RX_ALT} --salida ${DEMODED_FILE} 2>> $LOGFILE

  echo "$WX_GROUND_DIR/decode_satellite.sh \"${SAT}\" \"${FILEKEY}\" ${TLE_FILE} ${START_TIME}" >> $LOGFILE
  $WX_GROUND_DIR/decode_satellite.sh "${SAT}" "${FILEKEY}" ${TLE_FILE} ${START_TIME}
elif [[ "$SAT" == "METEOR-M 2" ]]; then
  echo "/usr/bin/timeout $DURATION \"${FLOWCHARTS_DIR}/WXsat_LRPT.py\" --arg-soapy \"${ARG_SOAPY}\" --samp-rate-soapy ${SOAPY_SAMPLERATE} --freq ${FREQ} --decim ${DECIMATION} --tle-file ${TLE_FILE} --sat-id \"${SAT}\" --gnd-lat ${RX_LAT} --gnd-lon ${RX_LON} --gnd-altitude ${RX_ALT} --salida ${DEMODED_FILE} 2>> $LOGFILE" >> $LOGFILE

  /usr/bin/timeout $DURATION "${FLOWCHARTS_DIR}/WXsat_LRPT.py" --arg-soapy "${ARG_SOAPY}" --samp-rate-soapy ${SOAPY_SAMPLERATE} --freq ${FREQ} --decim ${DECIMATION} --tle-file ${TLE_FILE} --sat-id \"${SAT}\" --gnd-lat ${RX_LAT} --gnd-lon ${RX_LON} --gnd-altitude ${RX_ALT} --salida ${DEMODED_FILE} 2>> $LOGFILE

  echo "$WX_GROUND_DIR/decode_satellite.sh \"${SAT}\" ${FILEKEY}" >> $LOGFILE
  $WX_GROUND_DIR/decode_satellite.sh "${SAT}" "${FILEKEY}"
fi
