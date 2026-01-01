@echo off
echo Creating ZIP archive of ILUMINATI project...
powershell -Command "Compress-Archive -Path 'C:\Users\engli\Desktop\v4\v4\*' -DestinationPath 'C:\Users\engli\Desktop\iluminati_complete_project_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.zip' -Force"
echo ZIP archive created successfully!
echo File location: C:\Users\engli\Desktop\iluminati_complete_project_*.zip
pause