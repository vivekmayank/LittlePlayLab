import base64,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
obj={f.stem:base64.b64encode(f.read_bytes()).decode() for f in (root/'private-pdfs').glob('*.pdf')}
(root/'lib/pdf-data.ts').write_text('export const pdfData:Record<string,string>='+json.dumps(obj)+';\n')
