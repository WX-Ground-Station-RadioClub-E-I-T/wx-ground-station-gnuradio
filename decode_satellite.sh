#!/bin/bash

SAT=$1
FILEKEY=$2
TLE_FILE=$3
START_TIME=$4

MAX_ELEV=$WX_GROUND_MAX_ELEV
IMAGE_DIR=${WX_GROUND_DIR}/images
LOG_DIR=${WX_GROUND_DIR}/logs
AUDIO_DIR=${WX_GROUND_DIR}/audio
DRAFT_DIR=${WX_GROUND_DIR}/draft
DEMODED_FILE=${AUDIO_DIR}/${FILEKEY}.s
LOGFILE=${LOG_DIR}/${FILEKEY}.log

echo $@ >> $LOGFILE

if [[ "$SAT" == "NOAA 19" || "$SAT" == "NOAA 15" || "$SAT" == "NOAA 18" ]]; then
  if [ -e $DEMODED_FILE ]
    then
      PassStart=`expr $START_TIME + 90`
      MAP_FILE=${IMAGE_DIR}/${FILEKEY}-map.png

      echo "bin/wxmap -T \"${SAT}\" -M ${MAX_ELEV} -H $TLE_FILE -b 0 -p 0 -l 0 -o $PassStart ${MAP_FILE}" >>$LOGFILE
      /usr/local/bin/wxmap -T "${SAT}" -M ${MAX_ELEV} -H $TLE_FILE -b 0 -p 0 -l 0 -o $PassStart ${MAP_FILE} >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e ZA $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-ZA.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e ZA $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-ZA.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e NO $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-NO.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e NO $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-NO.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e MSA $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MSA.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e MSA $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MSA.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e MCIR $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MCIR.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e MCIR $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MCIR.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e therm $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-THERM.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e therm $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-THERM.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e MB $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MB.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e MB $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MB.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e MD $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MD.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e MD $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MD.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e BD $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-BD.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e BD $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-BD.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e CC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-CC.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e CC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-CC.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e EC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-EC.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e EC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-EC.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e HE $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HE.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e HE $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HE.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e HF $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HF.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e HF $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HF.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e JF $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-JF.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e JF $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-JF.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e JJ $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-JJ.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e JJ $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-JJ.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e LC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-LC.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e LC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-LC.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e WV $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-WV.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e WV $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-WV.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e MSA-precip $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MSA-precip.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e MSA-precip $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-MSA-precip.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e HVC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HVC.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e HVC $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HVC.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e HVCT $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HVCT.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e HVCT $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-HVCT.png >> $LOGFILE 2>&1

      echo "/usr/local/bin/wxtoimg -m ${MAP_FILE} -e sea $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-sea.png" >> $LOGFILE
      /usr/local/bin/wxtoimg -m ${MAP_FILE} -e sea $DEMODED_FILE ${IMAGE_DIR}/${FILEKEY}-sea.png >> $LOGFILE 2>&1

      echo "$WX_GROUND_DIR/upload.sh \"${SAT}\" ${FILEKEY}" >> $LOGFILE
      $WX_GROUND_DIR/upload.sh "${SAT}" ${FILEKEY} >> $LOGFILE 2>&1
  else
    echo "NO AUDIO FILE" >>$LOGFILE
  fi
fi

if [[ "$SAT" == "METEOR-M 2" ]]; then
  DEMODED_FILE_BASE=${AUDIO_DIR}/${FILEKEY} # For METEOR-M 2

  # Decode
  medet ${DEMODED_FILE} ${DEMODED_FILE_BASE} -cd -q >> $LOGFILE 2>&1

  touch -r ${DEMODED_FILE} ${DEMODED_FILE_BASE}.dec >> $LOGFILE 2>&1

  # Create image:
  # composite only
  medet ${DEMODED_FILE_BASE}.dec ${DEMODED_FILE_BASE} -r 65 -g 65 -b 64 -d -q >> $LOGFILE 2>&1
  # three channels
  #medet ${DEMODED_FILE_BASE}.dec ${DEMODED_FILE_BASE} -S -r 65 -g 65 -b 64 -d -q
  # IR
  medet ${DEMODED_FILE_BASE}.dec ${DEMODED_FILE_BASE}_IR -r 68 -g 68 -b 68 -d -q >> $LOGFILE 2>&1

  if [[ -f "${DEMODED_FILE_BASE}.bmp" ]]; then
    convert ${DEMODED_FILE_BASE}.bmp ${IMAGE_DIR}/${FILEKEY}.png &> /dev/null
    rm -f ${DEMODED_FILE_BASE}.bmp
    touch -r ${DEMODED_FILE} ${IMAGE_DIR}/${FILEKEY}.png
    # check brightness
    brightness=`convert ${IMAGE_DIR}/${FILEKEY}.png -colorspace Gray -format "%[fx:image.mean]" info:`
    if (( $(echo "$brightness > 0.09" |bc -l) )); then
      echo -e "\nComposite image created!" >> $LOGFILE
    else
      mv ${IMAGE_DIR}/${FILEKEY}.png ${DRAFT_DIR}
      echo -e "\nComposite image too dark, probably bad quality." >> $LOGFILE
      exit # No upload if there is no image
    fi
  fi

  if [[ -f "${DEMODED_FILE_BASE}_IR.bmp" ]]; then
    convert ${DEMODED_FILE_BASE}_IR.bmp -negate -normalize ${IMAGE_DIR}/${FILEKEY}_IR.png &> /dev/null
    rm -f ${DEMODED_FILE_BASE}_IR.bmp
    touch -r ${DEMODED_FILE} ${IMAGE_DIR}/${FILEKEY}_IR.png
    # check brightness
    brightness=`convert ${IMAGE_DIR}/${FILEKEY}_IR.png -negate -colorspace Gray -format "%[fx:image.mean]" info:`
    if (( $(echo "$brightness > 0.09" |bc -l) )); then
      echo -e "\nIR image created!" >> $LOGFILE
    else
      mv ${IMAGE_DIR}/${FILEKEY}_IR.png ${DRAFT_DIR}
      echo -e "\nIR image too dark, probably bad quality." >> $LOGFILE
      exit # No upload if there is no image
    fi
  fi

  if [[ -e "${IMAGE_DIR}/${FILEKEY}.png" ]]; then
    echo "$WX_GROUND_DIR/upload.sh \"${SAT}\" ${FILEKEY}" >> $LOGFILE
    $WX_GROUND_DIR/upload.sh "${SAT}" ${FILEKEY} >> $LOGFILE 2>&1
  fi
fi
