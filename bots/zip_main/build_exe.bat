set scriptdir=%CD%
cd ..
copy [MySources]\cores.py %scriptdir%\cores.py
copy [MySources]\vis.py %scriptdir%\vis.py
copy [MySources]\soup_driver.py %scriptdir%\soup_driver.py
copy [MySources]\bot_socket.py %scriptdir%\bot_socket.py
copy [MySources]\telecore.py %scriptdir%\telecore.py
copy [MySources]\main_utils.py %scriptdir%\main_utils.py
cd %scriptdir%
pyinstaller --hidden-import bot_socket --hidden-import main_utils --hidden-import soup_driver --icon=main.ico --noconfirm zip_main.py
for %%I in (.) do set CurrDir=%%~nxI
xcopy to_dist dist\%CurrDir% /H /Y /S
del cores.py /Q
del vis.py /Q
del soup_driver.py /Q
del bot_socket.py /Q
del telecore.py /Q
del main_utils.py /Q
pause