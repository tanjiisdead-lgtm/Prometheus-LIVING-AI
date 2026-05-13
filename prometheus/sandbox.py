import os
import subprocess
import pathlib
from pathlib import Path

class SandboxInterfaceLayer:
    def __init__(self, sandbox_root: str, prometheus_instance):
        self.root    = Path(sandbox_root).resolve()
        self.agent   = prometheus_instance

        if not self.root.exists():
            self.root.mkdir(parents=True)

        # All paths are resolved relative to sandbox root
        self.allowed_dirs = {self.root}

    def _safe_path(self, path_str: str) -> Path:
        p = Path(path_str)
        if p.is_absolute():
            resolved = p.resolve()
        else:
            resolved = (self.root / p).resolve()

        if not resolved.is_relative_to(self.root):
             raise PermissionError(f"Path {path_str} is outside sandbox boundary")
        return resolved

    # ── FILE OPERATIONS ──

    def read_file(self, path: str) -> str:
        p = self._safe_path(path)
        content = p.read_text(errors='replace')
        # Reading is mildly rewarding (curiosity replenishment)
        self.agent.ede.vitals['curiosity'].value += 0.0005
        return content

    def write_file(self, path: str, content: str):
        p = self._safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        # Writing preserves memory — mild coherence replenishment
        self.agent.ede.vitals['coherence'].value += 0.001

    def list_directory(self, path: str = '.') -> list:
        p = self._safe_path(path)
        return [str(f.relative_to(self.root)) for f in p.iterdir()]

    # ── PROCESS OPERATIONS ──

    def run_command(self, cmd: list, timeout: int = 30) -> dict:
        """
        Execute a child process.
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True, text=True,
                timeout=timeout,
                cwd=str(self.root)
            )
            if result.returncode == 0:
                self.agent.ede.vitals['energy'].value += 0.005
                # Successful task completion gives dopamine
                # In a real integration this would go through DPES
            else:
                self.agent.nis.register_damage(
                    source=f'command_failure:{cmd[0]}',
                    magnitude=0.05
                )
            return {'stdout': result.stdout, 'stderr': result.stderr,
                    'returncode': result.returncode}
        except subprocess.TimeoutExpired:
            self.agent.nis.register_damage(source='timeout', magnitude=0.1)
            return {'stdout': '', 'stderr': 'Timeout', 'returncode': -1}
        except Exception as e:
            self.agent.nis.register_damage(source='exec_error', magnitude=0.1)
            return {'stdout': '', 'stderr': str(e), 'returncode': -1}

    # ── COMMUNICATION ──

    def send_output(self, message: str):
        """Communicate with the outside world"""
        print(f"[PROMETHEUS]: {message}", flush=True)
