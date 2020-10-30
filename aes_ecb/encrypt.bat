.\hex2bin.exe .\nrf52840_xxaa.hex
echo "bin file come into from hex"

python .\aes_ecb_sleep_band.py

pause