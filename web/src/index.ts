import {createApp} from 'vue';
import App from './App.vue';
import {router} from "./router";
import './style/main.scss'

const app = createApp(App);
app.use(router)

app.mount('#app');


// Hot Module Replacement (HMR) - Remove this snippet to remove HMR.
// Learn more: https://www.snowpack.dev/concepts/hot-module-replacement
// @ts-ignore
if (import.meta.hot) {
    // @ts-ignore
    import.meta.hot.accept();
    // @ts-ignore
    import.meta.hot.dispose(() => {
        app.unmount();
    });
}
