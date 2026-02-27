#!/usr/bin/env python3
"""Startup script: pulls 3D models from GitHub Assets repo."""
import os
import shutil
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ASSETS_REPO = os.getenv('ASSETS_REPO', 'https://github.com/PrudveeYellishetty/Assets.git')
MODELS_DIR = os.path.join(os.path.dirname(__file__), "static", "models")


def pull_models():
    """Clone or pull the Assets repo into static/models/."""
    git_dir = os.path.join(MODELS_DIR, ".git")

    if os.path.exists(git_dir):
        logger.info("Assets repo exists, pulling latest...")
        result = subprocess.run(
            ["git", "-C", MODELS_DIR, "pull", "--ff-only"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            logger.info("Models updated successfully")
        else:
            logger.warning(f"Git pull failed (non-critical): {result.stderr.strip()}")
    else:
        logger.info(f"Cloning assets from {ASSETS_REPO}...")

        if os.path.exists(MODELS_DIR):
            tmp_dir = MODELS_DIR + "_tmp"
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)

            result = subprocess.run(
                ["git", "clone", "--depth", "1", ASSETS_REPO, tmp_dir],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                for item in os.listdir(tmp_dir):
                    src = os.path.join(tmp_dir, item)
                    dst = os.path.join(MODELS_DIR, item)
                    if os.path.exists(dst):
                        if os.path.isdir(dst):
                            shutil.rmtree(dst)
                        else:
                            os.remove(dst)
                    shutil.move(src, dst)
                shutil.rmtree(tmp_dir, ignore_errors=True)
                logger.info("Models cloned successfully")
            else:
                logger.error(f"Git clone failed: {result.stderr.strip()}")
                shutil.rmtree(tmp_dir, ignore_errors=True)
                return False
        else:
            os.makedirs(MODELS_DIR, exist_ok=True)
            result = subprocess.run(
                ["git", "clone", "--depth", "1", ASSETS_REPO, MODELS_DIR],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                logger.info("Models cloned successfully")
            else:
                logger.error(f"Git clone failed: {result.stderr.strip()}")
                return False

    # Count models
    count = 0
    for root, dirs, files in os.walk(MODELS_DIR):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if f.endswith('.glb') or f.endswith('.gltf'):
                count += 1
    logger.info(f"Total models available: {count}")
    return True


if __name__ == "__main__":
    logger.info("=== GruhaAlankar Startup ===")
    pull_models()
    logger.info("=== Startup complete ===")
