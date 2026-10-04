/**
 * Xuat 1 chuong markdown -> .docx theo dinh dang Vien (docs/quy_dinh_vien.md):
 * A4 · Times New Roman · body 13 justify · gian dong 1,5 · before/after 6pt ·
 * H1 16 HOA dam giua · H2 14 dam trai · so trang cuoi trang canh phai ·
 * ten hinh tren (dam 13), "Nguon:" duoi-phai (nghieng 11).
 *
 * Chay:  node app/tools/export_docx.js thesis/chuong1.md thesis/chuong1.docx
 * Quy uoc: fence ```mermaid duoc thay bang anh thesis/figures/hinh_<x>_<y>.png,
 * lay caption tu dong "**Hình x.y:** ..." ngay sau fence. Noi dung sau "---" bi bo
 * (ghi chu bien tap). Doan trong ⟦…⟧ to highlight vang.
 */
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, Document, Footer, HeadingLevel, ImageRun, LevelFormat,
  PageNumber, Packer, Paragraph, TextRun,
} = require("docx");

const [, , IN, OUT] = process.argv;
if (!IN || !OUT) { console.error("usage: node export_docx.js in.md out.docx"); process.exit(1); }
const ROOT = path.resolve(__dirname, "..", "..");
const md = fs.readFileSync(path.resolve(ROOT, IN), "utf8");

const CM = 567; // 1 cm ~ 567 twips
const BODY = { size: 26, font: "Times New Roman" }; // 13pt

// --- inline markdown -> TextRun[] (ho tro **bold**, *italic*, ⟦highlight⟧) ---
function runs(text, extra = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|⟦[^⟧]*⟧)/g;
  let last = 0, m;
  const push = (t, o) => { if (t) out.push(new TextRun({ text: t, ...BODY, ...extra, ...o })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), {});
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith("⟦")) push(tok, { highlight: "yellow" });
    else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last), {});
  return out;
}

const SPACING = { line: 360, before: 120, after: 120 }; // 1.5 line, 6pt/6pt
const children = [];
const lines = md.split(/\r?\n/);
let i = 0, stopped = false;

while (i < lines.length && !stopped) {
  const line = lines[i];

  if (/^---\s*$/.test(line)) { stopped = true; break; }        // ghi chu bien tap -> bo
  if (line.startsWith(">") || /^\s*$/.test(line) || line.startsWith("<!--")) { i++; continue; }

  if (line.startsWith("# ")) {                                  // H1: 16 HOA dam giua
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER,
      spacing: { line: 360, before: 0, after: 240 },
      children: [new TextRun({ text: line.slice(2).toUpperCase(), bold: true, size: 32, font: "Times New Roman", color: "000000" })],
    }));
    i++; continue;
  }
  if (line.startsWith("## ")) {                                 // H2: 14 dam trai
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2, alignment: AlignmentType.LEFT,
      spacing: { line: 360, before: 240, after: 120 },
      children: [new TextRun({ text: line.slice(3), bold: true, size: 28, font: "Times New Roman", color: "000000" })],
    }));
    i++; continue;
  }
  if (line.startsWith("```mermaid")) {                          // fence -> anh + caption + nguon
    while (i < lines.length && !/^```\s*$/.test(lines[i + 1] ?? "")) i++;
    i += 2; // qua dong ```
    let caption = "", source = "Nguồn: tác giả đề xuất.";
    while (i < lines.length && /^\s*$/.test(lines[i])) i++;
    if (lines[i] && lines[i].includes("Hình")) {
      let cap = lines[i].replace(/<!--.*?-->/g, "").trim();
      const sm = cap.match(/\*Nguồn:[^*]*\*/);
      if (sm) { source = sm[0].slice(1, -1).trim(); cap = cap.replace(sm[0], ""); }
      caption = cap.replace(/\*\*/g, "").trim();
      i++;
    }
    const fig = caption.match(/Hình\s+(\d+)\.(\d+)/);
    const imgPath = path.resolve(ROOT, "thesis", "figures", fig ? `hinh_${fig[1]}_${fig[2]}.png` : "missing.png");
    const buf = fs.readFileSync(imgPath);
    const dim = { width: 620, height: Math.round(620 * 660 / 2360) };
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 240, before: 240, after: 60 },
      children: [new TextRun({ text: caption, bold: true, size: 26, font: "Times New Roman" })] }));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 240, before: 0, after: 0 },
      children: [new ImageRun({ type: "png", data: buf, transformation: dim })] }));
    children.push(new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { line: 240, before: 60, after: 240 },
      children: [new TextRun({ text: source, italics: true, size: 22, font: "Times New Roman" })] }));
    continue;
  }
  if (line.startsWith("- ")) {                                  // bullet
    children.push(new Paragraph({
      numbering: { reference: "dash", level: 0 },
      alignment: AlignmentType.JUSTIFIED, spacing: SPACING,
      children: runs(line.slice(2)),
    }));
    i++; continue;
  }
  children.push(new Paragraph({                                 // body
    alignment: AlignmentType.JUSTIFIED, spacing: SPACING, children: runs(line),
  }));
  i++;
}

const doc = new Document({
  styles: { default: { document: { run: BODY } } },
  numbering: { config: [{ reference: "dash", levels: [{
    level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: BODY },
  }] }] },
  sections: [{
    properties: { page: { margin: {
      top: Math.round(1.5 * CM), bottom: Math.round(2.5 * CM),
      left: Math.round(2.5 * CM), right: Math.round(2.0 * CM),
      header: CM, footer: CM,
    } } },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 24, font: "Times New Roman" })],
    })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(path.resolve(ROOT, OUT), b);
  console.log("Saved", OUT, b.length, "bytes;", children.length, "paragraphs");
});
