function postDownloadRequest(url, video_id) {
  fetch(url, {
    method: "POST",
    body: JSON.stringify({ video_id }),
  });
}

// DOM binding

const elForm = document.querySelector("form");
const elUrlInput = document.querySelector("input#url");
const elDwnldBtn = document.querySelector("input[type='submit']");

// Event listeneres

elForm.onsubmit = (event) => {
  event.preventDefault();

  downloadEndpoint = elForm.action;
  videoId = elUrlInput.value;

  elUrlInput.setAttribute("disabled", "");
  elDwnldBtn.setAttribute("disabled", "");
  elDwnldBtn.value = "Downloading...";

  postDownloadRequest(downloadEndpoint, videoId);
};
