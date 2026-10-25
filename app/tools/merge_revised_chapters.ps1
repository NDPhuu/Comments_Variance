param(
    [Parameter(Mandatory=$true)][string]$SourceDocx,
    [Parameter(Mandatory=$true)][string]$Chapter4,
    [Parameter(Mandatory=$true)][string]$Chapter5,
    [Parameter(Mandatory=$true)][string]$OutputDocx
)

$ErrorActionPreference = 'Stop'

function Copy-SharedFile([string]$Source, [string]$Destination) {
    $src = [IO.File]::Open($Source, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        $dst = [IO.File]::Open($Destination, [IO.FileMode]::Create, [IO.FileAccess]::Write, [IO.FileShare]::None)
        try { $src.CopyTo($dst) } finally { $dst.Dispose() }
    } finally { $src.Dispose() }
}

function Clean-Markdown([string]$Text) {
    return $Text.Replace('**','').Replace('`','')
}

function Insert-Paragraph($Document, [string]$Text, [int]$StyleId) {
    $start = $Document.Content.End - 1
    $range = $Document.Range($start, $start)
    $range.InsertAfter((Clean-Markdown $Text) + "`r")
    $paragraph = $Document.Range($start, $Document.Content.End - 1).Paragraphs.Item(1)
    $paragraph.Style = $StyleId
    return $paragraph
}

function Insert-MarkdownTable($Document, [System.Collections.Generic.List[string]]$Lines) {
    $rows = New-Object System.Collections.Generic.List[object]
    foreach ($line in $Lines) {
        if ($line -match '^\|\s*:?-+') { continue }
        $cells = $line.Trim().Trim('|').Split('|') | ForEach-Object { (Clean-Markdown $_.Trim()) }
        $rows.Add(@($cells))
    }
    if ($rows.Count -eq 0) { return }
    $cols = $rows[0].Count
    $start = $Document.Content.End - 1
    $range = $Document.Range($start, $start)
    $table = $Document.Tables.Add($range, $rows.Count, $cols)
    $table.Borders.Enable = 1
    $table.AllowAutoFit = $true
    for ($r = 0; $r -lt $rows.Count; $r++) {
        for ($c = 0; $c -lt $cols; $c++) {
            $table.Cell($r + 1, $c + 1).Range.Text = [string]$rows[$r][$c]
            $table.Cell($r + 1, $c + 1).Range.Font.Name = 'Times New Roman'
            $table.Cell($r + 1, $c + 1).Range.Font.Size = 11
        }
    }
    $table.Rows.Item(1).Range.Bold = 1
    $table.Rows.Item(1).Shading.BackgroundPatternColor = 15132390
    $table.Rows.Item(1).HeadingFormat = -1
    $table.Range.ParagraphFormat.SpaceAfter = 0
    $table.Range.ParagraphFormat.LineSpacingRule = 0
    $after = $Document.Range($Document.Content.End - 1, $Document.Content.End - 1)
    $after.InsertAfter("`r")
}

function Insert-Markdown($Document, [string]$Path) {
    $lines = [IO.File]::ReadAllLines($Path, [Text.Encoding]::UTF8)
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i]
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line.StartsWith('|') -and $i + 1 -lt $lines.Length -and $lines[$i + 1] -match '^\|\s*:?-+') {
            $block = New-Object 'System.Collections.Generic.List[string]'
            while ($i -lt $lines.Length -and $lines[$i].StartsWith('|')) {
                $block.Add($lines[$i])
                $i++
            }
            $i--
            Insert-MarkdownTable $Document $block
            continue
        }
        if ($line.StartsWith('### ')) { Insert-Paragraph $Document $line.Substring(4) -4 | Out-Null; continue }
        if ($line.StartsWith('## '))  { Insert-Paragraph $Document $line.Substring(3) -3 | Out-Null; continue }
        if ($line.StartsWith('# '))   { Insert-Paragraph $Document $line.Substring(2) -2 | Out-Null; continue }
        $p = Insert-Paragraph $Document $line -1
        if ($line -match '^\*\*(Bảng|Hình)') { $p.Style = -35 }
        if ($line.StartsWith('*Nguồn:') -or $line.StartsWith('*Ghi chú:')) { $p.Range.Italic = 1 }
    }
}

$source = (Resolve-Path -LiteralPath $SourceDocx).Path
$chapter4 = (Resolve-Path -LiteralPath $Chapter4).Path
$chapter5 = (Resolve-Path -LiteralPath $Chapter5).Path
$output = [IO.Path]::GetFullPath($OutputDocx)
Copy-SharedFile $source $output

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($output)
    try {
        $cutStart = $null
        $levelOneCount = 0
        foreach ($paragraph in $doc.Paragraphs) {
            if ($paragraph.OutlineLevel -eq 1) {
                $levelOneCount++
                if ($levelOneCount -eq 4) {
                    $cutStart = $paragraph.Range.Start
                    break
                }
            }
        }
        if ($null -eq $cutStart) { throw 'Khong tim thay heading cap 1 thu tu trong tai lieu nguon.' }
        $doc.Range($cutStart, $doc.Content.End - 1).Delete() | Out-Null
        Insert-Markdown $doc $chapter4
        Insert-Markdown $doc $chapter5
        $doc.Fields.Update() | Out-Null
        $doc.Save()
    } finally {
        $doc.Close()
    }
} finally {
    $word.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

Write-Output $output
