Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obter diretório do script
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Verificar se o Streamlit já está rodando
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'streamlit.exe' OR CommandLine LIKE '%streamlit%app.py%'")

If colProcesses.Count > 0 Then
    ' Streamlit já está rodando, apenas abrir navegador
    WshShell.Run "http://localhost:8501", 1
Else
    ' Iniciar Streamlit em background (sem janela de terminal)
    strCommand = "cmd /c cd /d """ & strScriptPath & """ && .venv\Scripts\python.exe -m streamlit run app.py --server.headless=true"
    WshShell.Run strCommand, 0, False
    
    ' Aguardar 6 segundos para o Streamlit inicializar
    WScript.Sleep 6000
    
    ' Abrir navegador
    WshShell.Run "http://localhost:8501", 1
End If
