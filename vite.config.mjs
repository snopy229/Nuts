import { defineConfig } from 'vite';
import path from "path";
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
    base: '/static/',

    plugins: [
        viteStaticCopy({
            targets: [
                {
                    src: 'src/core/static/fonts',
                    dest: ''
                }
            ]
        })
    ],

    build: {
        outDir: path.resolve('./src/core/static/dist'),
        emptyOutDir: true,
        manifest: true,

        rollupOptions: {
            input: {
                main: path.resolve('./src/core/static/js/common.js'),
            },

            external: ['jquery-mousewheel'],
        },
    },

    server: {
        port: 5173,
        strictPort: true,
        cors: true,
        fs: {
            strict: false
        }
    }
});
