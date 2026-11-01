"""Marca en el Project qué issues están listas para empezar y cuáles esperan a otras.

Para cada issue del Project:
1. Crea las dependencias nativas de GitHub (*blocked by*) que figuran en su sección
   «Depende de» y aún no existen. No borra ninguna.
2. Rellena el campo «Disponibilidad»: Hecha si está cerrada, Bloqueada si alguna dependencia
   sigue abierta y Lista si no.

Usa `gh`, así que necesita un token con permiso sobre el Project en `GH_TOKEN`.
Uso: python scripts/disponibilidad.py [--dueno USUARIO] [--proyecto N] [--repo DUEÑO/REPO]
"""

import argparse
import json
import re
import subprocess
import sys

CAMPO = "Disponibilidad"

CONSULTA = """
query($login: String!, $numero: Int!, $cursor: String) {
  user(login: $login) {
    projectV2(number: $numero) {
      id
      field(name: "Disponibilidad") {
        ... on ProjectV2SingleSelectField { id options { id name } }
      }
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          valor: fieldValueByName(name: "Disponibilidad") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
          content {
            ... on Issue {
              number state body
              repository { nameWithOwner }
              blockedBy(first: 50) { nodes { number state } }
            }
          }
        }
      }
    }
  }
}
"""

MUTACION = """
mutation($p: ID!, $i: ID!, $f: ID!, $o: String!) {
  updateProjectV2ItemFieldValue(input: {projectId: $p, itemId: $i, fieldId: $f,
    value: {singleSelectOptionId: $o}}) { clientMutationId }
}
"""


def leer_dependencias(cuerpo: str | None) -> list[int]:
    """Números de issue citados en la sección «## Depende de», sin repetir y en orden."""
    seccion = re.search(r"^##\s*Depende de\s*$(.*?)(?=^##\s|\Z)", cuerpo or "", re.M | re.S)
    if not seccion:
        return []
    # Los comentarios HTML de la plantilla («<!-- - #n -->») no son dependencias.
    texto = re.sub(r"<!--.*?-->", "", seccion.group(1), flags=re.S)
    return list(dict.fromkeys(int(n) for n in re.findall(r"#(\d+)", texto)))


def calcular_disponibilidad(estado: str, estados_dependencias: list[str]) -> str:
    if estado == "CLOSED":
        return "Hecha"
    return "Bloqueada" if "OPEN" in estados_dependencias else "Lista"


def gh(*args: str) -> str:
    salida = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=False
    )
    if salida.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {salida.stderr.strip()}")
    return salida.stdout


def graphql(consulta: str, **variables) -> dict:
    args = ["api", "graphql", "-f", f"query={consulta}"]
    for clave, valor in variables.items():
        if valor is not None:
            args += ["-F" if isinstance(valor, int) else "-f", f"{clave}={valor}"]
    return json.loads(gh(*args))["data"]


def leer_proyecto(dueno: str, numero: int) -> tuple[dict, list[dict]]:
    items, cursor = [], None
    while True:
        proyecto = graphql(CONSULTA, login=dueno, numero=numero, cursor=cursor)["user"]["projectV2"]
        items += proyecto["items"]["nodes"]
        if not proyecto["items"]["pageInfo"]["hasNextPage"]:
            return proyecto, items
        cursor = proyecto["items"]["pageInfo"]["endCursor"]


def anadir_dependencias(issue: dict, repo: str) -> list[dict]:
    """Crea las dependencias de «Depende de» que falten y devuelve todas las dependencias."""
    dependencias = list(issue["blockedBy"]["nodes"])
    existentes = {d["number"] for d in dependencias}
    for numero in leer_dependencias(issue["body"]):
        if numero in existentes or numero == issue["number"]:
            continue
        datos = json.loads(gh("api", f"repos/{repo}/issues/{numero}"))
        gh(
            "api",
            "-X",
            "POST",
            f"repos/{repo}/issues/{issue['number']}/dependencies/blocked_by",
            "-F",
            f"issue_id={datos['id']}",
        )
        dependencias.append({"number": numero, "state": datos["state"].upper()})
        print(f"#{issue['number']}: añadida dependencia de #{numero}")
    return dependencias


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dueno", default="irigoyen161817")
    parser.add_argument("--proyecto", type=int, default=1)
    parser.add_argument("--repo", default="irigoyen161817/analisis-relevos")
    args = parser.parse_args(argv)

    proyecto, items = leer_proyecto(args.dueno, args.proyecto)
    if not proyecto["field"]:
        print(f"El Project no tiene el campo «{CAMPO}».", file=sys.stderr)
        return 1
    opciones = {o["name"]: o["id"] for o in proyecto["field"]["options"]}

    for item in items:
        issue = item["content"]
        if not issue or issue.get("repository", {}).get("nameWithOwner") != args.repo:
            continue
        dependencias = (
            anadir_dependencias(issue, args.repo)
            if issue["state"] == "OPEN"
            else issue["blockedBy"]["nodes"]
        )
        valor = calcular_disponibilidad(issue["state"], [d["state"] for d in dependencias])
        if (item["valor"] or {}).get("name") != valor:
            graphql(
                MUTACION,
                p=proyecto["id"],
                i=item["id"],
                f=proyecto["field"]["id"],
                o=opciones[valor],
            )
            print(f"#{issue['number']}: {valor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
