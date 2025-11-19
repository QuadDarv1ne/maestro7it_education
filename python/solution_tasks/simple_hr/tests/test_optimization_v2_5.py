"""
Tests for API documentation, static optimization, and API optimization.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.api_docs import APIDocumentation, api_doc
from app.api_optimizer import APIOptimizer, get_api_optimizer, optimized_endpoint
from app.static_optimizer import CDNHelper, StaticAssetManager


class TestAPIDocumentation:
    """Tests for API documentation module."""

    def test_employee_schema(self):
        """Test employee schema generation."""
        schema = APIDocumentation.employee_schema()

        assert schema['type'] == 'object'
        assert 'first_name' in schema['properties']
        assert 'last_name' in schema['properties']
        assert 'email' in schema['properties']
        assert schema['required'] == ['first_name', 'last_name', 'email']

    def test_vacation_schema(self):
        """Test vacation schema generation."""
        schema = APIDocumentation.vacation_schema()

        assert schema['type'] == 'object'
        assert 'employee_id' in schema['properties']
        assert 'start_date' in schema['properties']
        assert 'end_date' in schema['properties']
        assert 'vacation_type' in schema['properties']
        assert schema['properties']['vacation_type']['enum'] == ['paid', 'unpaid', 'sick']

    def test_order_schema(self):
        """Test order schema generation."""
        schema = APIDocumentation.order_schema()

        assert schema['type'] == 'object'
        assert 'employee_id' in schema['properties']
        assert 'order_type' in schema['properties']
        assert schema['properties']['status']['enum'] == ['pending', 'executed', 'cancelled']

    def test_paginated_response_schema(self):
        """Test paginated response schema."""
        item_schema = {'type': 'object'}
        paginated = APIDocumentation.paginated_response(item_schema)

        assert 'items' in paginated['properties']
        assert 'pagination' in paginated['properties']
        assert 'page' in paginated['properties']['pagination']['properties']
        assert 'total' in paginated['properties']['pagination']['properties']

    def test_api_doc_decorator(self):
        """Test API documentation decorator."""

        @api_doc(
            summary='Test endpoint',
            description='Test description',
            tags=['test'],
        )
        def test_func():
            """Test function."""
            return 'result'

        assert hasattr(test_func, '__swagger__')
        assert test_func.__swagger__['summary'] == 'Test endpoint'
        assert test_func.__swagger__['description'] == 'Test description'
        assert test_func.__swagger__['tags'] == ['test']


class TestStaticAssetManager:
    """Tests for static asset manager."""

    def test_init(self):
        """Test manager initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StaticAssetManager(tmpdir)

            assert manager.static_dir == Path(tmpdir)
            assert manager.cache_max_age == 31536000
            assert len(manager.asset_manifest) == 0

    def test_get_asset_hash(self):
        """Test asset hash generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StaticAssetManager(tmpdir)

            # Create test file
            test_file = Path(tmpdir) / 'test.js'
            test_file.write_text('console.log("test");')

            hash_val = manager.get_asset_hash(test_file)

            assert isinstance(hash_val, str)
            assert len(hash_val) == 8

    def test_minify_css(self):
        """Test CSS minification."""
        manager = StaticAssetManager('/tmp')

        css = """
        body {
            margin: 0;
            padding: 0;
        }
        /* comment */
        """

        minified = manager.minify_css(css)

        assert '/*' not in minified
        assert '\n' not in minified or minified.count('\n') < css.count('\n')
        assert 'margin' in minified

    def test_minify_js(self):
        """Test JavaScript minification."""
        manager = StaticAssetManager('/tmp')

        js = """
        function test() {
            console.log("test");  // comment
            return 42;
        }
        """

        minified = manager.minify_js(js)

        assert '//' not in minified
        assert 'function' in minified
        assert len(minified) < len(js)

    def test_compress_gzip(self):
        """Test Gzip compression."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StaticAssetManager(tmpdir)

            # Create test file
            test_file = Path(tmpdir) / 'test.js'
            test_file.write_text('console.log("test");' * 100)

            gzip_path = manager.compress_gzip(test_file)

            assert gzip_path is not None
            assert gzip_path.exists()
            assert gzip_path.suffix == '.gz'

    def test_process_asset_css(self):
        """Test CSS asset processing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StaticAssetManager(tmpdir)

            # Create test CSS
            css_file = Path(tmpdir) / 'style.css'
            css_file.write_text('body { margin: 0; }')

            result = manager.process_asset(css_file)

            assert 'error' not in result
            assert 'minified_size' in result
            assert 'versioned_name' in result
            assert result['savings_percent'] > 0

    def test_process_asset_js(self):
        """Test JavaScript asset processing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = StaticAssetManager(tmpdir)

            # Create test JS
            js_file = Path(tmpdir) / 'app.js'
            js_file.write_text('console.log("test");')

            result = manager.process_asset(js_file)

            assert 'error' not in result
            assert 'versioned_name' in result

    def test_get_cache_headers_js(self):
        """Test cache headers for JS files."""
        manager = StaticAssetManager('/tmp')

        headers = manager.get_cache_headers('.js')

        assert 'Cache-Control' in headers
        assert 'max-age=' in headers['Cache-Control']
        assert 'Expires' in headers

    def test_get_cache_headers_html(self):
        """Test cache headers for HTML files."""
        manager = StaticAssetManager('/tmp')

        headers = manager.get_cache_headers('.html')

        assert headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

    def test_get_cache_headers_other(self):
        """Test cache headers for other files."""
        manager = StaticAssetManager('/tmp')

        headers = manager.get_cache_headers('.png')

        assert 'Cache-Control' in headers
        assert 'Vary' in headers


