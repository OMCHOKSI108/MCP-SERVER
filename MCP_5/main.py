import os
import shutil
import subprocess
import time
from typing import List, Optional, Dict, Any

from mcp.server import FastMCP

mcp = FastMCP()

# Prefer `manim` from PATH, allow override for Windows/custom
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")

# Base directory for all temporary media
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manim_media")
os.makedirs(BASE_DIR, exist_ok=True)


@mcp.tool()
def render_manim_scene(
    manim_code: str,
    scene_name: str,
    quality: str = "high",
    preview: bool = False,
    output_format: str = "video",
    extra_cli_args: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Render a Manim scene to full video just like CLI: manim -pqh scene.py <SceneName>

    Args:
      manim_code:
        Full Python source including imports + Scene class.
      scene_name:
        Name of the Scene class to render (e.g. "HelloManim").
      quality:
        Quality setting. Default "high" uses -qh.
      preview:
        If true, adds `-p` to open the result with the system player.
      output_format:
        Currently just informational. Manim decides actual format (video/image).
      extra_cli_args:
        Extra flags to pass directly to manim CLI, e.g. ["--fps", "60"].

    Returns:
      JSON with success status and file paths:
        - success: bool
        - video_path: str (absolute path to MP4)
        - thumbnail_path: str (absolute path to thumbnail if available)
        - error: str (only if success is false)
    """

    # 1. Create timestamped run folder
    timestamp = str(int(time.time()))
    run_folder = f"run_{timestamp}"
    run_path = os.path.join(BASE_DIR, run_folder)
    os.makedirs(run_path, exist_ok=True)

    script_path = os.path.join(run_path, "scene.py")

    try:
        # 2. Write the Manim Python code
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)

        # 3. Build manim CLI command (always use high quality -qh)
        cmd: List[str] = [MANIM_EXECUTABLE, "-qh"]

        if preview:
            cmd.append("-p")

        cmd.append("scene.py")
        cmd.append(scene_name)

        if extra_cli_args:
            cmd.extend(extra_cli_args)

        # 4. Run Manim (block until completion)
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=run_path,  # Run in the run folder
            )
        except FileNotFoundError as e:
            return {
                "success": False,
                "error": f"Manim executable not found: {MANIM_EXECUTABLE}"
            }

        # 5. Check if Manim succeeded
        if proc.returncode != 0:
            return {
                "success": False,
                "error": f"Manim failed with return code {proc.returncode}. Stderr: {proc.stderr}"
            }

        # 6. Locate the final MP4 output
        # Expected path: manim_media/run_<timestamp>/media/videos/scene/1080p60/<SceneName>.mp4
        video_dir = os.path.join(run_path, "media", "videos", "scene", "1080p60")
        video_filename = f"{scene_name}.mp4"
        video_path = os.path.join(video_dir, video_filename)

        if not os.path.exists(video_path):
            # Try alternative quality folders if 1080p60 doesn't exist
            for quality_folder in ["720p30", "480p15", "360p15"]:
                alt_video_dir = os.path.join(run_path, "media", "videos", "scene", quality_folder)
                alt_video_path = os.path.join(alt_video_dir, video_filename)
                if os.path.exists(alt_video_path):
                    video_path = alt_video_path
                    break
            else:
                return {
                    "success": False,
                    "error": f"Video file not found at expected locations. Manim stdout: {proc.stdout}"
                }

        # 7. Look for thumbnail (optional)
        thumbnail_path = None
        images_dir = os.path.join(run_path, "media", "images", "scene", "1080p60")
        thumbnail_filename = f"{scene_name}.png"
        potential_thumbnail = os.path.join(images_dir, thumbnail_filename)
        if os.path.exists(potential_thumbnail):
            thumbnail_path = potential_thumbnail

        # 8. Return success with paths
        return {
            "success": True,
            "video_path": video_path,
            "thumbnail_path": thumbnail_path
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


@mcp.tool()
def cleanup_temp_dir(tmp_dir: str) -> str:
    """
    Delete a temporary directory returned by render_manim_scene.
    Use this after you're done with the outputs.
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
