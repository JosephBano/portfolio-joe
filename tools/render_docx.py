#!/usr/bin/env python3
"""
tools/render_docx.py — Derivador de documentos conforme a ATS (ADR-001, RF-GEN-003, RF-GEN-004)

Contrato fijado en plan.md y ADR-001:
- Entrada: ruta de archivo Markdown (cv.md)
- Salida: ruta de archivo .docx (cv.docx)
- Una sola dependencia: python-docx
- Dos argumentos de ruta posicionales
- Error explícito ante cualquier construcción de Markdown no admitida
"""

import sys
import os
import re
import xml.sax.saxutils as saxutils
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.opc.constants import RELATIONSHIP_TYPE

def add_hyperlink(paragraph, url, text, font_name="Calibri", font_size_pt=10, is_bold=False):
    """Inserta un hipervínculo nativo OpenXML en el párrafo."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(
        f'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        f'r:id="{r_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
    )
    new_run = parse_xml('<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    rPr = parse_xml(
        f'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'<w:sz w:val="{int(font_size_pt * 2)}"/>'
        f'<w:color w:val="0563C1"/>'
        f'<w:u w:val="single"/>'
        f'</w:rPr>'
    )
    if is_bold:
        rPr.append(parse_xml('<w:b xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
    new_run.append(rPr)
    escaped_text = saxutils.escape(text)
    t = parse_xml(
        f'<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        f'xml:space="preserve">{escaped_text}</w:t>'
    )
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def _fail_residual(plain, line_num):
    """El marcado que no se consumió nunca se degrada en silencio (ADR-001, R-01)."""
    if '*' in plain:
        print(
            f"ERROR [render_docx]: Línea {line_num}: marcado de énfasis sin cerrar o no admitido: "
            f"{plain.strip()!r}. Admitidos: **negrita**, *cursiva*, [texto](url).",
            file=sys.stderr,
        )
        sys.exit(1)

def parse_inline(paragraph, text, font_name="Calibri", default_size=11, default_color=None, line_num=0):
    """
    Parsea tokens inline: enlaces [texto](url), negritas **texto** y cursivas *texto*.
    Cualquier elemento no admitido (imágenes ![], código ``, énfasis sin cerrar)
    provoca error explícito: nunca se emite al documento tal cual.
    """
    # Grupo 1 y 2: [texto](url) · Grupo 3: **negrita** · Grupo 4: *cursiva*
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*\n]+)\*')

    last_idx = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        # Texto plano anterior al match
        if start > last_idx:
            plain = text[last_idx:start]
            _fail_residual(plain, line_num)
            run = paragraph.add_run(plain)
            run.font.name = font_name
            run.font.size = Pt(default_size)
            if default_color:
                run.font.color.rgb = default_color

        link_text, link_url, bold_text, italic_text = match.groups()
        if link_text is not None:
            # Es un hipervínculo
            add_hyperlink(paragraph, link_url, link_text, font_name=font_name, font_size_pt=default_size)
        elif bold_text is not None:
            # Es texto en negrita
            run = paragraph.add_run(bold_text)
            run.font.name = font_name
            run.font.size = Pt(default_size)
            run.bold = True
            if default_color:
                run.font.color.rgb = default_color
        elif italic_text is not None:
            # Es texto en cursiva
            run = paragraph.add_run(italic_text)
            run.font.name = font_name
            run.font.size = Pt(default_size)
            run.italic = True
            if default_color:
                run.font.color.rgb = default_color

        last_idx = end

    # Texto restante
    if last_idx < len(text):
        plain = text[last_idx:]
        _fail_residual(plain, line_num)
        run = paragraph.add_run(plain)
        run.font.name = font_name
        run.font.size = Pt(default_size)
        if default_color:
            run.font.color.rgb = default_color

def render_md_to_docx(input_md_path, output_docx_path):
    if not os.path.exists(input_md_path):
        print(f"ERROR: El archivo de entrada '{input_md_path}' no existe.", file=sys.stderr)
        sys.exit(1)

    with open(input_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = docx.Document()

    # Configurar márgenes estándar de 1 pulgada (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        # Garantizar que no haya encabezado ni pie de página vinculados
        section.different_first_page_header_footer = False
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

    # Configuración de estilos base
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x1F, 0x24, 0x21) # Gris muy oscuro/carbón

    for line_num, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip('\r\n')
        stripped = line.strip()

        # Línea vacía
        if not stripped:
            continue

        # Separador horizontal Markdown
        if stripped in ['---', '***', '___']:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            # Agregar borde inferior fino al párrafo como separador
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(
                '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:bottom w:val="single" w:sz="6" w:space="1" w:color="D3D3D3"/>'
                '</w:pBdr>'
            )
            pPr.append(pBdr)
            continue

        # Comprobar construcciones no admitidas (R-01)
        if stripped.startswith('###') or stripped.startswith('####') or stripped.startswith('#####'):
            print(f"ERROR [render_docx]: Línea {line_num}: Encabezado de nivel 3 o superior no admitido en plantilla ATS: '{stripped}'", file=sys.stderr)
            sys.exit(1)
        if stripped.startswith('> '):
            print(f"ERROR [render_docx]: Línea {line_num}: Bloques de cita (blockquotes) no admitidos en ATS: '{stripped}'", file=sys.stderr)
            sys.exit(1)
        if stripped.startswith('```') or stripped.startswith('~~~'):
            print(f"ERROR [render_docx]: Línea {line_num}: Bloques de código no admitidos en ATS: '{stripped}'", file=sys.stderr)
            sys.exit(1)
        if stripped.startswith('|') or stripped.endswith('|'):
            print(f"ERROR [render_docx]: Línea {line_num}: Tablas no admitidas bajo la regla de cero tablas ATS: '{stripped}'", file=sys.stderr)
            sys.exit(1)
        if '![' in stripped:
            print(f"ERROR [render_docx]: Línea {line_num}: Imágenes no admitidas bajo la regla de cero imágenes ATS: '{stripped}'", file=sys.stderr)
            sys.exit(1)

        # Encabezado 1 (# Nombre del candidato)
        if line.startswith('# '):
            title_text = line[2:].strip()
            p = doc.add_paragraph(style='Heading 1')
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(title_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(18)
            run.bold = True
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Slate oscuro
            continue

        # Encabezado 2 (## SECCIÓN)
        if line.startswith('## '):
            sec_text = line[3:].strip()
            p = doc.add_paragraph(style='Heading 2')
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            # Añadir borde inferior sutil
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(
                '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:bottom w:val="single" w:sz="6" w:space="1" w:color="004B87"/>'
                '</w:pBdr>'
            )
            pPr.append(pBdr)

            run = p.add_run(sec_text.upper())
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.bold = True
            run.font.color.rgb = RGBColor(0x00, 0x4B, 0x87) # Azul corporativo sobrio
            continue

        # Lista de viñetas (- viñeta)
        if line.strip().startswith('- '):
            bullet_text = line.strip()[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2.5)
            p.paragraph_format.line_spacing = 1.15
            parse_inline(p, bullet_text, font_name='Calibri', default_size=10.5, line_num=line_num)
            continue

        # Párrafo regular
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        parse_inline(p, stripped, font_name='Calibri', default_size=10.5, line_num=line_num)

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
    doc.save(output_docx_path)
    print(f"Documento generado exitosamente en: {output_docx_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 tools/render_docx.py <cv.md> <cv.docx>", file=sys.stderr)
        sys.exit(1)

    render_md_to_docx(sys.argv[1], sys.argv[2])
