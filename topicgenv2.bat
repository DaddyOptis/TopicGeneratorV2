@echo off
setlocal enabledelayedexpansion

:loop
for /f "delims=" %%i in ('curl -s "https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=20&rnnamespace=0"') do (
    for /f "tokens=*" %%a in ("%%i") do (
        set "json=%%a"
        for /f "tokens=2 delims=:" %%b in ("!json:*title=!") do (
            for /f "tokens=1 delims=," %%c in ("%%b") do (
                set "title=%%c"
                echo !title:"=!
            )
        )
    )
)

timeout /t 1 >nul
goto loop

endlocal