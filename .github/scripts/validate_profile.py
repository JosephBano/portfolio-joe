#!/usr/bin/env bash
""":"
python3 "$0" "$@"
exit $?
"""
import os
import re
import sys
import yaml

def fail(msg):
    print(f"ERROR [profile-lint]: {msg}", file=sys.stderr)
    sys.exit(1)

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    profile_dir = os.path.join(repo_root, "profile")
    secrets_example_path = os.path.join(repo_root, ".secrets.example")

    # 1. Cargar .secrets.example para verificar claves disponibles (V-03, RF-DATOS-006)
    allowed_secrets = set()
    if os.path.exists(secrets_example_path):
        with open(secrets_example_path, "r", encoding="utf-8") as f:
            try:
                sec_data = yaml.safe_load(f) or {}
                allowed_secrets = set(sec_data.keys())
            except Exception as e:
                fail(f"Error al parsear .secrets.example: {e}")
    else:
        fail("No se encontró .secrets.example en la raíz del repositorio.")

    print(f"Claves permitidas en .secrets.example: {allowed_secrets}")

    # 2. Validar que todos los archivos YAML en profile/ carguen sin error de sintaxis (V-01)
    if not os.path.exists(profile_dir):
        print("El directorio profile/ no existe aún. Omitiendo validación detallada.")
        sys.exit(0)

    yaml_files = [f for f in os.listdir(profile_dir) if f.endswith(".yml") or f.endswith(".yaml")]
    loaded_data = {}
    for yf in yaml_files:
        full_path = os.path.join(profile_dir, yf)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                loaded_data[yf] = yaml.safe_load(f)
        except Exception as e:
            fail(f"Error de sintaxis YAML en {yf}: {e}")

    # 3. Validar taxonomía
    canonical_tags = set()
    if "taxonomy.yml" in loaded_data:
        tax_data = loaded_data["taxonomy.yml"]
        if not isinstance(tax_data, dict) or "tags" not in tax_data:
            fail("taxonomy.yml debe contener una sección raíz 'tags'")
        tags_entry = tax_data["tags"]
        if isinstance(tags_entry, dict):
            canonical_tags = set(tags_entry.keys())
        elif isinstance(tags_entry, list):
            for item in tags_entry:
                if isinstance(item, dict) and "name" in item:
                    canonical_tags.add(item["name"])
                elif isinstance(item, dict) and "canonical" in item:
                    canonical_tags.add(item["canonical"])
        print(f"Taxonomía validada: {len(canonical_tags)} etiquetas canónicas encontradas.")

    # 4. Validar fuentes de evidencia (sources.yml)
    known_sources = {}
    if "sources.yml" in loaded_data:
        sources_list = loaded_data["sources.yml"]
        if not isinstance(sources_list, list):
            fail("sources.yml debe ser una lista de fuentes")
        for src in sources_list:
            if not isinstance(src, dict):
                fail(f"Entrada inválida en sources.yml: {src}")
            for req_field in ["id", "ruta_local", "confidencialidad", "permite_extraer", "enlazable"]:
                if req_field not in src:
                    fail(f"Fuente {src.get('id', '?')} carece del campo obligatorio '{req_field}'")
            conf = src["confidencialidad"]
            if conf not in ["publico", "interno", "confidencial"]:
                fail(f"Fuente {src['id']}: confidencialidad inválida '{conf}'. Debe ser publico, interno o confidencial.")
            if conf == "publico" and not src["enlazable"]:
                fail(f"Fuente {src['id']} es publica pero enlazable es false. Las fuentes publicas deben ser enlazables.")
            if conf != "publico" and src["enlazable"]:
                fail(f"Fuente {src['id']} es {conf} pero enlazable es true (RF-EVID-006: solo fuentes publicas pueden ser enlazables).")
            known_sources[src["id"]] = src
        print(f"Fuentes validadas: {len(known_sources)} fuentes registradas.")

    # 5. Validar identidad (identity.yml)
    if "identity.yml" in loaded_data:
        ident = loaded_data["identity.yml"]
        if not isinstance(ident, dict):
            fail("identity.yml debe ser un objeto")
        contact = ident.get("contact", {})
        if not isinstance(contact, dict):
            fail("identity.yml debe contener una sección 'contact'")
        secret_pattern = re.compile(r"^\{\{secrets\.([a-zA-Z0-9_]+)\}\}$")
        for k, v in contact.items():
            if not isinstance(v, str):
                fail(f"Campo de contacto '{k}' debe ser una cadena con formato {{{{secrets.<clave>}}}}")
            match = secret_pattern.match(v.strip())
            if not match:
                fail(f"RF-DATOS-005 violado: el campo de contacto '{k}' contiene un valor literal '{v}'. Debe usar formato {{{{secrets.<clave>}}}}")
            ref_key = match.group(1)
            if ref_key not in allowed_secrets:
                fail(f"V-03 violado: la clave de secreto '{{secrets.{ref_key}}}' en contact.{k} no existe en .secrets.example.")
        print("identity.yml validado exitosamente.")

    # 6. Validar experiencia y proyectos (IDs únicos, tags en taxonomy, evidence en sources)
    bullet_ids = set()

    def validate_bullets(bullets, file_name):
        if not isinstance(bullets, list):
            fail(f"{file_name}: bullets debe ser una lista")
        for b in bullets:
            if not isinstance(b, dict):
                fail(f"{file_name}: viñeta inválida: {b}")
            b_id = b.get("id")
            if not b_id:
                fail(f"{file_name}: viñeta sin 'id'")
            if b_id in bullet_ids:
                fail(f"ID de viñeta duplicado detectado: '{b_id}' en {file_name}")
            bullet_ids.add(b_id)

            tags = b.get("tags")
            if not isinstance(tags, list) or len(tags) == 0:
                fail(f"{file_name}, viñeta {b_id}: 'tags' debe ser una lista no vacía")
            for t in tags:
                if canonical_tags and t not in canonical_tags:
                    fail(f"{file_name}, viñeta {b_id}: la etiqueta '{t}' no existe en profile/taxonomy.yml")

            weight = b.get("weight")
            if not isinstance(weight, int) or weight < 1 or weight > 5:
                fail(f"{file_name}, viñeta {b_id}: 'weight' debe ser un entero de 1 a 5 (recibido {weight})")

            for lang in ["es", "en"]:
                if not b.get(lang) or not isinstance(b[lang], str):
                    fail(f"{file_name}, viñeta {b_id}: campo '{lang}' ausente o no es texto")

            evidence = b.get("evidence", [])
            if not isinstance(evidence, list):
                fail(f"{file_name}, viñeta {b_id}: 'evidence' debe ser una lista")
            if known_sources:
                for ev in evidence:
                    if ev not in known_sources:
                        fail(f"{file_name}, viñeta {b_id}: la fuente de evidencia '{ev}' no existe en sources.yml")

    if "experience.yml" in loaded_data:
        exp_list = loaded_data["experience.yml"]
        if not isinstance(exp_list, list):
            fail("experience.yml debe ser una lista de experiencias")
        for exp in exp_list:
            validate_bullets(exp.get("bullets", []), "experience.yml")
        print(f"experience.yml validado exitosamente.")

    if "projects.yml" in loaded_data:
        proj_list = loaded_data["projects.yml"]
        if not isinstance(proj_list, list):
            fail("projects.yml debe ser una lista de proyectos")
        for proj in proj_list:
            validate_bullets(proj.get("bullets", []), "projects.yml")
        print(f"projects.yml validado exitosamente.")

    # 7. Validar habilidades (skills.yml)
    if "skills.yml" in loaded_data:
        skills_list = loaded_data["skills.yml"]
        if not isinstance(skills_list, list):
            fail("skills.yml debe ser una lista de habilidades")
        allowed_levels = {"basico", "intermedio", "avanzado"}
        for s in skills_list:
            s_name = s.get("name")
            if not s_name:
                fail("Habilidad en skills.yml sin campo 'name'")
            if canonical_tags and s_name not in canonical_tags:
                fail(f"Habilidad '{s_name}' no existe como etiqueta canónica en taxonomy.yml")
            lvl = s.get("level")
            if lvl not in allowed_levels:
                fail(f"Habilidad '{s_name}': nivel '{lvl}' inválido. Debe ser: {allowed_levels}")
        print("skills.yml validado exitosamente.")

    # 8. Validar educación (education.yml)
    if "education.yml" in loaded_data:
        edu_list = loaded_data["education.yml"]
        if not isinstance(edu_list, list):
            fail("education.yml debe ser una lista de instituciones")
        allowed_status = {"graduado", "cursado_sin_titulacion", "en_curso"}
        for ed in edu_list:
            status = ed.get("status")
            if status not in allowed_status:
                fail(f"Educación '{ed.get('institution', '?')}': status '{status}' no reconocido. Permitidos: {allowed_status}")
        print("education.yml validado exitosamente.")

    # 9. Validar certificaciones (certifications.yml)
    if "certifications.yml" in loaded_data:
        cert_list = loaded_data["certifications.yml"]
        if not isinstance(cert_list, list):
            fail("certifications.yml debe ser una lista de certificaciones")
        for cert in cert_list:
            if not cert.get("title") or not cert.get("issuer") or not cert.get("year"):
                fail(f"Certificación {cert.get('id', '?')} carece de title, issuer o year")
            tags = cert.get("tags", [])
            for t in tags:
                if canonical_tags and t not in canonical_tags:
                    fail(f"Certificación {cert.get('id', '?')}: etiqueta '{t}' no existe en taxonomy.yml")
        print("certifications.yml validado exitosamente.")

    # 10. Validar idiomas (languages.yml)
    if "languages.yml" in loaded_data:
        lang_list = loaded_data["languages.yml"]
        if not isinstance(lang_list, list):
            fail("languages.yml debe ser una lista de idiomas")
        print("languages.yml validado exitosamente.")

    print(f"\n✓ Validación completada con éxito. Total de viñetas verificadas: {len(bullet_ids)}")

if __name__ == "__main__":
    main()
