import "./app.postcss";
import App from "./App.svelte";

document.documentElement.classList.add("dark");

const app = new App({
  target: document.getElementById("app"),
});

export default app;
