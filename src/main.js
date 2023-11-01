import "./app.postcss";
import App from "./App.svelte";

document.documentElement.classList.add("dark");
document.documentElement.classList.add("dark:bg-gray-900");

const app = new App({
  target: document.getElementById("app"),
});

export default app;
