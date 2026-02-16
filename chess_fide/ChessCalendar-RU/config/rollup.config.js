import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';
import commonjs from '@rollup/plugin-commonjs';
import { visualizer } from 'rollup-plugin-visualizer';

// Define entry points for different feature bundles
const bundles = [
  // Core bundle - essential functionality
  {
    input: 'static/js/app.js',
    output: {
      file: 'static/js/bundles/core.min.js',
      format: 'iife',
      sourcemap: true
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      terser({
        module: true,
        compress: {
          drop_console: true, // Remove console.logs in production
          drop_debugger: true,
          passes: 2
        },
        mangle: {
          properties: {
            regex: /^__/ // Only mangle properties starting with double underscore
          }
        },
        format: {
          comments: false
        }
      }),
      visualizer({
        filename: 'dist/bundle-analysis-core.html',
        title: 'ChessCalendar Core Bundle Analysis'
      })
    ]
  },
  
  // Feature bundles
  {
    input: 'static/js/lazy-loader.js',
    output: {
      file: 'static/js/bundles/lazy-loader.min.js',
      format: 'iife',
      sourcemap: true
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      terser({
        module: true,
        compress: {
          drop_console: true,
          drop_debugger: true
        },
        mangle: true,
        format: {
          comments: false
        }
      })
    ]
  },
  
  // Tournament features bundle
  {
    input: 'static/js/tournament-features.js',
    output: {
      file: 'static/js/bundles/tournament-features.min.js',
      format: 'iife',
      sourcemap: true
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      terser({
        module: true,
        compress: {
          drop_console: true,
          drop_debugger: true
        },
        mangle: true,
        format: {
          comments: false
        }
      }),
      visualizer({
        filename: 'dist/bundle-analysis-tournament.html',
        title: 'ChessCalendar Tournament Features Bundle Analysis'
      })
    ]
  },
  
  // UI features bundle
  {
    input: 'static/js/ui-features.js',
    output: {
      file: 'static/js/bundles/ui-features.min.js',
      format: 'iife',
      sourcemap: true
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      terser({
        module: true,
        compress: {
          drop_console: true,
          drop_debugger: true
        },
        mangle: true,
        format: {
          comments: false
        }
      }),
      visualizer({
        filename: 'dist/bundle-analysis-ui.html',
        title: 'ChessCalendar UI Features Bundle Analysis'
      })
    ]
  },
  
  // Utility functions bundle
  {
    input: 'static/js/utils.js',
    output: {
      file: 'static/js/bundles/utils.min.js',
      format: 'iife',
      sourcemap: true
    },
    plugins: [
      resolve({ browser: true }),
      commonjs(),
      terser({
        module: true,
        compress: {
          drop_console: true,
          drop_debugger: true
        },
        mangle: true,
        format: {
          comments: false
        }
      })
    ]
  }
];

// Create a single combined bundle as fallback
bundles.push({
  input: 'static/js/bundle-input.js', // This will be a virtual file combining key modules
  output: {
    file: 'static/js/bundles/all.min.js',
    format: 'iife',
    sourcemap: true
  },
  plugins: [
    resolve({ browser: true }),
    commonjs(),
    terser({
      module: true,
      compress: {
        drop_console: true,
        drop_debugger: true,
        passes: 3
      },
      mangle: {
        properties: {
          regex: /^__/,
          reserved: ['showLoader', 'hideLoader', 'showToast', 'ChessCalendar', 'LazyLoader']
        }
      },
      format: {
        comments: false
      }
    }),
    visualizer({
      filename: 'dist/bundle-analysis-full.html',
      title: 'ChessCalendar Full Bundle Analysis'
    })
  ]
});

export default bundles;