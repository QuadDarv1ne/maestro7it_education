"""
Static file optimization and asset management.

Handles CSS/JS minification, compression, and CDN preparation.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Set

logger = logging.getLogger(__name__)


class StaticAssetManager:
    """Manages static assets optimization and versioning."""

    def __init__(self, static_dir: str, cache_max_age: int = 31536000):
        """
        Initialize static asset manager.

        Args:
            static_dir: Path to static files directory.
            cache_max_age: Browser cache time in seconds (default: 1 year).
        """
        self.static_dir = Path(static_dir)
        self.cache_max_age = cache_max_age
        self.asset_manifest: Dict[str, str] = {}
        self.minified_files: Set[str] = set()

    def get_asset_hash(self, file_path: Path) -> str:
        """
        Calculate hash of file for versioning.

        Args:
            file_path: Path to file.

        Returns:
            MD5 hash of file content.
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()[:8]

    def minify_css(self, content: str) -> str:
        """
        Basic CSS minification.

        Args:
            content: CSS content.

        Returns:
            Minified CSS.
        """
        # Remove comments
        content = content.split('/*')[0]
        for comment in content.split('*/')[1:]:
            content = comment.split('/*', 1)[-1]

        # Remove whitespace
        content = '\n'.join(line.strip() for line in content.split('\n'))
        content = ''.join(line for line in content.split('\n') if line)
        content = content.replace('  ', '')

        # Optimize values
        content = content.replace(': ', ':')
        content = content.replace(' {', '{')
        content = content.replace('} ', '}')
        content = content.replace(', ', ',')

        return content

    def minify_js(self, content: str) -> str:
        """
        Basic JavaScript minification.

        Args:
            content: JavaScript content.

        Returns:
            Minified JavaScript.
        """
        # Remove comments (simplified)
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            # Remove single-line comments
            if '//' in line:
                line = line.split('//')[0]
            cleaned.append(line.strip())

        content = ' '.join(line for line in cleaned if line)

        # Remove extra spaces
        for i in range(3):
            content = content.replace('  ', ' ')

        # Optimize
        for old, new in [
            (' { ', '{'),
            (' } ', '}'),
            (' , ', ','),
            (' = ', '='),
            (' + ', '+'),
            (' - ', '-'),
        ]:
            content = content.replace(old, new)

        return content

    def compress_gzip(self, file_path: Path) -> Optional[Path]:
        """
        Create gzipped version of file.

        Args:
            file_path: Path to original file.

        Returns:
            Path to gzipped file or None if failed.
        """
        try:
            gzip_path = file_path.with_suffix(file_path.suffix + '.gz')

            with open(file_path, 'rb') as f_in:
                with gzip.open(gzip_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            logger.info(f"Created gzip: {gzip_path}")
            return gzip_path

        except Exception as e:
            logger.error(f"Gzip compression failed for {file_path}: {e}")
            return None

    def process_asset(self, file_path: Path) -> Dict[str, Any]:
        """
        Process asset: minify if needed, compress, create versioned name.

        Args:
            file_path: Path to asset file.

        Returns:
            Asset processing results.
        """
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}

        try:
            suffix = file_path.suffix.lower()

            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_size = len(content.encode('utf-8'))

            # Minify if applicable
            if suffix == '.css':
                minified = self.minify_css(content)
                self.minified_files.add(str(file_path))
            elif suffix == '.js':
                minified = self.minify_js(content)
                self.minified_files.add(str(file_path))
            else:
                minified = content

            minified_size = len(minified.encode('utf-8'))

            # Calculate hash for versioning
            temp_path = file_path.with_stem(file_path.stem + '.min')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(minified)

            file_hash = self.get_asset_hash(temp_path)
            versioned_name = f"{file_path.stem}.{file_hash}{file_path.suffix}"

            # Compress
            gzip_path = self.compress_gzip(temp_path)

            return {
                'original': str(file_path),
                'minified_path': str(temp_path),
                'versioned_name': versioned_name,
                'hash': file_hash,
                'original_size': original_size,
                'minified_size': minified_size,
                'gzip_size': gzip_path.stat().st_size if gzip_path else None,
                'savings_percent': round(
                    (1 - minified_size / original_size) * 100, 2
                ),
            }

        except Exception as e:
            logger.error(f"Asset processing failed for {file_path}: {e}")
            return {'error': str(e)}

    def generate_manifest(self) -> Dict[str, str]:
        """
        Generate asset manifest for versioned references.

        Returns:
            Manifest mapping original names to versioned names.
        """
        manifest = {}

        for suffix in ['.css', '.js']:
            for file_path in self.static_dir.rglob(f'*{suffix}'):
                if '.min.' in file_path.name or '.gz' in file_path.name:
                    continue

                result = self.process_asset(file_path)
                if 'versioned_name' in result:
                    relative_path = file_path.relative_to(self.static_dir)
                    manifest[str(relative_path)] = result['versioned_name']

        self.asset_manifest = manifest

        # Save manifest
        manifest_path = self.static_dir / 'manifest.json'
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Generated manifest with {len(manifest)} assets")
        return manifest

    def get_cache_headers(self, file_extension: str) -> Dict[str, str]:
        """
        Get optimal cache headers for file type.

        Args:
            file_extension: File extension (e.g., '.js', '.css').

        Returns:
            Cache control headers.
        """
        headers = {}

        if file_extension in ['.js', '.css', '.woff', '.woff2', '.ttf']:
            # Cache versioned files for 1 year
            headers['Cache-Control'] = f'public, max-age={self.cache_max_age}'
            headers['Expires'] = (
                datetime.utcnow() + timedelta(seconds=self.cache_max_age)
            ).strftime('%a, %d %b %Y %H:%M:%S GMT')

        elif file_extension in ['.html']:
            # Don't cache HTML
            headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            headers['Pragma'] = 'no-cache'
            headers['Expires'] = '0'

        else:
            # Default: cache for 1 day
            headers['Cache-Control'] = 'public, max-age=86400'

        # Enable compression
        headers['Vary'] = 'Accept-Encoding'

        return headers

    def optimize_all(self) -> Dict[str, Any]:
        """
        Optimize all static assets.

        Returns:
            Optimization summary.
        """
        results = {
            'processed': 0,
            'errors': 0,
            'total_original_size': 0,
            'total_minified_size': 0,
            'total_gzip_size': 0,
            'files': [],
        }

        for suffix in ['.css', '.js', '.json']:
            for file_path in self.static_dir.rglob(f'*{suffix}'):
                if any(
                    skip in file_path.name
                    for skip in ['.min.', '.gz', 'manifest.json']
                ):
                    continue

                result = self.process_asset(file_path)

                if 'error' not in result:
                    results['processed'] += 1
                    results['total_original_size'] += result['original_size']
                    results['total_minified_size'] += result['minified_size']
                    if result['gzip_size']:
                        results['total_gzip_size'] += result['gzip_size']
                    results['files'].append(result)
                else:
                    results['errors'] += 1

        # Generate manifest
        self.generate_manifest()

        total_savings = results['total_original_size'] - results['total_minified_size']
        results['total_savings_percent'] = round(
            (total_savings / results['total_original_size'] * 100)
            if results['total_original_size'] > 0
            else 0,
            2,
        )

        logger.info(
            f"Optimization complete: {results['processed']} files, "
            f"{total_savings} bytes saved"
        )

        return results


