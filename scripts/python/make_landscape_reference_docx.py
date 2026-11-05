#!/usr/bin/env python3
"""Write a Pandoc reference .docx whose page is A4 landscape with narrow
margins, so the wide crosswalk tables in a volume's Word download stay legible.

Usage: pandoc --print-default-data-file reference.docx | \
       make_landscape_reference_docx.py <out.docx>

Pandoc takes page size and margins from the reference document's section
properties, and its default reference has none, so this adds them.
"""
import io
import sys
import zipfile

PAGE = (
    '<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
    '<w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" '
    'w:header="360" w:footer="360" w:gutter="0"/>'
)


def main():
    out_path = sys.argv[1]
    src = zipfile.ZipFile(io.BytesIO(sys.stdin.buffer.read()))
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                text = data.decode("utf-8")
                if "</w:footnotePr>" not in text:
                    sys.exit("make_landscape_reference_docx: unexpected reference.docx layout")
                text = text.replace("</w:footnotePr>", "</w:footnotePr>" + PAGE, 1)
                data = text.encode("utf-8")
            out.writestr(item, data)


if __name__ == "__main__":
    main()
