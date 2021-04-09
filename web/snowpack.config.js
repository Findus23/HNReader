const httpProxy = require('http-proxy');
const proxy = httpProxy.createProxyServer({
    target: 'http://localhost:8000',
    timeout: 30 * 1000
});

/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
    mount: {
        public: {url: '/', static: true},
        src: {url: '/dist'},
    },
    plugins: [
        '@snowpack/plugin-sass',
        '@snowpack/plugin-vue',
        [
            'snowpack-plugin-replace',
            {
                list: [
                    {
                        from: '__VUE_OPTIONS_API__',
                        to: 'false'
                    },
                    {
                        from: '__VUE_PROD_DEVTOOLS__',
                        to: 'true'
                    }
                ],
            }
        ],
    ],
    routes: [
        /* Enable an SPA Fallback in development: */
        {
            src: '/api/.*',
            dest: (req, res) => {
                proxy.web(req, res, e => console.log(e));
            },
        },
        {"match": "routes", "src": ".*", "dest": "/index.html"},
    ],
    optimize: {
        /* Example: Bundle your final build: */
        bundle: true,
        minify: true,
        target: "es2018"
    },
    packageOptions: {
        /* ... */
    },
    devOptions: {
        /* ... */
    },
    buildOptions: {
        /* ... */
    },
};
