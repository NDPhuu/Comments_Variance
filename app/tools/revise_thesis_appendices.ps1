param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,
    [Parameter(Mandatory = $true)]
    [string]$OutputDocx
)

$ErrorActionPreference = 'Stop'

$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputDocx)
$workspace = (Resolve-Path -LiteralPath (Split-Path -Parent (Split-Path -Parent $inputPath))).Path

if (-not $outputPath.StartsWith($workspace, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Output must stay inside $workspace"
}

Copy-Item -LiteralPath $inputPath -Destination $outputPath -Force

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$wNs = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
$xmlNs = 'http://www.w3.org/XML/1998/namespace'

function Read-ZipText([System.IO.Compression.ZipArchive]$zip, [string]$name) {
    $entry = $zip.GetEntry($name)
    if ($null -eq $entry) { throw "Missing DOCX part: $name" }
    $reader = [System.IO.StreamReader]::new($entry.Open(), [System.Text.Encoding]::UTF8, $true)
    try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
}

function Write-ZipText([System.IO.Compression.ZipArchive]$zip, [string]$name, [string]$text) {
    $old = $zip.GetEntry($name)
    if ($null -ne $old) { $old.Delete() }
    $entry = $zip.CreateEntry($name, [System.IO.Compression.CompressionLevel]::Optimal)
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    $writer = [System.IO.StreamWriter]::new($entry.Open(), $utf8NoBom)
    try { $writer.Write($text) } finally { $writer.Dispose() }
}

function New-WElement([xml]$xml, [string]$name) {
    return $xml.CreateElement('w', $name, $wNs)
}

function Set-WAttribute($element, [string]$name, [string]$value) {
    [void]$element.SetAttribute($name, $wNs, $value)
}

function New-Paragraph {
    param(
        [xml]$Xml,
        [string]$Text = '',
        [string]$Style = '',
        [bool]$Bold = $false,
        [bool]$Italic = $false,
        [int]$Size = 0,
        [string]$Align = '',
        [int]$LeftIndent = 0,
        [int]$FirstLine = 0,
        [int]$OutlineLevel = -1,
        [bool]$KeepNext = $false,
        [bool]$PageBreakBefore = $false
    )
    $p = New-WElement $Xml 'p'
    $pPr = New-WElement $Xml 'pPr'
    if ($Style) {
        $pStyle = New-WElement $Xml 'pStyle'
        Set-WAttribute $pStyle 'val' $Style
        [void]$pPr.AppendChild($pStyle)
    }
    if ($Align) {
        $jc = New-WElement $Xml 'jc'
        Set-WAttribute $jc 'val' $Align
        [void]$pPr.AppendChild($jc)
    }
    if ($LeftIndent -ne 0 -or $FirstLine -ne 0) {
        $ind = New-WElement $Xml 'ind'
        if ($LeftIndent -ne 0) { Set-WAttribute $ind 'left' ([string]$LeftIndent) }
        if ($FirstLine -ne 0) { Set-WAttribute $ind 'firstLine' ([string]$FirstLine) }
        [void]$pPr.AppendChild($ind)
    }
    if ($OutlineLevel -ge 0) {
        $outline = New-WElement $Xml 'outlineLvl'
        Set-WAttribute $outline 'val' ([string]$OutlineLevel)
        [void]$pPr.AppendChild($outline)
    }
    if ($KeepNext) { [void]$pPr.AppendChild((New-WElement $Xml 'keepNext')) }
    if ($PageBreakBefore) { [void]$pPr.AppendChild((New-WElement $Xml 'pageBreakBefore')) }
    if ($pPr.HasChildNodes) { [void]$p.AppendChild($pPr) }

    $r = New-WElement $Xml 'r'
    if ($Bold -or $Italic -or $Size -gt 0) {
        $rPr = New-WElement $Xml 'rPr'
        if ($Bold) { [void]$rPr.AppendChild((New-WElement $Xml 'b')) }
        if ($Italic) { [void]$rPr.AppendChild((New-WElement $Xml 'i')) }
        if ($Size -gt 0) {
            $sz = New-WElement $Xml 'sz'; Set-WAttribute $sz 'val' ([string]$Size); [void]$rPr.AppendChild($sz)
            $szCs = New-WElement $Xml 'szCs'; Set-WAttribute $szCs 'val' ([string]$Size); [void]$rPr.AppendChild($szCs)
        }
        [void]$r.AppendChild($rPr)
    }
    $t = New-WElement $Xml 't'
    [void]$t.SetAttribute('xml:space', 'preserve')
    $t.InnerText = $Text
    [void]$r.AppendChild($t)
    [void]$p.AppendChild($r)
    return $p
}

function New-PageBreak([xml]$Xml) {
    $p = New-WElement $Xml 'p'
    $r = New-WElement $Xml 'r'
    $br = New-WElement $Xml 'br'
    Set-WAttribute $br 'type' 'page'
    [void]$r.AppendChild($br)
    [void]$p.AppendChild($r)
    return $p
}

function New-Table {
    param(
        [xml]$Xml,
        [object[]]$Headers,
        [object[]]$Rows,
        [int[]]$Widths,
        [int]$FontSize = 19
    )
    $tbl = New-WElement $Xml 'tbl'
    $tblPr = New-WElement $Xml 'tblPr'
    $style = New-WElement $Xml 'tblStyle'; Set-WAttribute $style 'val' 'TableGrid'; [void]$tblPr.AppendChild($style)
    $tblW = New-WElement $Xml 'tblW'; Set-WAttribute $tblW 'w' ([string](($Widths | Measure-Object -Sum).Sum)); Set-WAttribute $tblW 'type' 'dxa'; [void]$tblPr.AppendChild($tblW)
    $layout = New-WElement $Xml 'tblLayout'; Set-WAttribute $layout 'type' 'fixed'; [void]$tblPr.AppendChild($layout)
    $margins = New-WElement $Xml 'tblCellMar'
    foreach ($side in @('top','left','bottom','right')) {
        $m = New-WElement $Xml $side; Set-WAttribute $m 'w' '70'; Set-WAttribute $m 'type' 'dxa'; [void]$margins.AppendChild($m)
    }
    [void]$tblPr.AppendChild($margins)
    [void]$tbl.AppendChild($tblPr)

    $grid = New-WElement $Xml 'tblGrid'
    foreach ($width in $Widths) { $gc = New-WElement $Xml 'gridCol'; Set-WAttribute $gc 'w' ([string]$width); [void]$grid.AppendChild($gc) }
    [void]$tbl.AppendChild($grid)

    $allRows = [System.Collections.ArrayList]::new()
    [void]$allRows.Add([object[]]$Headers)
    foreach ($dataRow in $Rows) { [void]$allRows.Add([object[]]$dataRow) }
    for ($ri = 0; $ri -lt $allRows.Count; $ri++) {
        $tr = New-WElement $Xml 'tr'
        $trPr = New-WElement $Xml 'trPr'
        if ($ri -eq 0) {
            [void]$trPr.AppendChild((New-WElement $Xml 'tblHeader'))
            [void]$trPr.AppendChild((New-WElement $Xml 'cantSplit'))
        }
        [void]$tr.AppendChild($trPr)
        $row = @($allRows[$ri])
        for ($ci = 0; $ci -lt $Headers.Count; $ci++) {
            $tc = New-WElement $Xml 'tc'
            $tcPr = New-WElement $Xml 'tcPr'
            $tcW = New-WElement $Xml 'tcW'; Set-WAttribute $tcW 'w' ([string]$Widths[$ci]); Set-WAttribute $tcW 'type' 'dxa'; [void]$tcPr.AppendChild($tcW)
            $vAlign = New-WElement $Xml 'vAlign'; Set-WAttribute $vAlign 'val' 'center'; [void]$tcPr.AppendChild($vAlign)
            if ($ri -eq 0) { $shd = New-WElement $Xml 'shd'; Set-WAttribute $shd 'fill' 'D9E2F3'; [void]$tcPr.AppendChild($shd) }
            [void]$tc.AppendChild($tcPr)
            $cellText = if ($ci -lt $row.Count -and $null -ne $row[$ci]) { [string]$row[$ci] } else { '' }
            $cellAlign = if ($ri -eq 0) { 'center' } else { 'left' }
            $cellP = New-Paragraph -Xml $Xml -Text $cellText -Bold ($ri -eq 0) -Size $FontSize -Align $cellAlign -FirstLine 0
            [void]$tc.AppendChild($cellP)
            [void]$tr.AppendChild($tc)
        }
        [void]$tbl.AppendChild($tr)
    }
    return $tbl
}

$zip = [System.IO.Compression.ZipFile]::Open($outputPath, [System.IO.Compression.ZipArchiveMode]::Update)
try {
    $xml = [System.Xml.XmlDocument]::new()
    $xml.PreserveWhitespace = $true
    $xml.LoadXml((Read-ZipText $zip 'word/document.xml'))
    $ns = [System.Xml.XmlNamespaceManager]::new($xml.NameTable)
    $ns.AddNamespace('w', $wNs)
    $paragraphs = @($xml.SelectNodes('//w:body/w:p', $ns))

    function Set-ParagraphText([int]$Index, [string]$Text) {
        $nodes = @($paragraphs[$Index].SelectNodes('.//w:t', $ns))
        if ($nodes.Count -eq 0) {
            $r = New-WElement $xml 'r'; $t = New-WElement $xml 't'; [void]$t.SetAttribute('xml:space', 'preserve'); $t.InnerText = $Text; [void]$r.AppendChild($t); [void]$paragraphs[$Index].AppendChild($r)
            return
        }
        $nodes[0].InnerText = $Text
        for ($j = 1; $j -lt $nodes.Count; $j++) { $nodes[$j].InnerText = '' }
    }

    $replacements = @{
        2 = 'Bất động sản khu công nghiệp là một phân khúc có mức tăng trưởng đáng chú ý trong thị trường bất động sản Việt Nam. Trong sáu tháng đầu năm 2026, GDP cả nước tăng 8,18% so với cùng kỳ. Tổng vốn đầu tư nước ngoài đăng ký đạt 34,65 tỷ USD, tăng 61% so với cùng kỳ (Cục Thống kê, 2026). Tại các thị trường cấp 1 miền Bắc, diện tích đất khu công nghiệp hấp thụ đạt 217 ha trong quý 2/2026 (CBRE Việt Nam, 2026a). Ở miền Nam, diện tích hấp thụ trong nửa đầu năm đạt 124 ha, tăng 125% so với cùng kỳ (CBRE Việt Nam, 2026b). Các giao dịch đáng chú ý đến từ nhóm sản xuất điện tử và bán dẫn.'
        6 = 'Đối với các chủ đầu tư quản lý nhiều dự án và khách thuê, quy mô hoạt động làm tăng khối lượng báo cáo quản trị định kỳ. Một nghiệp vụ quan trọng là phân tích chênh lệch ngân sách hằng tháng do bộ phận Hoạch định và Phân tích Tài chính (FP&A - Financial Planning and Analysis) thực hiện. Sau khi đóng sổ, chuyên viên FP&A giải thích chênh lệch giữa kết quả thực tế và ngân sách. Báo cáo này cung cấp thông tin để ban lãnh đạo xem xét hoạt động vận hành và báo cáo hội đồng quản trị.'
        20 = 'Các mô hình ngôn ngữ lớn (Large Language Model - LLM) như Claude, ChatGPT, Gemini và Copilot có thể hỗ trợ soạn thảo nội dung giải trình ban đầu. Tuy nhiên, nội dung do mô hình tạo ra vẫn cần được kiểm tra về số liệu và nguồn bằng chứng. Nếu không có cơ chế truy vết, chuyên viên tài chính phải đối chiếu lại văn bản với dữ liệu kế toán và tài liệu gốc, làm giảm lợi ích của bước soạn thảo tự động.'
        24 = 'Từ đó, khóa luận đặt ra vấn đề nghiên cứu: thiết kế hệ thống sinh giải trình chênh lệch ngân sách như thế nào để số liệu có thể truy vết về dữ liệu kế toán, nhận định nguyên nhân gắn với bằng chứng và hệ thống từ chối kết luận khi chưa đủ dữ liệu?'
        25 = 'Khoảng trống nghiên cứu xuất phát từ sự khác biệt giữa khả năng tạo văn bản của LLM và yêu cầu kiểm soát trong kế toán quản trị. LLM có thể tạo câu chữ trôi chảy, nhưng báo cáo quản trị còn yêu cầu số liệu chính xác và từng nhận định phải kiểm tra được từ nguồn.'
        26 = 'Trong thực tế, việc dùng AI qua các câu lệnh riêng lẻ chưa tạo thành một quy trình kiểm soát thống nhất. Vì vậy, khóa luận xem xét một kiến trúc kết hợp LLM với khối tính toán, truy xuất tài liệu và các quy tắc kiểm tra sau khi sinh. Mục tiêu và câu hỏi nghiên cứu được trình bày dưới đây.'
        82 = 'Các con số trong văn bản giải trình có thể đối soát với dữ liệu kế toán,'
        83 = 'Các nguyên nhân đã xác nhận được liên kết với tài liệu hoặc biên bản sự kiện,'
        87 = 'Các mô hình ngôn ngữ lớn có khả năng tạo văn bản tự nhiên nhưng có thể sinh thông tin không xuất hiện trong tài liệu nguồn. Hiện tượng này thường được gọi là ảo giác (hallucination) trong nghiên cứu xử lý ngôn ngữ tự nhiên (Ji và cộng sự, 2023). Rủi ro này cần được kiểm soát khi mô hình xử lý dữ liệu tài chính có cấu trúc và yêu cầu số học. LLM dự đoán từ tiếp theo theo xác suất, nên không thay thế một công cụ tính toán tất định.'
        88 = 'Các nghiên cứu trước cho thấy mô hình ngôn ngữ còn hạn chế trong suy luận số học trên dữ liệu tài chính. Trên bộ dữ liệu FinQA, mô hình được báo cáo đạt độ chính xác 65,05%, thấp hơn mức 91,16% của chuyên gia tài chính (Chen và cộng sự, 2021). Trên TAT-QA, các tác giả cũng ghi nhận lỗi liên quan đến dấu âm và dương của số liệu kế toán (Zhu và cộng sự, 2021). Sai dấu hoặc sai giá trị có thể làm thay đổi cách diễn giải khoản chênh lệch.'
        92 = 'Một hạn chế cần lưu ý của truy xuất vector là độ tương đồng ngữ nghĩa không trực tiếp kiểm tra quan hệ số học. Hai câu có cấu trúc giống nhau nhưng chứa các giá trị doanh thu khác nhau vẫn có thể nhận điểm tương đồng cao. Vì vậy, trong nghiệp vụ kế toán, kết quả truy xuất cần được kết hợp với bước kiểm tra số liệu thay vì dùng độ tương đồng vector làm căn cứ duy nhất.'
        94 = 'Tìm kiếm vector gần đúng cũng có thể không ưu tiên đúng các mã định danh như số hợp đồng hoặc mã khách hàng. Self-RAG và CRAG bổ sung bước đánh giá mức độ cần thiết hoặc mức độ phù hợp của tài liệu trước khi sinh văn bản (Asai và cộng sự, 2024; Yan và cộng sự, 2024). Tuy nhiên, các bước đánh giá này vẫn có thể tạo kết quả không ổn định. Trong bối cảnh tài chính, khóa luận kết hợp truy xuất lai với quy tắc kiểm tra mã, phạm vi và kỳ của tài liệu.'
        97 = 'Các nghiên cứu trước đã đề xuất cách đo mức độ gắn kết giữa văn bản và nguồn. Khung AIS (Attributable to Identified Sources) xem một phát biểu là có căn cứ khi người đọc có thể kiểm tra phát biểu đó từ tài liệu được chỉ định (Rashkin và cộng sự, 2023). Khung ALCE sử dụng hai chỉ số để đánh giá mức độ bao phủ và độ chính xác của trích dẫn (T. Gao và cộng sự, 2023). Cụ thể:'
        102 = 'Ngoài việc chấm nội dung đã sinh, hệ thống tài chính cần nhận biết khi bằng chứng chưa đủ để nêu nguyên nhân. Khi một khoản chênh lệch không có chứng từ giải thích, hệ thống nên thông báo thiếu hồ sơ và chuyển trường hợp đó cho người phụ trách xác minh. Nếu mô hình vẫn suy diễn một nguyên nhân không có chứng từ, nhận định này có thể được đưa vào báo cáo mà không có căn cứ kiểm tra.'
        103 = 'Vấn đề câu hỏi không có đáp án đã được nghiên cứu trước khi LLM trở nên phổ biến. Trong SQuAD, hệ thống nhận một đoạn văn và tìm câu trả lời cho câu hỏi trong đoạn văn đó. Rajpurkar, Jia và Liang (2018) chỉ ra rằng bộ dữ liệu ban đầu giả định mọi câu hỏi đều có đáp án. Nhóm tác giả xây dựng SQuAD 2.0 bằng cách bổ sung 53.775 câu hỏi không trả lời được, trong đó đoạn văn vẫn chứa các chi tiết có vẻ liên quan. Kết quả cho thấy mô hình có thể chọn câu trả lời dựa trên dấu hiệu bề mặt dù đoạn văn chưa cung cấp đủ thông tin. Cơ chế từ chối giúp giảm câu trả lời sai, nhưng từ chối quá nhiều cũng làm giảm mức độ hữu dụng của hệ thống.'
        107 = 'Để người dùng dựa vào hệ thống ở mức phù hợp, kết quả cần cho thấy dữ liệu và bằng chứng đã được sử dụng như thế nào. Lee và See (2004) cho rằng mức độ tin cậy của người dùng nên phù hợp với năng lực thực tế của hệ thống. Thiếu công cụ kiểm tra có thể khiến người dùng tin quá mức hoặc không muốn sử dụng kết quả. Doshi-Velez và Kim (2017) cũng nhấn mạnh vai trò của khả năng giải thích trong các tác vụ có hậu quả lớn khi xảy ra sai sót. Trong bối cảnh tài chính, điều này đòi hỏi số liệu và nhận định phải liên kết được với nguồn tương ứng.'
        108 = 'Các câu lệnh bằng ngôn ngữ tự nhiên không đủ để kiểm soát toàn bộ sai số của LLM. Vì vậy, kiến trúc đề xuất bổ sung một lớp kiểm tra bằng quy tắc xác định trước. Lớp này đối chiếu số liệu bằng mã chương trình, kiểm tra mã tài liệu và kích hoạt trạng thái từ chối khi thiếu bằng chứng phù hợp. Cơ chế này giúp người dùng phát hiện một số lỗi trước khi bản giải trình được đưa vào bước rà soát.'
        120 = 'Khoảng trống về cơ chế kiểm soát: Các nghiên cứu RAG nâng cao đã bổ sung bước tự đánh giá tài liệu và đầu ra, nhưng chưa tập trung vào các quy tắc đối chiếu số liệu, mã chứng từ và phạm vi tài liệu cho nghiệp vụ giải trình chênh lệch ngân sách.'
        121 = 'Để xử lý các khoảng trống trên, khóa luận đề xuất kiến trúc gồm bốn khối: (1) tính toán bằng quy tắc, (2) truy xuất chứng từ, (3) sinh văn bản có điều kiện và (4) kiểm chứng sau khi sinh. Chương 3 trình bày phương pháp thực nghiệm, bộ dữ liệu mô phỏng và các tiêu chí đánh giá.'
        136 = 'Bộ dữ liệu mô phỏng các hoạt động liên quan đến doanh thu và chi phí của năm khu công nghiệp trong 12 tháng. Dữ liệu gồm ngân sách, số thực tế, sổ theo dõi hợp đồng thuê, sổ cái chi tiết và kho chứng từ sự kiện. Quy trình sinh dữ liệu sử dụng random seed 26 để có thể tạo lại cùng một bộ dữ liệu. Các quy tắc tạo dữ liệu được xác định trước khi chạy thí nghiệm.'
        137 = 'Nghiên cứu thiết kế 12 loại kịch bản trong quá trình sinh dữ liệu. Mười kịch bản mô phỏng nguyên nhân có bằng chứng, như chấm dứt hợp đồng sớm, chậm bàn giao, thay đổi đơn giá thuê, sửa chữa đột xuất và sự kiện tài trợ vốn. Hai kịch bản còn lại dùng để kiểm tra cơ chế từ chối và lọc tài liệu: một nhóm không có chứng từ giải thích và một nhóm chèn tài liệu có từ khóa tương tự nhưng sai khu.'
        146 = 'Đầu vào của hệ thống gồm dữ liệu kế toán có cấu trúc, kho chứng từ dạng văn bản và yêu cầu giải trình cho một khoản chênh lệch. Đầu ra là dự thảo giải trình theo biểu mẫu kế toán quản trị. Hệ thống kiểm tra ba điều kiện: (1) số liệu khớp với kết quả tính toán, (2) nguyên nhân đã xác nhận đi kèm mã tài liệu hợp lệ và (3) hệ thống từ chối nêu nguyên nhân khi bằng chứng không đạt yêu cầu.'
        154 = 'Chiều hướng biến động được gán theo tính chất của dòng doanh thu hoặc chi phí. Với doanh thu cho thuê, hệ thống phân rã chênh lệch theo từng khách thuê dựa trên sổ theo dõi hợp đồng. Với chi phí, hệ thống lấy các giao dịch sổ cái có giá trị lớn trong kỳ. Kết quả của khối này là nguồn số liệu chuẩn cho các bước sau, qua đó giảm nguy cơ LLM tự tính hoặc thay đổi số liệu đã được cung cấp (Chen và cộng sự, 2021; Zhu và cộng sự, 2021).'
        172 = 'Năm thước đo chính và hai chỉ số bổ sung'
        173 = 'Khóa luận sử dụng năm thước đo chính để đánh giá số liệu, trích dẫn, nhận định và khả năng từ chối. Hai chỉ số Coverage và Risk được theo dõi bổ sung để phản ánh sự đánh đổi giữa mức độ trả lời và rủi ro trên phần đã trả lời. Công thức được trình bày tại Bảng 3.3.'
        178 = 'Thực nghiệm sử dụng ba lượt chạy cho mỗi cấu hình nhằm giảm mức độ phụ thuộc vào một lượt sinh riêng lẻ:'
        180 = 'Mỗi trường hợp được thực hiện bằng ba lệnh gọi API riêng biệt với cùng cấu hình mô hình, nhiệt độ và bộ tham số. Ba cấu hình, 34 trường hợp và ba lượt chạy tạo thành 306 bản ghi thực nghiệm (3 × 34 × 3 = 306).'
        182 = 'Điểm của từng cấu hình được tính riêng cho mỗi lượt chạy, sau đó báo cáo bằng giá trị trung bình và độ lệch chuẩn mẫu của ba giá trị này. Độ lệch chuẩn sử dụng mẫu số n - 1. Do chỉ có ba lượt chạy, chỉ số này được dùng để mô tả mức dao động quan sát được, không thay thế kiểm định suy luận. Trích dẫn và nhận định thiếu căn cứ được chấm bằng mã so khớp với đáp án chuẩn.'
        190 = 'Triển khai hệ thống trên nền tảng web'
        196 = 'Ứng dụng web minh họa cách người dùng đi từ danh sách chênh lệch đến số liệu, tài liệu, dự thảo giải trình và kết quả kiểm tra. Bản hiện tại là nguyên mẫu phục vụ trình diễn quy trình. Nghiên cứu chưa đo thời gian tiết kiệm hoặc mức độ dễ sử dụng trong môi trường doanh nghiệp.'
        205 = 'Về trích dẫn (Precite), M2 đạt 100,0% trong bộ thử nghiệm, cao hơn M1 6,5 điểm phần trăm. Các mã tài liệu mà M2 sử dụng đều thuộc tập chứng từ hợp lệ của đáp án chuẩn. Độ bao phủ trích dẫn (Reccite) của M2 đạt 95,2%, cao hơn M1 3,8 điểm phần trăm. Kết quả này phù hợp với mục tiêu đánh giá nguồn dẫn trong RQ2.'
        206 = 'Tỷ lệ nhận định thiếu căn cứ (Rateunsup) khác biệt rõ giữa ba cấu hình. M0 không nhận tài liệu nguồn nên tỷ lệ này là 100,0%. M1 đạt 29,3%, còn M2 đạt 5,4%, thấp hơn M1 23,9 điểm phần trăm. Trong phạm vi bộ dữ liệu thử nghiệm, kết quả cho thấy cấu trúc đầu ra và các cổng kiểm tra của M2 gắn với tỷ lệ nhận định thiếu căn cứ thấp hơn.'
        207 = 'Đối với khả năng từ chối (Accabs), M2 từ chối đúng 100% các trường hợp thiếu chứng từ qua ba lượt chạy. M0 đạt 11,1%, còn M1 đạt 0,0% vì vẫn nêu nguyên nhân trong các trường hợp bẫy. Kết quả này cung cấp bằng chứng cho RQ3 trong phạm vi ba trường hợp thiếu bằng chứng đã xây dựng.'
        221 = 'Tỷ lệ bao phủ của M2 đạt 91,2%, gần với mức 92,2% của M1. Vì vậy, mức lỗi thấp của M2 không chỉ đến từ việc từ chối nhiều trường hợp hơn. Trong bộ thử nghiệm, Risk trên phần M2 đã nêu nguyên nhân bằng 0,0%; kết quả này chưa cho phép suy rộng ra dữ liệu doanh nghiệp.'
        222 = 'Ở khâu truy xuất, Recall@5 đạt 100,0% trên các trường hợp có bằng chứng, nghĩa là tài liệu đúng xuất hiện trong năm kết quả đầu ở bộ thử nghiệm. Precision@5 đạt 33,8%, cho thấy danh sách vẫn chứa nhiều tài liệu ngoài đáp án chuẩn. Vì vậy, tầng sinh có cấu trúc và các bước kiểm tra sau khi sinh vẫn cần thiết để hạn chế việc sử dụng tài liệu không phù hợp.'
        230 = 'Ở M0, các con số khớp với đầu vào nhưng mô hình bổ sung cụm từ "driven entirely by TEN-060... starting occupancy" mà không dẫn tài liệu. Vì vậy, người duyệt không thể kiểm tra nguyên nhân này từ đầu ra. M0 còn sinh ký tự lặp trong "++$36.0k". M1 dẫn đúng EV-108 ở lượt minh họa, nhưng không có bước tự động chặn mã tài liệu sai ở các lượt khác. M2 yêu cầu mô hình tách đầu ra thành các trường và kiểm tra số liệu, mã khách thuê cùng mã chứng từ trước khi tạo đoạn văn cuối. Các quy tắc này giảm rủi ro phát hành đầu ra không khớp với dữ liệu đã cung cấp.'
        232 = 'Ghi chú: Bảng 4.4 minh họa cách ba cấu hình xử lý cùng một trường hợp chênh lệch, qua đó làm rõ sự khác biệt giữa văn bản sinh tự do (M0, M1) và đầu ra có cấu trúc (M2). Nội dung được trích từ lượt chạy thứ nhất của trường hợp 2026-05_PROP-A_Leasing_revenue; đầu ra đầy đủ được trình bày tại Phụ lục A.2.'
        245 = 'Việc chia kết quả theo kịch bản giúp xác định lỗi xuất hiện ở khâu tính toán, truy xuất hay liên kết nội dung. Tuy nhiên, số mẫu giữa các nhóm không đồng đều. Nhóm chấm dứt hợp đồng sớm có nhiều trường hợp nhất, trong khi một số nhóm chỉ có một hoặc hai trường hợp. Vì vậy, một lỗi đơn lẻ có thể làm thay đổi mạnh tỷ lệ của nhóm nhỏ. Kết quả theo nhóm được dùng để nhận diện điểm cần kiểm tra thêm, không đại diện cho toàn bộ nghiệp vụ ngoài thực tế.'
        247 = 'Nhóm thay đổi đơn giá thuê gồm hai trường hợp phát sinh từ phụ lục điều chỉnh giá thuê hoặc phí tiện ích. M2 đạt độ chính xác số liệu 100,0% và không ghi nhận nhận định thiếu căn cứ trong nhóm này. Trường hợp xử lý kế toán về phân bổ doanh thu theo thời gian cũng đạt 100,0% trên hai thước đo được báo cáo. Tuy nhiên, nhóm chỉ có một trường hợp nên kết quả cần được xem là mô tả của bộ thử nghiệm.'
        252 = 'Nhóm sự kiện tài trợ vốn gồm hai trường hợp, có tỷ lệ nhận định thiếu căn cứ 50,0% dù độ chính xác số liệu đạt 100,0%. Kết quả cho thấy quy tắc hiện tại chưa xử lý tốt một số điều khoản tín dụng phức tạp. Với ba trường hợp thiếu bằng chứng, M2 từ chối nêu nguyên nhân trong cả chín lượt chạy. Kết quả này mô tả hành vi của hệ thống trên các tình huống bẫy đã xây dựng.'
        258 = 'Phép thử đầu tiên xem xét phản ứng của hệ thống khi có chênh lệch nhưng không có chứng từ giải thích. LLM có thể tạo một nguyên nhân nghe hợp lý dù thông tin đầu vào chưa đủ (Ji và cộng sự, 2023). Trong quản trị tài chính, nhận định không có căn cứ có thể ảnh hưởng đến quyết định của người đọc báo cáo (Parasuraman & Riley, 1997). Vì vậy, hệ thống cần có cơ chế từ chối nêu nguyên nhân khi không tìm thấy bằng chứng phù hợp (Kamath và cộng sự, 2020).'
        259 = 'Phép thử sử dụng ba trường hợp: chi phí tiếp thị và chi phí an ninh của PROP-B tháng 5/2026, cùng chi phí tiếp thị của PROP-E tháng 7/2026. Các trường hợp này có số liệu kế toán nhưng không có chứng từ thuyết minh. Mỗi trường hợp được gọi API ba lần với cùng cấu hình, tạo ra chín quan sát cho mỗi cấu hình mô hình.'
        260 = 'M1 nêu nguyên nhân trong cả chín lượt chạy và không thực hiện lần từ chối nào. Tại PROP-E, M1 quy chênh lệch cho chi phí dịch vụ khác dù không có tài liệu hỗ trợ. Tại PROP-B, M1 dùng biên bản chậm bàn giao để giải thích chi phí vệ sinh. M2 áp dụng quy tắc liên kết nội dung, không tìm thấy tài liệu hợp lệ và chuyển kết luận thành yêu cầu xác minh trong cả chín lượt chạy. Tuy nhiên, năm lượt M2 bị cổng số liệu gắn cờ nhầm khi mô hình viết 0.7467 thay cho 74,67%. Đây là lỗi chuẩn hóa định dạng số của bộ phân tích, không phải khác biệt về nguyên nhân nghiệp vụ.'
        261 = 'Phép thử thứ hai xem xét nguy cơ chọn nhầm tài liệu do trùng từ khóa. Tài liệu có từ vựng tương tự nhưng không chứa bằng chứng phù hợp có thể được xếp hạng cao trong truy xuất ngữ nghĩa (Y. Gao và cộng sự, 2023; Yan và cộng sự, 2024). Trong doanh nghiệp có nhiều dự án, tài liệu cùng kỳ có thể thuộc các khu khác nhau. Nếu phạm vi tài liệu không được kiểm tra, bản giải trình có thể dẫn nhầm chứng từ (COSO, 2013).'
        263 = 'Trong bộ thử nghiệm, Recall@5 đạt 100,0%, nghĩa là EV-108 xuất hiện trong năm kết quả đầu của trường hợp minh họa. Precision@5 đạt 33,8%, tương ứng khoảng 66,2% tài liệu trong các danh sách truy xuất không thuộc đáp án chuẩn. Kết quả cho thấy tìm kiếm chỉ thu hẹp tập tài liệu; các bước kiểm tra phạm vi, mã chứng từ và nội dung vẫn cần thiết trước khi phát hành bản giải trình.'
    }
    foreach ($key in ($replacements.Keys | Sort-Object {[int]$_})) { Set-ParagraphText -Index ([int]$key) -Text $replacements[$key] }

    foreach ($p in $paragraphs) {
        $texts = @($p.SelectNodes('.//w:t', $ns))
        if ($texts.Count -gt 0) {
            $joined = ($texts | ForEach-Object {$_.InnerText}) -join ''
            $fixed = $joined.Replace('Gao và cộng sự (2023b)', 'T. Gao và cộng sự (2023)').Replace('(Gao và cộng sự, 2023b)', '(T. Gao và cộng sự, 2023)').Replace('(Gao và cộng sự, 2023a', '(Y. Gao và cộng sự, 2023')
            if ($fixed -ne $joined) {
                $texts[0].InnerText = $fixed
                for ($j = 1; $j -lt $texts.Count; $j++) { $texts[$j].InnerText = '' }
            }
        }
    }

    $body = $xml.SelectSingleNode('//w:body', $ns)
    $sectPr = $body.SelectSingleNode('./w:sectPr', $ns)
    function Add-BodyNode($node) { [void]$body.InsertBefore($node, $sectPr) }
    function Add-Heading([string]$text, [int]$level, [bool]$pageBreak = $false) {
        $size = if ($level -eq 0) { 30 } elseif ($level -eq 1) { 28 } else { 26 }
        $align = if ($level -le 1) { 'center' } else { 'left' }
        Add-BodyNode (New-Paragraph -Xml $xml -Text $text -Bold $true -Size $size -Align $align -FirstLine 0 -OutlineLevel ([Math]::Min($level,2)) -KeepNext $true -PageBreakBefore $pageBreak)
    }
    function Add-BodyText([string]$text) { Add-BodyNode (New-Paragraph -Xml $xml -Text $text -FirstLine 567) }
    function Add-Caption([string]$text) { Add-BodyNode (New-Paragraph -Xml $xml -Text $text -Bold $true -Align 'center' -FirstLine 0 -KeepNext $true) }
    function Add-Prompt([string]$promptText) {
        foreach ($line in ($promptText -split "`r?`n")) {
            Add-BodyNode (New-Paragraph -Xml $xml -Text $line -Size 21 -LeftIndent 360 -FirstLine 0)
        }
    }

    Add-BodyNode (New-PageBreak $xml)
    Add-Heading 'PHỤ LỤC' 0
    Add-BodyText 'Các phụ lục dưới đây trình bày dữ liệu, cấu hình, câu lệnh và quy tắc chấm được sử dụng trong thực nghiệm. Toàn bộ dữ liệu là dữ liệu mô phỏng.'

    Add-Heading 'PHỤ LỤC A. BỘ DỮ LIỆU VÀ KẾT QUẢ CHI TIẾT' 1 $true
    Add-Heading 'A.1. Tổng quan bộ dữ liệu' 2
    $manifestPath = Join-Path $workspace 'app\backend\data\dataset_v1\manifest.json'
    $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $manifestRows = @(
        ,@('Phiên bản dữ liệu', $manifest.dataset_version)
        ,@('Random seed', [string]$manifest.seed)
        ,@('Số khu công nghiệp mô phỏng', '5')
        ,@('Số khách thuê', [string]$manifest.tenants)
        ,@('Số tài liệu bằng chứng', [string]$manifest.evidence_docs)
        ,@('Số dòng sổ cái', [string]$manifest.gl_rows)
        ,@('Số trường hợp trọng yếu', [string]$manifest.material_cases_engine)
        ,@('Số trường hợp có đáp án chuẩn', [string]$manifest.gold_cases)
        ,@('Thời điểm tạo dữ liệu UTC', [string]$manifest.created_utc)
    )
    Add-Caption 'Bảng A.1. Thông tin bộ dữ liệu mô phỏng'
    Add-BodyNode (New-Table -Xml $xml -Headers @('Thuộc tính','Giá trị') -Rows $manifestRows -Widths @(3300,4800) -FontSize 21)
    Add-BodyText 'Ngưỡng trọng yếu được áp dụng theo nhóm khoản mục: doanh thu 50.000 USD hoặc 5%; chi phí 30.000 USD hoặc 15%; khoản mục cấp công ty 100.000 USD hoặc 10%. Một trường hợp được đưa vào bộ kiểm thử khi thỏa ít nhất một trong hai điều kiện về giá trị tuyệt đối hoặc tỷ lệ.'

    $dataFileRows = @(
        ,@('budget_rent.csv và actual_rent.csv','Ngân sách và thực tế doanh thu thuê theo khách thuê')
        ,@('budget_line.csv và actual_line.csv','Ngân sách và thực tế theo dòng P&L')
        ,@('gl.csv','Sổ cái chi tiết mô phỏng')
        ,@('tenants.csv','Danh mục khách thuê mô phỏng')
        ,@('evidence.json','Kho 55 tài liệu sự kiện')
        ,@('evidence_packs.json','Năm tài liệu truy xuất cho từng trường hợp')
        ,@('cases.json','Danh sách 34 trường hợp chênh lệch')
        ,@('gold_labels.json','Nguyên nhân, tài liệu đúng và yêu cầu từ chối')
    )
    Add-Caption 'Bảng A.2. Các tệp dữ liệu chính'
    Add-BodyNode (New-Table -Xml $xml -Headers @('Tệp','Nội dung') -Rows $dataFileRows -Widths @(3000,5100) -FontSize 20)

    Add-Heading 'A.2. Đầu ra của trường hợp minh họa' 2
    $caseId = '2026-05_PROP-A_Leasing_revenue'
    $cases = @(Get-Content -LiteralPath (Join-Path $workspace 'app\backend\data\dataset_v1\cases.json') -Raw -Encoding UTF8 | ConvertFrom-Json)
    $case = $cases | Where-Object {$_.case_id -eq $caseId} | Select-Object -First 1
    $goldAll = Get-Content -LiteralPath (Join-Path $workspace 'app\backend\data\dataset_v1\gold_labels.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $gold = $goldAll.$caseId
    $caseRows = @(
        ,@('Mã trường hợp',$case.case_id)
        ,@('Kỳ và khu',$case.month + ' / ' + $case.property)
        ,@('Khoản mục',$case.pl_line)
        ,@('Ngân sách / Thực tế',('{0:N0} / {1:N0}' -f $case.budget,$case.actual))
        ,@('Chênh lệch',('{0:N0} ({1:P2})' -f $case.variance,$case.variance_pct))
        ,@('Nguyên nhân chuẩn',($gold.gold_causes -join ', '))
        ,@('Tài liệu chuẩn',($gold.gold_evidence -join ', '))
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Trường','Giá trị') -Rows $caseRows -Widths @(2600,5500) -FontSize 20)
    $records = Get-Content -LiteralPath (Join-Path $workspace 'app\backend\results\raw\records_full.jsonl') -Encoding UTF8 | ForEach-Object { $_ | ConvertFrom-Json }
    $exampleRecords = @($records | Where-Object {$_.case_id -eq $caseId -and $_.rep -eq 0} | Sort-Object mode)
    foreach ($rec in $exampleRecords) {
        Add-Heading (($rec.mode.ToUpper()) + ' - lượt chạy 1') 2
        Add-BodyText ([string]$rec.output.draft_comment)
        $detail = if ($rec.mode -eq 'm2') {
            'Trạng thái: ' + $rec.verdict.overall + '; số liệu được đối chiếu với budget, actual và variance; EV-108 hợp lệ; nhận định xác nhận có mã bằng chứng.'
        } elseif ($rec.mode -eq 'm1') {
            'Trạng thái kiểm tra kỹ thuật: ' + $rec.verdict.overall + '; đầu ra có EV-108 nhưng cấu hình M1 không bắt buộc phân rã nhận định thành trường có cấu trúc.'
        } else {
            'Đầu ra không có mã tài liệu. Cụm nguyên nhân về TEN-060 không thể kiểm tra chỉ từ văn bản M0; chuỗi "++$36.0k" cũng cho thấy lỗi định dạng.'
        }
        Add-BodyText $detail
    }

    Add-Heading 'A.3. Danh sách 34 trường hợp và đáp án chuẩn' 2
    $caseCatalog = @()
    foreach ($c in ($cases | Sort-Object case_id)) {
        $g = $goldAll.($c.case_id)
        $cause = if ($g.abstain) { 'abstain' } elseif ($g.gold_causes.Count -gt 0) { $g.gold_causes -join ', ' } else { '' }
        $ev = if ($g.gold_evidence.Count -gt 0) { $g.gold_evidence -join ', ' } else { 'Không có' }
        $caseCatalog += ,@($c.case_id, ($c.property + ' / ' + $c.month), $c.pl_line, $cause, $ev)
    }
    Add-BodyNode (New-Table -Xml $xml -Headers @('Case ID','Khu / kỳ','Khoản mục','Nguyên nhân chuẩn','Bằng chứng') -Rows $caseCatalog -Widths @(2350,1100,1750,1700,1200) -FontSize 18)

    Add-Heading 'A.4. Kết quả theo lượt chạy và kịch bản' 2
    $summaryRep = Import-Csv -LiteralPath (Join-Path $workspace 'app\backend\results\summary_by_rep.csv')
    $repRows = @()
    foreach ($r in $summaryRep) {
        $repRows += ,@($r.mode.ToUpper(),([int]$r.rep + 1),('{0:P1}' -f [double]$r.numeric_accuracy),$r.citation_precision,$r.citation_recall,$r.unsupported_claim_rate,$r.'abstain_recall(trap)',$r.coverage,$r.risk_on_asserted)
    }
    Add-Caption 'Bảng A.3. Kết quả của từng lượt chạy'
    Add-BodyNode (New-Table -Xml $xml -Headers @('Mô hình','Lượt','Accnum','Precite','Reccite','Rateunsup','Accabs','Coverage','Risk') -Rows $repRows -Widths @(700,500,850,850,850,900,750,850,850) -FontSize 17)
    $scenarioCsv = Import-Csv -LiteralPath (Join-Path $workspace 'app\backend\results\by_scenario.csv')
    $scenarioRows = @()
    foreach ($r in ($scenarioCsv | Where-Object {$_.mode -eq 'm2'})) {
        $scenarioRows += ,@($r.scenario,$r.n,$r.numeric_accuracy,$r.unsupported_rate)
    }
    Add-Caption 'Bảng A.4. Kết quả M2 theo nhóm kịch bản'
    Add-BodyNode (New-Table -Xml $xml -Headers @('Nhóm kịch bản','Số case','Độ chính xác số liệu','Tỷ lệ nhận định thiếu căn cứ') -Rows $scenarioRows -Widths @(2600,900,2100,2500) -FontSize 19)
    Add-BodyText 'Tệp records_full.jsonl lưu toàn bộ 306 đầu ra và kết quả từng cổng kiểm tra. Do mỗi bản ghi chứa cả JSON đầu ra và chi tiết đối chiếu, tệp này được lưu như phụ lục điện tử tại app/backend/results/raw/records_full.jsonl thay vì chèn toàn bộ vào Word.'

    Add-Heading 'PHỤ LỤC B. PROMPT VÀ CẤU HÌNH SINH' 1 $true
    Add-Heading 'B.1. Cấu hình thực nghiệm' 2
    $runCfg = Get-Content -LiteralPath (Join-Path $workspace 'app\backend\results\run_config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $cfgRows = @(
        ,@('Model ID',$runCfg.model)
        ,@('Temperature',[string]$runCfg.temperature)
        ,@('Phiên bản prompt',$runCfg.prompt_version)
        ,@('Phiên bản dữ liệu',$runCfg.dataset_version)
        ,@('Số lượt chạy',[string]$runCfg.k)
        ,@('Số case',[string]$runCfg.n_cases)
        ,@('Git commit',$runCfg.git_head)
        ,@('Thời điểm bắt đầu UTC',$runCfg.started_utc)
        ,@('Truy xuất dense trong evidence packs',[string]$runCfg.dense_in_packs)
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Tham số','Giá trị') -Rows $cfgRows -Widths @(3300,4800) -FontSize 20)
    foreach ($mode in @('m0','m1','m2')) {
        Add-Heading (('B.' + (@{'m0'='2';'m1'='3';'m2'='4'}[$mode]) + '. Prompt ' + $mode.ToUpper())) 2
        $prompt = Get-Content -LiteralPath (Join-Path $workspace ('app\backend\vwb\generation\prompts_llm\' + $mode + '.txt')) -Raw -Encoding UTF8
        Add-Prompt $prompt
    }

    Add-Heading 'PHỤ LỤC C. THƯỚC ĐO VÀ QUY TẮC KIỂM TRA' 1 $true
    Add-Heading 'C.1. Định nghĩa thước đo' 2
    $metricRows = @(
        ,@('Accnum','Tỷ lệ giá trị số trong đầu ra khớp trường dữ liệu được phép; giữ dấu và đơn vị.')
        ,@('Precite','Tỷ lệ mã tài liệu được trích dẫn thuộc tập bằng chứng chuẩn.')
        ,@('Reccite','Tỷ lệ tài liệu trong đáp án chuẩn được đầu ra trích dẫn.')
        ,@('Rateunsup','Tỷ lệ nhận định nguyên nhân không gắn với ít nhất một mã bằng chứng chuẩn.')
        ,@('Accabs','Tỷ lệ trường hợp thiếu bằng chứng mà hệ thống không nêu nguyên nhân.')
        ,@('Coverage','Tỷ lệ trường hợp hệ thống đưa ra ít nhất một nguyên nhân đã xác nhận.')
        ,@('Risk','Tỷ lệ trường hợp có lỗi trong phần hệ thống đã nêu nguyên nhân.')
        ,@('Precision@5','Tỷ lệ tài liệu đúng trong tối đa năm kết quả truy xuất.')
        ,@('Recall@5','Tỷ lệ tài liệu chuẩn xuất hiện trong tối đa năm kết quả truy xuất.')
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Chỉ số','Cách hiểu trong khóa luận') -Rows $metricRows -Widths @(1800,6300) -FontSize 20)
    Add-BodyText 'Mỗi chỉ số được tính riêng theo từng lượt chạy. Giá trị báo cáo là trung bình của ba lượt và độ lệch chuẩn mẫu: SD = căn bậc hai của tổng bình phương độ lệch chia cho n - 1, với n = 3. Vì số lượt chạy nhỏ, SD chỉ mô tả mức dao động quan sát được.'

    Add-Heading 'C.2. Bốn cổng kiểm tra' 2
    $gateRows = @(
        ,@('Cổng số liệu','Tách giá trị số khỏi đầu ra và so với budget, actual, variance, contributor hoặc số trong tài liệu đã trích dẫn.','Gắn cờ khi không tìm thấy giá trị tương ứng hoặc sai dấu, đơn vị.')
        ,@('Cổng trích dẫn','Kiểm tra mã EV có tồn tại, đúng khu và không thuộc kỳ sau kỳ báo cáo.','Gắn cờ mã không tồn tại, sai khu hoặc sai kỳ.')
        ,@('Cổng nhận định','Kiểm tra mỗi drivers_confirmed có ít nhất một mã tài liệu đã vượt cổng trích dẫn.','Gắn cờ nhận định không có mã bằng chứng hợp lệ.')
        ,@('Cổng từ chối','Xác định evidence pack có tài liệu liên kết nội dung với case hay không.','Khi không có tài liệu liên kết, đầu ra phải abstain và không có drivers_confirmed.')
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Cổng','Cách kiểm tra','Kết quả khi không đạt') -Rows $gateRows -Widths @(1500,4100,2500) -FontSize 19)

    Add-Heading 'PHỤ LỤC D. KHO BẰNG CHỨNG MÔ PHỎNG' 1 $true
    $evidence = @(Get-Content -LiteralPath (Join-Path $workspace 'app\backend\data\dataset_v1\evidence.json') -Raw -Encoding UTF8 | ConvertFrom-Json)
    $evRows = @()
    foreach ($g in ($evidence | Group-Object type | Sort-Object Name)) { $evRows += ,@($g.Name,[string]$g.Count) }
    Add-BodyText 'Kho bằng chứng gồm 55 tài liệu mô phỏng. Mỗi tài liệu có doc_id, loại tài liệu, khu áp dụng, kỳ hiệu lực, mức thẩm quyền, tiêu đề và nội dung. Hai tài liệu distractor_memo được tạo để kiểm tra bộ lọc phạm vi.'
    Add-BodyNode (New-Table -Xml $xml -Headers @('Loại tài liệu','Số lượng') -Rows $evRows -Widths @(5600,2500) -FontSize 20)
    Add-BodyText 'Ví dụ EV-108 thuộc nhóm handover_minutes, áp dụng cho PROP-A và kỳ 2026-05. Tài liệu này là bằng chứng chuẩn cho trường hợp 2026-05_PROP-A_Leasing_revenue.'

    Add-Heading 'PHỤ LỤC E. CÁC LỖI ĐÁNG CHÚ Ý' 1 $true
    $errorRows = @(
        ,@('Định dạng tỷ lệ','Mô hình viết 0.0845 hoặc 0.7467 thay cho 8,45% hoặc 74,67%.','Bộ phân tích có thể gắn cờ dù hai cách biểu diễn tương đương. Cần chuẩn hóa số thập phân trước khi so sánh.')
        ,@('Nhận định thiếu căn cứ','M0 và M1 có thể nêu nguyên nhân khi không có chứng từ phù hợp.','Đo bằng Rateunsup và kiểm tra riêng ba case thiếu bằng chứng.')
        ,@('Tài liệu gây nhiễu','Tài liệu trùng từ khóa nhưng sai khu có thể xuất hiện trong danh sách truy xuất.','Kiểm tra property và period trước khi cho phép trích dẫn.')
        ,@('Hồ sơ tài trợ vốn','M2 có Rateunsup 50,0% trên hai case financing_event.','Cỡ mẫu nhỏ; cần bổ sung quy tắc cho điều khoản tín dụng và tăng số case.')
        ,@('Định dạng văn bản','M0 sinh chuỗi "++$36.0k" trong trường hợp minh họa.','Cần chuẩn hóa định dạng trước khi hiển thị.')
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Loại lỗi','Biểu hiện','Cách xử lý hoặc giới hạn') -Rows $errorRows -Widths @(1800,3000,3300) -FontSize 19)

    Add-Heading 'PHỤ LỤC F. LUỒNG DEMO WEB APP' 1 $true
    $demoSteps = @(
        '1. Hàng chờ chênh lệch: người dùng chọn khu, kỳ và khoản mục cần giải trình.',
        '2. Tổng quan trường hợp: giao diện hiển thị ngân sách, thực tế, chênh lệch và các đối tượng đóng góp.',
        '3. Bằng chứng: người dùng xem năm tài liệu truy xuất, phạm vi áp dụng và phần nội dung liên quan.',
        '4. Dự thảo: hệ thống hiển thị số liệu quan sát, nguyên nhân đã xác nhận, nội dung cần xác minh và đoạn giải trình.',
        '5. Kiểm tra: giao diện cho biết kết quả của cổng số liệu, trích dẫn, nhận định và từ chối.',
        '6. Quyết định: chuyên viên FP&A rà soát, chỉnh sửa nếu cần và quyết định chấp nhận hoặc yêu cầu bổ sung hồ sơ.'
    )
    foreach ($step in $demoSteps) { Add-BodyText $step }
    Add-BodyText 'Web-app hiện là nguyên mẫu trình diễn. Trạng thái verified chỉ cho biết đầu ra đã vượt qua các quy tắc được cài đặt; trạng thái này không thay thế phê duyệt của chuyên viên FP&A.'

    Add-Heading 'PHỤ LỤC G. THÔNG TIN TÁI LẬP THỰC NGHIỆM' 1 $true
    $reproRows = @(
        ,@('Mã nguồn thực nghiệm','app/backend/vwb')
        ,@('Dữ liệu','app/backend/data/dataset_v1')
        ,@('Kết quả tổng hợp','app/backend/results/summary.csv; summary_by_rep.csv; by_scenario.csv')
        ,@('Đầu ra đầy đủ','app/backend/results/raw/records_full.jsonl')
        ,@('Phiên bản Python','>= 3.12')
        ,@('Thư viện chính','pandas 2.2-<3.0; FastAPI 0.115-<1.0; rank-bm25 0.2.2-<0.3.0; google-genai 2.29-<3.0; FlagEmbedding 1.4.2-<2.0')
        ,@('Random seed','26')
        ,@('Git commit của lần chạy','f33c681')
    )
    Add-BodyNode (New-Table -Xml $xml -Headers @('Thành phần','Thông tin') -Rows $reproRows -Widths @(2600,5500) -FontSize 19)
    Add-BodyText 'Để kiểm tra lại kết quả, cần giữ nguyên dataset_v1, prompt_v1, model ID, nhiệt độ 0,2 và các tệp evidence_packs cùng gold_labels. Do API có thể thay đổi theo thời gian, lần chạy mới cần lưu ngày chạy, phiên bản SDK và model ID thực tế trả về trong log.'

    Write-ZipText $zip 'word/document.xml' $xml.OuterXml

}
finally {
    $zip.Dispose()
}

Write-Output $outputPath
