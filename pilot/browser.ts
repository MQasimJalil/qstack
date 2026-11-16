import { always, eventually } from "@antithesishq/bombadil";
import { actions, extract, getFingerprint } from "@antithesishq/bombadil/browser";

const preview = extract(({ document }) => {
  const pilot = document.querySelector("#pilot");
  if (!pilot) {
    return null;
  }
  return {
    staleDelivered: pilot.getAttribute("data-stale-delivered") === "true",
    refreshed: pilot.getAttribute("data-refreshed") === "true",
    attempt: document.querySelector("#job-attempt")?.textContent?.trim() ?? "",
    status: document.querySelector("#job-status")?.textContent?.trim() ?? "",
  };
});

export const staleCompletionCannotReplaceRetry = always(() => {
  const view = preview.current;
  return !view?.staleDelivered || (view.attempt === "2" && view.status === "Succeeded");
});

export const retrySucceedsBeforeLateCallback = eventually(() => {
  const view = preview.current;
  return view?.staleDelivered === false && view.attempt === "2" && view.status === "Succeeded";
}).within(9, "seconds");

export const resultWasRefreshed = eventually(() => preview.current?.refreshed === true).within(9, "seconds");

const nextButton = extract(({ document }) => {
  const target = document.querySelector("[data-next]");
  if (!target) {
    return null;
  }
  const rect = target.getBoundingClientRect();
  return {
    fingerprint: getFingerprint(target),
    point: { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 },
  };
});

export const followTlcWitness = actions(() => {
  const button = nextButton.current;
  return button ? [{ Click: button }] : [];
});