class TestCDNHelper:
    """Tests for CDN helper."""

    def test_get_cdn_url(self):
        """Test CDN URL generation."""
        url = CDNHelper.get_cdn_url('static/style.css', 'https://cdn.example.com')

        assert url == 'https://cdn.example.com/static/style.css'

    def test_get_cdn_url_with_slash(self):
        """Test CDN URL with leading slash."""
        url = CDNHelper.get_cdn_url('/static/app.js', 'https://cdn.example.com/')

        assert url.startswith('https://cdn.example.com/')
        assert 'app.js' in url

    def test_generate_sri_hash(self):
        """Test SRI hash generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / 'test.js'
            file_path.write_text('console.log("test");')

            sri = CDNHelper.generate_sri_hash(file_path)

            assert sri.startswith('sha384-')
            assert len(sri) > 10

    def test_create_sri_attributes(self):
        """Test SRI attributes creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / 'test.js'
            file_path.write_text('console.log("test");')

            assets = {'static/test.js': str(file_path)}

            sri_attrs = CDNHelper.create_sri_attributes(assets)

            assert 'static/test.js' in sri_attrs
            assert sri_attrs['static/test.js'].startswith('sha384-')


class TestAPIOptimizer:
    """Tests for API optimizer."""

    def test_init(self):
        """Test optimizer initialization."""
        optimizer = APIOptimizer()

        assert len(optimizer.query_cache) == 0
        assert len(optimizer.endpoint_stats) == 0

    def test_record_endpoint_stat(self):
        """Test endpoint stat recording."""
        optimizer = APIOptimizer()

        optimizer.record_endpoint_stat(
            endpoint='/api/employees',
            response_time=0.145,
            query_count=5,
            status_code=200,
        )

        assert '/api/employees' in optimizer.endpoint_stats
        stats = optimizer.endpoint_stats['/api/employees']
        assert stats['calls'] == 1
        assert stats['avg_time'] == 0.145

    def test_record_multiple_stats(self):
        """Test recording multiple stats."""
        optimizer = APIOptimizer()

        for i in range(5):
            optimizer.record_endpoint_stat(
                endpoint='/api/test',
                response_time=0.1 + i * 0.01,
                query_count=5 + i,
                status_code=200,
            )

        stats = optimizer.endpoint_stats['/api/test']
        assert stats['calls'] == 5
        assert stats['avg_time'] > 0.1
        assert stats['avg_queries'] > 5

    def test_get_endpoint_stats(self):
        """Test getting endpoint stats."""
        optimizer = APIOptimizer()

        optimizer.record_endpoint_stat('/api/test', 0.1, 5, 200)

        stats = optimizer.get_endpoint_stats('/api/test')

        assert stats['calls'] == 1

    def test_get_endpoint_stats_all(self):
        """Test getting all endpoint stats."""
        optimizer = APIOptimizer()

        optimizer.record_endpoint_stat('/api/test1', 0.1, 5, 200)
        optimizer.record_endpoint_stat('/api/test2', 0.2, 10, 200)

        all_stats = optimizer.get_endpoint_stats()

        assert len(all_stats) == 2

    def test_get_slow_endpoints(self):
        """Test getting slow endpoints."""
        optimizer = APIOptimizer()

        optimizer.record_endpoint_stat('/api/fast', 0.05, 1, 200)
        optimizer.record_endpoint_stat('/api/slow', 1.5, 15, 200)

        slow = optimizer.get_slow_endpoints(threshold=1.0)

        assert len(slow) == 1
        assert slow[0]['endpoint'] == '/api/slow'

    def test_get_high_query_endpoints(self):
        """Test getting high query endpoints."""
        optimizer = APIOptimizer()

        optimizer.record_endpoint_stat('/api/simple', 0.1, 2, 200)
        optimizer.record_endpoint_stat('/api/complex', 0.5, 25, 200)

        high_query = optimizer.get_high_query_endpoints(threshold=10)

        assert len(high_query) == 1
        assert high_query[0]['endpoint'] == '/api/complex'

    def test_optimized_endpoint_decorator(self):
        """Test optimized endpoint decorator."""

        @optimized_endpoint(cache_time=60)
        def test_endpoint():
            return {'result': 'success'}

        result = test_endpoint()

        assert result == {'result': 'success'}
        assert hasattr(test_endpoint, '__wrapped__')

    def test_get_api_optimizer(self):
        """Test getting API optimizer singleton."""
        optimizer1 = get_api_optimizer()
        optimizer2 = get_api_optimizer()

        assert optimizer1 is optimizer2

    def test_optimize_filter_endpoint(self):
        """Test filter endpoint optimization."""
        optimizer = APIOptimizer()

        # Mock query and model
        mock_item = Mock()
        mock_item.id = 1
        mock_query = Mock()
        mock_query.all.return_value = [mock_item]
        mock_query.filter.return_value = mock_query
        mock_query.options.return_value = mock_query

        mock_model = Mock()
        mock_model.department_id = Mock()
        mock_model.name = Mock()

        results = optimizer.optimize_filter_endpoint(
            query=mock_query,
            filters={'department_id': 5},
            model=mock_model,
            eager_load=['department'],
        )

        assert len(results) == 1


class TestOptimizationIntegration:
    """Integration tests for optimization modules."""

    def test_static_optimization_workflow(self):
        """Test complete static optimization workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir) / 'static'
            static_dir.mkdir()

            # Create test files
            (static_dir / 'style.css').write_text('body { margin: 0; }')
            (static_dir / 'app.js').write_text('console.log("test");')

            manager = StaticAssetManager(str(static_dir))

            # Process assets
            css_result = manager.process_asset(static_dir / 'style.css')
            js_result = manager.process_asset(static_dir / 'app.js')

            assert 'versioned_name' in css_result
            assert 'versioned_name' in js_result

    def test_api_optimizer_workflow(self):
        """Test API optimizer workflow."""
        optimizer = APIOptimizer()

        # Simulate endpoint calls
        for i in range(10):
            optimizer.record_endpoint_stat(
                '/api/employees',
                0.1 + (i % 3) * 0.05,
                5 + (i % 5),
                200,
            )

        stats = optimizer.get_endpoint_stats('/api/employees')
        assert stats['calls'] == 10
        assert stats['avg_time'] > 0.1