class CDNHelper:
    """Helper for CDN preparation and integration."""

    @staticmethod
    def get_cdn_url(asset_path: str, cdn_base_url: str) -> str:
        """
        Generate CDN URL for asset.

        Args:
            asset_path: Local asset path.
            cdn_base_url: CDN base URL.

        Returns:
            Full CDN URL.
        """
        # Remove leading slashes
        path = asset_path.lstrip('/')
        # Normalize path
        path = path.replace('\\', '/')
        return f"{cdn_base_url.rstrip('/')}/{path}"

    @staticmethod
    def generate_sri_hash(file_path: Path, algorithm: str = 'sha384') -> str:
        """
        Generate Subresource Integrity hash.

        Args:
            file_path: Path to file.
            algorithm: Hash algorithm.

        Returns:
            SRI hash value.
        """
        import base64

        import hashlib

        with open(file_path, 'rb') as f:
            file_hash = hashlib.new(algorithm)
            file_hash.update(f.read())
            hash_digest = file_hash.digest()

        sri = base64.b64encode(hash_digest).decode('utf-8')
        return f"{algorithm}-{sri}"

    @staticmethod
    def create_sri_attributes(
        assets: Dict[str, str],
    ) -> Dict[str, str]:
        """
        Create SRI attributes for assets.

        Args:
            assets: Mapping of file paths to integrity hashes.

        Returns:
            SRI attributes.
        """
        sri_attrs = {}

        for asset_path, file_path in assets.items():
            if Path(file_path).exists():
                sri = CDNHelper.generate_sri_hash(Path(file_path))
                sri_attrs[asset_path] = sri

        return sri_attrs
