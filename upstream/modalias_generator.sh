#!/bin/sh
#

LATEST_KERNEL_VER="$(uname -r|cut -f1-1 -d'-')"
EXCLUDE_KMOD_PKGS="kmod-xtables-addons akmod-xtables-addons"
NO_AKMOD_PKGS="kmod-staging"

OUTPUT_BASENAME=rpmfusion-modules
OUTPUT=${OUTPUT_BASENAME}.aliases
JSON=modaliases.json
OUTPUT_DIR=modaliases

[ -d "$OUTPUT_DIR" ] || mkdir $OUTPUT_DIR
cd $OUTPUT_DIR

echo "Downloading kmod packages..."
yumdownloader "kmod-*"
echo "Downloading akmod packages..."
yumdownloader "akmod-*"

#[ -e $OUTPUT ] && echo "Output file already exists: $OUTPUT" && exit 1

echo "Generating modalias files..."
echo "================================================================="

> $JSON
echo "{" >> $JSON


function find_kmod_variant() {
  _AKMOD=${1:-}
  
  [ -r "${_AKMOD}" ] || return 1

  _AKMOD_NAME=$(rpm -qp --queryformat "%{name}\n" $_AKMOD 2>/dev/null)
  
  for _VARIANT in $(ls -1 ${_AKMOD_NAME:1}* 2>/dev/null)
  do
    _MODULES=$(rpm -qlp "${_VARIANT}" 2>/dev/null| grep ".ko$" | wc -l)
    if [ ${_MODULES} -gt 0 ]
    then
      echo $_VARIANT
      return 0
    fi
    
    
  done

  return 1
}

for RPM in *.rpm
do
  if [[ $RPM == akmod* ]];
  then
    AKMOD_NAME=$(rpm -qp --queryformat "%{name}\n" $RPM 2>/dev/null)
    NAME=$AKMOD_NAME
    KMOD_VARIANT=$(find_kmod_variant $RPM)

    if [ -z "$KMOD_VARIANT" ];
    then
      echo "Skipping akmod, no kmod variant!"
      continue
    fi

    RPM=$KMOD_VARIANT

  elif [ "${RPM%%-${LATEST_KERNEL_VER}*}" == "$RPM" ]
  then
    echo "Skipping, kmod is not for current kernel."
    continue
  else
    NAME="${RPM%%-${LATEST_KERNEL_VER}*}"
  fi

  if [[ $EXCLUDE_KMOD_PKGS == *${NAME}* ]]; then
    echo "Excluded kmod: $EXCLUDE_KMOD_PKGS"
    continue;
  fi

  rpmdev-extract "$RPM" >/dev/null
  PKGDIR="${RPM%.rpm}"
  KMODS="$(find "$PKGDIR" -name "*ko")"

  echo $KERNEL_VER

  if [ -z "$KMODS" ]
  then
    echo "Skipping no kernel modules exist in: $RPM"
    continue
  fi

  echo "Processing: $NAME"
 
  echo " \"$NAME\": {" >> $JSON
  echo "   \"modaliases\": [" >> $JSON

  for kmod in $KMODS
  do
    echo "  -> $kmod"
    MODULE_NAME=$(basename $kmod)
    MODULE_NAME=${MODULE_NAME%.ko}

    VERMAGIC=$(modinfo $kmod | awk '/vermagic:/ { print $2 }')

    for ALIAS in $(modinfo $kmod | awk '/alias:/ { print $2 }')
    do
      echo "      {"                                 >> $JSON
      echo "         \"alias\": \"$ALIAS\","         >> $JSON
      echo "         \"module\": \"$MODULE_NAME\""   >> $JSON
      echo "      },"                                >> $JSON
    done
  done

  echo "    ]"   >> $JSON
  echo "  }," >> $JSON

  rm -rf "${PKGDIR}"
done

echo "}"     >> $JSON

echo "Output files ready in $OUTPUT_DIR"
