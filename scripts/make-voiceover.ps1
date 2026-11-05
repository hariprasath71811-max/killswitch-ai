param(
  [string]$TextPath = "demo-voice.txt",
  [string]$OutPath = "narration.wav",
  [int]$Rate = 0,
  [string]$Voice = "Microsoft Zira Desktop"
)
Add-Type -AssemblyName System.Speech
$text = [System.IO.File]::ReadAllText($TextPath, [System.Text.Encoding]::UTF8)
$paragraphs = $text -split "`r?`n`r?`n" | Where-Object { $_.Trim().Length -gt 0 }
$escaped = $paragraphs | ForEach-Object { [System.Security.SecurityElement]::Escape($_.Trim()) }
$body = $escaped -join '<break time="550ms"/>'
$ssml = @"
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="$Voice">
    $body
  </voice>
</speak>
"@
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$tts.SelectVoice($Voice)
$tts.Rate = $Rate
$tts.Volume = 100
$tts.SetOutputToWaveFile($OutPath)
$tts.SpeakSsml($ssml)
$tts.Dispose()
Write-Output "Generated $OutPath at rate $Rate with $Voice"
