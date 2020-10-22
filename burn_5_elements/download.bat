cd %~dp0
set /p convert_col_num=input convert colnum(default:0x01):
echo %convert_col_num%

python convert.py %convert_col_num%
python txt_to_bin.py %convert_col_num%
::pause
jlink -autoconnect  1 -device NRF52840_XXAA -if swd -speed 4000 -commandfile download.jlink
