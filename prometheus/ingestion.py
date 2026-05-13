import pathlib
import os

class DocumentIngestionEngine:
    SUPPORTED = {'.txt', '.pdf', '.md'}

    def __init__(self, sandbox_root: str, prometheus_instance):
        self.root    = pathlib.Path(sandbox_root)
        self.agent   = prometheus_instance
        self.ingested = set()   # track what has been read

        if not self.root.exists():
            self.root.mkdir(parents=True)

    def scan_library(self) -> list:
        """Discover all readable documents in sandbox"""
        found = []
        for ext in self.SUPPORTED:
            found.extend(list(self.root.rglob(f'*{ext}')))
        return sorted(found, key=lambda p: p.stat().st_size)  # small files first

    def extract_text(self, path: pathlib.Path) -> str:
        ext = path.suffix.lower()

        if ext == '.pdf':
            return self._extract_pdf(path)
        elif ext in {'.txt', '.md'}:
            return path.read_text(errors='replace')
        return ''

    def _extract_pdf(self, path: pathlib.Path) -> str:
        try:
            from pdfminer.high_level import extract_text
            return extract_text(str(path))
        except ImportError:
            print("pdfminer.six not installed. Cannot read PDF.")
            return ""
        except Exception as e:
            print(f"Error reading PDF {path}: {e}")
            return ""

    def ingest(self, path: pathlib.Path, chunk_size_words: int = 500):
        """
        Read a document and feed it to PROMETHEUS as a stream of experiences.
        """
        if path in self.ingested:
            return

        print(f"Ingesting: {path}")
        raw_text = self.extract_text(path)
        words    = raw_text.split()
        chunks   = [words[i:i+chunk_size_words]
                    for i in range(0, len(words), chunk_size_words)]

        for i, chunk in enumerate(chunks):
            text = ' '.join(chunk)

            # Feed chunk to agent
            self.agent.process_text_experience(
                text=text,
                source=str(path),
                chunk_index=i
            )

        self.ingested.add(path)

    def get_next_unread(self):
        library = self.scan_library()
        for doc in library:
            if doc not in self.ingested:
                return doc
        return None
