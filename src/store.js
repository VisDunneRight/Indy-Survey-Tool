import { writable } from "svelte/store";

export const filterBy = writable([]);
export const timeFilters = writable({ start: 2013, end: 2022 });
export const searchFilter = writable("");

export const urlParams = writable(new URLSearchParams(window.location.search));

let prevUrl = undefined;
setInterval(() => {
  const currUrl = window.location.href;
  if (currUrl != prevUrl) {
    // URL changed
    prevUrl = currUrl;
    urlParams.set(new URLSearchParams(window.location.search));
  }
}, 60);
