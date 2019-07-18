import os, sys, tarfile

import common
from pathlib import Path


class SymbolsCache:
    def __init__(self, cacheDirPath):
        self._cacheDirPath = cacheDirPath

    def get_symbols_path_for_build_url(self, buildUrl):
        symbolsArchive = os.path.join(self._cacheDirPath, os.path.basename(buildUrl))
        symbolsDir = os.path.join(self._cacheDirPath, Path(symbolsArchive).stem)

        if not os.path.exists(symbolsDir):
            # Download the archive to the temporary directory
            r = common.gHttpService.request('GET', buildUrl, preload_content=False)

            with open(symbolsArchive, 'wb') as out:
                while True:
                    data = r.read(2**16)
                    if not data:
                        break
                    out.write(data)

            r.release_conn()

            # Ungzip/untar the archive
            tar = tarfile.open(symbolsArchive, 'r:gz')
            for item in tar:
                tar.extract(item, symbolsDir)

        return symbolsDir
