#!/usr/bin/env python3
"""
grafana_git_sync.py
====================
Synchronise les dashboards/panels Grafana-OSS ↔ GitHub.

Usage:
    python grafana_git_sync.py export   # Grafana → Git
    python grafana_git_sync.py import   # Git → Grafana
    python grafana_git_sync.py diff     # Affiche les différences locales

Prérequis:
    pip install requests gitpython python-dotenv
"""

import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from git import Repo, InvalidGitRepositoryError

# ─────────────────────────── Configuration ───────────────────────────
load_dotenv()

GRAFANA_URL   = os.getenv("GRAFANA_URL",   "http://localhost:3000")
GRAFANA_TOKEN = os.getenv("GRAFANA_TOKEN", "")          # Service Account token
GITHUB_REPO   = os.getenv("GITHUB_REPO",  ".")          # Chemin local du repo Git cloné
DASHBOARDS_DIR = os.getenv("DASHBOARDS_DIR", "dashboards")  # Sous-dossier dans le repo
COMMIT_AUTHOR  = os.getenv("COMMIT_AUTHOR", "Grafana Sync Bot")
COMMIT_EMAIL   = os.getenv("COMMIT_EMAIL",  "bot@example.com")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ──────────────────────────── Grafana API ────────────────────────────

class GrafanaClient:
    def __init__(self, url: str, token: str):
        self.base = url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def _get(self, path: str) -> dict | list:
        r = self.session.get(f"{self.base}{path}")
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, payload: dict) -> dict:
        r = self.session.post(f"{self.base}{path}", json=payload)
        r.raise_for_status()
        return r.json()

    def list_folders(self) -> list[dict]:
        """Retourne tous les dossiers (+ General = uid vide)."""
        folders = [{"id": 0, "uid": "", "title": "General"}]
        folders += self._get("/api/folders")
        return folders

    def list_dashboards(self, folder_id: int = None) -> list[dict]:
        """Liste les dashboards (optionnellement filtrés par dossier)."""
        params = "?type=dash-db"
        if folder_id is not None:
            params += f"&folderIds={folder_id}"
        return self._get(f"/api/search{params}")

    def get_dashboard(self, uid: str) -> dict:
        """Récupère le JSON complet d'un dashboard."""
        return self._get(f"/api/dashboards/uid/{uid}")

    def import_dashboard(self, dashboard_json: dict, folder_uid: str = "") -> dict:
        """
        Importe (crée ou met à jour) un dashboard.
        dashboard_json : contenu de la clé 'dashboard' exportée.
        """
        payload = {
            "dashboard": dashboard_json,
            "folderUid": folder_uid,
            "overwrite": True,
            "message": f"Importé depuis Git le {datetime.utcnow().isoformat()}Z",
        }
        return self._post("/api/dashboards/import", payload)


# ──────────────────────────── Helpers ────────────────────────────────

def sanitize_filename(name: str) -> str:
    """Convertit un titre en nom de fichier sûr."""
    return "".join(c if c.isalnum() or c in " -_" else "_" for c in name).strip()


def get_or_init_repo(path: str) -> Repo:
    try:
        repo = Repo(path)
        log.info("Repo Git détecté : %s", repo.working_dir)
    except InvalidGitRepositoryError:
        log.warning("Initialisation d'un nouveau repo Git dans %s", path)
        repo = Repo.init(path)
    return repo


def dashboard_path(base: Path, folder_title: str, dash_title: str) -> Path:
    folder_dir = base / sanitize_filename(folder_title)
    folder_dir.mkdir(parents=True, exist_ok=True)
    return folder_dir / f"{sanitize_filename(dash_title)}.json"


# ──────────────────────────── Export ─────────────────────────────────

def export_dashboards(client: GrafanaClient, repo_path: str):
    """
    Exporte tous les dashboards Grafana en JSON dans le repo Git,
    puis crée un commit si des fichiers ont changé.
    """
    repo = get_or_init_repo(repo_path)
    base  = Path(repo_path) / DASHBOARDS_DIR

    exported: list[Path] = []

    for folder in client.list_folders():
        folder_uid   = folder["uid"]
        folder_title = folder["title"]
        folder_id    = folder.get("id", 0)

        dashboards = client.list_dashboards(folder_id=folder_id)
        for meta in dashboards:
            uid   = meta["uid"]
            title = meta["title"]
            try:
                full = client.get_dashboard(uid)
            except Exception as exc:
                log.error("Impossible de récupérer %s: %s", title, exc)
                continue

            # On retire les champs volatils avant de sauvegarder
            dash = full["dashboard"]
            dash.pop("version", None)   # évite des commits parasites
            dash.pop("iteration", None)

            # Métadonnées utiles
            meta_info = {
                "folderUid":   folder_uid,
                "folderTitle": folder_title,
                "slug":        full.get("meta", {}).get("slug", ""),
            }
            payload = {"meta": meta_info, "dashboard": dash}

            fpath = dashboard_path(base, folder_title, title)
            fpath.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            exported.append(fpath)
            log.info("✔  Exporté : %s / %s → %s", folder_title, title, fpath)

    # ── Commit Git ──
    repo.index.add([str(p) for p in exported])
    if repo.is_dirty(index=True, untracked_files=True):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        repo.index.commit(
            f"chore(grafana): export automatique dashboards – {now}",
            author_date=datetime.utcnow().isoformat(),
            commit_date=datetime.utcnow().isoformat(),
        )
        log.info("✔  Commit créé (%d fichiers).", len(exported))
    else:
        log.info("Aucun changement détecté — pas de commit.")

    log.info("Poussez le repo avec : git push")


# ──────────────────────────── Import ─────────────────────────────────

def import_dashboards(client: GrafanaClient, repo_path: str):
    """
    Importe dans Grafana tous les fichiers JSON présents dans le repo.
    """
    base = Path(repo_path) / DASHBOARDS_DIR
    if not base.exists():
        log.error("Dossier introuvable : %s", base)
        sys.exit(1)

    for json_file in sorted(base.rglob("*.json")):
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
            folder_uid = payload.get("meta", {}).get("folderUid", "")
            dash       = payload["dashboard"]
            # Réinitialise l'id pour forcer l'upsert par uid
            dash.pop("id", None)

            result = client.import_dashboard(dash, folder_uid=folder_uid)
            log.info("✔  Importé : %s (status=%s)", json_file.name, result.get("status"))
        except Exception as exc:
            log.error("Erreur import %s : %s", json_file, exc)


# ──────────────────────────── Diff ───────────────────────────────────

def show_diff(repo_path: str):
    """Affiche les fichiers modifiés dans le repo local."""
    repo = get_or_init_repo(repo_path)
    diff = repo.index.diff(None)           # unstaged
    staged = repo.index.diff("HEAD")       # staged vs HEAD

    if not diff and not staged:
        log.info("Aucune différence locale.")
        return

    for item in staged:
        print(f"[staged]    {item.change_type}  {item.a_path}")
    for item in diff:
        print(f"[unstaged]  {item.change_type}  {item.a_path}")


# ────────────────────────────  Main  ─────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("export", "import", "diff"):
        print(__doc__)
        sys.exit(1)

    cmd    = sys.argv[1]
    client = GrafanaClient(GRAFANA_URL, GRAFANA_TOKEN)

    if cmd == "export":
        export_dashboards(client, GITHUB_REPO)
    elif cmd == "import":
        import_dashboards(client, GITHUB_REPO)
    elif cmd == "diff":
        show_diff(GITHUB_REPO)


if __name__ == "__main__":
    main()