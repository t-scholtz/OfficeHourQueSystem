function removeName(queID) {
  fetch("/remove-name", {
    method: "POST",
    body: JSON.stringify({ queID:queID}),
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
  }).then((_res) => {
    const currentPageURL = window.location.href;
    window.location.href = currentPageURL;
  });
}

function joinQue(ubit, courseID) {
  fetch("/join-que", {
    method: "POST",
    body: JSON.stringify({ ubit:ubit, courseID:courseID }),
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
  }).then((_res) => {
    const currentPageURL = window.location.href;
    window.location.href = currentPageURL;
  });
}
function exitQue(ubit, courseID) {
  fetch("/leave-que", {
    method: "POST",
    body: JSON.stringify({  ubit: ubit, courseID: courseID }),
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
  }).then((_res) => {
    const currentPageURL = window.location.href;
    window.location.href = currentPageURL;
  });
}

function popQue(courseID) {
  fetch("/pop-que", {
    method: "POST",
    body: JSON.stringify({ courseID: courseID }),
    headers: {
      "Content-Type": "application/json", // Set the content type to JSON
    },
  }).then((_res) => {
    const currentPageURL = window.location.href;
    window.location.href = currentPageURL;
  });
}