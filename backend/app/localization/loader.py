import json
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_LOCALES_DIR = Path("locales")

class LocalizationManager:
    def __init__(self, locales_dir: Path = DEFAULT_LOCALES_DIR):
        self.locales_dir = locales_dir
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.load_all()

    def load_all(self):
        if not self.locales_dir.exists():
            return
        for lang_dir in self.locales_dir.iterdir():
            if lang_dir.is_dir():
                msg_file = lang_dir / "messages.json"
                if msg_file.exists():
                    try:
                        with open(msg_file, "r", encoding="utf-8") as f:
                            self._cache[lang_dir.name] = json.load(f)
                    except Exception as e:
                        print(f"Error loading locale {lang_dir.name}: {e}")

    def get_supported_languages(self):
        return list(self._cache.keys())

    def get_text(self, lang: str, key: str, default: Optional[str] = None) -> str:
        lang_data = self._cache.get(lang) or self._cache.get("en", {})
        val = lang_data.get(key)
        if val is None:
            val = self._cache.get("en", {}).get(key, default or key)
        return str(val)

    def get_dict(self, lang: str, key: str) -> Dict[str, str]:
        lang_data = self._cache.get(lang) or self._cache.get("en", {})
        val = lang_data.get(key)
        if isinstance(val, dict):
            return val
        en_val = self._cache.get("en", {}).get(key, {})
        return en_val if isinstance(en_val, dict) else {}

    def format_text(self, lang: str, key: str, **kwargs) -> str:
        raw = self.get_text(lang, key)
        try:
            return raw.format(**kwargs)
        except Exception:
            return raw

localization = LocalizationManager()
