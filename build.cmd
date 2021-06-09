
:: clean up
@rd /q /s .\build\

:: create out directory
@mkdir .\build > NUL
@mkdir .\build\bin > NUL

@copy ".\src\mikk.bell.py" ".\build\bin\" > NUL
@copy ".\src\mikk.dir.clamp.py" ".\build\bin\" > NUL
@copy ".\src\mikk.dir.flatten.py" ".\build\bin\" > NUL
@copy ".\src\mikk.file.random.py" ".\build\bin\" > NUL
@copy ".\src\mikk.file.rename.py" ".\build\bin\" > NUL
@copy ".\src\mikk.files.count.py" ".\build\bin\" > NUL
@copy ".\src\mikk.files.count.tree.py" ".\build\bin\" > NUL
@copy ".\src\mikk.files.exts.py" ".\build\bin\" > NUL
@copy ".\src\mikk.files.sort-by-ext.py" ".\build\bin\" > NUL
@copy ".\src\mikk.files.unique.py" ".\build\bin\" > NUL
@copy ".\src\mikk.grep.py" ".\build\bin\" > NUL
@copy ".\src\mikk.lines.similar.py" ".\build\bin\" > NUL
@copy ".\src\mikk.lines.unique.py" ".\build\bin\" > NUL
@copy ".\src\mikk.log.py" ".\build\bin\" > NUL
@copy ".\src\mikk.md5.py" ".\build\bin\" > NUL
@copy ".\src\mikk.media.player.py" ".\build\bin\" > NUL
@copy ".\src\mikk.PATH.py" ".\build\bin\" > NUL
@copy ".\src\mikk.random.choice.py" ".\build\bin\" > NUL
@copy ".\src\mikk.sha256.py" ".\build\bin\" > NUL
@copy ".\src\mikk.ts.py" ".\build\bin\" > NUL
@copy ".\src\mikk.wait.py" ".\build\bin\" > NUL

:: @copy ".\src\" ".\build\bin\" > NUL

@REM @rustc -g -O -o .\build\bin\quote.exe .\src\quote.rs
@REM @del .\build\bin\quote.pdb
@REM @rustc -g -O -o .\build\bin\count.exe .\src\count.rs
@REM @del .\build\bin\count.pdb

@ECHO OK
