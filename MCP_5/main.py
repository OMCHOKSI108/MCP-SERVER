import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

from mcp.server import FastMCP

mcp = FastMCP()

# Prefer `manim` from PATH, allow override for Windows/custom
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")

# Base directory for all temporary media
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manim_media")
os.makedirs(BASE_DIR, exist_ok=True)


@dataclass
class ManimOutputFile:
    path: str
    kind: str  # "video" | "image" | "other"
    size_bytes: int


@dataclass
class ManimResult:
    success: bool
    message: str
    tmp_dir: str
    outputs: List[ManimOutputFile]
    stdout: str
    stderr: str
    command: List[str]


def _quality_to_flag(quality: Optional[str]) -> str:
    """
    Map human-friendly quality to manim flags.
    - low   -> -ql
    - medium-> -qm
    - high  -> -qh
    """
    if not quality:
        return "-ql"
    q = quality.lower()
    if q in ("low", "l"):
        return "-ql"
    if q in ("medium", "m", "med"):
        return "-qm"
    if q in ("high", "h"):
        return "-qh"
    # fallback
    return "-ql"


def _discover_outputs(root: str) -> List[ManimOutputFile]:
    """Scan a directory for video/image files produced by Manim."""
    outputs: List[ManimOutputFile] = []
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".gif"}
    image_exts = {".png", ".jpg", ".jpeg", ".svg"}

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            if not os.path.isfile(full):
                continue

            if ext in video_exts:
                kind = "video"
            elif ext in image_exts:
                kind = "image"
            else:
                kind = "other"

            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0

            outputs.append(ManimOutputFile(path=full, kind=kind, size_bytes=size))

    return outputs


@mcp.tool()
def render_manim_scene(
    manim_code: str,
    scene_name: str,
    quality: str = "low",
    preview: bool = False,
    output_format: str = "video",
    extra_cli_args: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Render a Manim scene in ONE go.

    Args:
      manim_code:
        Full Python source including imports + Scene class.
      scene_name:
        Name of the Scene class to render (e.g. "HelloManim").
      quality:
        "low" | "medium" | "high" (mapped to -ql/-qm/-qh). Default: "low".
      preview:
        If true, adds `-p` to open the result with the system player (if supported).
      output_format:
        Currently just informational. Manim decides actual format (video/image).
      extra_cli_args:
        Extra flags to pass directly to manim CLI, e.g. ["--fps", "60"].

    Returns:
      JSON-serializable dict with:
        - success: bool
        - message: str
        - tmp_dir: str
        - outputs: list of {path, kind, size_bytes}
        - stdout: str
        - stderr: str
        - command: list[str]
    """

    # 1. Create isolated temp directory under BASE_DIR
    tmpdir = tempfile.mkdtemp(prefix="run_", dir=BASE_DIR)
    script_path = os.path.join(tmpdir, "scene.py")

    try:
        # 2. Write the Manim Python code
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)

        # 3. Build manim CLI command
        quality_flag = _quality_to_flag(quality)
        cmd: List[str] = [MANIM_EXECUTABLE, quality_flag]

        # Force media_dir inside this tmpdir so everything is self-contained
        cmd.extend(["--media_dir", os.path.join(tmpdir, "media")])

        if preview:
            cmd.append("-p")

        cmd.append(script_path)
        cmd.append(scene_name)

        if extra_cli_args:
            cmd.extend(extra_cli_args)

        # 4. Run Manim
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )
        except FileNotFoundError as e:
            result = ManimResult(
                success=False,
                message=f"Manim executable not found: {MANIM_EXECUTABLE}",
                tmp_dir=tmpdir,
                outputs=[],
                stdout="",
                stderr=str(e),
                command=cmd,
            )
            return asdict(result)

        # 5. Find output files (videos/images)
        media_root = os.path.join(tmpdir, "media")
        outputs = _discover_outputs(media_root) if os.path.exists(media_root) else []

        success = proc.returncode == 0 and any(o.kind == "video" or o.kind == "image" for o in outputs)

        # 6. Build result
        message = "Render successful." if success else "Render failed."
        result = ManimResult(
            success=success,
            message=message,
            tmp_dir=tmpdir,
            outputs=outputs,
            stdout=proc.stdout,
            stderr=proc.stderr,
            command=cmd,
        )

        return asdict(result)

    except Exception as e:
        result = ManimResult(
            success=False,
            message=f"Unexpected error: {e}",
            tmp_dir=tmpdir,
            outputs=[],
            stdout="",
            stderr=str(e),
            command=[],
        )
        return asdict(result)


@mcp.tool()
def cleanup_temp_dir(tmp_dir: str) -> str:
    """
    Delete a temporary directory returned by render_manim_scene.tmp_dir.
    Use this after you’re done with the outputs.
    """
    try:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
            return f"Cleanup successful for: {tmp_dir}"
        else:
            return f"Directory not found: {tmp_dir}"
    except Exception as e:
        return f"Cleanup error: {e}"


if __name__ == "__main__":
    # Run as an MCP server over stdio
    mcp.run(transport="stdio")
