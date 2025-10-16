import json
from pathlib import Path


class JsonlCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._seen: set[str] = set()

    def load_seen(self) -> set[str]:
        if not self.path or not self.path.is_file():
            return set()
        seen: set[str] = set()
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    p = obj.get("path")
                    if p:
                        seen.add(p)
                except Exception:
                    continue
        except Exception:
            return set()
        self._seen = seen
        return seen

    def should_skip(self, path: str) -> bool:
        return path in self._seen

    def append_result(self, result: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        p = result.get("path")
        if p:
            self._seen.add(p)
