const downloadEndpoint = "/download";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function enableControls() {
  elUrlInput.value = "";
  elDwnldBtn.value = "Download another one";
  elDwnldBtn.removeAttribute("disabled");
  elUrlInput.removeAttribute("disabled");
}

function disableControls() {
  elUrlInput.setAttribute("disabled", "");
  elDwnldBtn.setAttribute("disabled", "");
  elDwnldBtn.value = "Downloading...";
}

function initProgressBar() {
  elProgressBar.classList.remove("bg-success");
  updateProgressBar("0%");
  elProgressBarContainer.style.display = "";
}

function updateProgressBar(percentageDone) {
  elProgressBar.style.width = percentageDone;
  elProgressBar.innerText = percentageDone;
  ("100%");
  if (percentageDone == "100%") {
    elProgressBar.classList.add("bg-success");
    elProgressBar.classList.remove("progress-bar-animated");
    elProgressBar.classList.remove("progress-bar-striped");
  }
}

const possibleAlertTypes = [
  "primary",
  "secondary",
  "success",
  "danger",
  "warning",
  "info",
  "light",
  "dark",
];
function displayAlert(msg, type) {
  console.log("displayAlert");
  if (!possibleAlertTypes.includes(type)) {
    type = "info";
  }
  elAlertBox.classList.add(`alert-${type}`);
  elAlertBox.innerText = msg;
  elAlertBox.style.display = "block";
}

function hideAlert() {
  elAlertBox.style.display = "none";
}

function postDownloadRequest(video_id) {
  fetch(downloadEndpoint, {
    method: "POST",
    body: JSON.stringify({ video_id }),
  });
}

async function checkDownloadStatus() {
  try {
    response = await fetch(downloadEndpoint, { method: "GET" });
    if (response.status == 200) {
      return response.json();
    }
    return { success: false };
  } catch (e) {
    console.error(e);
    return { success: false };
  }
}

async function subscribeToDownloadStatus() {
  hideAlert();
  let status;
  let state = "download";
  while (state == "download") {
    await sleep(500);
    status = await checkDownloadStatus();
    if (status.success) {
      state = status.state;
      updateProgressBar(status.percentage_done);
    } else continue;
  }
  updateProgressBar("100%");
  // await sleep(1000);
  displayAlert("Video downloaded", "success");
}

// DOM binding

const elForm = document.querySelector("form");
const elUrlInput = document.querySelector("input#url");
const elDwnldBtn = document.querySelector("input[type='submit']");
const elProgressBarContainer = document.querySelector(".progress");
const elProgressBar = document.querySelector(".progress-bar");
const elAlertBox = document.querySelector(".alert");

// Event listeners

elForm.onsubmit = async (event) => {
  event.preventDefault();

  videoId = elUrlInput.value;
  disableControls();

  postDownloadRequest(videoId);
  initProgressBar();
  await subscribeToDownloadStatus();
  enableControls();
};
