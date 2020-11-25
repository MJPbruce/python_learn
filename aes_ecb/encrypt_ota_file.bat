cd %~dp0

::xcopy /y /s /i /c D:\mjp_workspace\Embedded_Nordic_Zigbee_BLE_Base\examples\multiprotocol_ota_RTOS\ble_zigbee_ota\ble_zigbee_sensor_ota_nus_rtos\pca10056\blank\arm5_no_packs\_build\nrf52840_xxaa.hex .


:: modify hex file to fill several 'F' in the file end
python .\modify_hex.py   

:: convert hex file into bin file 
.\hex2bin.exe .\nrf52840_xxaa.hex  
echo "bin file come into from hex"


set firmware_version=0x0000000C
set manufacturer_id=0x115F
set image_type=0x1288
set /p firmware_version=input ota firmware version (default: 0x0000000C):

echo "firmware_version: %firmware_version%"
echo "manufacturer_id: %manufacturer_id%"
echo "image_type: %image_type%"

nrfutil pkg generate --hw-version 52 --sd-req 0xCA --application-version %firmware_version% --application ./firmware/nrf52840_xxaa.hex --key-file ./key/priv.pem --app-boot-validation VALIDATE_ECDSA_P256_SHA256 app_dfu_package.zip --zigbee True --zigbee-manufacturer-id %manufacturer_id% --zigbee-image-type %image_type% --zigbee-comment OTA_lumi.lunar.acn01 --zigbee-ota-hw-version 52 --zigbee-ota-fw-version %firmware_version%

echo pack ota finish !

ren *.zigbee OTA_lumi.lunar.acn01.zigbee

:: generate encrypted ota file 
python .\aes_ecb_sleep_band.py

del OTA_lumi.lunar.acn01.ota
ren encrypt.bin OTA_lumi.lunar.acn01.ota


del *.txt
del *.bin
del *.zigbee
del *.hex

pause